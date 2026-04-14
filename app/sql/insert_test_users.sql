-- Script para insertar usuarios de prueba
-- NOTA: Los hashes están generados con bcrypt para la contraseña "admin123"
-- Para cambiarlos, ejecutar scripts/generate_password_hash.py

BEGIN;

-- Insertar roles si no existen
INSERT INTO roles_usuario (id_rol, nombre, descripcion) VALUES 
(1, 'admin', 'Administrador del sistema'),
(2, 'user', 'Usuario estándar'),
(3, 'aiagent', 'Usuario con acceso a IA')
ON CONFLICT (nombre) DO NOTHING;

-- Insertar usuario ADMIN (username: admin, password: admin123)
INSERT INTO personas (nombre, documento, correo, username, password_hash, id_rol, estado)
VALUES 
  ('Administrador', '1234567890', 'admin@universidad.edu', 'admin', 
   '$2b$12$1E9ztBRlV2DqzqM3UYZQkeWUEiFP5XMl3Md5KY4VQvhJq5qxXWEi.', 1, 1)
ON CONFLICT (username) DO NOTHING;

-- Insertar usuario USER (username: user, password: admin123)
INSERT INTO personas (nombre, documento, correo, username, password_hash, id_rol, estado)
VALUES 
  ('Usuario Regular', '9876543210', 'user@universidad.edu', 'user', 
   '$2b$12$1E9ztBRlV2DqzqM3UYZQkeWUEiFP5XMl3Md5KY4VQvhJq5qxXWEi.', 2, 1)
ON CONFLICT (username) DO NOTHING;

-- Insertar usuario AIAGENT (username: aiagent, password: admin123)
INSERT INTO personas (nombre, documento, correo, username, password_hash, id_rol, estado)
VALUES 
  ('Usuario IA', '1111111111', 'aiagent@universidad.edu', 'aiagent', 
   '$2b$12$1E9ztBRlV2DqzqM3UYZQkeWUEiFP5XMl3Md5KY4VQvhJq5qxXWEi.', 3, 1)
ON CONFLICT (username) DO NOTHING;

COMMIT;

-- Nota: Para todos los usuarios, la contraseña es: admin123
-- Cambiar las contraseñas en producción usando generate_password_hash.py
