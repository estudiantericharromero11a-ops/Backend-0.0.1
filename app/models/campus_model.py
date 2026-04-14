from pydantic import BaseModel
from datetime import datetime

class Campus(BaseModel):
    id_campus: int | None = None
    nombre: str
    direccion: str | None = None
    descripcion: str | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None
