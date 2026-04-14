# API FastAPI - Gestión de Instalaciones Universitarias

## Descripción
API REST desarrollada con FastAPI para la gestión de instalaciones universitarias. La aplicación se conecta a PostgreSQL y ofrece CRUD para campus, bloques, instalaciones, personas, roles, programas, materias, horarios y asignaciones.

## Instalación

1. Crear y configurar la base de datos PostgreSQL.
2. Editar `app/config/db_config.py` con los datos de conexión de tu servidor.
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```
4. Ejecutar el script de base de datos de inicialización:
```bash
psql -U <usuario> -d <nombre_bd> -f app/sql/scriptDatabase.sql
```
5. Iniciar la aplicación:
```bash
python main.py
```

## Funcionamiento del Proyecto

1. El backend arranca en `http://localhost:8000` y monta todos los routers definidos en `app/routes/`.
2. Cada router llama a un controlador en `app/controllers/` que ejecuta consultas SQL con `psycopg2`.
3. Las entidades principales del sistema se comportan como CRUD:
   - `campus`, `bloques`, `areas_funcionales`, `estado_instalacion`, `instalaciones`, `horario_instalacion`, `personas`, `roles`, `programas`, `materias`, `asignacion_instalaciones`, `persona_rol`, `programa_materia`, `conocimiento`.
4. La autenticación JWT se maneja con `/auth/login`, `/auth/logout` y `/auth/verify`.
5. Los datos se almacenan en PostgreSQL; los endpoints devuelven JSON compatibles con frontend y APIs externas.

## Conexión con el Frontend

1. El frontend puede consumir la API usando peticiones HTTP a `http://localhost:8000`.
2. Para obtener un token JWT se usa `POST /auth/login` con `username` y `password`.
3. El frontend puede enviar el token en el header `Authorization: Bearer <token>` para verificar sesión si lo necesita.
4. Para leer datos desde el frontend se usan rutas como `/campus`, `/bloques`, `/instalaciones`, `/personas`, `/programas`, `/materias`, etc.
5. Para crear o actualizar registros el frontend envía JSON válido a los endpoints correspondientes:
   - `POST /{recurso}/`
   - `PUT /{recurso}/{id}`
   - `DELETE /{recurso}/{id}`

## Conexión con el Proyecto de IA

1. El endpoint de `conocimiento` permite almacenar y recuperar datos de conocimiento con campos `contenido` y `embedding`.
2. Un proyecto de IA puede usar esta tabla para guardar información semántica o embeddings generados externamente.
3. El flujo típico es:
   - generar embeddings en el proyecto de IA,
   - enviar los datos a `POST /conocimientos` para persistirlos,
   - luego consultar `GET /conocimientos` o `GET /conocimientos/{id}` para recuperar contenido.
4. La API no incluye el motor de IA en este repositorio, pero ofrece el almacenamiento y los endpoints necesarios para integrarlo.

## Configuración de Base de Datos

La configuración de conexión está en `app/config/db_config.py`:

```python
host="localhost"
port="5432"
user="postgres"
password="<tu_password_segura>"
dbname="<tu_nombre_de_base_de_datos>"
```

Cambia estos valores según tu entorno PostgreSQL y no compartas credenciales reales en repositorios públicos.

## Estructura del Proyecto y Función de Archivos

- `main.py`
  - Punto de entrada de la aplicación.
  - Configura FastAPI, habilita CORS y monta los routers de cada módulo.
  - Selecciona el puerto 8000 por defecto, o busca otro disponible si está ocupado.

- `app/config/db_config.py`
  - Define la conexión con PostgreSQL usando `psycopg2`.
  - Ajusta `host`, `port`, `user`, `password` y `dbname` para tu proyecto.

- `app/config/jwt_config.py`
  - Define la clave secreta JWT, el algoritmo y la duración del token.
  - Usa `os.getenv` para permitir configuración desde variables de entorno.

- `app/routes/`
  - Contiene la definición de rutas y prefijos para cada recurso.
  - Cada archivo del directorio expone un router con endpoints CRUD.

- `app/controllers/`
  - Contiene la lógica de negocio y las consultas SQL contra PostgreSQL.
  - Maneja operaciones create, read, update, delete y autenticación.

- `app/models/`
  - Contiene los modelos Pydantic utilizados para validar entradas y salidas.

- `app/sql/scriptDatabase.sql`
  - Script principal para crear todas las tablas necesarias del sistema.
  - Incluye tablas de inventario, relaciones y autenticación.

- `scripts/generate_password_hash.py`
  - Genera hashes bcrypt de contraseñas para almacenar en la base de datos.
  - Verifica contraseñas contra hashes existentes.

- `scripts/verify_jwt_setup.py`
  - Verifica que las dependencias y la configuración JWT estén presentes.
  - Comprueba que las tablas necesarias existen en PostgreSQL.

## Base de Datos y SQL de Integración

El script de inicialización recomendado es `app/sql/scriptDatabase.sql`. Contiene la definición completa de:

- `roles_usuario`: permisos de autenticación.
- `personas`: usuarios con `username`, `password_hash`, `id_rol` y estado.
- `tokens_activos`: tokens JWT válidos e inactivos.
- `conocimiento`: almacenamiento de contenido y embedding.
- Tablas centrales: `campus`, `bloques`, `areas_funcionales`, `estado_instalacion`, `instalaciones`, `horario_instalacion`, `programas`, `materias`, `asignacion_instalaciones`, `persona_rol`, `programa_materia`.

El esquema actualizado debe tener 16 tablas en total.

## Endpoints principales

Base URL: `http://localhost:8000`

- `POST /auth/login` - Login y obtención de JWT.
- `POST /auth/logout` - Cierre de sesión e invalidación de token.
- `POST /auth/verify` - Verifica token enviado en cuerpo.
- `GET /auth/verify-header` - Verifica token enviado en header `Authorization`.
- `GET /campus/` - Lista campus.
- `GET /bloques/` - Lista bloques.
- `GET /areas_funcionales/` - Lista áreas funcionales.
- `GET /estado_instalacion/` - Lista estados de instalación.
- `GET /instalaciones/` - Lista instalaciones.
- `GET /horarios_instalacion/` - Lista horarios de instalación.
- `GET /personas/` - Lista personas.
- `GET /roles/` - Lista roles.
- `GET /programas/` - Lista programas.
- `GET /materias/` - Lista materias.
- `GET /asignacion_instalaciones/` - Lista asignaciones.
- `GET /persona_rol/` - Lista relaciones persona-rol.
- `GET /programa_materia/` - Lista relaciones programa-materia.
- `GET /conocimientos/` - Lista conocimientos.

Los routers implementan operaciones CRUD completas: listar, obtener por id, crear, actualizar y eliminar.

## Requisitos de Python

El archivo `requirements.txt` incluye las dependencias necesarias para ejecutar el backend actual.

## Notas de integración

- Ajusta siempre `app/config/db_config.py` a tu base de datos real.
- Si necesitas cambiar la configuración JWT, usa variables de entorno para `JWT_SECRET_KEY`.
- El script SQL recomendado para una instalación nueva es `app/sql/scriptDatabase.sql`.

## Documentación automática

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
