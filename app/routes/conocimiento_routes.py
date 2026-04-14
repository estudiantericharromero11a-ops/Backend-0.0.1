from fastapi import APIRouter
from app.controllers.conocimiento_controller import ConocimientoController
from app.models.conocimiento_model import Conocimiento

router = APIRouter()

controller = ConocimientoController()

@router.post("/")
async def create(conocimiento: Conocimiento):
    return controller.create_conocimiento(conocimiento)

@router.get("/")
async def get_all():
    return controller.get_conocimientos()

@router.get("/{conocimiento_id}")
async def get_one(conocimiento_id: int):
    return controller.get_conocimiento_by_id(conocimiento_id)

@router.put("/{conocimiento_id}")
async def update(conocimiento_id: int, conocimiento: Conocimiento):
    return controller.update_conocimiento(conocimiento_id, conocimiento)

@router.delete("/{conocimiento_id}")
async def delete(conocimiento_id: int):
    return controller.delete_conocimiento(conocimiento_id)
