from pydantic import BaseModel

class ProgramaMateria(BaseModel):
    id_programa: int
    id_materia: int