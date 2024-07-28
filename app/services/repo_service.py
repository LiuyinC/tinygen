import git
import os
from app.core.config import settings
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitRepo:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.repo_path = self.get_repo_subfolder(repo_url)
        
        self.repo_structure = {}
        self.default_branch = None
        self._repo = None    

    def get_latest_commit_sha(self):
        try:
            sha = self._repo.head.commit.hexsha
            return sha
        except Exception as e:
            logger.error(f"Error getting latest commit SHA: {e}")
            return None
    
    def setup_local_repo(self):
        logger.info(f"Setting up local repository for {self.repo_url}")
        self.clone_repo_if_needed()
        
        self._repo = git.Repo(self.repo_path)
        self.default_branch = self._repo.active_branch.name
        self._construct_repo_structure()
        return None

    def get_repo_subfolder(self, repo_url):
        repo_hash = hashlib.md5(repo_url.encode()).hexdigest()
        return os.path.join(settings.BASE_REPO_PATH, repo_hash)
    
    def get_git_diff(self, changed_files):
        """
        Get the git diff from the specified repository path.

        :return: The git diff as a string
        """
        self._repo.git.checkout('tmp_branch', b=True)
        for file_path, new_code in changed_files.items():
            full_path = self._construct_full_path(file_path)
            with open(full_path, 'w') as f:
                f.write(new_code)
        diff = self._repo.git.diff()
        self._repo.git.add('--all')
        self._repo.git.commit('-m', 'AI changes')
        
        self._repo.git.checkout(self.default_branch)
        self._repo.git.branch('-D', 'tmp_branch')
        return diff
    
    def clone_repo_if_needed(self):
        os.makedirs(settings.BASE_REPO_PATH, exist_ok=True)
        
        if os.path.exists(self.repo_path):
            current_sha = self.get_latest_commit_sha()
            temp_repo_path = os.path.join(settings.BASE_REPO_PATH, "temp_repo")
            if os.path.exists(temp_repo_path):
                os.system(f"rm -rf {temp_repo_path}")
            
            git.Repo.clone_from(self.repo_url, temp_repo_path)
            latest_sha = self.get_latest_commit_sha(temp_repo_path)
            
            os.system(f"rm -rf {temp_repo_path}")

            if current_sha == latest_sha:
                logger.infor("Local repository is up to date. No need to clone.")

            else:
                logger.info("Local repository is outdated. Cloning the latest version.")
                os.system(f"rm -rf {self.repo_path}")
                git.Repo.clone_from(self.repo_url, self.repo_path)

        else:
            git.Repo.clone_from(self.repo_url, self.repo_path)

    def get_repo_contents(self):
        content = ""
        for file_path, file_data in self.repo_structure.items():
            content += f"\n\nFile: {file_path}\n{file_data['content']}"
        return content

    def _construct_repo_structure(self):
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py') or file.endswith('.md'):  # Adjust file types as needed
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        self.repo_structure[self._substract_relative_path(file_path)] = {"content": content}

    def _substract_relative_path(self, file_path):
        return file_path.replace(self.repo_path + "/", "")
    
    def _construct_full_path(self, file_path):
        return os.path.join(self.repo_path, file_path)
    
    def __del__(self):
        self._clean_repo()

    def _clean_repo(self):
        os.system(f"rm -rf {self.repo_path}")
