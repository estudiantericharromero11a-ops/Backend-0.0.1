from pydantic import BaseModel

class Campus(BaseModel):
    id_campus: int | None = None
    nombre: str
    direccion: str | None = None
    descripcion: str | None = None
