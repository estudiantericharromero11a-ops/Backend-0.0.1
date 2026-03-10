import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.area_funcional_model import AreaFuncional
from fastapi.encoders import jsonable_encoder

class AreaFuncionalController:

    def create_area_funcional(self, area: AreaFuncional):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO areas_funcionales
                (nombre_area, descripcion)
                VALUES (%s, %s)""",
                (
                    area.nombre_area,
                    area.descripcion
                )
            )
            conn.commit()
            return {"resultado": "Área funcional creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear área funcional: {str(err)}")
        finally:
            conn.close()

    def get_areas_funcionales(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM areas_funcionales")
            result = cursor.fetchall()

            areas = []
            for data in result:
                areas.append({
                    "id_area": data[0],
                    "nombre_area": data[1],
                    "descripcion": data[2],
                })
            return jsonable_encoder(areas)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener áreas funcionales")
        finally:
            conn.close()

    def get_area_funcional_by_id(self, area_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM areas_funcionales WHERE id_area = %s", (area_id,))
            result = cursor.fetchone()

            if result:
                area = {
                    "id_area": result[0],
                    "nombre_area": result[1],
                    "descripcion": result[2],
                }
                return jsonable_encoder(area)
            else:
                raise HTTPException(status_code=404, detail="Área funcional no encontrada")
        finally:
            conn.close()

    def update_area_funcional(self, area_id: int, area: AreaFuncional):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE areas_funcionales SET
                nombre_area=%s,
                descripcion=%s
                WHERE id_area=%s""",
                (
                    area.nombre_area,
                    area.descripcion,
                    area_id
                )
            )
            conn.commit()
            return {"resultado": "Área funcional actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar área funcional: {str(err)}")
        finally:
            conn.close()

    def delete_area_funcional(self, area_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM areas_funcionales WHERE id_area = %s", (area_id,))
            conn.commit()
            return {"resultado": "Área funcional eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar área funcional: {str(err)}")
        finally:
            conn.close()