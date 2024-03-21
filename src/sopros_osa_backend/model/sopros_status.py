from pydantic import BaseModel
from typing import Annotated

class SoprosStatus (BaseModel):
    id: str
    name: str
    description: str | None = None