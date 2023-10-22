from pydantic import BaseModel
from typing import Annotated

class State (BaseModel):
    id: str
    title: str
    description: str | None = None