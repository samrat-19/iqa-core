import os
import requests
from flask import jsonify
from sqlalchemy import create_engine, text
from services.prompt_runner import call_llm_for_description


# Constants
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
ddls_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ddls")
metadata_dir = "metadata/tables"
os.makedirs(metadata_dir, exist_ok=True)

# Define metadata directory
summary_prompt_path = os.path.join(template_dir, "table_summary_prompt_template.txt")


def generate_ddl_files(host, port, database, username, password):
    # Construct the correct SQLAlchemy MySQL URL
    # Only supporting MySQL for the demo
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

def generate_table_description_metadata():
    """Extracts table descriptions from DDLs and stores them in a metadata file."""
    try:
        table_descriptions = []

        os.makedirs(metadata_dir, exist_ok=True)  # Ensure metadata directory exists

        for ddl_file in os.listdir(ddls_dir):
            if ddl_file.endswith(".sql"):
                with open(os.path.join(ddls_dir, ddl_file), "r") as file:
                    ddl_content = file.read()

                table_name = ddl_file.replace(".sql", "")
                table_summary = call_llm_for_description(ddl_content, summary_prompt_path)
                if table_summary:
                    table_descriptions.append(f"- {table_name}: {table_summary}")

        table_desc_path = os.path.join(metadata_dir, "table_descriptions.txt")

        with open(table_desc_path, "w") as file:
            file.write("\n".join(table_descriptions))

    except Exception as e:
        raise Exception(f"Error generating table descriptions: {str(e)}")


