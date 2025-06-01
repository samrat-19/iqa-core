import os
import sqlparse

from sqlalchemy import create_engine, text
from services.db_service import DB_CREDENTIALS
from services.llm_service import call_llm
from services.insight_service import call_llm_for_insights
from services.semantic_search import get_faiss_index, get_top_k_similar_tables
from services.enrich_service import enrich_user_query

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
ddls_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ddls")
metadata_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "metadata/tables")
sql_prompt_template_path = os.path.join(template_dir, "generate_sql_prompt_template.txt")
table_desc_path = os.path.join(metadata_dir, "table_descriptions.txt")
table_embeddings_path = os.path.join(metadata_dir, "table_embeddings.json")
DIALECT = "MySQL"  # Hardcoded dialect for now


def call_llm_for_sql(query):
    """Calls the LLM API to generate SQL from the query."""
    prompt = generate_sql_prompt(query)
    generated_sql = call_llm(prompt)  # Assuming this returns a valid SQL string

    parsed = sqlparse.parse(generated_sql)
    print("Parsed Successfully:", bool(parsed))

    # Extract SQL as string (first statement in parsed list)
    sql_statement = str(parsed[0]) if parsed else generated_sql  # Fallback to raw SQL

    if not is_safe(sql_statement):
        return "Restricted action. Your name has been logged in the system"

    # Check for non-SELECT queries
    # if parsed and parsed[0].get_type().upper() != "SELECT":
    #     return "Restricted action. Your name has been logged in the system"

    result = execute_sql(sql_statement)
    print("Execution Result:", result.get("result"))
    return generated_sql


def execute_sql(sql_statement):
    """Executes the SQL statement on the actual database using stored credentials."""
    try:
        if not DB_CREDENTIALS:
            return {"success": False, "error": "Database credentials not found. Please generate DDL files first."}

        # Construct DB connection URL from stored credentials
        db_url = f"mysql+pymysql://{DB_CREDENTIALS['username']}:{DB_CREDENTIALS['password']}@" \
                 f"{DB_CREDENTIALS['host']}:{DB_CREDENTIALS['port']}/{DB_CREDENTIALS['database']}"

        # Create a new SQLAlchemy engine for executing queries
        engine = create_engine(db_url)

        with engine.connect() as connection:
            result = connection.execute(text(sql_statement))
            fetched_data = result.fetchall()  # Fetch results

        return {"success": True, "result": [row._asdict() for row in fetched_data]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_sql_prompt(query):
    """Generates an SQL prompt dynamically based on identified tables, descriptions, and DDLs."""
    try:
        # Extract identified tables from LLM insights
        result = call_llm_for_insights(query)
        identified_tables = result.get("identified_tables", [])

        # Fetch relevant DDLs and descriptions
        ddls = fetch_table_ddls(identified_tables)
        table_descriptions = fetch_table_descriptions(identified_tables)

        # Read SQL prompt template
        with open(sql_prompt_template_path, "r") as file:
            sql_generator_prompt_template = file.read()

        # Format final prompt dynamically
        final_prompt = sql_generator_prompt_template.format(
            table_descriptions=table_descriptions,
            ddls=ddls,
            dbDialect=DIALECT,  # Hardcoded dialect
            query=query
        )

        return final_prompt
    except Exception as e:
        return {"error": str(e)}


def generate_sql_prompt_v2(query, k=5):
    index, table_names, summaries = get_faiss_index()
    """Uses semantic search to find relevant tables and builds SQL generation prompt."""
    try:
        enriched_query = enrich_user_query(query)
        print("Enriched Query: ", enriched_query)
        top_k_indices = get_top_k_similar_tables(enriched_query, index, summaries, k=k)
        identified_tables = [table_names[i] for i in top_k_indices]
        print("🧠 Identified tables from semantic search:", identified_tables)
        # Fetch relevant DDLs and descriptions
        ddls = fetch_table_ddls(identified_tables)
        table_descriptions = fetch_table_descriptions(identified_tables)

        # Read prompt template
        with open(sql_prompt_template_path, "r") as file:
            sql_generator_prompt_template = file.read()

        # Format the prompt
        final_prompt = sql_generator_prompt_template.format(
            table_descriptions=table_descriptions,
            ddls=ddls,
            dbDialect=DIALECT,
            query=query
        )

        return final_prompt
    except Exception as e:
        return {"error": str(e)}


def fetch_table_ddls(identified_tables):
    """Fetches DDLs for identified tables from the ddls directory."""
    ddls = []
    for table in identified_tables:
        ddl_path = os.path.join(ddls_dir, f"{table}.sql")
        if os.path.exists(ddl_path):
            with open(ddl_path, "r") as file:
                ddls.append(file.read())
    return "\n".join(ddls)


def fetch_table_descriptions(identified_tables):
    """Fetches table descriptions for identified tables."""
    if not os.path.exists(table_desc_path):
        return ""

    with open(table_desc_path, "r") as file:
        all_descriptions = file.read()

    # Extract descriptions relevant to identified tables
    descriptions = [
        desc for table in identified_tables for desc in all_descriptions.split("\n") if table in desc
    ]

    return "\n".join(descriptions)


def is_safe(sql):
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False  # Invalid SQL

    # Check every statement in the parsed SQL
    for stmt in parsed:
        stmt_type = stmt.get_type()

        # If any statement is not SELECT, immediately return False
        if stmt_type != "SELECT":
            return False

    return True  # If all statements are SELECT, allow execution
