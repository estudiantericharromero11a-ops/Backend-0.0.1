from pydantic import BaseModel
from datetime import datetime

class Materia(BaseModel):
    id_materia: int | None = None
    nombre: str
    creditos: int | None = None
    descripcion: str | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None