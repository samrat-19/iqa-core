import json
from services.prompt_loader import load_prompt_for_validation, load_prompt_for_keywords_extraction, load_prompt_for_sql_generation


def generate_sql_prompt(query, db_metadata):
    base_prompt = load_prompt_for_sql_generation()
    formatted_prompt = base_prompt.format(
        db_metadata=json.dumps(db_metadata, indent=4),
        query=query
    )
    return formatted_prompt

def generate_sql_validaation_prompt(query):
    base_prompt = load_prompt_for_validation()
    formatted_prompt = base_prompt.format(query=query)
    return formatted_prompt

def generate_insights_extraction_prompt(query):
    base_prompt = load_prompt_for_keywords_extraction()
    formatted_prompt = base_prompt.format(query=query)
    return formatted_prompt