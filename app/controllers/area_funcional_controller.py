import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.area_funcional_model import AreaFuncional
from fastapi.encoders import jsonable_encoder

class AreaFuncionalController:

    def create_area_funcional(self, area: AreaFuncional):
        """Crear nueva área funcional. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO areas_funcionales
                (nombre_area, descripcion, estado)
                VALUES (%s, %s, 1)
                RETURNING id_area, created_at, updated_at""",
                (
                    area.nombre_area,
                    area.descripcion
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Área funcional creada",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear área funcional: {str(err)}")
        finally:
            conn.close()

    def get_areas_funcionales(self):
        """Obtener todas las áreas funcionales activas."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_area, nombre_area, descripcion, estado, 
                          created_at, updated_at 
                   FROM areas_funcionales WHERE estado = 1 ORDER BY id_area"""
            )
            result = cursor.fetchall()

            areas = []
            for data in result:
                areas.append({
                    "id_area": data[0],
                    "nombre_area": data[1],
                    "descripcion": data[2],
                    "estado": data[3],
                    "created_at": data[4],
                    "updated_at": data[5],
                })
            return jsonable_encoder(areas)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener áreas funcionales")
        finally:
            conn.close()

    def get_area_funcional_by_id(self, area_id: int):
        """Obtener área funcional específica activa."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_area, nombre_area, descripcion, estado, 
                          created_at, updated_at 
                   FROM areas_funcionales WHERE id_area = %s AND estado = 1""",
                (area_id,)
            )
            result = cursor.fetchone()

            if result:
                area = {
                    "id_area": result[0],
                    "nombre_area": result[1],
                    "descripcion": result[2],
                    "estado": result[3],
                    "created_at": result[4],
                    "updated_at": result[5],
                }
                return jsonable_encoder(area)
            else:
                raise HTTPException(status_code=404, detail="Área funcional no encontrada")
        finally:
            conn.close()

    def update_area_funcional(self, area_id: int, area: AreaFuncional):
        """Actualizar área funcional. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE areas_funcionales SET
                nombre_area=%s,
                descripcion=%s
                WHERE id_area=%s AND estado = 1
                RETURNING updated_at""",
                (
                    area.nombre_area,
                    area.descripcion,
                    area_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Área funcional actualizada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Área funcional no encontrada o inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar área funcional: {str(err)}")
        finally:
            conn.close()

    def delete_area_funcional(self, area_id: int):
        """Soft delete: desactivar área funcional (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE areas_funcionales SET estado = 0 
                   WHERE id_area = %s AND estado = 1
                   RETURNING updated_at""",
                (area_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Área funcional desactivada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Área funcional no encontrada o ya inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar área funcional: {str(err)}")
        finally:
            conn.close()

    def restore_area_funcional(self, area_id: int):
        """Restaurar área funcional desactivada (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE areas_funcionales SET estado = 1 
                   WHERE id_area = %s AND estado = 0
                   RETURNING updated_at""",
                (area_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Área funcional restaurada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Área funcional no encontrada o ya activa")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar área funcional: {str(err)}")
        finally:
            conn.close()