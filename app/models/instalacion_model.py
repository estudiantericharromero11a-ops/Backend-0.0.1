from pydantic import BaseModel

class Instalacion(BaseModel):
    id_instalacion: int | None = None
    nombre: str
    tipo_instalacion: str | None = None
    piso: int | None = None
    capacidad: int | None = None
    id_bloque: int
    id_area: int
    id_estado: int