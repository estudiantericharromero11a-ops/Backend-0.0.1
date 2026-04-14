import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.asignacion_instalacion_model import AsignacionInstalacion
from fastapi.encoders import jsonable_encoder

class AsignacionInstalacionController:

    def create_asignacion_instalacion(self, asignacion: AsignacionInstalacion):
        """Crear nueva asignación de instalación. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO asignacion_instalaciones
                (id_instalacion, id_materia, dia_semana, hora_inicio, hora_fin, id_persona, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
                RETURNING id_asignacion, created_at, updated_at""",
                (
                    asignacion.id_instalacion,
                    asignacion.id_materia,
                    asignacion.dia_semana,
                    asignacion.hora_inicio,
                    asignacion.hora_fin,
                    asignacion.id_persona
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Asignación de instalación creada",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear asignación de instalación: {str(err)}")
        finally:
            conn.close()

    def get_asignaciones_instalaciones(self):
        """Obtener todas las asignaciones de instalaciones activas (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_asignacion, id_instalacion, id_materia, dia_semana, hora_inicio, hora_fin, 
                          id_persona, estado, created_at, updated_at 
                   FROM asignacion_instalaciones WHERE estado = 1 ORDER BY id_asignacion"""
            )
            result = cursor.fetchall()

            asignaciones = []
            for data in result:
                asignaciones.append({
                    "id_asignacion": data[0],
                    "id_instalacion": data[1],
                    "id_materia": data[2],
                    "dia_semana": data[3],
                    "hora_inicio": str(data[4]) if data[4] else None,
                    "hora_fin": str(data[5]) if data[5] else None,
                    "id_persona": data[6],
                    "estado": data[7],
                    "created_at": data[8],
                    "updated_at": data[9],
                })
            return jsonable_encoder(asignaciones)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener asignaciones de instalaciones")
        finally:
            conn.close()

    def get_asignacion_instalacion_by_id(self, asignacion_id: int):
        """Obtener asignación de instalación específica activa (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_asignacion, id_instalacion, id_materia, dia_semana, hora_inicio, hora_fin, 
                          id_persona, estado, created_at, updated_at 
                   FROM asignacion_instalaciones WHERE id_asignacion = %s AND estado = 1""",
                (asignacion_id,)
            )
            result = cursor.fetchone()

            if result:
                asignacion = {
                    "id_asignacion": result[0],
                    "id_instalacion": result[1],
                    "id_materia": result[2],
                    "dia_semana": result[3],
                    "hora_inicio": str(result[4]) if result[4] else None,
                    "hora_fin": str(result[5]) if result[5] else None,
                    "id_persona": result[6],
                    "estado": result[7],
                    "created_at": result[8],
                    "updated_at": result[9],
                }
                return jsonable_encoder(asignacion)
            else:
                raise HTTPException(status_code=404, detail="Asignación de instalación no encontrada")
        finally:
            conn.close()

    def update_asignacion_instalacion(self, asignacion_id: int, asignacion: AsignacionInstalacion):
        """Actualizar asignación de instalación. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE asignacion_instalaciones SET
                id_instalacion=%s,
                id_materia=%s,
                dia_semana=%s,
                hora_inicio=%s,
                hora_fin=%s,
                id_persona=%s
                WHERE id_asignacion=%s AND estado = 1
                RETURNING updated_at""",
                (
                    asignacion.id_instalacion,
                    asignacion.id_materia,
                    asignacion.dia_semana,
                    asignacion.hora_inicio,
                    asignacion.hora_fin,
                    asignacion.id_persona,
                    asignacion_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Asignación de instalación actualizada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Asignación de instalación no encontrada o inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar asignación de instalación: {str(err)}")
        finally:
            conn.close()

    def delete_asignacion_instalacion(self, asignacion_id: int):
        """Soft delete: desactivar asignación de instalación (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE asignacion_instalaciones SET estado = 0 
                   WHERE id_asignacion = %s AND estado = 1
                   RETURNING updated_at""",
                (asignacion_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Asignación de instalación desactivada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Asignación de instalación no encontrada o ya inactiva")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar asignación de instalación: {str(err)}")
        finally:
            conn.close()

    def restore_asignacion_instalacion(self, asignacion_id: int):
        """Restaurar asignación de instalación desactivada (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE asignacion_instalaciones SET estado = 1 
                   WHERE id_asignacion = %s AND estado = 0
                   RETURNING updated_at""",
                (asignacion_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Asignación de instalación restaurada",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Asignación de instalación no encontrada o ya activa")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar asignación de instalación: {str(err)}")
        finally:
            conn.close()