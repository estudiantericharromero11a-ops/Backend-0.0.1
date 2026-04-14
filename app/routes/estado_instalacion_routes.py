from fastapi import APIRouter, HTTPException
from app.controllers.estado_instalacion_controller import EstadoInstalacionController
from app.models.estado_instalacion_model import EstadoInstalacion

router = APIRouter()

controller = EstadoInstalacionController()

@router.post("/")
async def create(estado: EstadoInstalacion):
    return controller.create_estado_instalacion(estado)

@router.get("/")
async def get_all():
    return controller.get_estados_instalacion()

@router.get("/{estado_id}")
async def get_one(estado_id: int):
    return controller.get_estado_instalacion_by_id(estado_id)

@router.put("/{estado_id}")
async def update(estado_id: int, estado: EstadoInstalacion):
    return controller.update_estado_instalacion(estado_id, estado)

@router.delete("/{estado_id}")
async def delete(estado_id: int):
    return controller.delete_estado_instalacion(estado_id)

@router.patch("/{estado_id}/restore")
async def restore(estado_id: int):
    return controller.restore_estado_instalacion(estado_id)