import openai, json, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_prompt(schema_json, question):
    schema_description = ""
    for table, meta in schema_json.items():
        schema_description += f"\nTable: {table}\nDescription: {meta['description']}\n"
        for col, desc in meta["columns"].items():
            schema_description += f"  - {col}: {desc}\n"
    prompt = f"""
You are an expert SQL developer. Based on the schema below, write a SQL query to answer the question.

Schema:
{schema_description}

Question: {question}

SQL Query:
"""
    return prompt

def get_sql_from_question(schema_path, question):
    with open(schema_path) as f:
        schema_json = json.load(f)
    prompt = create_prompt(schema_json, question)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response['choices'][0]['message']['content'].strip()
