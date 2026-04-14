from fastapi import APIRouter, HTTPException
from app.controllers.materia_controller import MateriaController
from app.models.materia_model import Materia

router = APIRouter()

controller = MateriaController()

@router.post("/")
async def create(materia: Materia):
    return controller.create_materia(materia)

@router.get("/")
async def get_all():
    return controller.get_materias()

@router.get("/{materia_id}")
async def get_one(materia_id: int):
    return controller.get_materia_by_id(materia_id)

@router.put("/{materia_id}")
async def update(materia_id: int, materia: Materia):
    return controller.update_materia(materia_id, materia)

@router.delete("/{materia_id}")
async def delete(materia_id: int):
    return controller.delete_materia(materia_id)

@router.patch("/{materia_id}/restore")
async def restore(materia_id: int):
    return controller.restore_materia(materia_id)