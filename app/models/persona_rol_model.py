from pydantic import BaseModel

class PersonaRol(BaseModel):
    id_persona: int
    id_rol: int