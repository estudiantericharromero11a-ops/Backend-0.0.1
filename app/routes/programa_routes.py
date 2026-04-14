from fastapi import APIRouter, HTTPException
from app.controllers.programa_controller import ProgramaController
from app.models.programa_model import Programa

router = APIRouter()

controller = ProgramaController()

@router.post("/")
async def create(programa: Programa):
    return controller.create_programa(programa)

@router.get("/")
async def get_all():
    return controller.get_programas()

@router.get("/{programa_id}")
async def get_one(programa_id: int):
    return controller.get_programa_by_id(programa_id)

@router.put("/{programa_id}")
async def update(programa_id: int, programa: Programa):
    return controller.update_programa(programa_id, programa)

@router.delete("/{programa_id}")
async def delete(programa_id: int):
    return controller.delete_programa(programa_id)

@router.patch("/{programa_id}/restore")
async def restore(programa_id: int):
    return controller.restore_programa(programa_id)