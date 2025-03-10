import os
from sqlalchemy import create_engine, text

def generate_ddl_files(host, port, database, username, password):
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