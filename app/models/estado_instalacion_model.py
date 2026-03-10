from pydantic import BaseModel

class EstadoInstalacion(BaseModel):
    id_estado: int | None = None
    nombre_estado: str
    descripcion: str | None = None