import psycopg2
from fastapi import HTTPException
import jwt
import bcrypt
from datetime import datetime, timedelta
from app.config.db_config import get_db_connection
from app.config.jwt_config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_TIMEDELTA
from app.models.persona_model import Persona

class AuthController:
    """Controlador de autenticación JWT"""

    def hash_password(self, password: str) -> str:
        """Genera hash bcrypt de una contraseña"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def generate_token(self, id_persona: int, username: str) -> tuple:
        """Genera un token JWT"""
        payload = {
            'id_persona': id_persona,
            'username': username,
            'exp': datetime.utcnow() + ACCESS_TOKEN_EXPIRE_TIMEDELTA,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token, payload['exp']

    def verify_token(self, token: str) -> dict:
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")

    def login(self, username: str, password: str) -> dict:
        """Autentica un usuario y retorna el token JWT"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Buscar usuario por username - consulta simplificada
            cursor.execute(
                """SELECT p.id_persona, p.username, p.password_hash, p.id_rol, r.nombre
                   FROM personas p
                   LEFT JOIN roles_usuario r ON p.id_rol = r.id_rol
                   WHERE p.username = %s AND p.estado = 1""",
                (username,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=401, detail="Usuario o contraseña inválido")
            
            id_persona, db_username, password_hash, id_rol, rol_nombre = result
            
            # Verificar contraseña
            if not password_hash:
                raise HTTPException(status_code=401, detail="Usuario o contraseña inválido")
            
            if not self.verify_password(password, password_hash):
                raise HTTPException(status_code=401, detail="Usuario o contraseña inválido")
            
            # Generar token JWT
            token, expires_at = self.generate_token(id_persona, username)
            
            # Guardar token en tabla tokens_activos
            cursor.execute(
                """INSERT INTO tokens_activos (id_persona, token, expires_at)
                   VALUES (%s, %s, %s)""",
                (id_persona, token, expires_at)
            )
            
            conn.commit()
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "id_persona": id_persona,
                "username": username,
                "rol": rol_nombre if rol_nombre else "unknown",
                "expires_at": expires_at.isoformat()
            }
            
        except HTTPException:
            raise
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error en BD: {str(err)}")
        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def logout(self, token: str) -> dict:
        """Invalida un token JWT"""
        conn = None
        cursor = None
        try:
            payload = self.verify_token(token)
            id_persona = payload['id_persona']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Marcar token como inactivo
            cursor.execute(
                """UPDATE tokens_activos SET is_active = FALSE 
                   WHERE token = %s AND id_persona = %s""",
                (token, id_persona)
            )
            
            conn.commit()
            
            return {"mensaje": "Sesión cerrada correctamente"}
            
        except HTTPException:
            raise
        except Exception as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al cerrar sesión: {str(err)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def verify_current_token(self, token: str) -> dict:
        """Verifica que un token sea válido"""
        conn = None
        cursor = None
        try:
            payload = self.verify_token(token)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar que el token esté activo en BD
            cursor.execute(
                """SELECT is_active FROM tokens_activos 
                   WHERE token = %s AND id_persona = %s""",
                (token, payload['id_persona'])
            )
            result = cursor.fetchone()
            
            if not result or not result[0]:
                raise HTTPException(status_code=401, detail="Token no válido o inactivo")
            
            return payload
            
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(status_code=401, detail="Error verificando token")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
