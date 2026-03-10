from fastapi import APIRouter, HTTPException
from app.controllers.pedido_controller import BloqueController
from app.models.bloque_model import Bloque

router = APIRouter()

controller = BloqueController()

@router.post("/")
async def create(bloque: Bloque):
    return controller.create_bloque(bloque)

@router.get("/")
async def get_all():
    return controller.get_bloques()

@router.get("/{bloque_id}")
async def get_one(bloque_id: int):
    return controller.get_bloque_by_id(bloque_id)

@router.put("/{bloque_id}")
async def update(bloque_id: int, bloque: Bloque):
    return controller.update_bloque(bloque_id, bloque)

@router.delete("/{bloque_id}")
async def delete(bloque_id: int):
    return controller.delete_bloque(bloque_id)
