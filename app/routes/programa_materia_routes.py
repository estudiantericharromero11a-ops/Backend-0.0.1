from fastapi import APIRouter, HTTPException
from app.controllers.programa_materia_controller import ProgramaMateriaController
from app.models.programa_materia_model import ProgramaMateria

router = APIRouter()

controller = ProgramaMateriaController()

@router.post("/")
async def create(programa_materia: ProgramaMateria):
    return controller.create_programa_materia(programa_materia)

@router.get("/")
async def get_all():
    return controller.get_programas_materias()

@router.get("/{programa_id}/{materia_id}")
async def get_one(programa_id: int, materia_id: int):
    return controller.get_programa_materia_by_id(programa_id, materia_id)

@router.delete("/{programa_id}/{materia_id}")
async def delete(programa_id: int, materia_id: int):
    return controller.delete_programa_materia(programa_id, materia_id)
