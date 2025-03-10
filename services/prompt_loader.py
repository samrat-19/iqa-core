import os
import requests
import json


def load_prompt_for_keywords_extraction():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(root_dir, "prompts", "extraction_prompt.txt")

    with open(prompt_path, "r") as file:
        return file.read()

def load_prompt_for_sql_generation():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(root_dir, "prompts", "generate_sql_prompt.txt")
    with open(prompt_path, "r") as file:
        return file.read()

def load_prompt_for_validation():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(root_dir, "prompts", "validate_query_prompt.txt")
    with open(prompt_path, "r") as file:
        return file.read()