import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.analytic_event import ImproveCodebaseEvent
from app.models.request_and_response import ImproveCodebaseRequestBody, ImproveCodebaseResponseBody
from app.services.dependencies import get_gpt_service
from app.services.dependencies import get_event_logger
from app.services.event_logger_service import EventLogger
from app.services.gpt_service import GPTService
from app.services.repo_service import GitRepo

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
async def improve_codebase(request: ImproveCodebaseRequestBody, gpt_service: GPTService = Depends(get_gpt_service), event_logger: EventLogger = Depends(get_event_logger)) -> ImproveCodebaseResponseBody:
    repo_url: str = request.repoUrl
    prompt: str = request.prompt

    logger.info(f"Received request with repoUrl: {repo_url} and prompt: {prompt}")

    event = ImproveCodebaseEvent()
    event.repo_url = repo_url
    event.prompt = prompt

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
            event.is_reflected = True
        else:
            final_diff = diff
            event.is_reflected = False
        event.suggestion = final_diff

        return ImproveCodebaseResponseBody(suggested_git_diff=final_diff)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        event.error = str(e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Log the event with non-blocking pattern
        try:
            event_logger.log_event(event)
        except Exception as e:
            logger.error(f"Error logging event: {e}")
