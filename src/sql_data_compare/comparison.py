import logging
from typing import Any, Optional, Tuple

import pyodbc

from .connection import get_conn_string
from .execution import execute_sql_query
from .types import ComparisonConfig, ComparisonResult, QueryResult

logger = logging.getLogger(__name__)


def compare_sql(
    left_conn: pyodbc.Connection,
    right_conn: pyodbc.Connection,
    left_query: str,
    right_query: str,
    *,
    left_params: Optional[Tuple[Any, ...]] = None,
    right_params: Optional[Tuple[Any, ...]] = None,
) -> ComparisonResult:
    """Compare the results of two SQL queries"""
    logger.info("Executing left query...")
    left_results, left_duration = execute_sql_query(left_conn, left_query, left_params)
    left_result = QueryResult(
        results=left_results, duration=left_duration, row_count=len(left_results)
    )
    logger.info(f"Left query completed in {left_duration:.2f}s")

    logger.info("Executing right query...")
    right_results, right_duration = execute_sql_query(right_conn, right_query, right_params)
    right_result = QueryResult(
        results=right_results, duration=right_duration, row_count=len(right_results)
    )
    logger.info(f"Right query completed in {right_duration:.2f}s")

    comparison = ComparisonResult(left_result, right_result)
    logger.info(str(comparison))

    return comparison


def run_comparisons(config: ComparisonConfig) -> bool:
    """Run all SQL comparisons from config"""
    try:
        left_conn = pyodbc.connect(get_conn_string("left"))
        right_conn = pyodbc.connect(get_conn_string("right"))
    except (pyodbc.Error, KeyError) as e:
        logger.error(f"Failed to establish database connections: {e}")
        return False

    success = True
    try:
        for comparison in config.comparisons:
            name = comparison["name"]
            logger.info(f"\nRunning comparison: {name}")

            try:
                left_query = config.get_sql_query(comparison["left_query_file"])
                right_query = config.get_sql_query(comparison["right_query_file"])

                result = compare_sql(
                    left_conn=left_conn,
                    right_conn=right_conn,
                    left_query=left_query,
                    right_query=right_query,
                )

                if not result.is_equal:
                    success = False
                logger.info(f"Comparison {name}: {result}")

            except Exception as e:
                success = False
                logger.error(f"Error in comparison {name}: {e}")
                continue  # Continue with next comparison

    finally:
        left_conn.close()
        right_conn.close()

    return success
