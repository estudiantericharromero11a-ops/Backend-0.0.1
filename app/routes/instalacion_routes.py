from fastapi import APIRouter, HTTPException
from app.controllers.instalacion_controller import InstalacionController
from app.models.instalacion_model import Instalacion

router = APIRouter()

controller = InstalacionController()

@router.post("/")
async def create(instalacion: Instalacion):
    return controller.create_instalacion(instalacion)

@router.get("/")
async def get_all():
    return controller.get_instalaciones()

@router.get("/{instalacion_id}")
async def get_one(instalacion_id: int):
    return controller.get_instalacion_by_id(instalacion_id)

@router.put("/{instalacion_id}")
async def update(instalacion_id: int, instalacion: Instalacion):
    return controller.update_instalacion(instalacion_id, instalacion)

@router.delete("/{instalacion_id}")
async def delete(instalacion_id: int):
    return controller.delete_instalacion(instalacion_id)

@router.patch("/{instalacion_id}/restore")
async def restore(instalacion_id: int):
    return controller.restore_instalacion(instalacion_id)