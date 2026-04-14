from pydantic import BaseModel
from datetime import datetime

class ProgramaMateria(BaseModel):
    id_programa: int
    id_materia: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    estado: int | None = None