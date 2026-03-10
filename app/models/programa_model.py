from pydantic import BaseModel

class Programa(BaseModel):
    id_programa: int | None = None
    nombre: str
    tipo_programa: str | None = None
    duracion_semestres: int | None = None