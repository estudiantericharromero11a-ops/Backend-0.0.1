from fastapi import FastAPI
from app.routes.usuario_routes import router as campus_router
from app.routes.pedido_routes import router as bloque_router
from app.routes.area_funcional_routes import router as area_funcional_router
from app.routes.instalacion_routes import router as instalacion_router
from app.routes.persona_routes import router as persona_router
from app.routes.programa_routes import router as programa_router
from app.routes.materia_routes import router as materia_router
from app.routes.horario_instalacion_routes import router as horario_instalacion_router
from app.routes.rol_routes import router as rol_router
from app.routes.estado_instalacion_routes import router as estado_instalacion_router
from app.routes.asignacion_instalacion_routes import router as asignacion_instalacion_router
from app.routes.persona_rol_routes import router as persona_rol_router
from app.routes.programa_materia_routes import router as programa_materia_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir CORS desde cualquier origen para desarrollo local
origins = [
    "*",  # Permite todos los orígenes
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campus_router, prefix="/campus", tags=["campus"])
app.include_router(bloque_router, prefix="/bloques", tags=["bloques"])
app.include_router(area_funcional_router, prefix="/areas_funcionales", tags=["areas_funcionales"])
app.include_router(instalacion_router, prefix="/instalaciones", tags=["instalaciones"])
app.include_router(persona_router, prefix="/personas", tags=["personas"])
app.include_router(programa_router, prefix="/programas", tags=["programas"])
app.include_router(materia_router, prefix="/materias", tags=["materias"])
app.include_router(horario_instalacion_router, prefix="/horarios_instalacion", tags=["horarios_instalacion"])
app.include_router(rol_router, prefix="/roles", tags=["roles"])
app.include_router(estado_instalacion_router, prefix="/estado_instalacion", tags=["estado_instalacion"])
app.include_router(asignacion_instalacion_router, prefix="/asignacion_instalaciones", tags=["asignacion_instalaciones"])
app.include_router(persona_rol_router, prefix="/persona_rol", tags=["persona_rol"])
app.include_router(programa_materia_router, prefix="/programa_materia", tags=["programa_materia"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)