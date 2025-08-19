# Passo 1 
#    Criar uma senha secreta e colocar ela no .env   

    aqui gera sua senha secreta https://acte.ltd/utils/randomkeygen

    ## seu .env ficara assim
    SECRET_KEY=sua_senha_secreta
    # JWT 
    ALGORITHM=HS256  #tipo de hash usado pelo JWT
    ACCESS_TOKEN_EXPIRE_MINUTES=30 # tempo de duracao.

# Passo 2
# Crie um arquivo para fazer as importação das variaveis de ambiente

    no meu caso eu crie a config.py

    from dotenv import load_dotenv
    import os
    from passlib.context import CryptContext

    load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Passo 3

Criar uma função para gerar o token JWT 

def criar_token(usuario_id): # pega o id do seu usuario

    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    jwt_codificado = jwt.encode({
        "sub": usuario_id,
        "exp": data_expiracao
    }, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_codificado


# Passo 4
# Função que verifica se o token é valido
def autenticar_usuario(email, senha, db):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario:
        return False
    elif not crypt_context.verify(senha, usuario.senha):
        return False
    
    return usuario


# Passo 5
# Rota de login
@auth_router.post("/login")
async def login(login_schema: LoginSchema, db: SessionType = Depends(get_db)):

    usuario = autenticar_usuario(login_schema.email, login_schema.senha, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos!"
        )

    # Gerar token JWT
    token = criar_token(usuario.id)
    return {"access_token": token, "token_type": "bearer"}