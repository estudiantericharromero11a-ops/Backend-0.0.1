-- Script PASO A PASO para agregar autenticación JWT
-- Ejecutar en PostgreSQL sin transacciones para evitar errores

-- PASO 1: Crear tabla de roles PRIMERO (antes de cualquier otra cosa)
DROP TABLE IF EXISTS public.roles_usuario CASCADE;

CREATE TABLE public.roles_usuario (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE,
    descripcion TEXT
);

-- PASO 2: Insertar roles por defecto
INSERT INTO public.roles_usuario (nombre, descripcion) VALUES
    ('admin', 'Administrador del sistema'),
    ('user', 'Usuario estándar'),
    ('aiagent', 'Usuario con acceso a IA');

-- PASO 3: Agregar columnas a tabla personas
ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS username VARCHAR(50) UNIQUE;

ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS jwt_token TEXT;

ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS token_expires_at TIMESTAMP;

ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS id_rol INTEGER REFERENCES public.roles_usuario(id_rol);

-- PASO 4: Crear tabla de tokens activos
DROP TABLE IF EXISTS public.tokens_activos CASCADE;

CREATE TABLE public.tokens_activos (
    id_token SERIAL PRIMARY KEY,
    id_persona INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_tokens_persona FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona) ON DELETE CASCADE
);

-- PASO 5: Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_personas_username ON public.personas(username);
CREATE INDEX IF NOT EXISTS idx_tokens_token ON public.tokens_activos(token);
CREATE INDEX IF NOT EXISTS idx_tokens_persona ON public.tokens_activos(id_persona);

-- PASO 6: Verificar que todo se creó
SELECT 'Tabla roles_usuario creada' as status;
SELECT COUNT(*) as total_roles FROM public.roles_usuario;
SELECT 'Tabla tokens_activos creada' as status;
SELECT column_name FROM information_schema.columns WHERE table_name='personas' AND column_name IN ('username', 'password_hash', 'id_rol');
