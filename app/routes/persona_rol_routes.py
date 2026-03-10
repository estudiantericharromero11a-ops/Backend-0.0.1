from fastapi import APIRouter, HTTPException
from app.controllers.persona_rol_controller import PersonaRolController
from app.models.persona_rol_model import PersonaRol

router = APIRouter()

controller = PersonaRolController()

@router.post("/")
async def create(persona_rol: PersonaRol):
    return controller.create_persona_rol(persona_rol)

@router.get("/")
async def get_all():
    return controller.get_personas_roles()

@router.get("/{persona_id}/{rol_id}")
async def get_one(persona_id: int, rol_id: int):
    return controller.get_persona_rol_by_id(persona_id, rol_id)

@router.delete("/{persona_id}/{rol_id}")
async def delete(persona_id: int, rol_id: int):
    return controller.delete_persona_rol(persona_id, rol_id)
