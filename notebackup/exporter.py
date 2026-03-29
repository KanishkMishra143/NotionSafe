# exporter.py - Direct runner for notion2md
from __future__ import annotations
import sys
import io
from notion2md.console.application import main as notion2md_main
from cleo.io.outputs.stream_output import StreamOutput
from .logger import log

def _dummy_has_color_support(self) -> bool:
    """A dummy replacement that always reports no color support."""
    return False

def _direct_cli_runner(*args, **kwargs):
    """
    Patches sys.argv and stdout/stderr, monkey-patches cleo, then calls the 
    notion2md main entrypoint directly. This is a robust solution for 
    PyInstaller compatibility.
    """
    # Build the argument list that notion2md expects
    argv = []
    for a in args:
        if isinstance(a, (list, tuple)):
            argv.extend(map(str, a))
        else:
            argv.append(str(a))
    argv.append("--download")

    # Patch sys attributes for the duration of the call
    original_argv = sys.argv
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_color_support = StreamOutput._has_color_support

    sys.argv = ['notion2md'] + argv
    
    temp_stdout = io.StringIO()
    temp_stderr = io.StringIO()
    sys.stdout = temp_stdout
    sys.stderr = temp_stderr
    
    # Monkey-patch cleo to prevent it from calling fileno()
    StreamOutput._has_color_support = _dummy_has_color_support
    
    log.info(f"Calling notion2md in-process with args: {sys.argv}")

    try:
        exit_code = notion2md_main()
        
        stdout_val = temp_stdout.getvalue()
        stderr_val = temp_stderr.getvalue()
        if stdout_val:
            log.info(f"notion2md stdout: {stdout_val.strip()}")
        if stderr_val:
            log.error(f"notion2md stderr: {stderr_val.strip()}")

        if exit_code != 0:
            log.error(f"notion2md exited with non-zero code: {exit_code}")
        
        return exit_code
    except Exception as e:
        log.error(f"An unexpected error occurred while running notion2md in-process: {e}", exc_info=True)
        return 1
    finally:
        # Always restore the original attributes
        sys.argv = original_argv
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        StreamOutput._has_color_support = original_color_support

# Export the new function as the symbol expected by the rest of the codebase.
export_cli = _direct_cli_runner