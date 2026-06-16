from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
 
from database import get_db
from models import Contato, Imovel, Usuario
from schemas.contato import ContatoCreate, ContatoRead, ContatoUpdate

router = APIRouter(prefix="/contatos", tags=["Contatos"])
# ──────────────────────────────────────────────
 
@router.post(
    "/",
    response_model=ContatoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra interesse em um imóvel (público)",
)
def criar_contato(payload: ContatoCreate, db: Session = Depends(get_db)):
    """
    Qualquer visitante pode enviar um contato/lead sobre um imóvel.
    Valida se o imóvel existe antes de salvar.
    """
    imovel = db.get(Imovel, payload.imovel_id)
    if not imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imóvel {payload.imovel_id} não encontrado",
        )
 
    contato = Contato(**payload.model_dump())
    db.add(contato)
    db.commit()
    db.refresh(contato)
    return contato
 
 
# ──────────────────────────────────────────────
# GET /contatos — listagem com filtros (Administrador / Corretor)
# ──────────────────────────────────────────────
 
@router.get(
    "/",
    response_model=List[ContatoRead],
    summary="Lista contatos/leads com filtros opcionais (Administrador/Corretor)",
)
def listar_contatos(
    imovel_id:  Optional[int] = Query(None, description="Filtrar por imóvel"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuário vinculado"),
    canal:      Optional[str] = Query(None, description="Filtrar por canal: whatsapp, email, telefone, site"),
    skip:       int           = Query(0,    ge=0,   description="Paginação — offset"),
    limit:      int           = Query(20,   ge=1, le=100, description="Paginação — máximo de registros"),
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    """
    Retorna lista paginada de contatos.
    Filtrável por imóvel, usuário vinculado e canal de origem.
    """
    query = db.query(Contato)
 
    if imovel_id:
        query = query.filter(Contato.imovel_id == imovel_id)
    if usuario_id:
        query = query.filter(Contato.usuario_id == usuario_id)
    if canal:
        query = query.filter(Contato.canal == canal)
 
    return (
        query
        .order_by(Contato.criado_em.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
 
 
# ──────────────────────────────────────────────
# GET /contatos/{id} — detalhe
# ──────────────────────────────────────────────
 
@router.get(
    "/{contato_id}",
    response_model=ContatoRead,
    summary="Retorna um contato pelo ID (Administrador/Corretor)",
)
def obter_contato(
    contato_id: int,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    contato = db.get(Contato, contato_id)
    if not contato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato {contato_id} não encontrado",
        )
    return contato
 
 
# ──────────────────────────────────────────────
# PATCH /contatos/{id} — vincula usuário / atualiza observações
# ──────────────────────────────────────────────
 
@router.patch(
    "/{contato_id}",
    response_model=ContatoRead,
    summary="Atualiza dados de um contato (Administrador/Corretor)",
)
def atualizar_contato(
    contato_id: int,
    payload: ContatoUpdate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    """
    Permite vincular o lead a um usuário cadastrado
    ou atualizar a mensagem/canal do contato.
    """
    contato = db.get(Contato, contato_id)
    if not contato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato {contato_id} não encontrado",
        )
 
    # Valida o usuario_id se informado
    if payload.usuario_id:
        usuario = db.get(Usuario, payload.usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário {payload.usuario_id} não encontrado",
            )
 
    dados = payload.model_dump(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(contato, campo, valor)
 
    db.commit()
    db.refresh(contato)
    return contato
 
 
# ──────────────────────────────────────────────
# DELETE /contatos/{id} — remove (somente Administrador)
# ──────────────────────────────────────────────
 
@router.delete(
    "/{contato_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um contato (Administrador)",
)
def deletar_contato(
    contato_id: int,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    contato = db.get(Contato, contato_id)
    if not contato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contato {contato_id} não encontrado",
        )
 
    db.delete(contato)
    db.commit()