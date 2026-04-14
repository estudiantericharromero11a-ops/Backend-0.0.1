from pydantic import BaseModel
from datetime import time, datetime

class AsignacionInstalacion(BaseModel):
    id_asignacion: int | None = None
    id_instalacion: int
    id_materia: int | None = None
    dia_semana: str | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    id_persona: int | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None