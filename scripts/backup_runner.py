#!/usr/bin/env python3
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebackup import cli

if __name__ == "__main__":
    cli.main()
