from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import os

from config import settings
from routers import auth, usuarios, imoveis, fotos, contatos, categorias


# No Vercel as chamadas chegam como /api/auth/login — strip o prefixo /api
# para os routers FastAPI que usam /auth/login, /imoveis/, etc.
class StripApiPrefix(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.scope.get("path", "")
        if path.startswith("/api"):
            stripped = path[4:] or "/"
            request.scope["path"] = stripped
            request.scope["raw_path"] = stripped.encode()
        return await call_next(request)


# ──────────────────────────────────────────────
# Startup / Shutdown
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.upload_dir, exist_ok=True)
    print(f"Banco: {settings.database_url}")
    print(f"Upload dir: {settings.upload_dir}")
    yield
    print("Servidor encerrado.")


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

if os.environ.get("VERCEL"):
    app.add_middleware(StripApiPrefix)


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
# Arquivos estáticos — só monta se o diretório existir
# No Vercel usa /tmp/img (efêmero); em produção use CDN
# ──────────────────────────────────────────────

try:
    os.makedirs(settings.upload_dir, exist_ok=True)
    app.mount("/img", StaticFiles(directory=settings.upload_dir), name="img")
except Exception:
    pass


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
# Entrypoint local (python main.py)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
