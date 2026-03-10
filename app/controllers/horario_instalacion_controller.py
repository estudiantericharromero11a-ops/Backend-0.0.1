import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.horario_instalacion_model import HorarioInstalacion
from fastapi.encoders import jsonable_encoder

class HorarioInstalacionController:

    def create_horario_instalacion(self, horario: HorarioInstalacion):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO horario_instalacion
                (id_instalacion, dia_semana, hora_apertura, hora_cierre)
                VALUES (%s, %s, %s, %s)""",
                (
                    horario.id_instalacion,
                    horario.dia_semana,
                    horario.hora_apertura,
                    horario.hora_cierre
                )
            )
            conn.commit()
            return {"resultado": "Horario de instalación creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear horario de instalación: {str(err)}")
        finally:
            conn.close()

    def get_horarios_instalacion(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horario_instalacion")
            result = cursor.fetchall()

            horarios = []
            for data in result:
                horarios.append({
                    "id_horario": data[0],
                    "id_instalacion": data[1],
                    "dia_semana": data[2],
                    "hora_apertura": str(data[3]),
                    "hora_cierre": str(data[4]),
                })
            return jsonable_encoder(horarios)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener horarios de instalación")
        finally:
            conn.close()

    def get_horario_instalacion_by_id(self, horario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horario_instalacion WHERE id_horario = %s", (horario_id,))
            result = cursor.fetchone()

            if result:
                horario = {
                    "id_horario": result[0],
                    "id_instalacion": result[1],
                    "dia_semana": result[2],
                    "hora_apertura": str(result[3]),
                    "hora_cierre": str(result[4]),
                }
                return jsonable_encoder(horario)
            else:
                raise HTTPException(status_code=404, detail="Horario de instalación no encontrado")
        finally:
            conn.close()

    def update_horario_instalacion(self, horario_id: int, horario: HorarioInstalacion):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE horario_instalacion SET
                id_instalacion=%s,
                dia_semana=%s,
                hora_apertura=%s,
                hora_cierre=%s
                WHERE id_horario=%s""",
                (
                    horario.id_instalacion,
                    horario.dia_semana,
                    horario.hora_apertura,
                    horario.hora_cierre,
                    horario_id
                )
            )
            conn.commit()
            return {"resultado": "Horario de instalación actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar horario de instalación: {str(err)}")
        finally:
            conn.close()

    def delete_horario_instalacion(self, horario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM horario_instalacion WHERE id_horario = %s", (horario_id,))
            conn.commit()
            return {"resultado": "Horario de instalación eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar horario de instalación: {str(err)}")
        finally:
            conn.close()