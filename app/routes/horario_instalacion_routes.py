from fastapi import APIRouter, HTTPException
from app.controllers.horario_instalacion_controller import HorarioInstalacionController
from app.models.horario_instalacion_model import HorarioInstalacion

router = APIRouter()

controller = HorarioInstalacionController()

@router.post("/")
async def create(horario: HorarioInstalacion):
    return controller.create_horario_instalacion(horario)

@router.get("/")
async def get_all():
    return controller.get_horarios_instalacion()

@router.get("/{horario_id}")
async def get_one(horario_id: int):
    return controller.get_horario_instalacion_by_id(horario_id)

@router.put("/{horario_id}")
async def update(horario_id: int, horario: HorarioInstalacion):
    return controller.update_horario_instalacion(horario_id, horario)

@router.delete("/{horario_id}")
async def delete(horario_id: int):
    return controller.delete_horario_instalacion(horario_id)