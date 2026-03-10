import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.campus_model import Campus
from fastapi.encoders import jsonable_encoder

class CampusController:
        
    def create_campus(self, campus: Campus):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO campus
                (nombre, direccion, descripcion)
                VALUES (%s, %s, %s)""",
                (
                    campus.nombre,
                    campus.direccion,
                    campus.descripcion
                )
            )
            conn.commit()
            return {"resultado": "Campus creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear campus: {str(err)}")
        finally:
            conn.close()
        

    def get_campus(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM campus")
            result = cursor.fetchall()

            campus_list = []
            for data in result:
                campus_list.append({
                    "id_campus": data[0],
                    "nombre": data[1],
                    "direccion": data[2],
                    "descripcion": data[3],
                })
            return jsonable_encoder(campus_list)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener campus")
        finally:
            conn.close()


    def get_campus_by_id(self, campus_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM campus WHERE id_campus = %s", (campus_id,))
            result = cursor.fetchone()

            if result:
                campus = {
                    "id_campus": result[0],
                    "nombre": result[1],
                    "direccion": result[2],
                    "descripcion": result[3],
                }
                return jsonable_encoder(campus)
            else:
                raise HTTPException(status_code=404, detail="Campus no encontrado")
        finally:
            conn.close()


    def update_campus(self, campus_id: int, campus: Campus):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE campus SET
                nombre=%s,
                direccion=%s,
                descripcion=%s
                WHERE id_campus=%s""",
                (
                    campus.nombre,
                    campus.direccion,
                    campus.descripcion,
                    campus_id
                )
            )
            conn.commit()
            return {"resultado": "Campus actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar campus: {str(err)}")
        finally:
            conn.close()


    def delete_campus(self, campus_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM campus WHERE id_campus = %s", (campus_id,))
            conn.commit()
            return {"resultado": "Campus eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar campus: {str(err)}")
        finally:
            conn.close()
