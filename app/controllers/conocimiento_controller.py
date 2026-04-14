import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.conocimiento_model import Conocimiento
from fastapi.encoders import jsonable_encoder

class ConocimientoController:

    def create_conocimiento(self, conocimiento: Conocimiento):
        """Crear nuevo conocimiento."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO conocimiento
                (contenido, embedding)
                VALUES (%s, %s)
                RETURNING id""",
                (
                    conocimiento.contenido,
                    conocimiento.embedding
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Conocimiento creado",
                "id": result[0]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear conocimiento: {str(err)}")
        finally:
            conn.close()

    def get_conocimientos(self):
        """Obtener todos los conocimientos."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, contenido, embedding FROM conocimiento ORDER BY id")
            result = cursor.fetchall()

            conocimientos = []
            for data in result:
                conocimientos.append({
                    "id": data[0],
                    "contenido": data[1],
                    "embedding": data[2],
                })
            return jsonable_encoder(conocimientos)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener conocimientos")
        finally:
            conn.close()

    def get_conocimiento_by_id(self, conocimiento_id: int):
        """Obtener conocimiento específico."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, contenido, embedding FROM conocimiento WHERE id = %s", (conocimiento_id,))
            result = cursor.fetchone()

            if result:
                conocimiento = {
                    "id": result[0],
                    "contenido": result[1],
                    "embedding": result[2],
                }
                return jsonable_encoder(conocimiento)
            else:
                raise HTTPException(status_code=404, detail="Conocimiento no encontrado")
        finally:
            conn.close()

    def update_conocimiento(self, conocimiento_id: int, conocimiento: Conocimiento):
        """Actualizar conocimiento existente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE conocimiento SET
                contenido=%s,
                embedding=%s
                WHERE id=%s""",
                (
                    conocimiento.contenido,
                    conocimiento.embedding,
                    conocimiento_id
                )
            )
            conn.commit()
            return {"resultado": "Conocimiento actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar conocimiento: {str(err)}")
        finally:
            conn.close()

    def delete_conocimiento(self, conocimiento_id: int):
        """Eliminar conocimiento."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conocimiento WHERE id = %s", (conocimiento_id,))
            conn.commit()
            return {"resultado": "Conocimiento eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar conocimiento: {str(err)}")
        finally:
            conn.close()
