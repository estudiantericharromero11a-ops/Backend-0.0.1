from pydantic import BaseModel
from datetime import datetime

class AreaFuncional(BaseModel):
    id_area: int | None = None
    nombre_area: str
    descripcion: str | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None