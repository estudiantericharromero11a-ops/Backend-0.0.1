from pydantic import BaseModel
from datetime import datetime

class Programa(BaseModel):
    id_programa: int | None = None
    nombre: str
    tipo_programa: str | None = None
    duracion_semestres: int | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None