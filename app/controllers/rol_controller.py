import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.rol_model import Rol
from fastapi.encoders import jsonable_encoder

class RolController:

    def create_rol(self, rol: Rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO roles
                (nombre_rol, descripcion)
                VALUES (%s, %s)""",
                (
                    rol.nombre_rol,
                    rol.descripcion
                )
            )
            conn.commit()
            return {"resultado": "Rol creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear rol: {str(err)}")
        finally:
            conn.close()

    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles")
            result = cursor.fetchall()

            roles = []
            for data in result:
                roles.append({
                    "id_rol": data[0],
                    "nombre_rol": data[1],
                    "descripcion": data[2],
                })
            return jsonable_encoder(roles)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener roles")
        finally:
            conn.close()

    def get_rol_by_id(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles WHERE id_rol = %s", (rol_id,))
            result = cursor.fetchone()

            if result:
                rol = {
                    "id_rol": result[0],
                    "nombre_rol": result[1],
                    "descripcion": result[2],
                }
                return jsonable_encoder(rol)
            else:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
        finally:
            conn.close()

    def update_rol(self, rol_id: int, rol: Rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE roles SET
                nombre_rol=%s,
                descripcion=%s
                WHERE id_rol=%s""",
                (
                    rol.nombre_rol,
                    rol.descripcion,
                    rol_id
                )
            )
            conn.commit()
            return {"resultado": "Rol actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar rol: {str(err)}")
        finally:
            conn.close()

    def delete_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roles WHERE id_rol = %s", (rol_id,))
            conn.commit()
            return {"resultado": "Rol eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar rol: {str(err)}")
        finally:
            conn.close()