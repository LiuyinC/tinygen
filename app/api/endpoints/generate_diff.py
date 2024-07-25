from fastapi import APIRouter, HTTPException
from app.models.request_body import RequestBody
from app.services.gpt_service import generate_git_diff, generate_repo_summary, reflect_on_diff
from app.services.repo_service import clone_repo_if_needed, read_files_in_repo, clean_repo
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
async def generate_diff(request: RequestBody):
    repo_url = request.repoUrl
    prompt = request.prompt

    logger.info(f"Received request with repoUrl: {repo_url} and prompt: {prompt}")

    try:
        repo_path, cloned = clone_repo_if_needed(repo_url)
        if cloned:
            logger.info(f"Cloned repository to {repo_path}")
        else:
            logger.info(f"Repository already up to date at {repo_path}")

        file_contents = read_files_in_repo(repo_path)
        repo_summary = generate_repo_summary(file_contents)

        # Step 1: Generate the primary diff
        primary_response = generate_git_diff(prompt, repo_summary)
        logger.info(f"Primary response from GPT: {primary_response}")

        # Step 2: Run reflection on the primary diff
        reflection_prompt = f"Here is the diff:\n{primary_response}\nIs this correct, or would you like to make any corrections?"
        reflection_response = reflect_on_diff(reflection_prompt, repo_summary)
        logger.info(f"Reflection response from GPT: {reflection_response}")

        # Use the reflection response if it differs from the primary response
        final_response = reflection_response if reflection_response != primary_response else primary_response

        clean_repo(repo_path)
        logger.info("Cleaned up repository")

        return {"diff": final_response}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
