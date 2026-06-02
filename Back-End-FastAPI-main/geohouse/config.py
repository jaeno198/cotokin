from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
 
 
# ──────────────────────────────────────────────
# Settings — lê automaticamente do arquivo .env
# ──────────────────────────────────────────────
 
class Settings(BaseSettings):
 
    # ── Banco de dados SQLite ─────────────────
    db_path: str = "./geo_house.db"   # caminho do arquivo .db
 
    # ── JWT ───────────────────────────────────
    secret_key:        str = "TROQUE_POR_UMA_CHAVE_SEGURA"
    algorithm:         str = "HS256"
    access_token_exp:  int = 30           # minutos
    refresh_token_exp: int = 60 * 24 * 7  # 7 dias em minutos
 
    # ── Aplicação ─────────────────────────────
    app_name:        str       = "GEO HOUSE API"
    app_version:     str       = "1.0.0"
    debug:           bool      = False
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
 
    # ── Upload de fotos ───────────────────────
    upload_dir:    str = "uploads/fotos"
    max_upload_mb: int = 5
 
    # ── Montagem da DATABASE_URL ──────────────
    @property
    def database_url(self) -> str:
        """
        SQLite usa o formato:  sqlite:///./caminho/para/arquivo.db
        Três barras = caminho relativo ao diretório de execução.
        """
        return f"sqlite:///{self.db_path}"
 
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
 
 
# ──────────────────────────────────────────────
# Instância única (singleton via lru_cache)
# ──────────────────────────────────────────────
 
@lru_cache
def get_settings() -> Settings:
    """
    Retorna a instância única de Settings.
    Use como dependency no FastAPI:
 
        from config import get_settings
        settings = get_settings()
    """
    return Settings()
 
 
settings = get_settings()