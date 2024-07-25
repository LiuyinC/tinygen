from fastapi import FastAPI
from app.api.endpoints import generate_diff
from app.core.config import settings
import os
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"OpenAI API Key: {settings.OPENAI_API_KEY}")
    yield
    # Shutdown logic
    if os.path.exists(settings.BASE_REPO_PATH):
        os.system(f"rm -rf {settings.BASE_REPO_PATH}")
        logger.info("Cleaned up temporary repository files on shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(generate_diff.router, prefix="/generate-diff")
