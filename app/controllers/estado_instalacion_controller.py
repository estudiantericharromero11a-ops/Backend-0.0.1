import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.estado_instalacion_model import EstadoInstalacion
from fastapi.encoders import jsonable_encoder

class EstadoInstalacionController:

    def create_estado_instalacion(self, estado: EstadoInstalacion):
        """Crear nuevo estado de instalación. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO estado_instalacion
                (nombre_estado, descripcion, estado)
                VALUES (%s, %s, 1)
                RETURNING id_estado, created_at, updated_at""",
                (
                    estado.nombre_estado,
                    estado.descripcion
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Estado de instalación creado",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear estado de instalación: {str(err)}")
        finally:
            conn.close()

    def get_estados_instalacion(self):
        """Obtener todos los estados de instalación activos (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_estado, nombre_estado, descripcion, estado, created_at, updated_at 
                   FROM estado_instalacion WHERE estado = 1 ORDER BY id_estado"""
            )
            result = cursor.fetchall()

            estados = []
            for data in result:
                estados.append({
                    "id_estado": data[0],
                    "nombre_estado": data[1],
                    "descripcion": data[2],
                    "estado": data[3],
                    "created_at": data[4],
                    "updated_at": data[5],
                })
            return jsonable_encoder(estados)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener estados de instalación")
        finally:
            conn.close()

    def get_estado_instalacion_by_id(self, estado_id: int):
        """Obtener estado de instalación específico activo (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_estado, nombre_estado, descripcion, estado, created_at, updated_at 
                   FROM estado_instalacion WHERE id_estado = %s AND estado = 1""",
                (estado_id,)
            )
            result = cursor.fetchone()

            if result:
                estado = {
                    "id_estado": result[0],
                    "nombre_estado": result[1],
                    "descripcion": result[2],
                    "estado": result[3],
                    "created_at": result[4],
                    "updated_at": result[5],
                }
                return jsonable_encoder(estado)
            else:
                raise HTTPException(status_code=404, detail="Estado de instalación no encontrado")
        finally:
            conn.close()

    def update_estado_instalacion(self, estado_id: int, estado: EstadoInstalacion):
        """Actualizar estado de instalación. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE estado_instalacion SET
                nombre_estado=%s,
                descripcion=%s
                WHERE id_estado=%s AND estado = 1
                RETURNING updated_at""",
                (
                    estado.nombre_estado,
                    estado.descripcion,
                    estado_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Estado de instalación actualizado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Estado de instalación no encontrado o inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar estado de instalación: {str(err)}")
        finally:
            conn.close()

    def delete_estado_instalacion(self, estado_id: int):
        """Soft delete: desactivar estado de instalación (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE estado_instalacion SET estado = 0 
                   WHERE id_estado = %s AND estado = 1
                   RETURNING updated_at""",
                (estado_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Estado de instalación desactivado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Estado de instalación no encontrado o ya inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar estado de instalación: {str(err)}")
        finally:
            conn.close()

    def restore_estado_instalacion(self, estado_id: int):
        """Restaurar estado de instalación (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE estado_instalacion SET estado = 1 
                   WHERE id_estado = %s AND estado = 0
                   RETURNING updated_at""",
                (estado_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Estado de instalación restaurado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Estado de instalación no encontrado o ya activo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar estado de instalación: {str(err)}")
        finally:
            conn.close()