import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.persona_model import Persona
from fastapi.encoders import jsonable_encoder

class PersonaController:

    def create_persona(self, persona: Persona):
        """Crear una nueva persona. Estado y timestamps se asignan automáticamente en la BD."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO personas
                (nombre, documento, correo, telefono, estado)
                VALUES (%s, %s, %s, %s, 1)
                RETURNING id_persona, created_at, updated_at""",
                (
                    persona.nombre,
                    persona.documento,
                    persona.correo,
                    persona.telefono
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Persona creada", 
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear persona: {str(err)}")
        finally:
            conn.close()

    def get_personas(self):
        """Obtener todas las personas activas (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_persona, nombre, documento, correo, telefono, 
                          estado, created_at, updated_at 
                   FROM personas WHERE estado = 1 ORDER BY id_persona"""
            )
            result = cursor.fetchall()

            personas = []
            for data in result:
                personas.append({
                    "id_persona": data[0],
                    "nombre": data[1],
                    "documento": data[2],
                    "correo": data[3],
                    "telefono": data[4],
                    "estado": data[5],
                    "created_at": data[6],
                    "updated_at": data[7],
                })
            return jsonable_encoder(personas)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener personas")
        finally:
            conn.close()

    def get_persona_by_id(self, persona_id: int):
        """Obtener una persona específica activa (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_persona, nombre, documento, correo, telefono, 
                          estado, created_at, updated_at 
                   FROM personas WHERE id_persona = %s AND estado = 1""", 
                (persona_id,)
            )
            result = cursor.fetchone()

            if result:
                persona = {
                    "id_persona": result[0],
                    "nombre": result[1],
                    "documento": result[2],
                    "correo": result[3],
                    "telefono": result[4],
                    "estado": result[5],
                    "created_at": result[6],
                    "updated_at": result[7],
                }
                return jsonable_encoder(persona)
            else:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
        finally:
            conn.close()

    def update_persona(self, persona_id: int, persona: Persona):
        """Actualizar persona. El campo updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE personas SET
                nombre=%s,
                documento=%s,
                correo=%s,
                telefono=%s
                WHERE id_persona=%s AND estado = 1
                RETURNING updated_at""",
                (
                    persona.nombre,
                    persona.documento,
                    persona.correo,
                    persona.telefono,
                    persona_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Persona actualizada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Persona no encontrada o inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar persona: {str(err)}")
        finally:
            conn.close()

    def delete_persona(self, persona_id: int):
        """Soft delete: desactivar persona (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE personas SET estado = 0 
                   WHERE id_persona = %s AND estado = 1
                   RETURNING updated_at""",
                (persona_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Persona desactivada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Persona no encontrada o ya inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar persona: {str(err)}")
        finally:
            conn.close()

    def restore_persona(self, persona_id: int):
        """Restaurar una persona desactivada (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE personas SET estado = 1 
                   WHERE id_persona = %s AND estado = 0
                   RETURNING updated_at""",
                (persona_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Persona restaurada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Persona no encontrada o ya activa")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar persona: {str(err)}")
        finally:
            conn.close()