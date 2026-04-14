import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.horario_instalacion_model import HorarioInstalacion
from fastapi.encoders import jsonable_encoder

class HorarioInstalacionController:

    def create_horario_instalacion(self, horario: HorarioInstalacion):
        """Crear nuevo horario de instalación. Estado y timestamps se asignan automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO horario_instalacion
                (id_instalacion, dia_semana, hora_apertura, hora_cierre, estado)
                VALUES (%s, %s, %s, %s, 1)
                RETURNING id_horario, created_at, updated_at""",
                (
                    horario.id_instalacion,
                    horario.dia_semana,
                    horario.hora_apertura,
                    horario.hora_cierre
                )
            )
            conn.commit()
            result = cursor.fetchone()
            return {
                "resultado": "Horario de instalación creado",
                "id": result[0],
                "created_at": result[1],
                "updated_at": result[2]
            }
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear horario de instalación: {str(err)}")
        finally:
            conn.close()

    def get_horarios_instalacion(self):
        """Obtener todos los horarios de instalación activos (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_horario, id_instalacion, dia_semana, hora_apertura, hora_cierre, 
                          estado, created_at, updated_at 
                   FROM horario_instalacion WHERE estado = 1 ORDER BY id_horario"""
            )
            result = cursor.fetchall()

            horarios = []
            for data in result:
                horarios.append({
                    "id_horario": data[0],
                    "id_instalacion": data[1],
                    "dia_semana": data[2],
                    "hora_apertura": str(data[3]),
                    "hora_cierre": str(data[4]),
                    "estado": data[5],
                    "created_at": data[6],
                    "updated_at": data[7],
                })
            return jsonable_encoder(horarios)
        except psycopg2.Error:
            raise HTTPException(status_code=500, detail="Error al obtener horarios de instalación")
        finally:
            conn.close()

    def get_horario_instalacion_by_id(self, horario_id: int):
        """Obtener horario de instalación específico activo (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_horario, id_instalacion, dia_semana, hora_apertura, hora_cierre, 
                          estado, created_at, updated_at 
                   FROM horario_instalacion WHERE id_horario = %s AND estado = 1""",
                (horario_id,)
            )
            result = cursor.fetchone()

            if result:
                horario = {
                    "id_horario": result[0],
                    "id_instalacion": result[1],
                    "dia_semana": result[2],
                    "hora_apertura": str(result[3]),
                    "hora_cierre": str(result[4]),
                    "estado": result[5],
                    "created_at": result[6],
                    "updated_at": result[7],
                }
                return jsonable_encoder(horario)
            else:
                raise HTTPException(status_code=404, detail="Horario de instalación no encontrado")
        finally:
            conn.close()

    def update_horario_instalacion(self, horario_id: int, horario: HorarioInstalacion):
        """Actualizar horario de instalación. updated_at se actualiza automáticamente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE horario_instalacion SET
                id_instalacion=%s,
                dia_semana=%s,
                hora_apertura=%s,
                hora_cierre=%s
                WHERE id_horario=%s AND estado = 1
                RETURNING updated_at""",
                (
                    horario.id_instalacion,
                    horario.dia_semana,
                    horario.hora_apertura,
                    horario.hora_cierre,
                    horario_id
                )
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Horario de instalación actualizado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Horario de instalación no encontrado o inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar horario de instalación: {str(err)}")
        finally:
            conn.close()

    def delete_horario_instalacion(self, horario_id: int):
        """Soft delete: desactivar horario de instalación (estado = 0)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE horario_instalacion SET estado = 0 
                   WHERE id_horario = %s AND estado = 1
                   RETURNING updated_at""",
                (horario_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Horario de instalación desactivado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Horario de instalación no encontrado o ya inactivo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar horario de instalación: {str(err)}")
        finally:
            conn.close()

    def restore_horario_instalacion(self, horario_id: int):
        """Restaurar horario de instalación desactivado (estado = 1)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE horario_instalacion SET estado = 1 
                   WHERE id_horario = %s AND estado = 0
                   RETURNING updated_at""",
                (horario_id,)
            )
            conn.commit()
            result = cursor.fetchone()
            
            if result:
                return {
                    "resultado": "Horario de instalación restaurado",
                    "updated_at": result[0]
                }
            else:
                raise HTTPException(status_code=404, detail="Horario de instalación no encontrado o ya activo")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al restaurar horario de instalación: {str(err)}")
        finally:
            conn.close()