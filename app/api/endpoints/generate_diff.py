from fastapi import APIRouter, HTTPException
from app.models.request_body import RequestBody
from app.services.gpt_service import get_gpt_response
from app.services.repo_service import clone_repo, clean_repo
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
async def generate_diff(request: RequestBody):
    repo_url = request.repoUrl
    prompt = request.prompt

    logger.info(f"Received request with repoUrl: {repo_url} and prompt: {prompt}")

    repo_path = "/tmp/repo"
    try:
        clone_repo(repo_url, repo_path)
        logger.info(f"Cloned repository to {repo_path}")

        primary_response = get_gpt_response(prompt, repo_path)
        logger.info(f"Primary response from GPT: {primary_response}")

        reflection_prompt = f"Here is the diff:\\n{primary_response}\\nIs there anything you would like to correct?"
        reflection_response = get_gpt_response(reflection_prompt, repo_path)
        logger.info(f"Reflection response from GPT: {reflection_response}")

        if primary_response != reflection_response:
            primary_response = reflection_response

        clean_repo(repo_path)
        logger.info("Cleaned up repository")

        return {"diff": primary_response}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
