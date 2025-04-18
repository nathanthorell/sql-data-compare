import logging
from typing import Any, Optional, Tuple

import psycopg2
import pyodbc

from .connection import get_conn_string
from .execution import execute_sql_query
from .types import ComparisonConfig, ComparisonResult, ConnectionType, QueryResult

logger = logging.getLogger(__name__)


def compare_sql(
    left_conn: ConnectionType,
    right_conn: ConnectionType,
    left_db_type: str,
    left_query: str,
    right_db_type: str,
    right_query: str,
    *,
    left_params: Optional[Tuple[Any, ...]] = None,
    right_params: Optional[Tuple[Any, ...]] = None,
) -> ComparisonResult:
    """Compare the results of two SQL queries"""
    logger.info("Executing left query...")
    left_results, left_duration = execute_sql_query(
        conn=left_conn, sql_query=left_query, db_type=left_db_type, params=left_params
    )
    left_result = QueryResult(
        results=left_results, duration=left_duration, row_count=len(left_results)
    )
    logger.info(f"Left query completed in {left_duration:.2f}s")

    logger.info("Executing right query...")
    right_results, right_duration = execute_sql_query(
        conn=right_conn, sql_query=right_query, db_type=right_db_type, params=right_params
    )
    right_result = QueryResult(
        results=right_results, duration=right_duration, row_count=len(right_results)
    )
    logger.info(f"Right query completed in {right_duration:.2f}s")

    comparison = ComparisonResult(left_result, right_result)
    logger.info(str(comparison))

    return comparison


def run_comparisons(config: ComparisonConfig) -> bool:
    """Run all SQL comparisons from config"""
    success = True

    for comparison in config.comparisons:
        name = comparison["name"]
        logger.info(f"\nRunning comparison: {name}")

        left_conn = None
        right_conn = None

        try:
            left_db_type = comparison["left_db_type"]
            right_db_type = comparison["right_db_type"]
            left_query = config.get_sql_query(comparison["left_query_file"])
            right_query = config.get_sql_query(comparison["right_query_file"])

            # Establish connections based on database types
            if left_db_type == "mssql":
                left_conn = pyodbc.connect(get_conn_string("left", db_type="mssql"))
            else:  # pg
                left_conn = psycopg2.connect(get_conn_string("left", db_type="pg"))

            if right_db_type == "mssql":
                right_conn = pyodbc.connect(get_conn_string("right", db_type="mssql"))
            else:  # pg
                right_conn = psycopg2.connect(get_conn_string("right", db_type="pg"))

            result = compare_sql(
                left_conn=left_conn,
                right_conn=right_conn,
                left_db_type=left_db_type,
                left_query=left_query,
                right_db_type=right_db_type,
                right_query=right_query,
            )

            if not result.is_equal:
                success = False
            logger.info(f"Comparison {name}: {result}")

        except Exception as e:
            success = False
            logger.error(f"Error in comparison {name}: {e}")

        finally:
            # Close connections
            if left_conn:
                left_conn.close()
            if right_conn:
                right_conn.close()

    return success
