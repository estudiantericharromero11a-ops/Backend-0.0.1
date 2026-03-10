from pydantic import BaseModel

class Persona(BaseModel):
    id_persona: int | None = None
    nombre: str
    documento: str
    correo: str | None = None
    telefono: str | None = None