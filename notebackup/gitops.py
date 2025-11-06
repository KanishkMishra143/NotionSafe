import git
import os

def init_repo(repo_path):
    """Initializes a new Git repository if one doesn't exist."""
    if not os.path.exists(os.path.join(repo_path, ".git")):
        repo = git.Repo.init(repo_path)
        print(f"Initialized empty Git repository in {repo_path}")
        return repo
    return git.Repo(repo_path)

def lfs_track(repo, extensions):
    """Sets up Git LFS tracking for the given file extensions."""
    with repo.git.custom_environment(GIT_LFS_SKIP_SMUDGE="1"):
        repo.git.lfs("install")
        for ext in extensions:
            repo.git.lfs("track", f"**/*.{ext}")
    if ".gitattributes" not in repo.untracked_files:
        repo.index.add([".gitattributes"])
        repo.index.commit("Configure Git LFS tracking")
        print("Committed .gitattributes for LFS.")

def has_remote(repo, remote_name):
    """Checks if a remote with the given name exists."""
    return remote_name in [r.name for r in repo.remotes]

def check_for_changes(repo):
    """Check if there are any uncommitted changes."""
    return repo.is_dirty(untracked_files=True)

def commit_and_push(repo_path, commit_message, remote_name, remote_url):
    """
    Commits and pushes changes to the git repository.
    """
    try:
        repo = init_repo(repo_path)

        # Check for changes
        if not check_for_changes(repo):
            print("No changes to commit.")
            return

        repo.git.add(A=True)
        repo.index.commit(commit_message)
        print("Git commit successful.")

        # Handle remote
        if not has_remote(repo, remote_name):
            repo.create_remote(remote_name, remote_url)
            print(f"Added new remote: {remote_name} with URL {remote_url}")

        # Push to remote
        repo.remotes[remote_name].push()
        print("Git push to remote successful.")

    except git.exc.GitCommandError as e:
        print(f"An error occurred during Git operation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
