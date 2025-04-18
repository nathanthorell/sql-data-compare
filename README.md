# sql-data-compare

A Python tool for comparing SQL query results across different data sources. It executes queries against two databases and compares their result sets, making it useful for data validation and migration verification.

Supports both Microsoft SQL Server and PostgreSQL databases, with a flexible configuration system that allows comparing data across different database types.

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

This tool supports both Microsoft SQL Server and PostgreSQL databases:

Microsoft SQL Server: Tested with ODBC Driver 18. Connection strings are automatically formatted for SQL Server.
PostgreSQL: Implemented using the psycopg2 driver.

To specify which database type to use:

In your comparison configuration, set left_db_type and right_db_type to either "mssql" or "pg"
Ensure you have the appropriate environment variables configured for each database type

### SQL Queries

Store your SQL queries in the `sql/` directory at the project root. Each comparison can reference two different query files.

### Config File

Create a config.json file at the project root:

```json
{
  "compare_list": [
    {
      "name": "example compare",
      "left_db_type": "mssql",
      "left_query_file": "old_query.sql",
      "right_db_type": "pg",
      "right_query_file": "new_query.sql"
    }
  ]
}
```

You can mix and match database types for your comparisons as needed. SQL syntax differences between database engines should be handled in your query files.

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
