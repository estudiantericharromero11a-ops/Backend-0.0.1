import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.programa_materia_model import ProgramaMateria
from fastapi.encoders import jsonable_encoder

class ProgramaMateriaController:

    def create_programa_materia(self, programa_materia: ProgramaMateria):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO programa_materia
                (id_programa, id_materia)
                VALUES (%s, %s)""",
                (
                    programa_materia.id_programa,
                    programa_materia.id_materia
                )
            )
            conn.commit()
            return {"resultado": "Asignación programa-materia creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear asignación: {str(err)}")
        finally:
            conn.close()

    def get_programas_materias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programa_materia")
            result = cursor.fetchall()

            programas_materias = []
            for data in result:
                programas_materias.append({
                    "id_programa": data[0],
                    "id_materia": data[1],
                })
            return jsonable_encoder(programas_materias)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener asignaciones")
        finally:
            conn.close()

    def get_programa_materia_by_id(self, programa_id: int, materia_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programa_materia WHERE id_programa = %s AND id_materia = %s", (programa_id, materia_id))
            result = cursor.fetchone()

            if result:
                programa_materia = {
                    "id_programa": result[0],
                    "id_materia": result[1],
                }
                return jsonable_encoder(programa_materia)
            else:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")
        finally:
            conn.close()

    def delete_programa_materia(self, programa_id: int, materia_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """DELETE FROM programa_materia
                WHERE id_programa=%s AND id_materia=%s""",
                (programa_id, materia_id)
            )
            conn.commit()
            return {"resultado": "Asignación eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(err)}")
        finally:
            conn.close()
