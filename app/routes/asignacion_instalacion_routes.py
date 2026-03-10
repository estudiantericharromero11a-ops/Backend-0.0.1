from fastapi import APIRouter, HTTPException
from app.controllers.asignacion_instalacion_controller import AsignacionInstalacionController
from app.models.asignacion_instalacion_model import AsignacionInstalacion

router = APIRouter()

controller = AsignacionInstalacionController()

@router.post("/")
async def create(asignacion: AsignacionInstalacion):
    return controller.create_asignacion_instalacion(asignacion)

@router.get("/")
async def get_all():
    return controller.get_asignaciones_instalaciones()

@router.get("/{asignacion_id}")
async def get_one(asignacion_id: int):
    return controller.get_asignacion_instalacion_by_id(asignacion_id)

@router.put("/{asignacion_id}")
async def update(asignacion_id: int, asignacion: AsignacionInstalacion):
    return controller.update_asignacion_instalacion(asignacion_id, asignacion)

@router.delete("/{asignacion_id}")
async def delete(asignacion_id: int):
    return controller.delete_asignacion_instalacion(asignacion_id)