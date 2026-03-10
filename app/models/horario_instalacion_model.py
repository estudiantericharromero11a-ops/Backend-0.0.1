from pydantic import BaseModel
from datetime import time

class HorarioInstalacion(BaseModel):
    id_horario: int | None = None
    id_instalacion: int
    dia_semana: str
    hora_apertura: time
    hora_cierre: time