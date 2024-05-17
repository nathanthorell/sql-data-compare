import os
import time
import pyodbc
import json
from utils.get_conn import get_conn_string


def execute_sql_query(conn, sql_query):
    """
    Execute a SQL file
    """
    start_time = time.time()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    cursor.close()
    end_time = time.time()
    duration = end_time - start_time
    return result, duration


def compare_sql(left_conn, right_conn, left_query, right_query):
    left_result, left_duration = execute_sql_query(left_conn, left_query)
    print(f"Left query runtime: {left_duration} seconds")

    right_result, right_duration = execute_sql_query(right_conn, right_query)
    print(f"Right query runtime: {right_duration} seconds")

    if left_result == right_result:
        return "EQUAL"
    else:
        return "NOT EQUAL"


def main():
    left_conn_str = get_conn_string("left")
    right_conn_str = get_conn_string("right")

    left_conn = pyodbc.connect(left_conn_str)
    right_conn = pyodbc.connect(right_conn_str)

    script_dir = os.path.dirname(__file__)
    full_sql_dir = os.path.join(script_dir, "sql")
    config_path = os.path.join(script_dir, "config.json")

    with open(config_path, "r") as f:
        config = json.load(f)

    # Loop through compare_list
    for comparison in config["compare_list"]:
        name = comparison["name"]
        left_query_file = comparison["left_query_file"]
        right_query_file = comparison["right_query_file"]

        left_sql_file_path = os.path.join(full_sql_dir, left_query_file)
        right_sql_file_path = os.path.join(full_sql_dir, right_query_file)

        with open(left_sql_file_path, "r") as f:
            left_query = f.read()
        with open(right_sql_file_path, "r") as f:
            right_query = f.read()

        compare_sql_result = compare_sql(left_conn, right_conn, left_query, right_query)
        print(f"{name}: {compare_sql_result}")

    left_conn.close()
    right_conn.close()


if __name__ == "__main__":
    main()
