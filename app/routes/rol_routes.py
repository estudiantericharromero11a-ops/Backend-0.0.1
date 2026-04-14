from fastapi import APIRouter, HTTPException
from app.controllers.rol_controller import RolController
from app.models.rol_model import Rol

router = APIRouter()

controller = RolController()

@router.post("/")
async def create(rol: Rol):
    return controller.create_rol(rol)

@router.get("/")
async def get_all():
    return controller.get_roles()

@router.get("/{rol_id}")
async def get_one(rol_id: int):
    return controller.get_rol_by_id(rol_id)

@router.put("/{rol_id}")
async def update(rol_id: int, rol: Rol):
    return controller.update_rol(rol_id, rol)

@router.delete("/{rol_id}")
async def delete(rol_id: int):
    return controller.delete_rol(rol_id)

@router.patch("/{rol_id}/restore")
async def restore(rol_id: int):
    return controller.restore_rol(rol_id)