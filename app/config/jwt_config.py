# Configuración JWT
import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu-clave-secreta-muy-segura-cambiar-en-produccion")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Tiempo de expiración del token
ACCESS_TOKEN_EXPIRE_TIMEDELTA = timedelta(hours=JWT_EXPIRATION_HOURS)
