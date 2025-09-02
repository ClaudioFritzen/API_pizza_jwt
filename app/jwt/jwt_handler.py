from app.models.models import Usuario
from app.db.session import  get_db
from sqlalchemy.orm import Session as SessionType

from fastapi import Depends, HTTPException
from app.config import SECRET_KEY, ALGORITHM, oauth2_scheme

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

#TODO Criar token JWT
def create_token_access_token(
        usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
   # Função para criar um token JWT

    data_expiracao = datetime.now(timezone.utc) + duracao_token

    access_payload = {
        "sub": str(usuario_id),
        "exp": data_expiracao,
        "iat": datetime.now(timezone.utc),
    }

    refresh_token = {
        "sub": str(usuario_id),
        "exp": data_expiracao + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_token, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token 


def verificar_token(
    token: str = Depends(oauth2_scheme), session: SessionType = Depends(get_db)
):

    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(dic_info.get("sub"))
    except JWTError as erro:
        raise HTTPException(
            status_code=401,
            detail=f"Acesso Negado, verifique a validade do token: {erro}",
        )

    # veficar se o token é valido
    # extrair o ID do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return usuario


def verificar_refresh_token(
        token: str = Depends(oauth2_scheme), session: SessionType = Depends(get_db)
):
    print("🔍 Iniciando verificação do refresh token...")
    print(f"📥 Token recebido: {token[:30]}...")  # Mostra só o início do token

     # 🔍 Verifica se o token contém vírgula (caso Swagger envie dois juntos)
    if ',' in token:
        print("⚠️ Token contém vírgula — múltiplos tokens enviados!")
        token = token.split(',')[1].strip()  # Pega só o refresh_token
        print(f"🧹 Token corrigido: {token[:60]}...")
        
    # DEBUG: Exibir chave secreta e algoritmo
    print(f"🔑 SECRET_KEY usada: {SECRET_KEY}")
    print(f"⚙️ Algoritmo usado: {ALGORITHM}")

    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"📤 Payload decodificado: {dic_info}")
        usuario_id = int(dic_info.get("sub"))
        print(f"🧑 ID extraído do token: {usuario_id}")

    except JWTError as erro:
        print(f"❌ Erro ao decodificar o token: {erro}")
        raise HTTPException(
            status_code=401,
            detail=f"Acesso Negado, verifique a validade do token: {erro}",
        )

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    print(f"🔎 Resultado da busca no banco: {'Usuário encontrado' if usuario else 'Usuário não encontrado'}")

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    print(f"✅ Verificação concluída com sucesso para o usuário: {usuario.email}")
    return usuario
