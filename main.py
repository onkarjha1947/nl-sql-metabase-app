from fastapi import FastAPI, Request
from services.nlp_to_sql import get_sql_from_question
from services.metabase import run_sql

app = FastAPI()

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    question = body["question"]

    sql_query = get_sql_from_question("data/schema.json", question)
    result = run_sql(sql_query)
    return {"sql": sql_query, "result": result}
