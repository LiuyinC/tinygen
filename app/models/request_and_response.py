from pydantic import BaseModel

class ImproveCodebaseRequestBody(BaseModel):
    repoUrl: str
    prompt: str

class ImproveCodebaseResponseBody(BaseModel):
    suggested_git_diff: str
