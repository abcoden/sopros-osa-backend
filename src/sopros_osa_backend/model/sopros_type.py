from pydantic import BaseModel
from typing import Annotated

class SoprosType (BaseModel):
    id: str
    name: str
    description: str | None = None