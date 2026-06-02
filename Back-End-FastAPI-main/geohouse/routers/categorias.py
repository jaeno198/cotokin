from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
 
from models import Categoria
from schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
 
router = APIRouter(prefix="/categorias", tags=["Categorias"])
 
 
# ──────────────────────────────────────────────
# Dependency: sessão do banco
# (substituída automaticamente quando database.py
#  for importado no main.py via get_db)
# ──────────────────────────────────────────────
 
def get_db():
    """Placeholder — substituído pelo SessionLocal do database.py."""
    raise NotImplementedError("Conecte ao database.py")
 
 
# ──────────────────────────────────────────────
# GET /categorias — lista todas
# ──────────────────────────────────────────────
 
@router.get(
    "/",
    response_model=List[CategoriaRead],
    summary="Lista todas as categorias de imóveis",
)
def listar_categorias(db: Session = Depends(get_db)):
    """
    Endpoint público — não requer autenticação.
    Retorna todas as categorias ordenadas pelo nome.
    """
    return db.query(Categoria).order_by(Categoria.nome).all()
 
 
# ──────────────────────────────────────────────
# GET /categorias/{id} — detalhe
# ──────────────────────────────────────────────
 
@router.get(
    "/{categoria_id}",
    response_model=CategoriaRead,
    summary="Retorna uma categoria pelo ID",
)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria {categoria_id} não encontrada",
        )
    return categoria
 
 
# ──────────────────────────────────────────────
# POST /categorias — cria (somente Administrador)
# ──────────────────────────────────────────────
 
@router.post(
    "/",
    response_model=CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova categoria (Administrador)",
)
def criar_categoria(
    payload: CategoriaCreate,
    db: Session = Depends(get_db),
    # Descomente após criar auth.py:
    # _: Usuario = Depends(require_role("Administrador")),
):
    """
    Cria uma categoria nova.
    O slug deve ser único — ex.: 'apartamento', 'casa', 'terreno'.
    """
    slug_existente = (
        db.query(Categoria).filter(Categoria.slug == payload.slug).first()
    )
    if slug_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe uma categoria com o slug '{payload.slug}'",
        )
 
    categoria = Categoria(**payload.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria
 
 
# ──────────────────────────────────────────────
# PUT /categorias/{id} — atualiza (Administrador)
# ──────────────────────────────────────────────
 
@router.put(
    "/{categoria_id}",
    response_model=CategoriaRead,
    summary="Atualiza uma categoria (Administrador)",
)
def atualizar_categoria(
    categoria_id: int,
    payload: CategoriaUpdate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria {categoria_id} não encontrada",
        )
 
    # Se o slug mudou, garante que não entra em conflito
    if payload.slug and payload.slug != categoria.slug:
        conflito = (
            db.query(Categoria).filter(Categoria.slug == payload.slug).first()
        )
        if conflito:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Slug '{payload.slug}' já está em uso",
            )
 
    dados = payload.model_dump(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(categoria, campo, valor)
 
    db.commit()
    db.refresh(categoria)
    return categoria
 
 
# ──────────────────────────────────────────────
# DELETE /categorias/{id} — remove (Administrador)
# ──────────────────────────────────────────────
 
@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma categoria (Administrador)",
)
def deletar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    """
    Remove a categoria somente se não houver imóveis vinculados a ela.
    """
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria {categoria_id} não encontrada",
        )
 
    if categoria.imoveis:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Não é possível remover: {len(categoria.imoveis)} imóvel(is) "
                "vinculado(s) a esta categoria"
            ),
        )
 
    db.delete(categoria)
    db.commit()