import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.materia_model import Materia
from fastapi.encoders import jsonable_encoder

class MateriaController:

    def create_materia(self, materia: Materia):
        """Crear nueva materia. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO materias
                (nombre, creditos, descripcion, estado)
                VALUES (%s, %s, %s, 1)
                RETURNING id_materia, created_at, updated_at""",
                (
                    materia.nombre,
                    materia.creditos,
                    materia.descripcion
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Materia creada",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear materia: {str(err)}")
        finally:
            conn.close()

    def get_materias(self):
        """Obtener todas las materias activas (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_materia, nombre, creditos, descripcion, estado, created_at, updated_at 
                   FROM materias WHERE estado = 1 ORDER BY id_materia"""
            )
            result = cursor.fetchall()

            materias = []
            for data in result:
                materias.append({
                    "id_materia": data[0],
                    "nombre": data[1],
                    "creditos": data[2],
                    "descripcion": data[3],
                    "estado": data[4],
                    "created_at": data[5],
                    "updated_at": data[6],
                })
            return jsonable_encoder(materias)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener materias")
        finally:
            conn.close()

    def get_materia_by_id(self, materia_id: int):
        """Obtener materia específica activa (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_materia, nombre, creditos, descripcion, estado, created_at, updated_at 
                   FROM materias WHERE id_materia = %s AND estado = 1""",
                (materia_id,)
            )
            result = cursor.fetchone()

            if result:
                materia = {
                    "id_materia": result[0],
                    "nombre": result[1],
                    "creditos": result[2],
                    "descripcion": result[3],
                    "estado": result[4],
                    "created_at": result[5],
                    "updated_at": result[6],
                }
                return jsonable_encoder(materia)
            else:
                raise HTTPException(status_code=404, detail="Materia no encontrada")
        finally:
            conn.close()

    def update_materia(self, materia_id: int, materia: Materia):
        """Actualizar materia. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE materias SET
                nombre=%s,
                creditos=%s,
                descripcion=%s
                WHERE id_materia=%s AND estado = 1
                RETURNING updated_at""",
                (
                    materia.nombre,
                    materia.creditos,
                    materia.descripcion,
                    materia_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Materia actualizada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Materia no encontrada o inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar materia: {str(err)}")
        finally:
            conn.close()

    def delete_materia(self, materia_id: int):
        """Soft delete: desactivar materia (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE materias SET estado = 0 
                   WHERE id_materia = %s AND estado = 1
                   RETURNING updated_at""",
                (materia_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Materia desactivada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Materia no encontrada o ya inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar materia: {str(err)}")
        finally:
            conn.close()

    def restore_materia(self, materia_id: int):
        """Restaurar materia desactivada (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE materias SET estado = 1 
                   WHERE id_materia = %s AND estado = 0
                   RETURNING updated_at""",
                (materia_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Materia restaurada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Materia no encontrada o ya activa")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar materia: {str(err)}")
        finally:
            conn.close()