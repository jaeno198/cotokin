from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
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
    ANUNCIANTE   = "anunciante"
    INTERESSADO  = "interessado"
    PROPRIETARIO = "proprietario"
    CORRETOR     = "corretor"


class CanalContato(str, Enum):
    WHATSAPP   = "WhatsApp"
    TELEFONE   = "Telefone"
    EMAIL      = "E-mail"
    FORMULARIO = "Formulário"


# ──────────────────────────────────────────────
# Tabelas de domínio
# ──────────────────────────────────────────────

class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="tipo_usuario")

    def __repr__(self) -> str:
        return f"<TipoUsuario id={self.id} tipo={self.tipo!r}>"


class Status(Base):
    __tablename__ = "status"

    id:       Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    situacao: Mapped[str] = mapped_column(String(50), nullable=False)

    imoveis: Mapped[list["Imovel"]] = relationship(back_populates="status")

    def __repr__(self) -> str:
        return f"<Status id={self.id} situacao={self.situacao!r}>"


class Categoria(Base):
    __tablename__ = "categorias"

    id:            Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug:          Mapped[str]      = mapped_column(String(100), nullable=False, unique=True, index=True)
    nome:          Mapped[str]      = mapped_column(String(100), nullable=False)
    criado_em:     Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    imoveis: Mapped[list["Imovel"]] = relationship(back_populates="categoria")

    def __repr__(self) -> str:
        return f"<Categoria id={self.id} slug={self.slug!r}>"


class Regiao(Base):
    __tablename__ = "regioes"

    id:         Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome:       Mapped[str]            = mapped_column(Text, nullable=False)
    slug:       Mapped[str]            = mapped_column(Text, nullable=False)
    cidade:     Mapped[str]            = mapped_column(Text, nullable=False)
    lat_centro: Mapped[Optional[float]] = mapped_column(Double, nullable=True)
    lng_centro: Mapped[Optional[float]] = mapped_column(Double, nullable=True)
    raio_km:    Mapped[Optional[float]] = mapped_column(Double, nullable=True)

    imoveis: Mapped[list["Imovel"]] = relationship(back_populates="regiao")

    def __repr__(self) -> str:
        return f"<Regiao id={self.id} slug={self.slug!r}>"


class Finalidade(Base):
    __tablename__ = "finalidades"

    id:            Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome:          Mapped[str]           = mapped_column(Text, nullable=False)
    slug:          Mapped[str]           = mapped_column(Text, nullable=False)
    prazo_minimo:  Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    descricao:     Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    imoveis: Mapped[list["Imovel"]] = relationship(back_populates="finalidade")

    def __repr__(self) -> str:
        return f"<Finalidade id={self.id} slug={self.slug!r}>"


class Plano(Base):
    __tablename__ = "planos"

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="plano")

    def __repr__(self) -> str:
        return f"<Plano id={self.id}>"


# ──────────────────────────────────────────────
# Tabelas principais
# ──────────────────────────────────────────────

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("email", name="uq_usuarios_email"),
    )

    id:              Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome:            Mapped[str]           = mapped_column(Text, nullable=False)
    email:           Mapped[str]           = mapped_column(Text, nullable=False)
    hashed_password: Mapped[str]           = mapped_column(Text, nullable=False)
    role:            Mapped[str]           = mapped_column(Text, nullable=False, default=UserRole.CLIENTE)
    is_active:       Mapped[bool]          = mapped_column(Integer, nullable=False, default=1)
    tipo_usuario_id: Mapped[int]           = mapped_column(Integer, ForeignKey("tipo_usuario.id"), nullable=False)
    plano_id:        Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("planos.id"), nullable=True)
    criado_em:       Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())
    atualizado_em:   Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())

    tipo_usuario:    Mapped["TipoUsuario"]         = relationship(back_populates="usuarios")
    plano:           Mapped[Optional["Plano"]]     = relationship(back_populates="usuarios")
    contatos:        Mapped[list["Contato"]]       = relationship(back_populates="usuario")
    imovel_usuarios: Mapped[list["ImovelUsuario"]] = relationship(back_populates="usuario")

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email!r} role={self.role!r}>"


class Imovel(Base):
    __tablename__ = "imoveis"

    id:              Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo:          Mapped[str]            = mapped_column(String(200), nullable=False)
    descricao:       Mapped[Optional[str]]  = mapped_column(Text, nullable=True)
    tipo_negocio:    Mapped[str]            = mapped_column(String(50), nullable=False)

    # Localização
    cep:             Mapped[Optional[str]]   = mapped_column(String(9), nullable=True)
    logradouro:      Mapped[Optional[str]]   = mapped_column(String(255), nullable=True)
    numero:          Mapped[Optional[str]]   = mapped_column(String(10), nullable=True)
    complemento:     Mapped[Optional[str]]   = mapped_column(String(100), nullable=True)
    bairro:          Mapped[Optional[str]]   = mapped_column(String(100), nullable=True)
    cidade:          Mapped[str]             = mapped_column(String(100), nullable=False)
    estado:          Mapped[Optional[str]]   = mapped_column(String(2), nullable=True)
    latitude:        Mapped[Optional[float]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude:       Mapped[Optional[float]] = mapped_column(Numeric(10, 7), nullable=True)

    # Características
    area_total:      Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    area_construida: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    quartos:         Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)
    suites:          Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)
    banheiros:       Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)
    vagas_garagem:   Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)

    # Valores
    preco:           Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    preco_aluguel:   Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    condominio:      Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    iptu_anual:      Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)

    # FKs
    status_id:       Mapped[int]             = mapped_column(Integer, ForeignKey("status.id"), nullable=False)
    categoria_id:    Mapped[int]             = mapped_column(Integer, ForeignKey("categorias.id"), nullable=False)
    regiao_id:       Mapped[Optional[int]]   = mapped_column(Integer, ForeignKey("regioes.id"), nullable=True)
    finalidade_id:   Mapped[Optional[int]]   = mapped_column(Integer, ForeignKey("finalidades.id"), nullable=True)
    foto_capa:       Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)

    criado_em:       Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())
    atualizado_em:   Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    status:          Mapped["Status"]              = relationship(back_populates="imoveis")
    categoria:       Mapped["Categoria"]           = relationship(back_populates="imoveis")
    regiao:          Mapped[Optional["Regiao"]]    = relationship(back_populates="imoveis")
    finalidade:      Mapped[Optional["Finalidade"]] = relationship(back_populates="imoveis")
    fotos:           Mapped[list["FotoImovel"]]    = relationship(back_populates="imovel", cascade="all, delete-orphan")
    imovel_usuarios: Mapped[list["ImovelUsuario"]] = relationship(back_populates="imovel", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Imovel id={self.id} titulo={self.titulo!r}>"


# ──────────────────────────────────────────────
# Tabelas dependentes
# ──────────────────────────────────────────────

class FotoImovel(Base):
    __tablename__ = "fotos_imoveis"

    id:        Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    imovel_id: Mapped[int]           = mapped_column(Integer, ForeignKey("imoveis.id"), nullable=False)
    url:       Mapped[str]           = mapped_column(Text, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ordem:     Mapped[int]           = mapped_column(Integer, nullable=False, default=0)
    capa:      Mapped[int]           = mapped_column(Integer, nullable=False, default=0)
    criado_em: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())

    imovel: Mapped["Imovel"] = relationship(back_populates="fotos")

    def __repr__(self) -> str:
        return f"<FotoImovel id={self.id} imovel_id={self.imovel_id} ordem={self.ordem}>"


class Contato(Base):
    __tablename__ = "contatos"

    id:         Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int]           = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nome:       Mapped[str]           = mapped_column(Text, nullable=False)
    telefone:   Mapped[str]           = mapped_column(Text, nullable=False)
    canal:      Mapped[str]           = mapped_column(Text, nullable=False)
    criado_em:  Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="contatos")

    def __repr__(self) -> str:
        return f"<Contato id={self.id} nome={self.nome!r} canal={self.canal!r}>"


# ──────────────────────────────────────────────
# Tabela de junção N:N
# ──────────────────────────────────────────────

class ImovelUsuario(Base):
    __tablename__ = "imovel_usuario"

    id:         Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    imovel_id:  Mapped[int]           = mapped_column(Integer, ForeignKey("imoveis.id"), nullable=False)
    usuario_id: Mapped[int]           = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    papel:      Mapped[str]           = mapped_column(String(50), nullable=False)
    criado_em:  Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())

    imovel:  Mapped["Imovel"]   = relationship(back_populates="imovel_usuarios")
    usuario: Mapped["Usuario"]  = relationship(back_populates="imovel_usuarios")

    def __repr__(self) -> str:
        return f"<ImovelUsuario imovel_id={self.imovel_id} usuario_id={self.usuario_id} papel={self.papel!r}>"
