from pydantic import BaseModel
from datetime import datetime

class EstadoInstalacion(BaseModel):
    id_estado: int | None = None
    nombre_estado: str
    descripcion: str | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None