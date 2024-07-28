import json
import logging
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from app.models.request_body import RequestBody
from app.services.dependencies import get_gpt_service
from app.services.gpt_service import GPTService
from app.services.repo_service import GitRepo

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
async def improve_codebase(request: RequestBody, gpt_service: GPTService = Depends(get_gpt_service)) -> Dict[str, str]:
    repo_url: str = request.repoUrl
    prompt: str = request.prompt

    logger.info(f"Received request with repoUrl: {repo_url} and prompt: {prompt}")

    try:
        git_repo = GitRepo(repo_url)
        git_repo.setup_local_repo()

        repo_summary = git_repo.get_repo_contents(16000)

        # Step 1: Suggest code improvements
        suggested_changes = gpt_service.suggest_code_improvements(prompt, repo_summary)
        logger.info(f"Primary response from GPT: {suggested_changes}")

        diff = git_repo.get_git_diff(json.loads(suggested_changes))

        # # Step 2: Run reflection on the diff
        reflected_changes = gpt_service.reflect_on_diff(diff, repo_summary)
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
