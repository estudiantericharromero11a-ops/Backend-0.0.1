-- Script para agregar campos de autenticación JWT a la tabla personas
-- Ejecutar este script para habilitar el sistema de login con JWT

BEGIN;

-- Agregar columnas de autenticación a personas
ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS username VARCHAR(50) UNIQUE,
ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255),
ADD COLUMN IF NOT EXISTS jwt_token TEXT,
ADD COLUMN IF NOT EXISTS token_expires_at TIMESTAMP;

-- Crear tabla de tokens activos (para mayor control y seguridad)
CREATE TABLE IF NOT EXISTS public.tokens_activos (
    id_token SERIAL PRIMARY KEY,
    id_persona INTEGER NOT NULL REFERENCES personas(id_persona) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_persona FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
);

-- Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_personas_username ON personas(username);
CREATE INDEX IF NOT EXISTS idx_tokens_token ON tokens_activos(token);
CREATE INDEX IF NOT EXISTS idx_tokens_persona ON tokens_activos(id_persona);

-- Crear tabla de roles si no existe
CREATE TABLE IF NOT EXISTS public.roles_usuario (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Insertar roles por defecto
INSERT INTO roles_usuario (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('user', 'Usuario estándar'),
('aiagent', 'Usuario con acceso a IA')
ON CONFLICT (nombre) DO NOTHING;

-- Agregar columna de rol a personas (relación con roles_usuario)
ALTER TABLE IF EXISTS public.personas
ADD COLUMN IF NOT EXISTS id_rol INTEGER REFERENCES roles_usuario(id_rol);

COMMIT;
