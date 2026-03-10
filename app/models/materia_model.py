from pydantic import BaseModel

class Materia(BaseModel):
    id_materia: int | None = None
    nombre: str
    creditos: int | None = None
    descripcion: str | None = None