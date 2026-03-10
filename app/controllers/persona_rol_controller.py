import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.persona_rol_model import PersonaRol
from fastapi.encoders import jsonable_encoder

class PersonaRolController:

    def create_persona_rol(self, persona_rol: PersonaRol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO persona_rol
                (id_persona, id_rol)
                VALUES (%s, %s)""",
                (
                    persona_rol.id_persona,
                    persona_rol.id_rol
                )
            )
            conn.commit()
            return {"resultado": "Asignación persona-rol creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear asignación: {str(err)}")
        finally:
            conn.close()

    def get_personas_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM persona_rol")
            result = cursor.fetchall()

            personas_roles = []
            for data in result:
                personas_roles.append({
                    "id_persona": data[0],
                    "id_rol": data[1],
                })
            return jsonable_encoder(personas_roles)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener asignaciones")
        finally:
            conn.close()

    def get_persona_rol_by_id(self, persona_id: int, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM persona_rol WHERE id_persona = %s AND id_rol = %s", (persona_id, rol_id))
            result = cursor.fetchone()

            if result:
                persona_rol = {
                    "id_persona": result[0],
                    "id_rol": result[1],
                }
                return jsonable_encoder(persona_rol)
            else:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")
        finally:
            conn.close()

    def delete_persona_rol(self, persona_id: int, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """DELETE FROM persona_rol
                WHERE id_persona=%s AND id_rol=%s""",
                (persona_id, rol_id)
            )
            conn.commit()
            return {"resultado": "Asignación eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(err)}")
        finally:
            conn.close()
