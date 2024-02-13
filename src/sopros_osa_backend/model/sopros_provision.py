from pydantic import BaseModel
from typing import Annotated

class SoprosProvision (BaseModel):
    id: str
    name: str
    description: str | None = None