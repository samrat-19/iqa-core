from flask import Blueprint, request, jsonify
from utility.generate_sql_files import generate_ddl_files

db_metadata_bp = Blueprint("dbMetadata", __name__)

@db_metadata_bp.route("/extract-ddls", methods=["POST"])
def extract_ddls():
    """Handles the request to extract and save table DDLs from a MySQL database."""
    try:
        # Parse request JSON
        data = request.get_json()
        host = data.get("host")
        port = data.get("port")
        database = data.get("database")
        username = data.get("username")
        password = data.get("password")

        # Validate input
        if not host or not port or not database or not username or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Call function to generate SQL files
        generate_ddl_files(host, port, database, username, password)

        return jsonify({"message": "DDL extraction completed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500