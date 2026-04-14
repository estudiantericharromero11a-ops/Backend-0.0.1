from pydantic import BaseModel
from datetime import datetime

class PersonaRol(BaseModel):
    id_persona: int
    id_rol: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    estado: int | None = None