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
