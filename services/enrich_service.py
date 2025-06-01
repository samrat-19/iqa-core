from services.llm_service import call_llm

def load_prompt_template(path):
    with open(path, "r") as f:
        return f.read()


def load_table_descriptions(path="metadata/tables/table_descriptions.txt"):
    with open(path, "r") as f:
        return f.read()


def format_enrichment_prompt(user_query, template_path="templates/enrich_user_query_prompt_template.txt"):
    """Fills the enrichment prompt template with just the general table descriptions."""
    descriptions = load_table_descriptions()
    template = load_prompt_template(template_path)
    return template.format(descriptions=descriptions.strip(), query=user_query.strip())


def enrich_user_query(user_query):
    """Main callable to enrich user query using LLM."""
    prompt = format_enrichment_prompt(user_query)
    enriched_query = call_llm(prompt)  # Replace this with your actual LLM handler
    return enriched_query.strip()