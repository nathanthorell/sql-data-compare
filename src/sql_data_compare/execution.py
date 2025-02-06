from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator, List, Optional, Tuple

import pyodbc


@contextmanager
def get_cursor(connection: pyodbc.Connection) -> Generator[pyodbc.Cursor, None, None]:
    """Context manager for cursor handling"""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def execute_sql_query(
    conn: pyodbc.Connection, sql_query: str, params: Optional[Tuple[Any, ...]] = None
) -> Tuple[List[Any], float]:
    """Execute a SQL query and return results with execution duration"""
    start_time = datetime.now()

    try:
        with get_cursor(conn) as cursor:
            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)
            results = cursor.fetchall()

        duration = (datetime.now() - start_time).total_seconds()
        return results, duration

    except pyodbc.Error as e:
        duration = (datetime.now() - start_time).total_seconds()
        raise pyodbc.Error(f"Query failed after {duration:.2f}s: {str(e)}") from e
