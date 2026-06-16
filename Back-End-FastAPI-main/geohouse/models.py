from datetime import datetime
from enum import Enum
 
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
 
 
# ──────────────────────────────────────────────
# Base
# ──────────────────────────────────────────────
 
class Base(DeclarativeBase):
    pass
 
 
# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────
 
class UserRole(str, Enum):
    ADMINISTRADOR = "Administrador"
    CORRETOR      = "Corretor"
    CLIENTE       = "Cliente"
 
 
class StatusImovel(str, Enum):
    ALUGA_SE = "Aluga-se"
    VENDIDO  = "Vendido"
    ALUGADO  = "Alugado"
    INATIVO  = "Inativo"
    A_VENDA  = "A venda"
 
 
class CategoriaSlug(str, Enum):
    APARTAMENTO = "apartamento"
    CASA        = "casa"
    TERRENO     = "terreno"
    COMERCIAL   = "comercial"
    RURAL       = "rural"
 
 
class PapelImovel(str, Enum):
    ANUNCIANTE  = "anunciante"
    INTERESSADO = "interessado"
    PROPRIETARIO = "proprietario"
    CORRETOR    = "corretor"
 
 
class CanalContato(str, Enum):
    WHATSAPP  = "WhatsApp"
    TELEFONE  = "Telefone"
    EMAIL     = "E-mail"
    FORMULARIO = "Formulário"
 
 
# ──────────────────────────────────────────────
# Tabelas de domínio
# ──────────────────────────────────────────────
 
class TipoUsuario(Base):
    """Perfis possíveis de um usuário: Administrador, Corretor, Cliente."""
 
    __tablename__ = "tipo_usuario"
 
    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
 
    # Relacionamento reverso
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="tipo_usuario")
 
    def __repr__(self) -> str:
        return f"<TipoUsuario id={self.id} tipo={self.tipo!r}>"
 
 
class Status(Base):
    """Situação atual de um imóvel: Aluga-se, Vendido, Alugado, Inativo, A venda."""
 
    __tablename__ = "status"
 
    id:       Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    situacao: Mapped[str] = mapped_column(String(50), nullable=False)
 
    # Relacionamento reverso
    imoveis: Mapped[list["Imovel"]] = relationship(back_populates="status")
 
    def __repr__(self) -> str:
        return f"<Status id={self.id} situacao={self.situacao!r}>"
 
 
class Categoria(Base):
    """Tipo do imóvel: Apartamento, Casa, Terreno, Comercial, Rural."""
 
    __tablename__ = "categorias"
 
    id:            Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug:          Mapped[str]      = mapped_column(String(100), nullable=False, unique=True, index=True)
    nome:          Mapped[str]      = mapped_column(String(100), nullable=False)
    criado_em:     Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
 
    # Relacionamento reverso
    imoveis: Mapped[list["Imovel"]] = relationship(back_populates="categoria")
 
    def __repr__(self) -> str:
        return f"<Categoria id={self.id} slug={self.slug!r}>"
 
 
# ──────────────────────────────────────────────
# Tabelas principais
# ──────────────────────────────────────────────
 
class Usuario(Base):
    """Usuário do sistema (administrador, corretor ou cliente)."""
 
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("email", name="uq_usuarios_email"),
    )
 
    id:              Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome:            Mapped[str]      = mapped_column(String(100), nullable=False)
    email:           Mapped[str]      = mapped_column(String(150), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str]      = mapped_column(String(255), nullable=False)
    role:            Mapped[str]      = mapped_column(String(50), nullable=False, default=UserRole.CLIENTE)
    is_active:       Mapped[bool]     = mapped_column(Boolean, nullable=False, default=True)
    tipo_usuario_id: Mapped[int]      = mapped_column(Integer, ForeignKey("tipo_usuario.id"), nullable=False)
    criado_em:       Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em:   Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
 
    # Relacionamentos
    tipo_usuario:    Mapped["TipoUsuario"]       = relationship(back_populates="usuarios")
    contatos:        Mapped[list["Contato"]]     = relationship(back_populates="usuario")
    imovel_usuarios: Mapped[list["ImovelUsuario"]] = relationship(back_populates="usuario")
 
    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email!r} role={self.role!r}>"
 
 
class Imovel(Base):
    """Imóvel cadastrado no sistema."""
 
    __tablename__ = "imoveis"
 
    id:            Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo:        Mapped[str]      = mapped_column(String(200), nullable=False)
    preco:         Mapped[float]    = mapped_column(Numeric(15, 2), nullable=False)
    quartos:       Mapped[int]      = mapped_column(Integer, nullable=False)
    cidade:        Mapped[str]      = mapped_column(String(100), nullable=False)
    status_id:     Mapped[int]      = mapped_column(Integer, ForeignKey("status.id"), nullable=False)
    categoria_id:  Mapped[int]      = mapped_column(Integer, ForeignKey("categorias.id"), nullable=False)
    criado_em:     Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
 
    # Relacionamentos
    status:          Mapped["Status"]              = relationship(back_populates="imoveis")
    categoria:       Mapped["Categoria"]           = relationship(back_populates="imoveis")
    fotos:           Mapped[list["FotoImovel"]]    = relationship(back_populates="imovel", cascade="all, delete-orphan")
    imovel_usuarios: Mapped[list["ImovelUsuario"]] = relationship(back_populates="imovel", cascade="all, delete-orphan")
 
    def __repr__(self) -> str:
        return f"<Imovel id={self.id} titulo={self.titulo!r} preco={self.preco}>"
 
 
# ──────────────────────────────────────────────
# Tabelas dependentes
# ──────────────────────────────────────────────
 
class FotoImovel(Base):
    """Foto associada a um imóvel (relação 1:N)."""
 
    __tablename__ = "fotos_imoveis"
 
    id:        Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    imovel_id: Mapped[int]      = mapped_column(Integer, ForeignKey("imoveis.id"), nullable=False)
    url:       Mapped[str]      = mapped_column(String(500), nullable=False)
    descricao: Mapped[str]      = mapped_column(String(255), nullable=True)
    ordem:     Mapped[int]      = mapped_column(Integer, nullable=False, default=0)
    capa:      Mapped[bool]     = mapped_column(Boolean, nullable=False, default=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
 
    # Relacionamento
    imovel: Mapped["Imovel"] = relationship(back_populates="fotos")
 
    def __repr__(self) -> str:
        return f"<FotoImovel id={self.id} imovel_id={self.imovel_id} ordem={self.ordem}>"
 
 
class Contato(Base):
    """Lead/contato gerado por um usuário."""
 
    __tablename__ = "contatos"
 
    id:         Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int]      = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nome:       Mapped[str]      = mapped_column(String(100), nullable=False)
    telefone:   Mapped[str]      = mapped_column(String(20), nullable=False)
    canal:      Mapped[str]      = mapped_column(String(50), nullable=False)
    criado_em:  Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
 
    # Relacionamento
    usuario: Mapped["Usuario"] = relationship(back_populates="contatos")
 
    def __repr__(self) -> str:
        return f"<Contato id={self.id} nome={self.nome!r} canal={self.canal!r}>"
 
 
# ──────────────────────────────────────────────
# Tabela de junção N:N
# ──────────────────────────────────────────────
 
class ImovelUsuario(Base):
    """Liga imóveis a usuários com um papel definido (anunciante, corretor, etc.)."""
 
    __tablename__ = "imovel_usuario"
 
    id:         Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    imovel_id:  Mapped[int]      = mapped_column(Integer, ForeignKey("imoveis.id"), nullable=False)
    usuario_id: Mapped[int]      = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    papel:      Mapped[str]      = mapped_column(String(50), nullable=False)
    criado_em:  Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
 
    # Relacionamentos
    imovel:  Mapped["Imovel"]   = relationship(back_populates="imovel_usuarios")
    usuario: Mapped["Usuario"]  = relationship(back_populates="imovel_usuarios")
 
    def __repr__(self) -> str:
        return f"<ImovelUsuario imovel_id={self.imovel_id} usuario_id={self.usuario_id} papel={self.papel!r}>"
 