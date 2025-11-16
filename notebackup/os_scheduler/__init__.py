# notebackup/os_scheduler/__init__.py

import sys
import platform

class Scheduler:
    """Base class for OS-specific schedulers."""
    def create(self, interval_hours):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def is_scheduled(self):
        raise NotImplementedError

class WindowsScheduler(Scheduler):
    """Windows Task Scheduler implementation."""
    def __init__(self):
        from . import windows
        self.backend = windows

    def create(self, interval_hours):
        return self.backend.create(interval_hours)

    def delete(self):
        return self.backend.delete()

    def is_scheduled(self):
        return self.backend.is_scheduled()

class LinuxScheduler(Scheduler):
    """Linux systemd timer implementation."""
    def __init__(self):
        from . import linux
        self.backend = linux

    def create(self, interval_hours):
        return self.backend.create(interval_hours)

    def delete(self):
        return self.backend.delete()

    def is_scheduled(self):
        return self.backend.is_scheduled()

class UnsupportedScheduler(Scheduler):
    """Scheduler for unsupported operating systems."""
    def create(self, interval_hours):
        return (False, "Unsupported operating system.")

    def delete(self):
        return (False, "Unsupported operating system.")

    def is_scheduled(self):
        return False

def get_scheduler():
    """Factory function to get the appropriate scheduler for the current OS."""
    if platform.system() == "Windows":
        return WindowsScheduler()
    elif platform.system() == "Linux":
        return LinuxScheduler()
    else:
        return UnsupportedScheduler()