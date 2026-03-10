import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.estado_instalacion_model import EstadoInstalacion
from fastapi.encoders import jsonable_encoder

class EstadoInstalacionController:

    def create_estado_instalacion(self, estado: EstadoInstalacion):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO estado_instalacion
                (nombre_estado, descripcion)
                VALUES (%s, %s)""",
                (
                    estado.nombre_estado,
                    estado.descripcion
                )
            )
            conn.commit()
            return {"resultado": "Estado de instalación creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear estado de instalación: {str(err)}")
        finally:
            conn.close()

    def get_estados_instalacion(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estado_instalacion")
            result = cursor.fetchall()

            estados = []
            for data in result:
                estados.append({
                    "id_estado": data[0],
                    "nombre_estado": data[1],
                    "descripcion": data[2],
                })
            return jsonable_encoder(estados)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener estados de instalación")
        finally:
            conn.close()

    def get_estado_instalacion_by_id(self, estado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estado_instalacion WHERE id_estado = %s", (estado_id,))
            result = cursor.fetchone()

            if result:
                estado = {
                    "id_estado": result[0],
                    "nombre_estado": result[1],
                    "descripcion": result[2],
                }
                return jsonable_encoder(estado)
            else:
                raise HTTPException(status_code=404, detail="Estado de instalación no encontrado")
        finally:
            conn.close()

    def update_estado_instalacion(self, estado_id: int, estado: EstadoInstalacion):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE estado_instalacion SET
                nombre_estado=%s,
                descripcion=%s
                WHERE id_estado=%s""",
                (
                    estado.nombre_estado,
                    estado.descripcion,
                    estado_id
                )
            )
            conn.commit()
            return {"resultado": "Estado de instalación actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar estado de instalación: {str(err)}")
        finally:
            conn.close()

    def delete_estado_instalacion(self, estado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estado_instalacion WHERE id_estado = %s", (estado_id,))
            conn.commit()
            return {"resultado": "Estado de instalación eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar estado de instalación: {str(err)}")
        finally:
            conn.close()