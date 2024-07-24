from pydantic import BaseModel

class RequestBody(BaseModel):
    repoUrl: str
    prompt: str
