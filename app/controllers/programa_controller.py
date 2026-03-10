import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.programa_model import Programa
from fastapi.encoders import jsonable_encoder

class ProgramaController:

    def create_programa(self, programa: Programa):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO programas
                (nombre, tipo_programa, duracion_semestres)
                VALUES (%s, %s, %s)""",
                (
                    programa.nombre,
                    programa.tipo_programa,
                    programa.duracion_semestres
                )
            )
            conn.commit()
            return {"resultado": "Programa creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear programa: {str(err)}")
        finally:
            conn.close()

    def get_programas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programas")
            result = cursor.fetchall()

            programas = []
            for data in result:
                programas.append({
                    "id_programa": data[0],
                    "nombre": data[1],
                    "tipo_programa": data[2],
                    "duracion_semestres": data[3],
                })
            return jsonable_encoder(programas)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener programas")
        finally:
            conn.close()

    def get_programa_by_id(self, programa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programas WHERE id_programa = %s", (programa_id,))
            result = cursor.fetchone()

            if result:
                programa = {
                    "id_programa": result[0],
                    "nombre": result[1],
                    "tipo_programa": result[2],
                    "duracion_semestres": result[3],
                }
                return jsonable_encoder(programa)
            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado")
        finally:
            conn.close()

    def update_programa(self, programa_id: int, programa: Programa):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE programas SET
                nombre=%s,
                tipo_programa=%s,
                duracion_semestres=%s
                WHERE id_programa=%s""",
                (
                    programa.nombre,
                    programa.tipo_programa,
                    programa.duracion_semestres,
                    programa_id
                )
            )
            conn.commit()
            return {"resultado": "Programa actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar programa: {str(err)}")
        finally:
            conn.close()

    def delete_programa(self, programa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programas WHERE id_programa = %s", (programa_id,))
            conn.commit()
            return {"resultado": "Programa eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar programa: {str(err)}")
        finally:
            conn.close()