from pydantic import BaseModel, Field
from typing import Optional
 
 
# ──────────────────────────────────────────────
# Schemas de Categoria
# ──────────────────────────────────────────────
 
class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, examples=["Apartamento"])
    slug: str = Field(..., min_length=2, max_length=50, examples=["apartamento"])
    descricao: Optional[str] = Field(None, max_length=255)
 
 
class CategoriaCreate(CategoriaBase):
    """Payload para criar uma nova categoria (somente Administrador)."""
    pass
 
 
class CategoriaUpdate(BaseModel):
    """Campos opcionais para atualizar uma categoria."""
    nome:      Optional[str] = Field(None, min_length=2, max_length=100)
    slug:      Optional[str] = Field(None, min_length=2, max_length=50)
    descricao: Optional[str] = Field(None, max_length=255)
 
 
class CategoriaRead(CategoriaBase):
    """Resposta pública — inclui o id gerado pelo banco."""
    id: int
 
    model_config = {"from_attributes": True}
 