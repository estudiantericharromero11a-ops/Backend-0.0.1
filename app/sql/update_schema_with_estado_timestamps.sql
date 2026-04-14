-- Script para agregar campos estado y timestamps a todas las tablas
-- Con triggers automáticos para updated_at

BEGIN;

-- ============================================================================
-- 1. AGREGAR CAMPOS A TODAS LAS TABLAS
-- ============================================================================

-- Campus
ALTER TABLE IF EXISTS public.campus
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Bloques
ALTER TABLE IF EXISTS public.bloques
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Áreas Funcionales
ALTER TABLE IF EXISTS public.areas_funcionales
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Estado Instalación
ALTER TABLE IF EXISTS public.estado_instalacion
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Instalaciones
ALTER TABLE IF EXISTS public.instalaciones
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Horario Instalación
ALTER TABLE IF EXISTS public.horario_instalacion
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Personas
ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Roles
ALTER TABLE IF EXISTS public.roles
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Programas
ALTER TABLE IF EXISTS public.programas
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Materias
ALTER TABLE IF EXISTS public.materias
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Asignación Instalaciones
ALTER TABLE IF EXISTS public.asignacion_instalaciones
ADD COLUMN IF NOT EXISTS estado INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Persona Rol (tabla puente)
ALTER TABLE IF EXISTS public.persona_rol
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Programa Materia (tabla puente)
ALTER TABLE IF EXISTS public.programa_materia
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- ============================================================================
-- 2. CREAR FUNCIÓN TRIGGER PARA ACTUALIZAR updated_at
-- ============================================================================

-- Crear función que se ejecute cuando se actualiza un registro
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3. CREAR TRIGGERS EN TODAS LAS TABLAS
-- ============================================================================

-- Trigger para campus
DROP TRIGGER IF EXISTS campus_update_updated_at ON public.campus;
CREATE TRIGGER campus_update_updated_at
BEFORE UPDATE ON public.campus
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para bloques
DROP TRIGGER IF EXISTS bloques_update_updated_at ON public.bloques;
CREATE TRIGGER bloques_update_updated_at
BEFORE UPDATE ON public.bloques
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para areas_funcionales
DROP TRIGGER IF EXISTS areas_funcionales_update_updated_at ON public.areas_funcionales;
CREATE TRIGGER areas_funcionales_update_updated_at
BEFORE UPDATE ON public.areas_funcionales
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para estado_instalacion
DROP TRIGGER IF EXISTS estado_instalacion_update_updated_at ON public.estado_instalacion;
CREATE TRIGGER estado_instalacion_update_updated_at
BEFORE UPDATE ON public.estado_instalacion
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para instalaciones
DROP TRIGGER IF EXISTS instalaciones_update_updated_at ON public.instalaciones;
CREATE TRIGGER instalaciones_update_updated_at
BEFORE UPDATE ON public.instalaciones
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para horario_instalacion
DROP TRIGGER IF EXISTS horario_instalacion_update_updated_at ON public.horario_instalacion;
CREATE TRIGGER horario_instalacion_update_updated_at
BEFORE UPDATE ON public.horario_instalacion
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para personas
DROP TRIGGER IF EXISTS personas_update_updated_at ON public.personas;
CREATE TRIGGER personas_update_updated_at
BEFORE UPDATE ON public.personas
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para roles
DROP TRIGGER IF EXISTS roles_update_updated_at ON public.roles;
CREATE TRIGGER roles_update_updated_at
BEFORE UPDATE ON public.roles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para programas
DROP TRIGGER IF EXISTS programas_update_updated_at ON public.programas;
CREATE TRIGGER programas_update_updated_at
BEFORE UPDATE ON public.programas
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para materias
DROP TRIGGER IF EXISTS materias_update_updated_at ON public.materias;
CREATE TRIGGER materias_update_updated_at
BEFORE UPDATE ON public.materias
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para asignacion_instalaciones
DROP TRIGGER IF EXISTS asignacion_instalaciones_update_updated_at ON public.asignacion_instalaciones;
CREATE TRIGGER asignacion_instalaciones_update_updated_at
BEFORE UPDATE ON public.asignacion_instalaciones
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para persona_rol
DROP TRIGGER IF EXISTS persona_rol_update_updated_at ON public.persona_rol;
CREATE TRIGGER persona_rol_update_updated_at
BEFORE UPDATE ON public.persona_rol
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para programa_materia
DROP TRIGGER IF EXISTS programa_materia_update_updated_at ON public.programa_materia;
CREATE TRIGGER programa_materia_update_updated_at
BEFORE UPDATE ON public.programa_materia
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

COMMIT;

-- ============================================================================
-- Verificación: Listar todas las tablas y sus columnas
-- ============================================================================
-- SELECT table_name, column_name, data_type 
-- FROM information_schema.columns 
-- WHERE table_schema = 'public' 
-- ORDER BY table_name, ordinal_position;
