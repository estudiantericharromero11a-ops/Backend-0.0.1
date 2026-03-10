from pydantic import BaseModel

class Rol(BaseModel):
    id_rol: int | None = None
    nombre_rol: str
    descripcion: str | None = None