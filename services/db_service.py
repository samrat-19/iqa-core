import os
import json
from sqlalchemy import create_engine, text
from services.llm_service import call_llm, call_embedding

# Constants
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
ddls_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ddls")
metadata_dir = "metadata/tables"
os.makedirs(metadata_dir, exist_ok=True)

# Define metadata directory
summary_prompt_path = os.path.join(template_dir, "table_summary_prompt_template.txt")

# Global variable to store DB credentials
DB_CREDENTIALS = {}


def generate_ddl_files(host, port, database, username, password):
    """Generates DDL files and stores DB credentials for later use."""

    DB_CREDENTIALS.update({
        "host": host,
        "port": port,
        "database": database,
        "username": username,
        "password": password
    })

    # Construct the correct SQLAlchemy MySQL URL
    db_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

    # Create the SQLAlchemy engine
    engine = create_engine(db_url)

    # Create directory for storing DDLs
    ddls_dir = os.path.join(os.path.dirname(__file__), "..", "ddls")
    os.makedirs(ddls_dir, exist_ok=True)

    with engine.connect() as connection:
        # Fetch all table names
        result = connection.execute(text("SHOW TABLES;"))
        tables = [row[0] for row in result]

        for table in tables:
            # Fetch DDL statement
            ddl_result = connection.execute(text(f"SHOW CREATE TABLE {table};")).fetchone()
            ddl_statement = ddl_result[1]  # The DDL is in the second column

            # Write to individual .sql file
            with open(os.path.join(ddls_dir, f"{table}.sql"), "w") as file:
                file.write(ddl_statement)

    print(f"Generated DDL files for {len(tables)} tables in {ddls_dir}")


def generate_db_metadata():
    """Generates table summaries and their embeddings from DDLs."""
    try:
        table_descriptions_txt = []
        table_embeddings = []

        os.makedirs(metadata_dir, exist_ok=True)

        for ddl_file in os.listdir(ddls_dir):
            if ddl_file.endswith(".sql"):
                with open(os.path.join(ddls_dir, ddl_file), "r") as file:
                    ddl_content = file.read()

                table_name = ddl_file.replace(".sql", "")
                table_summary = call_llm_for_description(ddl_content, summary_prompt_path)

                if table_summary:
                    # Add to .txt version
                    table_descriptions_txt.append(f"- {table_name}: {table_summary}")

                    # Embed the summary
                    embedding = call_embedding(table_summary)
                    if embedding:
                        table_embeddings.append({
                            "table": table_name,
                            "summary": table_summary,
                            "embedding": embedding
                        })

        # Write to table_descriptions.txt
        with open(os.path.join(metadata_dir, "table_descriptions.txt"), "w") as file:
            file.write("\n".join(table_descriptions_txt))

        # Write to table_embeddings.json
        with open(os.path.join(metadata_dir, "table_embeddings.json"), "w") as file:
            json.dump(table_embeddings, file, indent=2)

        print("✅ Metadata generation complete.")

    except Exception as e:
        raise Exception(f"❌ Error in generate_metadata: {str(e)}")


def call_llm_for_description(ddl, summary_prompt_path):
    """Calls the LLM API to generate a table description from DDL."""
    with open(summary_prompt_path, "r") as file:
        prompt_template = file.read()

    prompt = prompt_template.replace("{ddl}", ddl)
    return call_llm(prompt)
