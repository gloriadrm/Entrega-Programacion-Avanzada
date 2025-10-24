import os, jwt
from dotenv import load_dotenv
import hashlib
from passlib.context import CryptContext     # metodología de encriptación perimite actualizar sin romper contraseñas anteriores
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError



# ------ Cargamos variables de entorno ------
load_dotenv() 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ------ Función para crear token JWT ------
def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Genera un token JWT con expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ------ Función para verificar y decodificar el token JWT ------
def decode_access_token(token: str) -> dict:
    """Verifica y decodifica un JWT, lanzando excepción si está expirado o es inválido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token expirado")
    except InvalidTokenError:
        raise InvalidTokenError("Token inválido o manipulado")
    

# ------ Configuración del contexto de contraseñas ------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Límite de bytes para bcrypt
BCRYPT_MAX_LENGTH = 72

# ------ Hashing de contraseñas ------
def hash_password(raw_password: str) -> str:
    """Devuelve un hash de la contraseña."""
    # Trunca la contraseña si es demasiado larga para evitar ValueError
    truncated_password = raw_password[:BCRYPT_MAX_LENGTH]
    # Convierte a bytes (bcrypt opera en bytes)
    password_bytes = truncated_password.encode("utf-8")
    return pwd_context.hash(password_bytes)

def verify_password(raw_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash almacenado."""
    truncated_password = raw_password[:BCRYPT_MAX_LENGTH]
    password_bytes = truncated_password.encode("utf-8")
    return pwd_context.verify(password_bytes, hashed_password)

# ------ Generación de ID único a partir del email ------
def generate_user_id(email: str) -> str:
    """Genera un ID único a partir del email."""
    return hashlib.sha256(email.lower().encode()).hexdigest()[:10]

