# Robust shim for notion2md exporting API changes.
from __future__ import annotations
import importlib
import pkgutil
import subprocess
import sys
from typing import Callable, Any

CANDIDATE_NAMES = ["export_cli", "export", "main", "run", "cli", "exporter"]

def _iter_submodules(pkg_name: str):
    try:
        pkg = importlib.import_module(pkg_name)
    except Exception:
        return
    yield pkg_name, pkg
    for finder, name, ispkg in pkgutil.walk_packages(path=getattr(pkg, "__path__", None), prefix=pkg_name + "."):
        try:
            mod = importlib.import_module(name)
            yield name, mod
        except Exception:
            continue

def _find_export_callable() -> Callable[..., Any] | None:
    # Search notion2md.exporter and its submodules for a callable
    for mod_name, mod in _iter_submodules("notion2md.exporter"):
        for cand in CANDIDATE_NAMES:
            if hasattr(mod, cand):
                obj = getattr(mod, cand)
                if callable(obj):
                    return obj
    # Search top-level package for candidate names
    try:
        top = importlib.import_module("notion2md")
        for cand in CANDIDATE_NAMES:
            if hasattr(top, cand):
                obj = getattr(top, cand)
                if callable(obj):
                    return obj
        # sometimes package exposes a submodule object
        if hasattr(top, "exporter"):
            mod2 = getattr(top, "exporter")
            for cand in CANDIDATE_NAMES:
                if hasattr(mod2, cand):
                    obj = getattr(mod2, cand)
                    if callable(obj):
                        return obj
    except Exception:
        pass
    return None

def _find_main_callable() -> Callable[..., Any] | None:
    # Try notion2md.__main__.main
    try:
        main_mod = importlib.import_module("notion2md.__main__")
        if hasattr(main_mod, "main") and callable(getattr(main_mod, "main")):
            return getattr(main_mod, "main")
    except Exception:
        pass
    return None

# Primary export_cli: prefer in-process callable, else fallback to __main__, else subprocess runner.
def _subprocess_runner(argv):
    """Run `python -m notion2md` with argv list; return exit code or raise subprocess.CalledProcessError."""
    from .logger import log
    cmd = [sys.executable, "-m", "notion2md"] + list(argv)
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        log.error(f"notion2md failed with exit code {completed.returncode}")
        log.error(f"notion2md stdout: {completed.stdout}")
        log.error(f"notion2md stderr: {completed.stderr}")
    return completed.returncode

# Build the export_cli that other code expects to call.
_export_callable = _find_export_callable()
_main_callable = _find_main_callable()

def _export_cli_passthrough(*args, **kwargs):
    """
    Generic wrapper that tries in-process calls first, then __main__, then subprocess fallback.
    Behavior:
      - If in-process callable exists, call it with same signature.
      - Else if __main__.main exists, call it with args (if it expects argv style, pass through).
      - Else run python -m notion2md as subprocess, passing positional args as argv.
    """
    if _export_callable is not None:
        return _export_callable(*args, **kwargs)
    if _main_callable is not None:
        # try to call main. If args is empty, call without arguments.
        try:
            return _main_callable(*args, **kwargs)
        except TypeError:
            # perhaps main expects argv list; convert positional args to argv
            argv = []
            for a in args:
                if isinstance(a, (list, tuple)):
                    argv.extend(map(str, a))
                else:
                    argv.append(str(a))
            return _main_callable(argv)
    # final fallback: run module as subprocess. Convert args into argv list.
    argv = []
    for a in args:
        if isinstance(a, (list, tuple)):
            argv.extend(map(str, a))
        else:
            argv.append(str(a))
    argv.append("--download") # Add the --download flag here
    return _subprocess_runner(argv)

# Export the symbol expected by notebackup code.
export_cli = _export_cli_passthrough
