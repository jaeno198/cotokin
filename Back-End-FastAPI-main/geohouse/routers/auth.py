from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
 
from database import get_db
from models import Usuario
from services.auth_services import (
    authenticate_usuario,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_usuario_by_id,
)
 
router = APIRouter(prefix="/auth", tags=["Auth"])
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
 
 
# ──────────────────────────────────────────────
# Dependency: sessão do banco
# (substitua pela sua função get_db real)
# ──────────────────────────────────────────────
 
 
 
# ──────────────────────────────────────────────
# Schemas inline (mova para schemas/token.py)
# ──────────────────────────────────────────────
 
class TokenResponse(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"
 
 
class RefreshRequest(BaseModel):
    refresh_token: str
 
 
class UsuarioPublic(BaseModel):
    id:        int
    nome:      str
    email:     str
    role:      str
    is_active: bool
 
    model_config = {"from_attributes": True}
 
 
# ──────────────────────────────────────────────
# Dependency: usuário autenticado
# ──────────────────────────────────────────────
 
def get_current_usuario(
    token: str = Depends(oauth2_scheme),
    db:    Session = Depends(get_db),
) -> Usuario:
    """
    Valida o JWT do header Authorization: Bearer <token>
    e retorna o usuário correspondente.
    Levanta 401 se o token for inválido ou o usuário inativo.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
 
    usuario = get_usuario_by_id(db, int(usuario_id))
    if usuario is None or not usuario.is_active:
        raise credentials_exception
    return usuario
 
 
def require_role(*roles: str):
    """
    Factory de dependency que restringe o endpoint a roles específicas.
 
    Uso:
        @router.delete("/...", dependencies=[Depends(require_role("Administrador"))])
    """
    def _check(current: Usuario = Depends(get_current_usuario)) -> Usuario:
        if current.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso restrito a: {', '.join(roles)}",
            )
        return current
    return _check
 
 
# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────
 
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login — retorna access e refresh token",
)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db:   Session = Depends(get_db),
):
    """
    Autentica com e-mail (campo `username`) e senha.
    Retorna um JWT de acesso (30 min) e um de refresh (7 dias).
    """
    usuario = authenticate_usuario(db, email=form.username, password=form.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(
        access_token=create_access_token(usuario.id, usuario.role),
        refresh_token=create_refresh_token(usuario.id),
    )
 
 
@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Renova o access token usando o refresh token",
)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    """
    Recebe o refresh token e devolve um novo par access + refresh.
    Levanta 401 se o refresh token for inválido ou expirado.
    """
    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido ou expirado",
    )
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise invalid
        usuario_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise invalid
 
    usuario = get_usuario_by_id(db, usuario_id)
    if not usuario or not usuario.is_active:
        raise invalid
 
    return TokenResponse(
        access_token=create_access_token(usuario.id, usuario.role),
        refresh_token=create_refresh_token(usuario.id),
    )
 
 
@router.get(
    "/me",
    response_model=UsuarioPublic,
    summary="Retorna os dados do usuário autenticado",
)
def me(current: Usuario = Depends(get_current_usuario)):
    """Endpoint protegido — requer Bearer token válido."""
    return current
