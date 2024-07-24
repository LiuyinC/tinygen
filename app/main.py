from fastapi import FastAPI
from app.api.endpoints import generate_diff

app = FastAPI()

app.include_router(generate_diff.router, prefix="/generate-diff")
