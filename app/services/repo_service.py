import git
import os
from app.core.config import settings
import hashlib

def get_latest_commit_sha(repo_path):
    try:
        repo = git.Repo(repo_path)
        sha = repo.head.commit.hexsha
        return sha
    except Exception as e:
        print(f"Error getting latest commit SHA: {e}")
        return None

def get_repo_subfolder(repo_url):
    repo_hash = hashlib.md5(repo_url.encode()).hexdigest()
    return os.path.join(settings.BASE_REPO_PATH, repo_hash)

def clone_repo_if_needed(repo_url):
    repo_path = get_repo_subfolder(repo_url)
    
    os.makedirs(settings.BASE_REPO_PATH, exist_ok=True)
    
    if os.path.exists(repo_path):
        current_sha = get_latest_commit_sha(repo_path)
        temp_repo_path = os.path.join(settings.BASE_REPO_PATH, "temp_repo")
        if os.path.exists(temp_repo_path):
            os.system(f"rm -rf {temp_repo_path}")
        
        git.Repo.clone_from(repo_url, temp_repo_path)
        latest_sha = get_latest_commit_sha(temp_repo_path)
        
        os.system(f"rm -rf {temp_repo_path}")

        if current_sha == latest_sha:
            print("Local repository is up to date. No need to clone.")
            return repo_path, False
        else:
            print("Local repository is outdated. Cloning the latest version.")
            os.system(f"rm -rf {repo_path}")
            git.Repo.clone_from(repo_url, repo_path)
            return repo_path, True
    else:
        git.Repo.clone_from(repo_url, repo_path)
        return repo_path, True

def read_files_in_repo(repo_path):
    file_contents = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py') or file.endswith('.md'):  # Adjust file types as needed
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    file_contents.append((file_path, content))
    return file_contents

def clean_repo(repo_path):
    os.system(f"rm -rf {repo_path}")
