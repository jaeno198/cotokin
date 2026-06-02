from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
 
 
# ──────────────────────────────────────────────
# Enum de perfil (espelha models.py)
# ──────────────────────────────────────────────
 
class UserRole(str, Enum):
    ADMINISTRADOR = "Administrador"
    CORRETOR      = "Corretor"
    CLIENTE       = "Cliente"
 
 
# ──────────────────────────────────────────────
# Base — campos compartilhados
# ──────────────────────────────────────────────
 
class UsuarioBase(BaseModel):
    nome:            str          = Field(..., min_length=2, max_length=100, examples=["João Silva"])
    email:           EmailStr     = Field(...,                               examples=["joao@email.com"])
    role:            UserRole     = Field(UserRole.CLIENTE)
    tipo_usuario_id: Optional[int]= Field(None, gt=0)
    is_active:       bool         = Field(True)
 
 
# ──────────────────────────────────────────────
# Create — inclui senha obrigatória
# ──────────────────────────────────────────────
 
class UsuarioCreate(UsuarioBase):
    """Payload para cadastrar um novo usuário."""
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["SenhaForte@123"],
        description="Mínimo 8 caracteres",
    )
 
 
# ──────────────────────────────────────────────
# Update — todos os campos opcionais
# ──────────────────────────────────────────────
 
class UsuarioUpdate(BaseModel):
    """Atualização parcial — somente os campos enviados são alterados."""
    nome:            Optional[str]     = Field(None, min_length=2, max_length=100)
    email:           Optional[EmailStr]= None
    role:            Optional[UserRole]= None
    tipo_usuario_id: Optional[int]     = Field(None, gt=0)
    is_active:       Optional[bool]    = None
 
 
class UsuarioUpdateSenha(BaseModel):
    """Payload exclusivo para troca de senha."""
    senha_atual: str = Field(..., min_length=8, max_length=128)
    nova_senha:  str = Field(..., min_length=8, max_length=128)
 
 
# ──────────────────────────────────────────────
# Read — resposta pública (sem senha)
# ──────────────────────────────────────────────
 
class UsuarioRead(BaseModel):
    """Resposta completa — nunca expõe hashed_password."""
    id:              int
    nome:            str
    email:           str
    role:            UserRole
    tipo_usuario_id: Optional[int]
    is_active:       bool
    criado_em:       datetime
    atualizado_em:   datetime
 
    model_config = {"from_attributes": True}
 
 
# ──────────────────────────────────────────────
# Read resumido — usado em listagens
# ──────────────────────────────────────────────
 
class UsuarioResumo(BaseModel):
    """Versão enxuta para listagens e relações."""
    id:    int
    nome:  str
    email: str
    role:  UserRole
 
    model_config = {"from_attributes": True}