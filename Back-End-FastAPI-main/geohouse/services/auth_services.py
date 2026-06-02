from datetime import datetime, timedelta, timezone
from typing import Optional
 
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
 
from models import Usuario
 
# ──────────────────────────────────────────────
# Configurações JWT
# Substitua SECRET_KEY por uma variável de ambiente via config.py
# ──────────────────────────────────────────────
 
SECRET_KEY       = "TROQUE_POR_UMA_CHAVE_SEGURA_NO_.ENV"   # settings.secret_key
ALGORITHM        = "HS256"
ACCESS_TOKEN_EXP = 30      # minutos
REFRESH_TOKEN_EXP = 60 * 24 * 7  # 7 dias em minutos
 
 
# ──────────────────────────────────────────────
# Contexto de hashing — bcrypt
# ──────────────────────────────────────────────
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
 
# ──────────────────────────────────────────────
# Funções de senha
# ──────────────────────────────────────────────
 
def hash_password(plain: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    return pwd_context.hash(plain)
 
 
def verify_password(plain: str, hashed: str) -> bool:
    """Compara senha em texto puro com o hash armazenado."""
    return pwd_context.verify(plain, hashed)
 
 
# ──────────────────────────────────────────────
# Funções JWT
# ──────────────────────────────────────────────
 
def _create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Base interna para geração de tokens.
    Adiciona `exp` e `iat` automaticamente.
    """
    payload = data.copy()
    now = datetime.now(timezone.utc)
    payload.update({
        "iat": now,
        "exp": now + expires_delta,
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
 
 
def create_access_token(usuario_id: int, role: str) -> str:
    """
    Gera um JWT de acesso com duração de 30 minutos.
    Inclui o ID e o perfil do usuário no payload.
    """
    return _create_token(
        data={"sub": str(usuario_id), "role": role, "type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXP),
    )
 
 
def create_refresh_token(usuario_id: int) -> str:
    """
    Gera um JWT de refresh com duração de 7 dias.
    Não inclui o role — use o access token para isso.
    """
    return _create_token(
        data={"sub": str(usuario_id), "type": "refresh"},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXP),
    )
 
 
def decode_token(token: str) -> dict:
    """
    Decodifica e valida um JWT.
    Levanta JWTError se o token for inválido ou expirado.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
 
 
# ──────────────────────────────────────────────
# Funções de banco de dados
# ──────────────────────────────────────────────
 
def get_usuario_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    """Busca um usuário pelo ID. Retorna None se não existir."""
    return db.get(Usuario, usuario_id)
 
 
def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca um usuário pelo e-mail. Retorna None se não existir."""
    return db.query(Usuario).filter(Usuario.email == email).first()
 
 
def authenticate_usuario(
    db: Session,
    email: str,
    password: str,
) -> Optional[Usuario]:
    """
    Autentica um usuário por e-mail e senha.
 
    Retorna o objeto Usuario se as credenciais forem válidas
    e a conta estiver ativa. Retorna None caso contrário.
    """
    usuario = get_usuario_by_email(db, email)
 
    if not usuario:
        return None
    if not usuario.is_active:
        return None
    if not verify_password(password, usuario.hashed_password):
        return None
 
    return usuario