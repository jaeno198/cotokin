from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
 
 
# ──────────────────────────────────────────────
# Enum de canal (espelha o Enum do models.py)
# ──────────────────────────────────────────────
 
class CanalContato(str, Enum):
    WHATSAPP  = "whatsapp"
    EMAIL     = "email"
    TELEFONE  = "telefone"
    SITE      = "site"
 
 
# ──────────────────────────────────────────────
# Schemas de Contato
# ──────────────────────────────────────────────
 
class ContatoCreate(BaseModel):
    """Payload enviado pelo visitante/lead ao demonstrar interesse."""
    imovel_id:  int          = Field(..., gt=0)
    nome:       str          = Field(..., min_length=2, max_length=100,  examples=["João Silva"])
    email:      EmailStr     = Field(...,                                 examples=["joao@email.com"])
    telefone:   Optional[str]= Field(None, max_length=20,               examples=["(41) 99999-9999"])
    mensagem:   Optional[str]= Field(None, max_length=1000)
    canal:      CanalContato = Field(CanalContato.SITE)
 
 
class ContatoRead(BaseModel):
    """Resposta completa — usada nos endpoints de listagem/detalhe."""
    id:          int
    imovel_id:   int
    usuario_id:  Optional[int]
    nome:        str
    email:       str
    telefone:    Optional[str]
    mensagem:    Optional[str]
    canal:       CanalContato
    criado_em:   datetime
 
    model_config = {"from_attributes": True}
 
 
class ContatoUpdate(BaseModel):
    """
    Permite que um Administrador/Corretor atualize observações
    ou vincule o contato a um usuário existente.
    """
    usuario_id: Optional[int] = Field(None, gt=0)
    mensagem:   Optional[str] = Field(None, max_length=1000)
    canal:      Optional[CanalContato] = None