from flask import Blueprint, request, jsonify
from services.prompt_runner import call_llm_for_insights, call_llm_for_sql, call_llm_for_validation

user_query_bp = Blueprint("userQuery", __name__)

@user_query_bp.route('/answer', methods=['POST'])
def answer_query():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        result = call_llm_for_insights(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_query_bp.route('/generate-sql', methods=['POST'])
def generate_sql():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        result = call_llm_for_sql(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_query_bp.route('/validate-query', methods=['POST'])
def validate_sql():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        result = call_llm_for_validation(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
