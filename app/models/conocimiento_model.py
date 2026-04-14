from pydantic import BaseModel

class Conocimiento(BaseModel):
    id: int | None = None
    contenido: str | None = None
    embedding: str | None = None
