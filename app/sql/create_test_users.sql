-- Script para insertar usuarios de prueba con JWT
-- NOTA: Asegúrate de ejecutar setup_auth_fix.sql PRIMERO

-- PASO 1: Limpiar usuarios anteriores que tengan username (OPCIONAL, comentar si no quieres)
-- DELETE FROM personas WHERE username IS NOT NULL;

-- PASO 2: Insertar usuario ADMIN
INSERT INTO public.personas (nombre, documento, correo, username, password_hash, id_rol, estado)
VALUES 
  ('Administrador Sistema', '1234567890', 'admin@universidad.edu', 'admin', 
   '$2b$12$1E9ztBRlV2DqzqM3UYZQkeWUEiFP5XMl3Md5KY4VQvhJq5qxXWEi.',
   (SELECT id_rol FROM public.roles_usuario WHERE nombre='admin'),
   1)
ON CONFLICT (username) DO UPDATE SET
  password_hash = EXCLUDED.password_hash,
  id_rol = EXCLUDED.id_rol;

-- PASO 3: Insertar usuario USER
INSERT INTO public.personas (nombre, documento, correo, username, password_hash, id_rol, estado)
VALUES 
  ('Usuario Regular', '9876543210', 'user@universidad.edu', 'user', 
   '$2b$12$1E9ztBRlV2DqzqM3UYZQkeWUEiFP5XMl3Md5KY4VQvhJq5qxXWEi.',
   (SELECT id_rol FROM public.roles_usuario WHERE nombre='user'),
   1)
ON CONFLICT (username) DO UPDATE SET
  password_hash = EXCLUDED.password_hash,
  id_rol = EXCLUDED.id_rol;

-- PASO 4: Insertar usuario AIAGENT
INSERT INTO public.personas (nombre, documento, correo, username, password_hash, id_rol, estado)
VALUES 
  ('Usuario IA Agent', '1111111111', 'aiagent@universidad.edu', 'aiagent', 
   '$2b$12$1E9ztBRlV2DqzqM3UYZQkeWUEiFP5XMl3Md5KY4VQvhJq5qxXWEi.',
   (SELECT id_rol FROM public.roles_usuario WHERE nombre='aiagent'),
   1)
ON CONFLICT (username) DO UPDATE SET
  password_hash = EXCLUDED.password_hash,
  id_rol = EXCLUDED.id_rol;

-- PASO 5: Verificar que se insertaron correctamente
SELECT 'Usuarios creados:' as status;
SELECT id_persona, nombre, username, (SELECT nombre FROM public.roles_usuario WHERE id_rol=personas.id_rol) as rol, estado 
FROM public.personas WHERE username IS NOT NULL
ORDER BY id_persona;

-- Nota: Contraseña para todos: admin123
-- Los hash ya contienen encriptada la contraseña "admin123"
