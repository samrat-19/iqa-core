import os
import requests
import json
from services.prompt_generator import generate_sql_prompt, generate_sql_validaation_prompt, generate_insights_extraction_prompt
from mockData.db_schema import db_metadata


def call_llm_for_insights(query):
    api_url = "http://localhost:11434/api/generate"
    prompt = generate_insights_extraction_prompt(query)
    body = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=body, headers=headers)
    if response.status_code == 200:
        parsed_response = response.json()
        return json.loads(parsed_response["response"])
    else:
        return "Error in generating insights"


def call_llm_for_sql(query):
    api_url = "http://localhost:11434/api/generate"
    prompt = generate_sql_prompt(query, db_metadata)
    body = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=body, headers=headers)
    if response.status_code == 200:
        parsed_response = response.json()
        return json.loads(parsed_response["response"])
    else:
        return "Error in generating sql"


def call_llm_for_validation(query):
    api_url = "http://localhost:11434/api/generate"
    prompt = generate_sql_validaation_prompt(query)
    body = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=body, headers=headers)
    if response.status_code == 200:
        parsed_response = response.json()
        return parsed_response["response"]
    else:
        return "Error in generating sql"
