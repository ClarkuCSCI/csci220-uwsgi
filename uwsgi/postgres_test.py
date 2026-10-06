import os

import psycopg


def application(env, start_response):
    body = "Available databases: "
    try:
        conn = psycopg.connect(
            host="postgres",
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        )
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database")
        body += str(cur.fetchall())
    except psycopg.Warning as e:
        print(f"Database warning: {e}")
        body += "Check logs for DB warning"
    except psycopg.Error as e:
        print(f"Database error: {e}")
        body += "Check logs for DB error"
    start_response("200 OK", [("Content-Type", "text/html")])
    return [body.encode("utf-8")]
