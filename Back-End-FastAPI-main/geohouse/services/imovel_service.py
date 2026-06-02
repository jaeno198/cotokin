from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from typing import Optional, List
from decimal import Decimal
 
from models import Imovel, FotoImovel, Categoria, Status
from schemas.imovel import ImovelResumo
 
 
# ──────────────────────────────────────────────
# Filtros e busca
# ──────────────────────────────────────────────
 
def build_query(
    db:           Session,
    # Localização
    cidade:       Optional[str]     = None,
    estado:       Optional[str]     = None,
    bairro:       Optional[str]     = None,
    cep:          Optional[str]     = None,
    # Negócio
    tipo_negocio: Optional[str]     = None,
    categoria_id: Optional[int]     = None,
    status_id:    Optional[int]     = None,
    # Características
    quartos_min:  Optional[int]     = None,
    quartos_max:  Optional[int]     = None,
    suites_min:   Optional[int]     = None,
    banheiros_min:Optional[int]     = None,
    vagas_min:    Optional[int]     = None,
    area_min:     Optional[Decimal] = None,
    area_max:     Optional[Decimal] = None,
    # Preço
    preco_min:    Optional[Decimal] = None,
    preco_max:    Optional[Decimal] = None,
    aluguel_min:  Optional[Decimal] = None,
    aluguel_max:  Optional[Decimal] = None,
    # Busca textual
    busca:        Optional[str]     = None,
):
    """
    Monta a query base com todos os filtros disponíveis.
    Retorna um objeto Query ainda não executado,
    permitindo que o chamador adicione order_by/offset/limit.
    """
    query = db.query(Imovel).options(joinedload(Imovel.fotos))
 
    # ── Localização ──────────────────────────
    if cidade:
        query = query.filter(Imovel.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.filter(Imovel.estado == estado.upper())
    if bairro:
        query = query.filter(Imovel.bairro.ilike(f"%{bairro}%"))
    if cep:
        query = query.filter(Imovel.cep == cep)
 
    # ── Negócio ───────────────────────────────
    if tipo_negocio:
        query = query.filter(
            or_(Imovel.tipo_negocio == tipo_negocio, Imovel.tipo_negocio == "ambos")
        )
    if categoria_id:
        query = query.filter(Imovel.categoria_id == categoria_id)
    if status_id:
        query = query.filter(Imovel.status_id == status_id)
 
    # ── Características ───────────────────────
    if quartos_min is not None:
        query = query.filter(Imovel.quartos >= quartos_min)
    if quartos_max is not None:
        query = query.filter(Imovel.quartos <= quartos_max)
    if suites_min is not None:
        query = query.filter(Imovel.suites >= suites_min)
    if banheiros_min is not None:
        query = query.filter(Imovel.banheiros >= banheiros_min)
    if vagas_min is not None:
        query = query.filter(Imovel.vagas_garagem >= vagas_min)
    if area_min is not None:
        query = query.filter(Imovel.area_total >= area_min)
    if area_max is not None:
        query = query.filter(Imovel.area_total <= area_max)
 
    # ── Preço ─────────────────────────────────
    if preco_min is not None:
        query = query.filter(Imovel.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Imovel.preco <= preco_max)
    if aluguel_min is not None:
        query = query.filter(Imovel.preco_aluguel >= aluguel_min)
    if aluguel_max is not None:
        query = query.filter(Imovel.preco_aluguel <= aluguel_max)
 
    # ── Busca textual (título + descrição) ────
    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            or_(
                Imovel.titulo.ilike(termo),
                Imovel.descricao.ilike(termo),
                Imovel.bairro.ilike(termo),
                Imovel.cidade.ilike(termo),
            )
        )
 
    return query
 
 
# ──────────────────────────────────────────────
# Paginação
# ──────────────────────────────────────────────
 
def paginar(query, skip: int = 0, limit: int = 20) -> List[Imovel]:
    """Aplica offset e limit à query e retorna os resultados."""
    return query.offset(skip).limit(limit).all()
 
 
def contar(query) -> int:
    """Retorna o total de registros da query sem paginação."""
    return query.with_entities(func.count(Imovel.id)).scalar()
 
 
# ──────────────────────────────────────────────
# Montagem do resumo (foto de capa)
# ──────────────────────────────────────────────
 
def montar_resumo(imovel: Imovel) -> ImovelResumo:
    """
    Converte um objeto Imovel ORM em ImovelResumo,
    extraindo automaticamente a URL da foto de capa.
    """
    capa = next((f.url for f in imovel.fotos if f.capa), None)
 
    return ImovelResumo(
        id=imovel.id,
        titulo=imovel.titulo,
        tipo_negocio=imovel.tipo_negocio,
        cidade=imovel.cidade,
        estado=imovel.estado,
        bairro=imovel.bairro,
        preco=imovel.preco,
        preco_aluguel=imovel.preco_aluguel,
        quartos=imovel.quartos,
        area_total=imovel.area_total,
        foto_capa=capa,
        criado_em=imovel.criado_em,
    )
 
 
def listar_resumos(imoveis: List[Imovel]) -> List[ImovelResumo]:
    """Converte uma lista de Imovel ORM em lista de ImovelResumo."""
    return [montar_resumo(im) for im in imoveis]
 
 
# ──────────────────────────────────────────────
# Busca por proximidade geográfica (haversine)
# ──────────────────────────────────────────────
 
def buscar_por_proximidade(
    db:         Session,
    latitude:   float,
    longitude:  float,
    raio_km:    float = 5.0,
    skip:       int   = 0,
    limit:      int   = 20,
) -> List[Imovel]:
    """
    Retorna imóveis dentro de um raio (em km) de uma coordenada,
    usando a fórmula de Haversine via SQL.
 
    Requer que os campos latitude e longitude estejam preenchidos.
    """
    # Haversine em SQL (compatível com MySQL e PostgreSQL)
    distancia = (
        6371 * func.acos(
            func.cos(func.radians(latitude))
            * func.cos(func.radians(Imovel.latitude))
            * func.cos(func.radians(Imovel.longitude) - func.radians(longitude))
            + func.sin(func.radians(latitude))
            * func.sin(func.radians(Imovel.latitude))
        )
    ).label("distancia_km")
 
    return (
        db.query(Imovel)
        .options(joinedload(Imovel.fotos))
        .filter(Imovel.latitude.isnot(None), Imovel.longitude.isnot(None))
        .having(distancia <= raio_km)
        .order_by(distancia)
        .offset(skip)
        .limit(limit)
        .all()
    )
 
 
# ──────────────────────────────────────────────
# Imóveis em destaque (mais recentes por cidade)
# ──────────────────────────────────────────────
 
def imoveis_em_destaque(
    db:     Session,
    cidade: Optional[str] = None,
    limit:  int = 6,
) -> List[Imovel]:
    """
    Retorna os imóveis mais recentes com foto de capa cadastrada.
    Usado na home page ou em seções de destaque.
    """
    query = (
        db.query(Imovel)
        .options(joinedload(Imovel.fotos))
        .join(Imovel.fotos)
        .filter(FotoImovel.capa.is_(True))
    )
 
    if cidade:
        query = query.filter(Imovel.cidade.ilike(f"%{cidade}%"))
 
    return query.order_by(Imovel.criado_em.desc()).limit(limit).all()
 
 
# ──────────────────────────────────────────────
# Imóveis similares
# ──────────────────────────────────────────────
 
def imoveis_similares(
    db:       Session,
    imovel:   Imovel,
    limit:    int = 4,
) -> List[Imovel]:
    """
    Retorna imóveis similares ao fornecido:
    mesma categoria, cidade e faixa de preço (±30%).
    Exclui o próprio imóvel do resultado.
    """
    query = (
        db.query(Imovel)
        .options(joinedload(Imovel.fotos))
        .filter(
            Imovel.id != imovel.id,
            Imovel.categoria_id == imovel.categoria_id,
            Imovel.cidade.ilike(f"%{imovel.cidade}%"),
        )
    )
 
    if imovel.preco:
        faixa_min = imovel.preco * Decimal("0.70")
        faixa_max = imovel.preco * Decimal("1.30")
        query = query.filter(Imovel.preco.between(faixa_min, faixa_max))
 
    return query.order_by(Imovel.criado_em.desc()).limit(limit).all()