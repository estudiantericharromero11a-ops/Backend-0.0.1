from fastapi import APIRouter, HTTPException
from app.controllers.persona_controller import PersonaController
from app.models.persona_model import Persona

router = APIRouter()

controller = PersonaController()

@router.post("/")
async def create(persona: Persona):
    return controller.create_persona(persona)

@router.get("/")
async def get_all():
    return controller.get_personas()

@router.get("/{persona_id}")
async def get_one(persona_id: int):
    return controller.get_persona_by_id(persona_id)

@router.put("/{persona_id}")
async def update(persona_id: int, persona: Persona):
    return controller.update_persona(persona_id, persona)

@router.delete("/{persona_id}")
async def delete(persona_id: int):
    return controller.delete_persona(persona_id)