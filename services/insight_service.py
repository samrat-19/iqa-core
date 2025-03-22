import os

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
dynamic_prompt_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dynamicPrompts")
metadata_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "metadata/tables")

table_desc_path = os.path.join(metadata_dir, "table_descriptions.txt")
insight_prompt_template_path = os.path.join(template_dir, "query_insight_prompt_template.txt")
generated_insight_prompt_path = os.path.join(dynamic_prompt_dir, "insight_query_prompt.txt")

# Ensure dynamicPrompts directory exists
os.makedirs(dynamic_prompt_dir, exist_ok=True)


def generate_insight_prompt():
    """Generates an insight prompt by appending table descriptions."""
    try:
        # Read table descriptions
        if os.path.exists(table_desc_path):
            with open(table_desc_path, "r") as file:
                table_descriptions = file.read()
        else:
            table_descriptions = ""

        # Read prompt template
        with open(insight_prompt_template_path, "r") as file:
            insight_template = file.read()

        # Format final prompt
        final_prompt = insight_template.format(table_descriptions=table_descriptions, query="{query}")

        # Save the generated prompt
        with open(generated_insight_prompt_path, "w") as file:
            file.write(final_prompt)

        return {"message": "Insight prompt generated successfully."}
    except Exception as e:
        return {"error": str(e)}
