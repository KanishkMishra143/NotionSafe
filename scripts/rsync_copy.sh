#!/bin/bash
set -euo pipefail

# This script uses rsync to copy a snapshot to an external location.

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_directory> <destination_directory>"
    exit 1
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found at ${SOURCE_DIR}"
    exit 1
fi

# Ensure destination exists
mkdir -p "$DEST_DIR"

echo "Syncing snapshot from ${SOURCE_DIR} to ${DEST_DIR}..."
rsync -avh --delete "${SOURCE_DIR}/" "${DEST_DIR}"
echo "Rsync complete."
