from typing import Any, Optional, Tuple

import psycopg2
import pyodbc
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn

from utils.rich_utils import COLORS, console

from .connection import get_conn_string
from .execution import execute_sql_query
from .types import ComparisonConfig, ComparisonResult, ConnectionType, QueryResult


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
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="green"),
        TimeElapsedColumn(),
        console=console,
        expand=False,
    ) as progress:
        # Left Query Execution
        task_left = progress.add_task("Executing left query...", total=1)
        left_results, left_duration = execute_sql_query(
            conn=left_conn, sql_query=left_query, db_type=left_db_type, params=left_params
        )
        left_result = QueryResult(
            results=left_results, duration=left_duration, row_count=len(left_results)
        )
        progress.update(task_left, completed=1)

        # Right Query Execution
        task_right = progress.add_task("Executing right query...", total=1)
        right_results, right_duration = execute_sql_query(
            conn=right_conn, sql_query=right_query, db_type=right_db_type, params=right_params
        )
        right_result = QueryResult(
            results=right_results, duration=right_duration, row_count=len(right_results)
        )
        progress.update(task_right, completed=1)

    comparison = ComparisonResult(left_result, right_result)
    comparison.rich_display()

    return comparison


def run_comparisons(config: ComparisonConfig) -> bool:
    """Run all SQL comparisons from config"""
    success = True

    console.print()
    console.rule("[bold]SQL Data Comparison[/]")
    console.print("[italic]Comparing queries across database systems[/]", justify="center")
    console.print()

    for i, comparison in enumerate(config.comparisons):
        name = comparison["name"]
        color = COLORS[i % len(COLORS)]
        console.print()
        console.rule(f"[bold {color}]{name}[/]")

        left_conn = None
        right_conn = None

        try:
            left_db_type = comparison["left_db_type"]
            right_db_type = comparison["right_db_type"]
            left_query = config.get_sql_query(comparison["left_query_file"])
            right_query = config.get_sql_query(comparison["right_query_file"])

            console.print(
                f"Left database:  [{color}]{left_db_type}[/] ({comparison['left_query_file']})"
            )
            console.print(
                f"Right database: [{color}]{right_db_type}[/] ({comparison['right_query_file']})"
            )
            console.print()

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

        except Exception as e:
            success = False
            console.print(f"[bold red]Error in comparison {name}:[/] {e}")

        finally:
            # Close connections
            if left_conn:
                left_conn.close()
            if right_conn:
                right_conn.close()

    console.print()
    if success:
        console.rule("[bold green]All comparisons successful[/]")
    else:
        console.rule("[bold red]Some comparisons failed[/]")
    console.print()

    return success
