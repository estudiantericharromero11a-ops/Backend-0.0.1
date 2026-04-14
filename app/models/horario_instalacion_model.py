from pydantic import BaseModel
from datetime import time, datetime

class HorarioInstalacion(BaseModel):
    id_horario: int | None = None
    id_instalacion: int
    dia_semana: str
    hora_apertura: time
    hora_cierre: time
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None