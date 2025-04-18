from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator, List, Optional, Tuple

import psycopg2
import pyodbc

from utils.rich_utils import console

from .types import ConnectionType, CursorType


@contextmanager
def get_cursor(connection: ConnectionType, db_type: str) -> Generator[CursorType, None, None]:
    """Context manager for cursor handling"""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def execute_sql_query(
    conn: ConnectionType, sql_query: str, db_type: str, params: Optional[Tuple[Any, ...]] = None
) -> Tuple[List[Any], float]:
    """Execute a SQL query and return results with execution duration"""
    start_time = datetime.now()

    query_preview = sql_query[:50].replace("\n", " ") + ("..." if len(sql_query) > 50 else "")
    console.print(f"[dim]Executing query:[/] [blue]{query_preview}[/]", end="\r")

    try:
        with get_cursor(conn, db_type) as cursor:
            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)
            results = cursor.fetchall()

        duration = (datetime.now() - start_time).total_seconds()
        console.print(f"[green]Query completed in {duration:.2f}s[/]       ")
        return results, duration

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        console.print(f"[red]Query failed after {duration:.2f}s[/]       ")
        # Handle different exception types based on db_type
        if db_type == "mssql":
            raise pyodbc.Error(f"Query failed after {duration:.2f}s: {str(e)}") from e
        else:
            raise psycopg2.Error(f"Query failed after {duration:.2f}s: {str(e)}") from e
