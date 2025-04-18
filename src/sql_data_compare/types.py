import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, TypedDict, Union

import psycopg2
import pyodbc

from utils.rich_utils import COLORS, console

ConnectionType = Union[pyodbc.Connection, "psycopg2.extensions.connection"]
CursorType = Union[pyodbc.Cursor, "psycopg2.extensions.cursor"]


@dataclass
class QueryResult:
    """Contains the results and metadata from a query execution"""

    results: List[Any]
    duration: float
    row_count: int


class ComparisonResult:
    """Represents the result of comparing two query results"""

    def __init__(self, left: QueryResult, right: QueryResult):
        self.left = left
        self.right = right
        self.is_equal = left.results == right.results
        self.row_count_match = left.row_count == right.row_count

    def __str__(self) -> str:
        status = "EQUAL" if self.is_equal else "NOT EQUAL"
        return (
            f"Comparison Result: {status}\n"
            f"Left:  {self.left.row_count} rows, {self.left.duration:.2f}s\n"
            f"Right: {self.right.row_count} rows, {self.right.duration:.2f}s"
        )

    def rich_display(self) -> None:
        """Display the comparison result using Rich formatting"""
        status_color = "green" if self.is_equal else "red"
        row_color = "green" if self.row_count_match else "yellow"

        # Performance comparison
        if self.left.duration > 0 and self.right.duration > 0:
            perf_ratio = self.right.duration / self.left.duration
            perf_text = f"{perf_ratio:.2f}x" + (" faster" if perf_ratio < 1 else " slower")
            perf_color = "green" if perf_ratio < 1 else "yellow" if perf_ratio < 2 else "red"
        else:
            perf_text = "N/A"
            perf_color = "white"

        console.rule(
            f"[bold]Comparison Result: [{status_color}]"
            + f"{self.is_equal and 'EQUAL' or 'NOT EQUAL'}[/]"
        )

        console.print(
            f"[bold]Rows:[/] [bold {row_color}]{self.left.row_count}[/] vs "
            + f"[bold {row_color}]{self.right.row_count}[/]"
        )
        console.print(f"[bold]Performance:[/] [{perf_color}]{perf_text}[/]")

        console.print(f"[dim]Left:[/] {self.left.row_count} rows, {self.left.duration:.2f}s")
        console.print(f"[dim]Right:[/] {self.right.row_count} rows, {self.right.duration:.2f}s")
        console.print()


@dataclass
class ComparisonItem(TypedDict):
    """Type definition for a single comparison configuration"""

    name: str
    left_db_type: str
    left_query_file: str
    right_db_type: str
    right_query_file: str


class ComparisonConfig:
    """Configuration for SQL comparisons"""

    def __init__(self, config_path: Path, sql_dir: Path):
        self.config_path = config_path
        self.sql_dir = sql_dir
        self.comparisons = self._load_config()

    def _load_config(self) -> List[ComparisonItem]:
        """Load and validate the configuration file"""

        try:
            with open(self.config_path) as f:
                config = json.load(f)

            if not isinstance(config.get("compare_list"), list):
                raise ValueError("Config must contain 'compare_list' array")

            comparisons: List[ComparisonItem] = []
            for comp in config["compare_list"]:
                required = {"name", "left_query_file", "right_query_file"}
                if not all(key in comp for key in required):
                    raise ValueError(f"Each comparison must contain: {required}")

                # Verify SQL files exist
                for key in ["left_query_file", "right_query_file"]:
                    sql_path = self.sql_dir / comp[key]
                    if not sql_path.exists():
                        raise FileNotFoundError(f"SQL file not found: {sql_path}")

                # Cast dictionary to ComparisonItem
                comparisons.append(
                    ComparisonItem(
                        name=comp["name"],
                        left_db_type=comp["left_db_type"],
                        left_query_file=comp["left_query_file"],
                        right_db_type=comp["right_db_type"],
                        right_query_file=comp["right_query_file"],
                    )
                )

            return comparisons
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}") from e

    def get_sql_query(self, filename: str) -> str:
        """Read SQL query from file"""

        with open(self.sql_dir / filename) as f:
            return f.read()

    def rich_display(self) -> None:
        """Display the configuration using Rich formatting"""
        console.rule("[bold]Comparison Configuration")

        for i, comp in enumerate(self.comparisons):
            color = COLORS[i % len(COLORS)]
            console.print(f"[bold {color}]{comp['name']}[/]")
            console.print(
                f"  Left:  [{color}]{comp['left_db_type']}[/] - {comp['left_query_file']}"
            )
            console.print(
                f"  Right: [{color}]{comp['right_db_type']}[/] - {comp['right_query_file']}"
            )

        console.print()
