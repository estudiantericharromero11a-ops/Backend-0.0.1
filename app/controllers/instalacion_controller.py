import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.instalacion_model import Instalacion
from fastapi.encoders import jsonable_encoder

class InstalacionController:

    def create_instalacion(self, instalacion: Instalacion):
        """Crear nueva instalación. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO instalaciones
                (nombre, tipo_instalacion, piso, capacidad, id_bloque, id_area, id_estado, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                RETURNING id_instalacion, created_at, updated_at""",
                (
                    instalacion.nombre,
                    instalacion.tipo_instalacion,
                    instalacion.piso,
                    instalacion.capacidad,
                    instalacion.id_bloque,
                    instalacion.id_area,
                    instalacion.id_estado
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Instalación creada",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear instalación: {str(err)}")
        finally:
            conn.close()

    def get_instalaciones(self):
        """Obtener todas las instalaciones activas (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_instalacion, nombre, tipo_instalacion, piso, capacidad, 
                          id_bloque, id_area, id_estado, estado, created_at, updated_at 
                   FROM instalaciones WHERE estado = 1 ORDER BY id_instalacion"""
            )
            result = cursor.fetchall()

            instalaciones = []
            for data in result:
                instalaciones.append({
                    "id_instalacion": data[0],
                    "nombre": data[1],
                    "tipo_instalacion": data[2],
                    "piso": data[3],
                    "capacidad": data[4],
                    "id_bloque": data[5],
                    "id_area": data[6],
                    "id_estado": data[7],
                    "estado": data[8],
                    "created_at": data[9],
                    "updated_at": data[10],
                })
            return jsonable_encoder(instalaciones)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener instalaciones")
        finally:
            conn.close()

    def get_instalacion_by_id(self, instalacion_id: int):
        """Obtener instalación específica activa (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_instalacion, nombre, tipo_instalacion, piso, capacidad, 
                          id_bloque, id_area, id_estado, estado, created_at, updated_at 
                   FROM instalaciones WHERE id_instalacion = %s AND estado = 1""",
                (instalacion_id,)
            )
            result = cursor.fetchone()

            if result:
                instalacion = {
                    "id_instalacion": result[0],
                    "nombre": result[1],
                    "tipo_instalacion": result[2],
                    "piso": result[3],
                    "capacidad": result[4],
                    "id_bloque": result[5],
                    "id_area": result[6],
                    "id_estado": result[7],
                    "estado": result[8],
                    "created_at": result[9],
                    "updated_at": result[10],
                }
                return jsonable_encoder(instalacion)
            else:
                raise HTTPException(status_code=404, detail="Instalación no encontrada")
        finally:
            conn.close()

    def update_instalacion(self, instalacion_id: int, instalacion: Instalacion):
        """Actualizar instalación. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE instalaciones SET
                nombre=%s,
                tipo_instalacion=%s,
                piso=%s,
                capacidad=%s,
                id_bloque=%s,
                id_area=%s,
                id_estado=%s
                WHERE id_instalacion=%s AND estado = 1
                RETURNING updated_at""",
                (
                    instalacion.nombre,
                    instalacion.tipo_instalacion,
                    instalacion.piso,
                    instalacion.capacidad,
                    instalacion.id_bloque,
                    instalacion.id_area,
                    instalacion.id_estado,
                    instalacion_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Instalación actualizada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Instalación no encontrada o inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar instalación: {str(err)}")
        finally:
            conn.close()

    def delete_instalacion(self, instalacion_id: int):
        """Soft delete: desactivar instalación (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE instalaciones SET estado = 0 
                   WHERE id_instalacion = %s AND estado = 1
                   RETURNING updated_at""",
                (instalacion_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Instalación desactivada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Instalación no encontrada o ya inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar instalación: {str(err)}")
        finally:
            conn.close()

    def restore_instalacion(self, instalacion_id: int):
        """Restaurar instalación desactivada (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE instalaciones SET estado = 1 
                   WHERE id_instalacion = %s AND estado = 0
                   RETURNING updated_at""",
                (instalacion_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Instalación restaurada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Instalación no encontrada o ya activa")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar instalación: {str(err)}")
        finally:
            conn.close()