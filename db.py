import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

RDS_HOST = os.environ["RDS_HOST"]
RDS_PORT = int(os.environ.get("RDS_PORT", "5432"))
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]


def get_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require",
    )


if __name__ == "__main__":
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"Connected successfully!\nPostgreSQL version: {version}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")
