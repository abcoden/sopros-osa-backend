from pydantic import BaseModel
from typing import Annotated


from .sopros_question import SoprosQuestion
from .sopros_rule import SoprosRule

class SoprosCountry (BaseModel):
    id: str
    name: str
    questions: list[SoprosQuestion]
    rules: list[SoprosRule]