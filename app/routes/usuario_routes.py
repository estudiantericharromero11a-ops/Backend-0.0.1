from fastapi import APIRouter, HTTPException
from app.controllers.usuario_controller import CampusController
from app.models.campus_model import Campus

router = APIRouter()

controller = CampusController()

@router.post("/")
async def create(campus: Campus):
    return controller.create_campus(campus)

@router.get("/")
async def get_all():
    return controller.get_campus()

@router.get("/{campus_id}")
async def get_one(campus_id: int):
    return controller.get_campus_by_id(campus_id)

@router.put("/{campus_id}")
async def update(campus_id: int, campus: Campus):
    return controller.update_campus(campus_id, campus)

@router.delete("/{campus_id}")
async def delete(campus_id: int):
    return controller.delete_campus(campus_id)
