from pydantic import BaseModel
from datetime import datetime

class Persona(BaseModel):
    id_persona: int | None = None
    nombre: str
    documento: str
    correo: str | None = None
    telefono: str | None = None
    username: str | None = None
    password_hash: str | None = None
    jwt_token: str | None = None
    token_expires_at: datetime | None = None
    id_rol: int | None = None
    estado: int | None = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None