from pydantic import BaseModel
from typing import Annotated

class Claim (BaseModel):
    id: str
    title: str
    description: str | None = None