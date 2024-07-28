import json
from fastapi import APIRouter, HTTPException
from app.models.request_body import RequestBody
from app.services.gpt_service import suggest_code_improvements, generate_repo_summary, reflect_on_diff
from app.services.repo_service import GitRepo
import logging
import hashlib
import difflib
import os

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compute_sha1(content):
    """Compute SHA-1 hash of the given content."""
    header = f"blob {len(content)}\0".encode('utf-8')
    store = header + content
    sha1 = hashlib.sha1(store).hexdigest()
    return sha1

def generate_git_diff(old_content, new_content, filename):
    """Generate a git diff between old and new content."""
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        old_lines, new_lines, 
        fromfile=f"a/{filename}", 
        tofile=f"b/{filename}",
        lineterm=""
    )
    return ''.join(diff)

@router.post("/")
async def generate_diff(request: RequestBody):
    repo_url = request.repoUrl
    prompt = request.prompt

    logger.info(f"Received request with repoUrl: {repo_url} and prompt: {prompt}")

    try:
        git_repo = GitRepo(repo_url)
        git_repo.setup_local_repo()

        file_contents = git_repo.get_repo_contents()
        repo_summary = generate_repo_summary(file_contents)

        # Step 1: Suggest code improvements
        suggested_changes = suggest_code_improvements(prompt, repo_summary)
        logger.info(f"Primary response from GPT: {suggested_changes}")

        # Example structure for suggested_changes:
        # suggested_changes = {
        #     "src/main.py": {
        #         "old_code": "os.system('bash temp.sh')",
        #         "new_code": """if os.name == 'nt':
        #         os.system('powershell.exe .\\temp.sh')
        #     else:
        #         os.system('bash temp.sh')"""
        #     }
        # }
        diff = git_repo.get_git_diff(json.loads(suggested_changes))

        # # Step 2: Run reflection on the diff
        reflected_changes = reflect_on_diff(diff, repo_summary)
        logger.info(f"Reflection response from GPT: {reflected_changes}")
        reflection = json.loads(reflected_changes)
        if len(reflection["corrections"]) > 0:
            # Use the reflected changes if they are provided
            final_diff = git_repo.get_git_diff(reflection["corrections"])
        else:
            final_diff = diff

        # Save the final diff to a file
        logger.info(f"Generated diff:\n{final_diff}")

        return {"diff": final_diff}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
