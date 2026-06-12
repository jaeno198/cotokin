from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    # ── Banco de dados MariaDB ─────────────────
    db_host:     str = "141.11.72.90"
    db_port:     int = 3306
    db_name:     str = "geohousegeo_geohouse_segundou"
    db_user:     str = "geohousegeo"
    db_password: str = "123456789"

    # ── JWT ───────────────────────────────────
    secret_key:        str = "geohouse_chave_secreta_2026"
    algorithm:         str = "HS256"
    access_token_exp:  int = 30
    refresh_token_exp: int = 60 * 24 * 7

    # ── Aplicação ─────────────────────────────
    app_name:        str       = "GEO HOUSE API"
    app_version:     str       = "1.0.0"
    debug:           bool      = False
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://141.11.72.90",
    ]

    # ── Upload ────────────────────────────────
    upload_dir:    str = "uploads/fotos"
    max_upload_mb: int = 5

    # ── URL de conexão MariaDB ─────────────────
    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
