from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum
 
from schemas.foto import FotoRead
 
 
# ──────────────────────────────────────────────
# Enums (espelham models.py)
# ──────────────────────────────────────────────
 
class StatusImovel(str, Enum):
    DISPONIVEL  = "disponivel"
    VENDIDO     = "vendido"
    ALUGADO     = "alugado"
    INATIVO     = "inativo"
 
 
class TipoNegocio(str, Enum):
    VENDA   = "venda"
    ALUGUEL = "aluguel"
    AMBOS   = "ambos"
 
 
# ──────────────────────────────────────────────
# Base — campos compartilhados
# ──────────────────────────────────────────────
 
class ImovelBase(BaseModel):
    titulo:          str            = Field(..., min_length=5, max_length=200,  examples=["Apartamento 3 quartos no Batel"])
    descricao:       Optional[str]  = Field(None, max_length=5000)
    tipo_negocio:    TipoNegocio    = Field(...,                                examples=["venda"])
 
    # Localização
    cep:             Optional[str]  = Field(None, max_length=9,   examples=["80420-100"])
    logradouro:      Optional[str]  = Field(None, max_length=255, examples=["Rua Comendador Araújo"])
    numero:          Optional[str]  = Field(None, max_length=10,  examples=["341"])
    complemento:     Optional[str]  = Field(None, max_length=100, examples=["Apto 42"])
    bairro:          Optional[str]  = Field(None, max_length=100, examples=["Batel"])
    cidade:          str            = Field(..., max_length=100,   examples=["Curitiba"])
    estado:          str            = Field(..., min_length=2, max_length=2, examples=["PR"])
    latitude:        Optional[Decimal] = Field(None, ge=-90,  le=90)
    longitude:       Optional[Decimal] = Field(None, ge=-180, le=180)
 
    # Características
    area_total:      Optional[Decimal] = Field(None, gt=0, description="Área total em m²")
    area_construida: Optional[Decimal] = Field(None, gt=0, description="Área construída em m²")
    quartos:         Optional[int]     = Field(None, ge=0)
    suites:          Optional[int]     = Field(None, ge=0)
    banheiros:       Optional[int]     = Field(None, ge=0)
    vagas_garagem:   Optional[int]     = Field(None, ge=0)
 
    # Valores
    preco:           Optional[Decimal] = Field(None, gt=0, description="Preço de venda em R$")
    preco_aluguel:   Optional[Decimal] = Field(None, gt=0, description="Valor do aluguel mensal em R$")
    condominio:      Optional[Decimal] = Field(None, ge=0, description="Taxa de condomínio em R$")
    iptu_anual:      Optional[Decimal] = Field(None, ge=0, description="IPTU anual em R$")
 
    # Relações
    categoria_id:    int            = Field(..., gt=0)
    status_id:       int            = Field(..., gt=0)
 
 
# ──────────────────────────────────────────────
# Create
# ──────────────────────────────────────────────
 
class ImovelCreate(ImovelBase):
    """Payload para cadastrar um novo imóvel."""
    pass
 
 
# ──────────────────────────────────────────────
# Update — todos os campos opcionais
# ──────────────────────────────────────────────
 
class ImovelUpdate(BaseModel):
    titulo:          Optional[str]     = Field(None, min_length=5, max_length=200)
    descricao:       Optional[str]     = Field(None, max_length=5000)
    tipo_negocio:    Optional[TipoNegocio] = None
 
    cep:             Optional[str]     = Field(None, max_length=9)
    logradouro:      Optional[str]     = Field(None, max_length=255)
    numero:          Optional[str]     = Field(None, max_length=10)
    complemento:     Optional[str]     = Field(None, max_length=100)
    bairro:          Optional[str]     = Field(None, max_length=100)
    cidade:          Optional[str]     = Field(None, max_length=100)
    estado:          Optional[str]     = Field(None, min_length=2, max_length=2)
    latitude:        Optional[Decimal] = Field(None, ge=-90,  le=90)
    longitude:       Optional[Decimal] = Field(None, ge=-180, le=180)
 
    area_total:      Optional[Decimal] = Field(None, gt=0)
    area_construida: Optional[Decimal] = Field(None, gt=0)
    quartos:         Optional[int]     = Field(None, ge=0)
    suites:          Optional[int]     = Field(None, ge=0)
    banheiros:       Optional[int]     = Field(None, ge=0)
    vagas_garagem:   Optional[int]     = Field(None, ge=0)
 
    preco:           Optional[Decimal] = Field(None, gt=0)
    preco_aluguel:   Optional[Decimal] = Field(None, gt=0)
    condominio:      Optional[Decimal] = Field(None, ge=0)
    iptu_anual:      Optional[Decimal] = Field(None, ge=0)
 
    categoria_id:    Optional[int]     = Field(None, gt=0)
    status_id:       Optional[int]     = Field(None, gt=0)
 
 
# ──────────────────────────────────────────────
# Read — resposta completa
# ──────────────────────────────────────────────
 
class ImovelRead(ImovelBase):
    """Resposta completa — inclui id, fotos e timestamps."""
    id:          int
    fotos:       List[FotoRead] = []
    criado_em:   datetime
    atualizado_em: datetime
 
    model_config = {"from_attributes": True}
 
 
# ──────────────────────────────────────────────
# Read resumido — usado em listagens
# ──────────────────────────────────────────────
 
class ImovelResumo(BaseModel):
    """Versão enxuta para listagens — sem descrição longa nem todas as fotos."""
    id:            int
    titulo:        str
    tipo_negocio:  TipoNegocio
    cidade:        str
    estado:        str
    bairro:        Optional[str]
    preco:         Optional[Decimal]
    preco_aluguel: Optional[Decimal]
    quartos:       Optional[int]
    area_total:    Optional[Decimal]
    foto_capa:     Optional[str] = None   # URL da foto marcada como capa
    criado_em:     datetime
 
    model_config = {"from_attributes": True}