from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional
from decimal import Decimal
 
from models import Imovel, FotoImovel, Categoria, Status
from schemas.imovel import ImovelCreate, ImovelRead, ImovelUpdate, ImovelResumo
 
router = APIRouter(prefix="/imoveis", tags=["Imóveis"])
 
 
# ──────────────────────────────────────────────
# Dependency: sessão do banco
# ──────────────────────────────────────────────
 
def get_db():
    """Placeholder — substituído pelo SessionLocal do database.py."""
    raise NotImplementedError("Conecte ao database.py")
 
 
# ──────────────────────────────────────────────
# Helper: busca imóvel ou lança 404
# ──────────────────────────────────────────────
 
def _get_imovel_or_404(imovel_id: int, db: Session) -> Imovel:
    imovel = (
        db.query(Imovel)
        .options(joinedload(Imovel.fotos))
        .filter(Imovel.id == imovel_id)
        .first()
    )
    if not imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imóvel {imovel_id} não encontrado",
        )
    return imovel
 
 
# ──────────────────────────────────────────────
# GET /imoveis — listagem pública com filtros
# ──────────────────────────────────────────────
 
@router.get(
    "/",
    response_model=List[ImovelResumo],
    summary="Lista imóveis com filtros e paginação (público)",
)
def listar_imoveis(
    # Filtros de localização
    cidade:       Optional[str]     = Query(None, description="Filtra por cidade"),
    estado:       Optional[str]     = Query(None, min_length=2, max_length=2, description="UF — ex: PR"),
    bairro:       Optional[str]     = Query(None, description="Filtra por bairro"),
 
    # Filtros de negócio
    tipo_negocio: Optional[str]     = Query(None, description="venda | aluguel | ambos"),
    categoria_id: Optional[int]     = Query(None, description="ID da categoria"),
    status_id:    Optional[int]     = Query(None, description="ID do status"),
 
    # Filtros de características
    quartos_min:  Optional[int]     = Query(None, ge=0),
    quartos_max:  Optional[int]     = Query(None, ge=0),
    vagas_min:    Optional[int]     = Query(None, ge=0),
 
    # Filtros de preço
    preco_min:    Optional[Decimal] = Query(None, ge=0),
    preco_max:    Optional[Decimal] = Query(None, ge=0),
 
    # Busca textual
    busca:        Optional[str]     = Query(None, description="Busca no título e descrição"),
 
    # Paginação
    skip:  int = Query(0,  ge=0),
    limit: int = Query(20, ge=1, le=100),
 
    db: Session = Depends(get_db),
):
    """
    Endpoint público — retorna lista resumida de imóveis disponíveis.
    Suporta múltiplos filtros combinados e paginação.
    """
    query = db.query(Imovel).options(joinedload(Imovel.fotos))
 
    if cidade:
        query = query.filter(Imovel.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.filter(Imovel.estado == estado.upper())
    if bairro:
        query = query.filter(Imovel.bairro.ilike(f"%{bairro}%"))
    if tipo_negocio:
        query = query.filter(
            or_(Imovel.tipo_negocio == tipo_negocio, Imovel.tipo_negocio == "ambos")
        )
    if categoria_id:
        query = query.filter(Imovel.categoria_id == categoria_id)
    if status_id:
        query = query.filter(Imovel.status_id == status_id)
    if quartos_min is not None:
        query = query.filter(Imovel.quartos >= quartos_min)
    if quartos_max is not None:
        query = query.filter(Imovel.quartos <= quartos_max)
    if vagas_min is not None:
        query = query.filter(Imovel.vagas_garagem >= vagas_min)
    if preco_min is not None:
        query = query.filter(Imovel.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Imovel.preco <= preco_max)
    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            or_(Imovel.titulo.ilike(termo), Imovel.descricao.ilike(termo))
        )
 
    imoveis = query.order_by(Imovel.criado_em.desc()).offset(skip).limit(limit).all()
 
    # Monta o resumo com a URL da foto de capa
    resultado = []
    for im in imoveis:
        capa = next((f.url for f in im.fotos if f.capa), None)
        resumo = ImovelResumo(
            id=im.id,
            titulo=im.titulo,
            tipo_negocio=im.tipo_negocio,
            cidade=im.cidade,
            estado=im.estado,
            bairro=im.bairro,
            preco=im.preco,
            preco_aluguel=im.preco_aluguel,
            quartos=im.quartos,
            area_total=im.area_total,
            foto_capa=capa,
            criado_em=im.criado_em,
        )
        resultado.append(resumo)
 
    return resultado
 
 
# ──────────────────────────────────────────────
# GET /imoveis/{id} — detalhe completo
# ──────────────────────────────────────────────
 
@router.get(
    "/{imovel_id}",
    response_model=ImovelRead,
    summary="Retorna os detalhes completos de um imóvel (público)",
)
def obter_imovel(imovel_id: int, db: Session = Depends(get_db)):
    return _get_imovel_or_404(imovel_id, db)
 
 
# ──────────────────────────────────────────────
# POST /imoveis — cadastra novo imóvel
# ──────────────────────────────────────────────
 
@router.post(
    "/",
    response_model=ImovelRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo imóvel (Administrador/Corretor)",
)
def criar_imovel(
    payload: ImovelCreate,
    db: Session = Depends(get_db),
    # current: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    # Valida categoria e status
    if not db.get(Categoria, payload.categoria_id):
        raise HTTPException(status_code=404, detail=f"Categoria {payload.categoria_id} não encontrada")
    if not db.get(Status, payload.status_id):
        raise HTTPException(status_code=404, detail=f"Status {payload.status_id} não encontrado")
 
    imovel = Imovel(**payload.model_dump())
    db.add(imovel)
    db.commit()
    db.refresh(imovel)
    return _get_imovel_or_404(imovel.id, db)
 
 
# ──────────────────────────────────────────────
# PUT /imoveis/{id} — atualização completa
# ──────────────────────────────────────────────
 
@router.put(
    "/{imovel_id}",
    response_model=ImovelRead,
    summary="Atualiza todos os dados de um imóvel (Administrador/Corretor)",
)
def atualizar_imovel(
    imovel_id: int,
    payload: ImovelCreate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    imovel = _get_imovel_or_404(imovel_id, db)
 
    if not db.get(Categoria, payload.categoria_id):
        raise HTTPException(status_code=404, detail=f"Categoria {payload.categoria_id} não encontrada")
    if not db.get(Status, payload.status_id):
        raise HTTPException(status_code=404, detail=f"Status {payload.status_id} não encontrado")
 
    for campo, valor in payload.model_dump().items():
        setattr(imovel, campo, valor)
 
    db.commit()
    return _get_imovel_or_404(imovel_id, db)
 
 
# ──────────────────────────────────────────────
# PATCH /imoveis/{id} — atualização parcial
# ──────────────────────────────────────────────
 
@router.patch(
    "/{imovel_id}",
    response_model=ImovelRead,
    summary="Atualiza campos específicos de um imóvel (Administrador/Corretor)",
)
def atualizar_imovel_parcial(
    imovel_id: int,
    payload: ImovelUpdate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    imovel = _get_imovel_or_404(imovel_id, db)
 
    dados = payload.model_dump(exclude_unset=True)
 
    if "categoria_id" in dados and not db.get(Categoria, dados["categoria_id"]):
        raise HTTPException(status_code=404, detail=f"Categoria {dados['categoria_id']} não encontrada")
    if "status_id" in dados and not db.get(Status, dados["status_id"]):
        raise HTTPException(status_code=404, detail=f"Status {dados['status_id']} não encontrado")
 
    for campo, valor in dados.items():
        setattr(imovel, campo, valor)
 
    db.commit()
    return _get_imovel_or_404(imovel_id, db)
 
 
# ──────────────────────────────────────────────
# DELETE /imoveis/{id} — remove
# ──────────────────────────────────────────────
 
@router.delete(
    "/{imovel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um imóvel e suas fotos (Administrador)",
)
def deletar_imovel(
    imovel_id: int,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador")),
):
    """
    Remove o imóvel e todas as fotos vinculadas
    (cascade configurado no models.py).
    """
    imovel = _get_imovel_or_404(imovel_id, db)
    db.delete(imovel)
    db.commit()