import git
import os

def clone_repo(repo_url, repo_path):
    if os.path.exists(repo_path):
        os.system(f"rm -rf {repo_path}")
    git.Repo.clone_from(repo_url, repo_path)

def clean_repo(repo_path):
    os.system(f"rm -rf {repo_path}")
