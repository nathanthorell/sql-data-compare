import os


def get_conn_string(type):
    """
    Extract DB Credentials from environment variables
    type expects "left" or "right"
    """
    if type == "left":
        env_type = "LEFT"
    elif type == "right":
        env_type = "RIGHT"

    host = os.getenv(f"{env_type}_DB_HOST")
    db = os.getenv(f"{env_type}_DB_NAME")
    user = os.getenv(f"{env_type}_DB_USER")
    password = os.getenv(f"{env_type}_DB_PASS")
    port = os.getenv(f"{env_type}_DB_PORT")
    driver = os.getenv("DB_DRIVER")
    encrypt = os.getenv("DB_ENCRYPT")

    conn = (
        f"DRIVER={driver};"
        f"SERVER={host},{port};"
        f"DATABASE={db};"
        f"UID={user};"
        f"PWD={password};"
        f"Encrypt={encrypt};"
    )
    return conn
