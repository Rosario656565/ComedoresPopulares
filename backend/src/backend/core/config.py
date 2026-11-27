from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Configuración de la aplicación leída desde el archivo .env."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_server: str = r"DESKTOP-01HT3G5\SQLEXPRESS"
    db_name: str = "ComedoresPopularesDB"
    db_user: str = ""
    db_password: SecretStr = SecretStr("")
    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_trusted_connection: bool = True
    db_encrypt: bool = True
    db_trust_server_certificate: bool = True
    db_timeout: int = 30

    @property
    def connection_string(self) -> str:
        """Cadena de conexión ODBC para pyodbc."""
        encrypt = "yes" if self.db_encrypt else "no"
        trust_certificate = "yes" if self.db_trust_server_certificate else "no"
        parts = [
            f"DRIVER={{{self.db_driver}}}",
            f"SERVER={self.db_server}",
            f"DATABASE={self.db_name}",
            f"Encrypt={encrypt}",
            f"TrustServerCertificate={trust_certificate}",
        ]
        if self.db_trusted_connection or not self.db_user:
            parts.append("Trusted_Connection=yes")
        else:
            parts.append(f"UID={self.db_user}")
            parts.append(f"PWD={self.db_password.get_secret_value()}")
        return ";".join(parts) + ";"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
