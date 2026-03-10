import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.persona_model import Persona
from fastapi.encoders import jsonable_encoder

class PersonaController:

    def create_persona(self, persona: Persona):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO personas
                (nombre, documento, correo, telefono)
                VALUES (%s, %s, %s, %s)""",
                (
                    persona.nombre,
                    persona.documento,
                    persona.correo,
                    persona.telefono
                )
            )
            conn.commit()
            return {"resultado": "Persona creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear persona: {str(err)}")
        finally:
            conn.close()

    def get_personas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas")
            result = cursor.fetchall()

            personas = []
            for data in result:
                personas.append({
                    "id_persona": data[0],
                    "nombre": data[1],
                    "documento": data[2],
                    "correo": data[3],
                    "telefono": data[4],
                })
            return jsonable_encoder(personas)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener personas")
        finally:
            conn.close()

    def get_persona_by_id(self, persona_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas WHERE id_persona = %s", (persona_id,))
            result = cursor.fetchone()

            if result:
                persona = {
                    "id_persona": result[0],
                    "nombre": result[1],
                    "documento": result[2],
                    "correo": result[3],
                    "telefono": result[4],
                }
                return jsonable_encoder(persona)
            else:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
        finally:
            conn.close()

    def update_persona(self, persona_id: int, persona: Persona):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE personas SET
                nombre=%s,
                documento=%s,
                correo=%s,
                telefono=%s
                WHERE id_persona=%s""",
                (
                    persona.nombre,
                    persona.documento,
                    persona.correo,
                    persona.telefono,
                    persona_id
                )
            )
            conn.commit()
            return {"resultado": "Persona actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar persona: {str(err)}")
        finally:
            conn.close()

    def delete_persona(self, persona_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM personas WHERE id_persona = %s", (persona_id,))
            conn.commit()
            return {"resultado": "Persona eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar persona: {str(err)}")
        finally:
            conn.close()