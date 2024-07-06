from pydantic import BaseModel
from datetime import datetime


class SoprosAnswer (BaseModel):
    id: str = ""
    country: str = ""
    created: datetime = ""
    status_ids: list[str] = []
    provision_ids: list[str] = []

