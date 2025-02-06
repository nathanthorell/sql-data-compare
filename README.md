# sql-data-compare

A Python tool for comparing SQL query results across different data sources. It executes queries against two databases and compares their result sets, making it useful for data validation and migration verification.

Currently optimized for Microsoft SQL Server, with possible support for PostgreSQL and MySQL in future versions.

## Local Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install package with development dependencies
make install
```

## Configuration

### Database Support

Currently tested with Microsoft SQL Server using the ODBC Driver 18. While pyodbc supports other databases, you may need to modify the connection string format and SQL syntax for other database engines.

### SQL Queries

Store your SQL queries in the `sql/` directory at the project root. Each comparison can reference two different query files.

### Config File

Create a config.json file at the project root:

```json
{
  "compare_list": [
    {
      "name": "example compare",
      "left_query_file": "old_query.sql",
      "right_query_file": "new_query.sql"
    }
  ]
}
```

## Environment Variables

Required environment variables can be set directly or via a .env file in your working directory:

```text
DB_DRIVER="ODBC Driver 18 for SQL Server"
DB_ENCRYPT=no

# Left database connection
LEFT_DB_HOST=
LEFT_DB_NAME=
LEFT_DB_PORT=
LEFT_DB_USER=
LEFT_DB_PASS=

# Right database connection
RIGHT_DB_HOST=
RIGHT_DB_NAME=
RIGHT_DB_PORT=
RIGHT_DB_USER=
RIGHT_DB_PASS=
```

## Usage

```bash
# Run comparisons
make run

# Development commands
make lint        # Run ruff and mypy
make test        # Run pytest
make coverage    # Run tests with coverage
make format      # Format code with ruff
make clean       # Clean build artifacts
```
