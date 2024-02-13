from pydantic import BaseModel
from typing import Annotated

class SoprosRule (BaseModel):
    id: str
    provision_id: str
    type_id: str
    status_id: str
    name: str
    characteristics: str | None = None
    legal_act: str | None = None
    additions: str | None = None