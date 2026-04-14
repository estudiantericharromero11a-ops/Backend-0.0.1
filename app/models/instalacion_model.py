from pydantic import BaseModel
from datetime import datetime

class Instalacion(BaseModel):
    id_instalacion: int | None = None
    nombre: str
    tipo_instalacion: str | None = None
    piso: int | None = None
    capacidad: int | None = None
    id_bloque: int
    id_area: int
    id_estado: int
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None