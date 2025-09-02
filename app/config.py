from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# Segurança
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Admin inicial
ADM_USER = os.getenv("ADM_USER")
ADM_PASSWORD = os.getenv("ADM_PASSWORD")

# Criptografia
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")


# Cria a engine do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")