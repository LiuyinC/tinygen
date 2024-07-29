import logging
import os
from app.api.endpoints import improve_codebase
from app.core.config import settings
from app.services.dependencies import get_gpt_service
from app.services.gpt_service import GPTService
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_gpt_service_instance() -> GPTService:
    return get_gpt_service()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    # Startup logic
    gpt_service: GPTService = await get_gpt_service_instance()
    yield
    # Shutdown logic
    if os.path.exists(settings.BASE_REPO_PATH):
        os.system(f"rm -rf {settings.BASE_REPO_PATH}")
        logger.info("Cleaned up temporary repository files on shutdown")
    gpt_service.notify_gpt_context_off()

app = FastAPI(lifespan=lifespan)

app.include_router(improve_codebase.router, prefix="/improve-codebase")
