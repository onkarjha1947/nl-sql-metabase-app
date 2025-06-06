import os, requests
from dotenv import load_dotenv

load_dotenv()

METABASE_URL = os.getenv("METABASE_URL")
METABASE_USER = os.getenv("METABASE_USER")
METABASE_PASS = os.getenv("METABASE_PASS")
METABASE_DB_ID = os.getenv("METABASE_DB_ID")

def get_token():
    res = requests.post(f"{METABASE_URL}/api/session", json={
        "username": METABASE_USER,
        "password": METABASE_PASS
    })
    return res.json()["id"]

def run_sql(sql_query):
    token = get_token()
    headers = {"X-Metabase-Session": token}
    payload = {
        "database": int(METABASE_DB_ID),
        "type": "native",
        "native": {"query": sql_query}
    }
    response = requests.post(f"{METABASE_URL}/api/dataset", headers=headers, json=payload)
    return response.json()
