from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
 
 
# ──────────────────────────────────────────────
# Schemas de FotoImovel
# ──────────────────────────────────────────────
 
class FotoCreate(BaseModel):
    """
    Payload para vincular uma foto já enviada ao storage
    a um imóvel específico.
    """
    imovel_id:   int           = Field(..., gt=0)
    url:         str           = Field(..., max_length=500, examples=["https://storage.geohouse.com/imoveis/foto1.jpg"])
    descricao:   Optional[str] = Field(None, max_length=255, examples=["Sala de estar"])
    ordem:       int           = Field(0, ge=0, description="Posição na galeria — 0 = primeira")
    capa:        bool          = Field(False, description="Define se é a foto de capa do imóvel")
 
 
class FotoRead(BaseModel):
    """Resposta pública — retornada junto com os dados do imóvel."""
    id:          int
    imovel_id:   int
    url:         str
    descricao:   Optional[str]
    ordem:       int
    capa:        bool
    criado_em:   datetime
 
    model_config = {"from_attributes": True}
 
 
class FotoUpdate(BaseModel):
    """Permite reordenar, trocar descrição ou redefinir a capa."""
    descricao:   Optional[str] = Field(None, max_length=255)
    ordem:       Optional[int] = Field(None, ge=0)
    capa:        Optional[bool] = None
 