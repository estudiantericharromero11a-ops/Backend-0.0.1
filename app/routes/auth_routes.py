from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.controllers.auth_controller import AuthController
from typing import Optional

router = APIRouter()
auth_controller = AuthController()

# Modelos Pydantic para requests
class LoginRequest(BaseModel):
    username: str
    password: str

class VerifyTokenRequest(BaseModel):
    token: str

class LogoutRequest(BaseModel):
    token: str

@router.post("/login")
async def login(request: LoginRequest):
    """
    Endpoint de login - valida usuario y contraseña, retorna JWT token
    
    Ejemplo:
    {
        "username": "admin",
        "password": "admin123"
    }
    """
    return auth_controller.login(request.username, request.password)

@router.post("/logout")
async def logout(request: LogoutRequest):
    """
    Endpoint de logout - invalida el token JWT
    """
    return auth_controller.logout(request.token)

@router.post("/verify")
async def verify(request: VerifyTokenRequest):
    """
    Endpoint para verificar si un token es válido
    
    Retorna los datos del payload del token
    """
    payload = auth_controller.verify_current_token(request.token)
    return {
        "valid": True,
        "id_persona": payload['id_persona'],
        "username": payload['username'],
        "exp": payload['exp']
    }

@router.get("/verify-header")
async def verify_header(authorization: Optional[str] = Header(None)):
    """
    Endpoint para verificar token desde header Authorization
    Esperado: "Bearer <token>"
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Header Authorization requerido")
    
    token = authorization.split(" ")[1]
    payload = auth_controller.verify_current_token(token)
    return {
        "valid": True,
        "id_persona": payload['id_persona'],
        "username": payload['username'],
        "exp": payload['exp']
    }
