from pydantic import BaseModel
from typing import Annotated

from .state import State
from .claim import Claim
from .sopros_rule import SOPROSRule

class SOPROSCountry (BaseModel):
    states: list[State]
    claims: list[Claim]
    sopros_rules: list[SOPROSRule]