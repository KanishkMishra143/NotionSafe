import os
import sys
import subprocess
import traceback
import yaml
import tempfile
from datetime import datetime, time

def write_log(log_file, message):
    """Writes a message to the specified log file."""
    try:
        with open(log_file, "w") as f:
            f.write(message)
    except Exception as e:
        print(f"Fatal: Could not write to log file {log_file}. Error: {e}", file=sys.stderr)

def get_task_xml(command, author, frequency_hours, start_time_str):
    """Generates the XML definition for the scheduled task."""
    
    try:
        start_time = time.fromisoformat(start_time_str)
        start_boundary = datetime.now().replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second).isoformat()
    except (ValueError, TypeError):
        start_boundary = datetime.now().replace(hour=3, minute=0, second=0).isoformat() # Default to 3 AM

    # Determine the trigger type based on frequency
    if frequency_hours <= 24:
        trigger = f"""
    <CalendarTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>"""
    elif frequency_hours <= 168: # Weekly
        trigger = f"""
    <CalendarTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Sunday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>"""
    else: # Monthly
        trigger = f"""
    <CalendarTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <ScheduleByMonth>
        <DaysOfMonth>
          <Day>1</Day>
        </DaysOfMonth>
        <Months>
          <January/><February/><March/><April/><May/><June/><July/><August/><September/><October/><November/><December/>
        </Months>
      </ScheduleByMonth>
    </CalendarTrigger>"""

    xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{datetime.now().isoformat()}</Date>
    <Author>{author}</Author>
    <Description>Runs the NotionSafe backup script.</Description>
    <URI>\\NotionSafeBackup</URI>
  </RegistrationInfo>
  <Triggers>
    {trigger}
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId> <!-- LOCAL SYSTEM -->
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"{command[0]}"</Command>
      <Arguments>{command[1]}</Arguments>
    </Exec>
  </Actions>
</Task>
"""
    return xml

def main():
    """
    Installs or uninstalls the NotionSafe backup scheduler as a Windows Scheduled Task.
    Writes the outcome to a log file specified in the command-line arguments.
    """
    if len(sys.argv) < 2:
        print("Usage: install_windows_task.py <log_file_path> [uninstall]", file=sys.stderr)
        sys.exit(1)

    log_file = sys.argv[1]
    
    try:
        task_name = "NotionSafeBackup"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
        scheduler_script = os.path.join(script_dir, "run_scheduler_service.py")
        config_path = os.path.expanduser("~/.noteback/config.yaml")

        if not os.path.exists(venv_python):
            raise FileNotFoundError(f"Python executable not found at {venv_python}")
        if not os.path.exists(scheduler_script):
            raise FileNotFoundError(f"Scheduler script not found at {scheduler_script}")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        storage_config = config.get('storage', {})
        frequency_hours = storage_config.get('backup_frequency_hours', 24)
        start_time_str = storage_config.get('backup_start_time', '03:00:00')

        command_parts = (venv_python, f'"{scheduler_script}"')

        is_uninstall = len(sys.argv) > 2 and sys.argv[2].lower() == "uninstall"

        if is_uninstall:
            result = uninstall_task(task_name)
        else:
            author = os.environ.get("USERNAME", "NotionSafe")
            task_xml = get_task_xml(command_parts, author, frequency_hours, start_time_str)
            result = install_task(task_name, task_xml)
        
        write_log(log_file, result)

    except Exception as e:
        error_message = f"An unexpected error occurred:\n{traceback.format_exc()}"
        write_log(log_file, error_message)
        sys.exit(1)

def install_task(task_name, task_xml):
    """Creates or updates the scheduled task from an XML definition."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".xml", encoding='utf-16') as tmp:
            tmp.write(task_xml)
            xml_path = tmp.name
        
        # Use /F to force update if the task already exists
        create_command = ["schtasks", "/create", "/tn", task_name, "/xml", xml_path, "/f"]
        
        result = subprocess.run(create_command, check=True, capture_output=True, text=True)
        
        os.remove(xml_path)

        return (
            "SUCCESS: Scheduled task 'NotionSafeBackup' was created/updated successfully.\n\n"
            "The schedule is now based on your configuration.\n"
            "The task will also run as soon as possible if a scheduled start is missed.\n\n"
            "To view task history, open Task Scheduler, right-click 'Task Scheduler Library' and select 'Enable All Tasks History'."
        )

    except subprocess.CalledProcessError as e:
        if os.path.exists(xml_path):
            os.remove(xml_path)
        return f"ERROR: Failed to create scheduled task.\nStderr: {e.stderr}\nStdout: {e.stdout}"

def uninstall_task(task_name):
    """Removes the scheduled task and returns a result string."""
    try:
        result = subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], check=True, capture_output=True, text=True)
        return f"SUCCESS: Scheduled task '{task_name}' was deleted successfully."
    except subprocess.CalledProcessError as e:
        if "The system cannot find the file specified" in e.stderr:
            return f"INFO: Scheduled task '{task_name}' was not found (already uninstalled)."
        else:
            return f"ERROR: Failed to delete scheduled task.\nStderr: {e.stderr}"

if __name__ == "__main__":
    main()
