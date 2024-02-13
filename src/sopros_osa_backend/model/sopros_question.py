from pydantic import BaseModel
from typing import Annotated

class SoprosQuestion (BaseModel):
    status_id: str
    question: str
    addition: str | None = None