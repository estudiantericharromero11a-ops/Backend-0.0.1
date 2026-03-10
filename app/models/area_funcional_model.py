from pydantic import BaseModel

class AreaFuncional(BaseModel):
    id_area: int | None = None
    nombre_area: str
    descripcion: str | None = None