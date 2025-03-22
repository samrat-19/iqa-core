import os
import requests
import json
from services.prompt_generator import generate_sql_prompt, generate_sql_validaation_prompt, generate_insights_extraction_prompt
from mockData.db_schema import db_metadata


API_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}

def call_llm(prompt, max_retries=3):
    """Generic function to call LLM API with retries."""
    body = {"model": "llama3.1", "prompt": prompt, "stream": False}

    for _ in range(max_retries):
        response = requests.post(API_URL, json=body, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("response", "")

    return ""  # Return empty string if all retries fail

def call_llm_for_description(ddl, summary_prompt_path):
    """Calls the LLM API to generate a table description from DDL."""
    with open(summary_prompt_path, "r") as file:
        prompt_template = file.read()

    prompt = prompt_template.replace("{ddl}", ddl)
    return call_llm(prompt)

def call_llm_for_insights(query):
    """Calls the LLM API to extract insights from the query."""
    prompt = generate_insights_extraction_prompt(query)
    response = call_llm(prompt)
    return json.loads(response) if response else {}

def call_llm_for_sql(query, db_metadata):
    """Calls the LLM API to generate SQL from the query."""
    prompt = generate_sql_prompt(query, db_metadata)
    response = call_llm(prompt)
    return json.loads(response) if response else {}

def call_llm_for_validation(query):
    """Calls the LLM API to validate SQL."""
    prompt = generate_sql_validaation_prompt(query)
    return call_llm(prompt)
