import os
import requests
from flask import Blueprint, jsonify

# Define Blueprint
generate_validation_prompt_bp = Blueprint("generate_prompt", __name__)

# Constants
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
dynamic_prompt_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dynamicPrompts")
ddls_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ddls")
summary_prompt_path = os.path.join(template_dir, "table_summary_prompt_template.txt")
validation_prompt_path = os.path.join(template_dir, "validation_prompt_template.txt")
generated_prompt_path = os.path.join(dynamic_prompt_dir, "validate_query_prompt.txt")

# Ensure dynamicPrompts directory exists
os.makedirs(dynamic_prompt_dir, exist_ok=True)


def call_llm_for_description(ddl):
    """Calls the LLM API to generate a table description from DDL."""
    api_url = "http://localhost:11434/api/generate"

    with open(summary_prompt_path, "r") as file:
        prompt_template = file.read()

    prompt = prompt_template.replace("{ddl}", ddl)
    body = {"model": "llama3.1", "prompt": prompt, "stream": False}
    headers = {"Content-Type": "application/json"}

    for _ in range(3):  # Retry up to 3 times
        response = requests.post(api_url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json().get("response", "")

    return ""  # Return empty string if all retries fail


@generate_validation_prompt_bp.route("/generate-validation-prompt", methods=["POST"])
def generate_validation_prompt():
    """Generates a validation prompt by extracting table descriptions."""
    try:
        table_descriptions = []

        for ddl_file in os.listdir(ddls_dir):
            if ddl_file.endswith(".sql"):
                with open(os.path.join(ddls_dir, ddl_file), "r") as file:
                    ddl_content = file.read()

                table_name = ddl_file.replace(".sql", "")
                table_summary = call_llm_for_description(ddl_content)
                if table_summary:
                    table_descriptions.append(f"- {table_name}: {table_summary}")

        with open(validation_prompt_path, "r") as file:
            validation_template = file.read()

        final_prompt = validation_template.format(
            table_descriptions="\n".join(table_descriptions),
            query="{query}"  # Keep this as a placeholder for later use
        )
        with open(generated_prompt_path, "w") as file:
            file.write(final_prompt)

        return jsonify({"message": "Validation prompt generated successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
