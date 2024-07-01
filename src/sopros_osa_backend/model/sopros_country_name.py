from pydantic import BaseModel
from typing import Annotated


from .sopros_question import SoprosQuestion
from .sopros_rule import SoprosRule

class SoprosCountryName (BaseModel):
    id: str
    name: str
