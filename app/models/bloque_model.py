from pydantic import BaseModel

class Bloque(BaseModel):
    id_bloque: int | None = None
    nombre: str
    descripcion: str | None = None
    id_campus: int