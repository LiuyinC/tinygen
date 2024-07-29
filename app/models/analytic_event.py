import datetime
import uuid
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, PrivateAttr

class AnalyticEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_name: str
    ts_created: str = Field(default_factory=lambda: str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
    _data: Dict[str, Any] = PrivateAttr(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class ImproveCodebaseEvent(AnalyticEvent):
    repo_url: Optional[str] = None
    prompt: Optional[str] = None
    suggestion: Optional[str] = None
    is_reflected: Optional[bool] = None
    error: Optional[str] = None
    
    def __init__(self, **data):
        super().__init__(event_name='improve_codebase', **data)
