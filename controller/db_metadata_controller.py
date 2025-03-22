from flask import Blueprint, request, jsonify
import os
from services.db_service import generate_ddl_files,generate_table_description_metadata




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

@db_metadata_bp.route("/generate-table-desc-metadata", methods=["POST"])
def generate_table_desc_metadata():
    """Generates and saves table descriptions in the metadata directory."""
    try:
        generate_table_description_metadata()
        return jsonify({"message": "Table description metadata generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500