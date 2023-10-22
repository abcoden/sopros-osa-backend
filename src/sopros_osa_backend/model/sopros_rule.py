from pydantic import BaseModel
from typing import Annotated

class SOPROSRule (BaseModel):
    id: str
    state_id: str
    claim_id: str
    title: str | None = None
    description: str | None = None