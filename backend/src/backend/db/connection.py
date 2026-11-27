import pyodbc
from backend.core.config import settings


def get_connection():
    return pyodbc.connect(
        settings.connection_string,
        timeout=settings.db_timeout,
    )
