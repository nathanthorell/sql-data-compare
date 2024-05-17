# sql-data-compare

Simple data comparison of the result set from two different queries, that could also be from two different data sources.

## Local Env Setup

1. python -m venv .venv/
1. source .venv/bin/activate
1. python -m pip install -r ./requirements.txt

  - Note: on Apple Silicon use `brew install unixodbc` and `pip install --no-binary :all: pyodbc`
  - Also [https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16#microsoft-odbc-18]

## Config Setup

A `config.json` file is required. Example:

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

## Environment Variable Setup

These are required

```text
DB_DRIVER="ODBC Driver 18 for SQL Server"
DB_ENCRYPT=no
LEFT_DB_HOST=
LEFT_DB_NAME=
LEFT_DB_PORT=
LEFT_DB_USER=
LEFT_DB_PASS=
RIGHT_DB_HOST=
RIGHT_DB_NAME=
RIGHT_DB_PORT=
RIGHT_DB_USER=
RIGHT_DB_PASS=
```
