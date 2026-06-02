from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
 
from models import Usuario
from schemas.usuario import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioResumo,
    UsuarioUpdate,
    UsuarioUpdateSenha,
    UserRole,
)
 
router = APIRouter(prefix="/usuarios", tags=["Usuários"])
 
 
# ──────────────────────────────────────────────
# Dependencies — placeholders
# ──────────────────────────────────────────────
 
def get_db():
    """Placeholder — substituído pelo SessionLocal do database.py."""
    raise NotImplementedError("Conecte ao database.py")
 
 
def hash_password(plain: str) -> str:
    """Placeholder — substituído pelo hash_password do auth_service.py."""
    raise NotImplementedError("Conecte ao auth_service.py")
 
 
def verify_password(plain: str, hashed: str) -> bool:
    """Placeholder — substituído pelo verify_password do auth_service.py."""
    raise NotImplementedError("Conecte ao auth_service.py")
 
 
# ──────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────
 
def _get_usuario_or_404(usuario_id: int, db: Session) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário {usuario_id} não encontrado",
        )
    return usuario
 
 
# ──────────────────────────────────────────────
# POST /usuarios — cadastro público (auto-registro)
# ──────────────────────────────────────────────
 
@router.post(
    "/",
    response_model=UsuarioRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo usuário (público — auto-registro)",
)
def criar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Qualquer visitante pode criar uma conta com role=Cliente.
    Para criar Administrador ou Corretor, use o endpoint admin.
    """
    # Bloqueia auto-registro com role elevada
    if payload.role != UserRole.CLIENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auto-registro permitido apenas para Clientes",
        )
 
    # Verifica e-mail duplicado
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado",
        )
 
    dados = payload.model_dump(exclude={"password"})
    usuario = Usuario(**dados, hashed_password=hash_password(payload.password))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
 
 
# ──────────────────────────────────────────────
# POST /usuarios/admin — criação privilegiada
# ──────────────────────────────────────────────
 
@router.post(
    "/admin",
    response_model=UsuarioRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria usuário com qualquer role (Administrador)",
)
def criar_usuario_admin(
    payload: UsuarioCreate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    """Permite criar Administradores e Corretores. Requer autenticação de Administrador."""
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado",
        )
 
    dados = payload.model_dump(exclude={"password"})
    usuario = Usuario(**dados, hashed_password=hash_password(payload.password))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
 
 
# ──────────────────────────────────────────────
# GET /usuarios — listagem (Administrador)
# ──────────────────────────────────────────────
 
@router.get(
    "/",
    response_model=List[UsuarioResumo],
    summary="Lista usuários com filtros (Administrador)",
)
def listar_usuarios(
    role:      Optional[str]  = Query(None, description="Filtrar por role: Administrador, Corretor, Cliente"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo/inativo"),
    busca:     Optional[str]  = Query(None, description="Busca por nome ou e-mail"),
    skip:      int            = Query(0,  ge=0),
    limit:     int            = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    query = db.query(Usuario)
 
    if role:
        query = query.filter(Usuario.role == role)
    if is_active is not None:
        query = query.filter(Usuario.is_active == is_active)
    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            Usuario.nome.ilike(termo) | Usuario.email.ilike(termo)
        )
 
    return query.order_by(Usuario.nome).offset(skip).limit(limit).all()
 
 
# ──────────────────────────────────────────────
# GET /usuarios/{id} — detalhe
# ──────────────────────────────────────────────
 
@router.get(
    "/{usuario_id}",
    response_model=UsuarioRead,
    summary="Retorna os dados de um usuário (Administrador ou próprio usuário)",
)
def obter_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    # current: Usuario = Depends(get_current_usuario),
):
    """
    Administradores podem ver qualquer usuário.
    Clientes e Corretores só podem ver o próprio perfil.
    """
    # Descomente para validar acesso ao próprio perfil:
    # if current.role != "Administrador" and current.id != usuario_id:
    #     raise HTTPException(status_code=403, detail="Acesso negado")
 
    return _get_usuario_or_404(usuario_id, db)
 
 
# ──────────────────────────────────────────────
# PATCH /usuarios/{id} — atualização parcial
# ──────────────────────────────────────────────
 
@router.patch(
    "/{usuario_id}",
    response_model=UsuarioRead,
    summary="Atualiza dados do usuário (Administrador ou próprio usuário)",
)
def atualizar_usuario(
    usuario_id: int,
    payload: UsuarioUpdate,
    db: Session = Depends(get_db),
    # current: Usuario = Depends(get_current_usuario),
):
    usuario = _get_usuario_or_404(usuario_id, db)
 
    # Verifica e-mail duplicado se estiver sendo alterado
    if payload.email and payload.email != usuario.email:
        if db.query(Usuario).filter(Usuario.email == payload.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado por outro usuário",
            )
 
    dados = payload.model_dump(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(usuario, campo, valor)
 
    db.commit()
    db.refresh(usuario)
    return usuario
 
 
# ──────────────────────────────────────────────
# PATCH /usuarios/{id}/senha — troca de senha
# ──────────────────────────────────────────────
 
@router.patch(
    "/{usuario_id}/senha",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Altera a senha do usuário (próprio usuário)",
)
def alterar_senha(
    usuario_id: int,
    payload: UsuarioUpdateSenha,
    db: Session = Depends(get_db),
    # current: Usuario = Depends(get_current_usuario),
):
    usuario = _get_usuario_or_404(usuario_id, db)
 
    if not verify_password(payload.senha_atual, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta",
        )
 
    usuario.hashed_password = hash_password(payload.nova_senha)
    db.commit()
 
 
# ──────────────────────────────────────────────
# DELETE /usuarios/{id} — desativa ou remove
# ──────────────────────────────────────────────
 
@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativa um usuário (Administrador)",
)
def deletar_usuario(
    usuario_id: int,
    remover: bool = Query(False, description="True = remove permanentemente | False = só desativa"),
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    """
    Por padrão apenas desativa (is_active=False) para preservar histórico.
    Passe ?remover=true para exclusão permanente.
    """
    usuario = _get_usuario_or_404(usuario_id, db)
 
    if remover:
        db.delete(usuario)
    else:
        usuario.is_active = False
 
    db.commit()
