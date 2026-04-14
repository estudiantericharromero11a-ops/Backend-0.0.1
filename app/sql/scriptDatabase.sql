BEGIN;

-- Tabla de roles de autenticación
CREATE TABLE IF NOT EXISTS public.roles_usuario (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de roles de aplicación
CREATE TABLE IF NOT EXISTS public.roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL,
    descripcion TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campus
CREATE TABLE IF NOT EXISTS public.campus (
    id_campus SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    descripcion TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bloques
CREATE TABLE IF NOT EXISTS public.bloques (
    id_bloque SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    id_campus INTEGER,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT bloques_id_campus_fkey FOREIGN KEY (id_campus)
        REFERENCES public.campus (id_campus)
);

-- Áreas Funcionales
CREATE TABLE IF NOT EXISTS public.areas_funcionales (
    id_area SERIAL PRIMARY KEY,
    nombre_area VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Estado de Instalación
CREATE TABLE IF NOT EXISTS public.estado_instalacion (
    id_estado SERIAL PRIMARY KEY,
    nombre_estado VARCHAR(50) NOT NULL,
    descripcion TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Instalaciones
CREATE TABLE IF NOT EXISTS public.instalaciones (
    id_instalacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_instalacion VARCHAR(50),
    piso INTEGER,
    capacidad INTEGER,
    id_bloque INTEGER,
    id_area INTEGER,
    id_estado INTEGER,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT instalaciones_id_bloque_fkey FOREIGN KEY (id_bloque)
        REFERENCES public.bloques (id_bloque),
    CONSTRAINT instalaciones_id_area_fkey FOREIGN KEY (id_area)
        REFERENCES public.areas_funcionales (id_area),
    CONSTRAINT instalaciones_id_estado_fkey FOREIGN KEY (id_estado)
        REFERENCES public.estado_instalacion (id_estado)
);

-- Horario de Instalación
CREATE TABLE IF NOT EXISTS public.horario_instalacion (
    id_horario SERIAL PRIMARY KEY,
    id_instalacion INTEGER,
    dia_semana VARCHAR(20),
    hora_apertura TIME,
    hora_cierre TIME,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT horario_instalacion_id_instalacion_fkey FOREIGN KEY (id_instalacion)
        REFERENCES public.instalaciones (id_instalacion)
);

-- Personas
CREATE TABLE IF NOT EXISTS public.personas (
    id_persona SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE,
    correo VARCHAR(100),
    telefono VARCHAR(20),
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    id_rol INTEGER,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT personas_id_rol_fkey FOREIGN KEY (id_rol)
        REFERENCES public.roles_usuario (id_rol)
);

-- Conocimiento
CREATE TABLE IF NOT EXISTS public.conocimiento (
    id SERIAL PRIMARY KEY,
    contenido TEXT,
    embedding TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relación persona-rol
CREATE TABLE IF NOT EXISTS public.persona_rol (
    id_persona INTEGER NOT NULL,
    id_rol INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_persona, id_rol),
    CONSTRAINT persona_rol_id_persona_fkey FOREIGN KEY (id_persona)
        REFERENCES public.personas (id_persona),
    CONSTRAINT persona_rol_id_rol_fkey FOREIGN KEY (id_rol)
        REFERENCES public.roles (id_rol)
);

-- Programas
CREATE TABLE IF NOT EXISTS public.programas (
    id_programa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_programa VARCHAR(50),
    duracion_semestres INTEGER,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Materias
CREATE TABLE IF NOT EXISTS public.materias (
    id_materia SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INTEGER,
    descripcion TEXT,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relación programa-materia
CREATE TABLE IF NOT EXISTS public.programa_materia (
    id_programa INTEGER NOT NULL,
    id_materia INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_programa, id_materia),
    CONSTRAINT programa_materia_id_programa_fkey FOREIGN KEY (id_programa)
        REFERENCES public.programas (id_programa),
    CONSTRAINT programa_materia_id_materia_fkey FOREIGN KEY (id_materia)
        REFERENCES public.materias (id_materia)
);

-- Asignaciones de Instalaciones
CREATE TABLE IF NOT EXISTS public.asignacion_instalaciones (
    id_asignacion SERIAL PRIMARY KEY,
    id_instalacion INTEGER,
    id_materia INTEGER,
    dia_semana VARCHAR(20),
    hora_inicio TIME,
    hora_fin TIME,
    id_persona INTEGER,
    estado INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT asignacion_instalaciones_id_instalacion_fkey FOREIGN KEY (id_instalacion)
        REFERENCES public.instalaciones (id_instalacion),
    CONSTRAINT asignacion_instalaciones_id_materia_fkey FOREIGN KEY (id_materia)
        REFERENCES public.materias (id_materia),
    CONSTRAINT fk_profesor FOREIGN KEY (id_persona)
        REFERENCES public.personas (id_persona)
);

-- Tokens activos para sesión JWT
CREATE TABLE IF NOT EXISTS public.tokens_activos (
    id_token SERIAL PRIMARY KEY,
    id_persona INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT tokens_activos_id_persona_fkey FOREIGN KEY (id_persona)
        REFERENCES public.personas (id_persona) ON DELETE CASCADE
);

-- Índices de soporte
CREATE INDEX IF NOT EXISTS idx_personas_username ON public.personas(username);
CREATE INDEX IF NOT EXISTS idx_tokens_token ON public.tokens_activos(token);
CREATE INDEX IF NOT EXISTS idx_tokens_persona ON public.tokens_activos(id_persona);

-- Roles de autenticación iniciales
INSERT INTO public.roles_usuario (nombre, descripcion)
VALUES
    ('admin', 'Administrador del sistema'),
    ('user', 'Usuario estándar'),
    ('aiagent', 'Usuario con acceso especial')
ON CONFLICT (nombre) DO NOTHING;

COMMIT;