from app.models.models import SECRET_KEY, Usuario
from app.db.session import Session, get_db
from sqlalchemy.orm import Session as SessionType

from fastapi import Depends, HTTPException
from app.config import SECRET_KEY, ALGORITHM, oauth2_scheme

from jose import jwt, JWTError


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
