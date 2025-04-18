import os
from contextlib import contextmanager
from typing import Generator, Literal

from .types import ConnectionType, CursorType


@contextmanager
def get_cursor(connection: ConnectionType) -> Generator[CursorType, None, None]:
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def get_conn_string(type: Literal["left", "right"], db_type: str) -> str:
    """
    Extract DB Credentials from environment variables
    type expects "left" or "right"
    """
    if type not in ["left", "right"]:
        raise ValueError('type must be either "left" or "right"')

    if db_type not in ["mssql", "pg"]:
        raise ValueError('db_type must be either "mssql" or "pg"')

    env_type = type.upper()

    common_vars = [
        f"{env_type}_DB_HOST",
        f"{env_type}_DB_NAME",
        f"{env_type}_DB_USER",
        f"{env_type}_DB_PASS",
        f"{env_type}_DB_PORT",
    ]

    # Database-specific required variables
    if db_type == "mssql":
        db_specific_vars = ["DB_DRIVER", "DB_ENCRYPT"]
    else:  # PostgreSQL
        db_specific_vars = []  # PostgreSQL doesn't need these specific variables

    required_vars = common_vars + db_specific_vars

    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    if missing_vars:
        raise KeyError(f"Missing required environment variables: {', '.join(missing_vars)}")

    if db_type == "mssql":
        conn = (
            f"DRIVER={os.getenv('DB_DRIVER')};"
            f"SERVER={os.getenv(f'{env_type}_DB_HOST')},{os.getenv(f'{env_type}_DB_PORT')};"
            f"DATABASE={os.getenv(f'{env_type}_DB_NAME')};"
            f"UID={os.getenv(f'{env_type}_DB_USER')};"
            f"PWD={os.getenv(f'{env_type}_DB_PASS')};"
            f"Encrypt={os.getenv('DB_ENCRYPT')};"
        )
    else:  # PostgreSQL
        conn = (
            f"host={os.getenv(f'{env_type}_DB_HOST')} "
            f"port={os.getenv(f'{env_type}_DB_PORT')} "
            f"dbname={os.getenv(f'{env_type}_DB_NAME')} "
            f"user={os.getenv(f'{env_type}_DB_USER')} "
            f"password={os.getenv(f'{env_type}_DB_PASS')}"
        )
    return conn
