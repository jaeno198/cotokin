from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from config import settings
from database import create_tables

from routers import auth, usuarios, imoveis, fotos, contatos, categorias


# ──────────────────────────────────────────────
# Startup / Shutdown
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executado uma vez ao iniciar o servidor:
      - Cria as tabelas no SQLite (se não existirem)
      - Cria o diretório de uploads (se não existir)
    """
    create_tables()
    os.makedirs(settings.upload_dir, exist_ok=True)
    print(f"✅ Banco de dados: {settings.database_url}")
    print(f"✅ Upload dir:     {settings.upload_dir}")
    yield
    # Código após o yield roda no shutdown (opcional)
    print("🛑 Servidor encerrado.")


# ──────────────────────────────────────────────
# App FastAPI
# ──────────────────────────────────────────────

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "API REST do sistema imobiliário GEO HOUSE. "
        "Gerencie imóveis, usuários, contatos e fotos."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ──────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Arquivos estáticos (fotos enviadas via upload)
# ──────────────────────────────────────────────

os.makedirs(settings.upload_dir, exist_ok=True)

app.mount(
    "/img",
    StaticFiles(directory="img"),
    name="img",
)


# ──────────────────────────────────────────────
# Routers
# ──────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(imoveis.router)
app.include_router(fotos.router)
app.include_router(contatos.router)
app.include_router(categorias.router)


# ──────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────

@app.get("/", tags=["Health"], summary="Health check da API")
def root():
    return {
        "app":     settings.app_name,
        "version": settings.app_version,
        "status":  "online",
        "docs":    "/docs",
    }


# ──────────────────────────────────────────────
# Entrypoint direto (python main.py)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )