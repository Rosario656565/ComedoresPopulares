import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "comedores.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS beneficiarios (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nom  TEXT NOT NULL,
            dni  TEXT NOT NULL,
            dir  TEXT DEFAULT '',
            nac  TEXT DEFAULT '',
            mail TEXT DEFAULT '',
            est  TEXT DEFAULT 'Activo'
        );

        CREATE TABLE IF NOT EXISTS insumos (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nom   TEXT NOT NULL,
            cant  REAL NOT NULL DEFAULT 0,
            min   REAL NOT NULL DEFAULT 0,
            tipo  TEXT DEFAULT 'Compra',
            costo REAL DEFAULT 0,
            don   TEXT DEFAULT '',
            venc  TEXT DEFAULT '',
            reg   TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS asistencias (
            fecha TEXT PRIMARY KEY,
            ids   TEXT NOT NULL DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS reportes (
            mes  TEXT PRIMARY KEY,
            ven  REAL DEFAULT 0,
            gas  REAL DEFAULT 0
        );
        """)
