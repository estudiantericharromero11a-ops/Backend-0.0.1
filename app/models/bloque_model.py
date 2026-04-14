from pydantic import BaseModel
from datetime import datetime

class Bloque(BaseModel):
    id_bloque: int | None = None
    nombre: str
    descripcion: str | None = None
    id_campus: int
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None