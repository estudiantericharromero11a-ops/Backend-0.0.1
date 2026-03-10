import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.instalacion_model import Instalacion
from fastapi.encoders import jsonable_encoder

class InstalacionController:

    def create_instalacion(self, instalacion: Instalacion):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO instalaciones
                (nombre, tipo_instalacion, piso, capacidad, id_bloque, id_area, id_estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
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
            return {"resultado": "Instalación creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear instalación: {str(err)}")
        finally:
            conn.close()

    def get_instalaciones(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM instalaciones")
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
                })
            return jsonable_encoder(instalaciones)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener instalaciones")
        finally:
            conn.close()

    def get_instalacion_by_id(self, instalacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM instalaciones WHERE id_instalacion = %s", (instalacion_id,))
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
                }
                return jsonable_encoder(instalacion)
            else:
                raise HTTPException(status_code=404, detail="Instalación no encontrada")
        finally:
            conn.close()

    def update_instalacion(self, instalacion_id: int, instalacion: Instalacion):
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
                WHERE id_instalacion=%s""",
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
            return {"resultado": "Instalación actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar instalación: {str(err)}")
        finally:
            conn.close()

    def delete_instalacion(self, instalacion_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM instalaciones WHERE id_instalacion = %s", (instalacion_id,))
            conn.commit()
            return {"resultado": "Instalación eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar instalación: {str(err)}")
        finally:
            conn.close()