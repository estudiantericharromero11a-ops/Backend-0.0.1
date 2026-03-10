import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.materia_model import Materia
from fastapi.encoders import jsonable_encoder

class MateriaController:

    def create_materia(self, materia: Materia):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO materias
                (nombre, creditos, descripcion)
                VALUES (%s, %s, %s)""",
                (
                    materia.nombre,
                    materia.creditos,
                    materia.descripcion
                )
            )
            conn.commit()
            return {"resultado": "Materia creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear materia: {str(err)}")
        finally:
            conn.close()

    def get_materias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materias")
            result = cursor.fetchall()

            materias = []
            for data in result:
                materias.append({
                    "id_materia": data[0],
                    "nombre": data[1],
                    "creditos": data[2],
                    "descripcion": data[3],
                })
            return jsonable_encoder(materias)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener materias")
        finally:
            conn.close()

    def get_materia_by_id(self, materia_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materias WHERE id_materia = %s", (materia_id,))
            result = cursor.fetchone()

            if result:
                materia = {
                    "id_materia": result[0],
                    "nombre": result[1],
                    "creditos": result[2],
                    "descripcion": result[3],
                }
                return jsonable_encoder(materia)
            else:
                raise HTTPException(status_code=404, detail="Materia no encontrada")
        finally:
            conn.close()

    def update_materia(self, materia_id: int, materia: Materia):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE materias SET
                nombre=%s,
                creditos=%s,
                descripcion=%s
                WHERE id_materia=%s""",
                (
                    materia.nombre,
                    materia.creditos,
                    materia.descripcion,
                    materia_id
                )
            )
            conn.commit()
            return {"resultado": "Materia actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar materia: {str(err)}")
        finally:
            conn.close()

    def delete_materia(self, materia_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materias WHERE id_materia = %s", (materia_id,))
            conn.commit()
            return {"resultado": "Materia eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar materia: {str(err)}")
        finally:
            conn.close()