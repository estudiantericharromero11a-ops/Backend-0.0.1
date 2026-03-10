# API FastAPI - Gestión de Instalaciones Universitarias

## 📋 Descripción
API REST desarrollada con FastAPI para la gestión de instalaciones universitarias. Conecta a PostgreSQL/pgAdmin con 13 tablas (11 principales + 2 puente).

## 🗄️ Estructura de Base de Datos
**13 tablas totales:**

### Tablas Principales (11):
1. `campus` - Campus universitarios
2. `bloques` - Bloques dentro de campus
3. `areas_funcionales` - Áreas funcionales
4. `estado_instalacion` - Estados de instalación
5. `instalaciones` - Instalaciones físicas
6. `horario_instalacion` - Horarios de instalaciones
7. `personas` - Personas del sistema
8. `roles` - Roles de usuarios
9. `programas` - Programas académicos
10. `materias` - Materias académicas
11. `asignacion_instalaciones` - Asignaciones de instalaciones

### Tablas Puente/Relación (2):
1. `persona_rol` - Relación muchos-a-muchos entre personas y roles
2. `programa_materia` - Relación muchos-a-muchos entre programas y materias

## 🚀 Cómo Iniciar la API

### Opción 1: Usando Python directamente
```bash
# Iniciar servidor
python main.py
```

### Opción 2: Usando uvicorn directamente
```bash
# Iniciar con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Opción 3: Desde cualquier terminal (Windows)
```bash
# Desde el directorio del proyecto
python main.py
```

**Nota:** Si el puerto 8000 está ocupado, la API se iniciará automáticamente en el puerto 8001.

## 📡 Endpoints Disponibles

### Base URL: `http://localhost:8000`

- `GET /docs` - Documentación interactiva de Swagger
- `GET /campus/` - Lista todos los campus
- `GET /bloques/` - Lista todos los bloques
- `GET /areas_funcionales/` - Lista áreas funcionales
- `GET /estado_instalacion/` - Lista estados de instalación
- `GET /instalaciones/` - Lista todas las instalaciones
- `GET /horarios-instalacion/` - Lista horarios de instalación
- `GET /personas/` - Lista todas las personas
- `GET /roles/` - Lista todos los roles
- `GET /programas/` - Lista todos los programas
- `GET /materias/` - Lista todas las materias
- `GET /asignacion_instalacion/` - Lista asignaciones

Cada endpoint soporta operaciones CRUD completas:
- `GET /` - Listar todos
- `GET /{id}` - Obtener específico
- `POST /` - Crear nuevo
- `PUT /{id}` - Actualizar
- `DELETE /{id}` - Eliminar

## 🔧 Configuración de Base de Datos

La configuración se encuentra en `app/config/db_config.py`:

```python
host="localhost"
port="5432"
user="postgres"
password="jklm212rich17"  # Cambia según tu configuración
dbname="university_db"
```

## 📁 Estructura del Proyecto

```
fast-api-0.0.1/
├── main.py                 # Punto de entrada de la aplicación
├── app/
│   ├── config/
│   │   └── db_config.py    # Configuración de base de datos
│   ├── controllers/        # Lógica de negocio
│   ├── models/            # Modelos Pydantic
│   ├── routes/            # Definición de rutas/endpoints
│   └── sql/               # Scripts SQL de referencia
└── myvenv/                # Entorno virtual
```

## ✅ Verificación de Funcionamiento

Para verificar que todo funciona correctamente:

```bash
# Activar entorno virtual
myvenv\Scripts\activate

# Ejecutar prueba completa
python -c "
import requests
response = requests.get('http://localhost:8001/campus/')
print(f'Status: {response.status_code}')
print(f'Datos: {len(response.json())} campus encontrados')
"
```

O accede directamente a:
- **Documentación Swagger:** http://localhost:8001/docs
- **Documentación ReDoc:** http://localhost:8001/redoc

## 🌐 Conexión con Frontend

La API incluye configuración CORS para permitir conexiones desde cualquier origen:

```javascript
// Ejemplo de conexión desde frontend
fetch('http://localhost:8000/campus/')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 📊 Estado Actual

- ✅ **13 tablas** en PostgreSQL verificadas
- ✅ **21 endpoints** funcionando correctamente
- ✅ **Conexión activa** a base de datos
- ✅ **CORS habilitado** para frontend
- ✅ **Documentación automática** en `/docs`
- ✅ **API probada y funcionando** en puerto 8001
- ✅ **Proyecto optimizado** y limpio

¡La API está lista para producción! 🎉