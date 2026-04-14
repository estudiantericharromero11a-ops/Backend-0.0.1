import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.rol_model import Rol
from fastapi.encoders import jsonable_encoder

class RolController:

    def create_rol(self, rol: Rol):
        """Crear nuevo rol. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO roles
                (nombre_rol, descripcion, estado)
                VALUES (%s, %s, 1)
                RETURNING id_rol, created_at, updated_at""",
                (
                    rol.nombre_rol,
                    rol.descripcion
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Rol creado",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear rol: {str(err)}")
        finally:
            conn.close()

    def get_roles(self):
        """Obtener todos los roles activos (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_rol, nombre_rol, descripcion, estado, created_at, updated_at 
                   FROM roles WHERE estado = 1 ORDER BY id_rol"""
            )
            result = cursor.fetchall()

            roles = []
            for data in result:
                roles.append({
                    "id_rol": data[0],
                    "nombre_rol": data[1],
                    "descripcion": data[2],
                    "estado": data[3],
                    "created_at": data[4],
                    "updated_at": data[5],
                })
            return jsonable_encoder(roles)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener roles")
        finally:
            conn.close()

    def get_rol_by_id(self, rol_id: int):
        """Obtener rol específico activo (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_rol, nombre_rol, descripcion, estado, created_at, updated_at 
                   FROM roles WHERE id_rol = %s AND estado = 1""",
                (rol_id,)
            )
            result = cursor.fetchone()

            if result:
                rol = {
                    "id_rol": result[0],
                    "nombre_rol": result[1],
                    "descripcion": result[2],
                    "estado": result[3],
                    "created_at": result[4],
                    "updated_at": result[5],
                }
                return jsonable_encoder(rol)
            else:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
        finally:
            conn.close()

    def update_rol(self, rol_id: int, rol: Rol):
        """Actualizar rol. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE roles SET
                nombre_rol=%s,
                descripcion=%s
                WHERE id_rol=%s AND estado = 1
                RETURNING updated_at""",
                (
                    rol.nombre_rol,
                    rol.descripcion,
                    rol_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Rol actualizado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Rol no encontrado o inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar rol: {str(err)}")
        finally:
            conn.close()

    def delete_rol(self, rol_id: int):
        """Soft delete: desactivar rol (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE roles SET estado = 0 
                   WHERE id_rol = %s AND estado = 1
                   RETURNING updated_at""",
                (rol_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Rol desactivado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Rol no encontrado o ya inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar rol: {str(err)}")
        finally:
            conn.close()

    def restore_rol(self, rol_id: int):
        """Restaurar rol desactivado (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE roles SET estado = 1 
                   WHERE id_rol = %s AND estado = 0
                   RETURNING updated_at""",
                (rol_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Rol restaurado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Rol no encontrado o ya activo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar rol: {str(err)}")
        finally:
            conn.close()