from fastapi import APIRouter, HTTPException
from app.controllers.area_funcional_controller import AreaFuncionalController
from app.models.area_funcional_model import AreaFuncional

router = APIRouter()

controller = AreaFuncionalController()

@router.post("/")
async def create(area: AreaFuncional):
    return controller.create_area_funcional(area)

@router.get("/")
async def get_all():
    return controller.get_areas_funcionales()

@router.get("/{area_id}")
async def get_one(area_id: int):
    return controller.get_area_funcional_by_id(area_id)

@router.put("/{area_id}")
async def update(area_id: int, area: AreaFuncional):
    return controller.update_area_funcional(area_id, area)

@router.delete("/{area_id}")
async def delete(area_id: int):
    return controller.delete_area_funcional(area_id)