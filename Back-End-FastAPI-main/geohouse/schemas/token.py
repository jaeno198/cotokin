from pydantic import BaseModel, Field
from typing import Optional
 
 
# ──────────────────────────────────────────────
# Schemas de Token JWT
# ──────────────────────────────────────────────
 
class Token(BaseModel):
    """Resposta do endpoint /auth/login e /auth/refresh."""
    access_token:  str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    refresh_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type:    str = Field("bearer", examples=["bearer"])
 
 
class TokenData(BaseModel):
    """
    Payload decodificado do JWT.
    Populado pela dependency get_current_usuario no auth.py.
    """
    sub:  Optional[str] = Field(None, description="ID do usuário (subject)")
    role: Optional[str] = Field(None, description="Perfil do usuário: Administrador, Corretor, Cliente")
    type: Optional[str] = Field(None, description="Tipo do token: access | refresh")
 
 
class RefreshRequest(BaseModel):
    """Payload para renovar o par de tokens via /auth/refresh."""
    refresh_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
 
 
class TokenResponse(BaseModel):
    """Alias de Token — mantido para compatibilidade com o auth.py."""
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"