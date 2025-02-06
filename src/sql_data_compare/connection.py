import os
from contextlib import contextmanager
from typing import Generator, Literal

import pyodbc


@contextmanager
def get_cursor(connection: pyodbc.Connection) -> Generator[pyodbc.Cursor, None, None]:
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def get_conn_string(type: Literal["left", "right"]) -> str:
    """
    Extract DB Credentials from environment variables
    type expects "left" or "right"
    """
    if type not in ["left", "right"]:
        raise ValueError('type must be either "left" or "right"')

    env_type = type.upper()
    required_vars = [
        f"{env_type}_DB_HOST",
        f"{env_type}_DB_NAME",
        f"{env_type}_DB_USER",
        f"{env_type}_DB_PASS",
        f"{env_type}_DB_PORT",
        "DB_DRIVER",
        "DB_ENCRYPT",
    ]

    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    if missing_vars:
        raise KeyError(f"Missing required environment variables: {', '.join(missing_vars)}")

    conn = (
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv(f'{env_type}_DB_HOST')},{os.getenv(f'{env_type}_DB_PORT')};"
        f"DATABASE={os.getenv(f'{env_type}_DB_NAME')};"
        f"UID={os.getenv(f'{env_type}_DB_USER')};"
        f"PWD={os.getenv(f'{env_type}_DB_PASS')};"
        f"Encrypt={os.getenv('DB_ENCRYPT')};"
    )
    return conn
