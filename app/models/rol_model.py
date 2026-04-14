from pydantic import BaseModel
from datetime import datetime

class Rol(BaseModel):
    id_rol: int | None = None
    nombre_rol: str
    descripcion: str | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None