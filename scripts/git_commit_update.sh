#!/bin/bash
set -euo pipefail

# This script commits a new snapshot to the 'backup' branch
# and updates the 'main' branch to contain only the latest snapshot.

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <repo_path> <snapshot_folder> <remote_name> <remote_url>"
    exit 1
fi

REPO_PATH="$1"
SNAPSHOT_FOLDER="$2"
REMOTE_NAME="$3"
REMOTE_URL="$4"
COMMIT_MESSAGE="Backup snapshot: ${SNAPSHOT_FOLDER}"

cd "$REPO_PATH"

# Ensure remote is configured
if ! git remote | grep -q "^${REMOTE_NAME}$"; then
    git remote add "${REMOTE_NAME}" "${REMOTE_URL}"
    echo "Added git remote '${REMOTE_NAME}'."
fi

# --- Backup Branch ---
# Create or checkout the backup branch
if git show-ref --verify --quiet refs/heads/backup; then
    git checkout backup
else
    git checkout -b backup
fi

git pull "${REMOTE_NAME}" backup --rebase || echo "Could not pull from remote. Continuing with local changes."

# Add and commit the new snapshot
git add "${SNAPSHOT_FOLDER}"
git commit -m "$COMMIT_MESSAGE"
echo "Committing to backup branch..."
git push "${REMOTE_NAME}" backup

# --- Main Branch ---
# Create or checkout the main branch
if git show-ref --verify --quiet refs/heads/main; then
    git checkout main
else
    git checkout -b main
fi

git pull "${REMOTE_NAME}" main --rebase || echo "Could not pull from remote. Continuing with local changes."

# Remove all tracked files from the main branch
git rm -rf --cached .
rm -rf *

# Copy the contents of the latest snapshot
cp -r "${SNAPSHOT_FOLDER}/"* .

# Add, commit, and force-push the new state
git add .
git commit -m "Update latest snapshot: ${SNAPSHOT_FOLDER}"
echo "Force-pushing to main branch..."
git push --force "${REMOTE_NAME}" main

# Return to the backup branch
git checkout backup

echo "Git operations complete."
