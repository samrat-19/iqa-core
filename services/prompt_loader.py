import os

def load_prompt_for_keywords_extraction():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(root_dir, "dynamicPrompts", "insight_query_prompt.txt")

    with open(prompt_path, "r") as file:
        return file.read()

def load_prompt_for_validation():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(root_dir, "dynamicPrompts", "validate_query_prompt.txt")
    with open(prompt_path, "r") as file:
        return file.read()