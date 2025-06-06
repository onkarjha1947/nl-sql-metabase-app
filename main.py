from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from services.nlp_to_sql import get_sql_from_question
from services.metabase import run_sql

app = FastAPI()

# ✅ Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    try:
        body = await request.json()
        question = body["question"]
    except Exception:
        return {"error": "Invalid request. Please send JSON with a 'question' key."}

    sql_query = get_sql_from_question("data/schema.json", question)
    result = run_sql(sql_query)
    return {"sql": sql_query, "result": result}
