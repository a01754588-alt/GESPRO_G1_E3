from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: Optional[int]
    titulo: str
    estado: str
