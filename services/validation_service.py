import os
from services.prompt_loader import load_prompt_for_validation
from services.llm_service import call_llm

# Paths
metadata_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "metadata/tables")
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
dynamic_prompt_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dynamicPrompts")

table_desc_path = os.path.join(metadata_dir, "table_descriptions.txt")
validation_prompt_path = os.path.join(template_dir, "validation_prompt_template.txt")
generated_prompt_path = os.path.join(dynamic_prompt_dir, "validate_query_prompt.txt")

os.makedirs(dynamic_prompt_dir, exist_ok=True)  # Ensure directory exists

def generate_validation_prompt():
    """Generates validation prompt using stored table descriptions."""
    try:
        if not os.path.exists(table_desc_path):
            return {"error": "Table descriptions metadata not found."}

        with open(table_desc_path, "r") as file:
            table_descriptions = file.read().strip()

        with open(validation_prompt_path, "r") as file:
            validation_template = file.read()

        final_prompt = validation_template.format(
            table_descriptions=table_descriptions,
            query="{query}"  # Placeholder for later use
        )

        with open(generated_prompt_path, "w") as file:
            file.write(final_prompt)

        return {"message": "Validation prompt generated successfully."}

    except Exception as e:
        return {"error": str(e)}

def generate_sql_validaation_prompt(query):
    base_prompt = load_prompt_for_validation()
    formatted_prompt = base_prompt.format(query=query)
    return formatted_prompt

def call_llm_for_validation(query):
    """Calls the LLM API to validate SQL."""
    prompt = generate_sql_validaation_prompt(query)
    return call_llm(prompt)