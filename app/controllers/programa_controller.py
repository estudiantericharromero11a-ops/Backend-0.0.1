import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.programa_model import Programa
from fastapi.encoders import jsonable_encoder

class ProgramaController:

    def create_programa(self, programa: Programa):
        """Crear nuevo programa. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO programas
                (nombre, tipo_programa, duracion_semestres, estado)
                VALUES (%s, %s, %s, 1)
                RETURNING id_programa, created_at, updated_at""",
                (
                    programa.nombre,
                    programa.tipo_programa,
                    programa.duracion_semestres
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Programa creado",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear programa: {str(err)}")
        finally:
            conn.close()

    def get_programas(self):
        """Obtener todos los programas activos (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_programa, nombre, tipo_programa, duracion_semestres, 
                          estado, created_at, updated_at 
                   FROM programas WHERE estado = 1 ORDER BY id_programa"""
            )
            result = cursor.fetchall()

            programas = []
            for data in result:
                programas.append({
                    "id_programa": data[0],
                    "nombre": data[1],
                    "tipo_programa": data[2],
                    "duracion_semestres": data[3],
                    "estado": data[4],
                    "created_at": data[5],
                    "updated_at": data[6],
                })
            return jsonable_encoder(programas)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener programas")
        finally:
            conn.close()

    def get_programa_by_id(self, programa_id: int):
        """Obtener programa específico activo (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_programa, nombre, tipo_programa, duracion_semestres, 
                          estado, created_at, updated_at 
                   FROM programas WHERE id_programa = %s AND estado = 1""",
                (programa_id,)
            )
            result = cursor.fetchone()

            if result:
                programa = {
                    "id_programa": result[0],
                    "nombre": result[1],
                    "tipo_programa": result[2],
                    "duracion_semestres": result[3],
                    "estado": result[4],
                    "created_at": result[5],
                    "updated_at": result[6],
                }
                return jsonable_encoder(programa)
            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado")
        finally:
            conn.close()

    def update_programa(self, programa_id: int, programa: Programa):
        """Actualizar programa. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE programas SET
                nombre=%s,
                tipo_programa=%s,
                duracion_semestres=%s
                WHERE id_programa=%s AND estado = 1
                RETURNING updated_at""",
                (
                    programa.nombre,
                    programa.tipo_programa,
                    programa.duracion_semestres,
                    programa_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Programa actualizado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado o inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar programa: {str(err)}")
        finally:
            conn.close()

    def delete_programa(self, programa_id: int):
        """Soft delete: desactivar programa (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE programas SET estado = 0 
                   WHERE id_programa = %s AND estado = 1
                   RETURNING updated_at""",
                (programa_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Programa desactivado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado o ya inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar programa: {str(err)}")
        finally:
            conn.close()

    def restore_programa(self, programa_id: int):
        """Restaurar programa desactivado (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE programas SET estado = 1 
                   WHERE id_programa = %s AND estado = 0
                   RETURNING updated_at""",
                (programa_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Programa restaurado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Programa no encontrado o ya activo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar programa: {str(err)}")
        finally:
            conn.close()