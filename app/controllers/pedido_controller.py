import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.bloque_model import Bloque
from fastapi.encoders import jsonable_encoder

class BloqueController:

    def create_bloque(self, bloque: Bloque):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO bloques
                (nombre, descripcion, id_campus)
                VALUES (%s, %s, %s)""",
                (
                    bloque.nombre,
                    bloque.descripcion,
                    bloque.id_campus
                )
            )
            conn.commit()
            return {"resultado": "Bloque creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear bloque: {str(err)}")
        finally:
            conn.close()

    def get_bloques(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bloques")
            result = cursor.fetchall()

            bloques = []
            for data in result:
                bloques.append({
                    "id_bloque": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "id_campus": data[3],
                    "estado": data[4],
                    "created_at": data[5],
                    "updated_at": data[6],
                })
            return jsonable_encoder(bloques)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener bloques")
        finally:
            conn.close()

    def get_bloque_by_id(self, bloque_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bloques WHERE id_bloque = %s", (bloque_id,))
            result = cursor.fetchone()

            if result:
                bloque = {
                    "id_bloque": result[0],
                    "nombre": result[1],
                    "descripcion": result[2],
                    "id_campus": result[3],
                    "estado": result[4],
                    "created_at": result[5],
                    "updated_at": result[6],
                }
                return jsonable_encoder(bloque)
            else:
                raise HTTPException(status_code=404, detail="Bloque no encontrado")
        finally:
            conn.close()

    def update_bloque(self, bloque_id: int, bloque: Bloque):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE bloques SET
                nombre=%s,
                descripcion=%s,
                id_campus=%s
                WHERE id_bloque=%s""",
                (
                    bloque.nombre,
                    bloque.descripcion,
                    bloque.id_campus,
                    bloque_id
                )
            )
            conn.commit()
            return {"resultado": "Bloque actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar bloque: {str(err)}")
        finally:
            conn.close()

    def delete_bloque(self, bloque_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bloques WHERE id_bloque = %s", (bloque_id,))
            conn.commit()
            return {"resultado": "Bloque eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar bloque: {str(err)}")
        finally:
            conn.close()
