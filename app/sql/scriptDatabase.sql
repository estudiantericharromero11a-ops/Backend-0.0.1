BEGIN;

-- =========================
-- CAMPUS
-- =========================
CREATE TABLE public.campus (
    id_campus SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    descripcion TEXT
);

-- =========================
-- BLOQUES
-- =========================
CREATE TABLE public.bloques (
    id_bloque SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    id_campus INTEGER,
    CONSTRAINT bloques_id_campus_fkey
        FOREIGN KEY (id_campus)
        REFERENCES public.campus(id_campus)
);

-- =========================
-- AREAS FUNCIONALES
-- =========================
CREATE TABLE public.areas_funcionales (
    id_area SERIAL PRIMARY KEY,
    nombre_area VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- =========================
-- ESTADO INSTALACION
-- =========================
CREATE TABLE public.estado_instalacion (
    id_estado SERIAL PRIMARY KEY,
    nombre_estado VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- =========================
-- INSTALACIONES
-- =========================
CREATE TABLE public.instalaciones (
    id_instalacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_instalacion VARCHAR(50),
    piso INTEGER,
    capacidad INTEGER,
    id_bloque INTEGER,
    id_area INTEGER,
    id_estado INTEGER,

    CONSTRAINT instalaciones_id_bloque_fkey
        FOREIGN KEY (id_bloque)
        REFERENCES public.bloques(id_bloque),

    CONSTRAINT instalaciones_id_area_fkey
        FOREIGN KEY (id_area)
        REFERENCES public.areas_funcionales(id_area),

    CONSTRAINT instalaciones_id_estado_fkey
        FOREIGN KEY (id_estado)
        REFERENCES public.estado_instalacion(id_estado)
);

-- =========================
-- HORARIO INSTALACION
-- =========================
CREATE TABLE public.horario_instalacion (
    id_horario SERIAL PRIMARY KEY,
    id_instalacion INTEGER,
    dia_semana VARCHAR(20),
    hora_apertura TIME,
    hora_cierre TIME,

    CONSTRAINT horario_instalacion_id_instalacion_fkey
        FOREIGN KEY (id_instalacion)
        REFERENCES public.instalaciones(id_instalacion)
);

-- =========================
-- PERSONAS
-- =========================
CREATE TABLE public.personas (
    id_persona SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE,
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

-- =========================
-- ROLES
-- =========================
CREATE TABLE public.roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- =========================
-- PERSONA_ROL
-- =========================
CREATE TABLE public.persona_rol (
    id_persona INTEGER NOT NULL,
    id_rol INTEGER NOT NULL,

    PRIMARY KEY (id_persona, id_rol),

    CONSTRAINT persona_rol_id_persona_fkey
        FOREIGN KEY (id_persona)
        REFERENCES public.personas(id_persona),

    CONSTRAINT persona_rol_id_rol_fkey
        FOREIGN KEY (id_rol)
        REFERENCES public.roles(id_rol)
);

-- =========================
-- PROGRAMAS
-- =========================
CREATE TABLE public.programas (
    id_programa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_programa VARCHAR(50),
    duracion_semestres INTEGER
);

-- =========================
-- MATERIAS
-- =========================
CREATE TABLE public.materias (
    id_materia SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INTEGER,
    descripcion TEXT
);

-- =========================
-- PROGRAMA_MATERIA
-- =========================
CREATE TABLE public.programa_materia (
    id_programa INTEGER NOT NULL,
    id_materia INTEGER NOT NULL,

    PRIMARY KEY (id_programa, id_materia),

    CONSTRAINT programa_materia_id_programa_fkey
        FOREIGN KEY (id_programa)
        REFERENCES public.programas(id_programa),

    CONSTRAINT programa_materia_id_materia_fkey
        FOREIGN KEY (id_materia)
        REFERENCES public.materias(id_materia)
);

-- =========================
-- ASIGNACION INSTALACIONES
-- =========================
CREATE TABLE public.asignacion_instalaciones (
    id_asignacion SERIAL PRIMARY KEY,
    id_instalacion INTEGER,
    id_materia INTEGER,
    dia_semana VARCHAR(20),
    hora_inicio TIME,
    hora_fin TIME,
    id_persona INTEGER,

    CONSTRAINT asignacion_instalaciones_id_instalacion_fkey
        FOREIGN KEY (id_instalacion)
        REFERENCES public.instalaciones(id_instalacion),

    CONSTRAINT asignacion_instalaciones_id_materia_fkey
        FOREIGN KEY (id_materia)
        REFERENCES public.materias(id_materia),

    CONSTRAINT fk_profesor
        FOREIGN KEY (id_persona)
        REFERENCES public.personas(id_persona)
);

COMMIT;