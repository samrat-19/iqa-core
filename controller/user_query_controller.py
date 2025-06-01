from flask import Blueprint, request, jsonify
from services.insight_service import call_llm_for_insights
from services.mysql_service import call_llm_for_sql, generate_sql_prompt_v2, execute_sql
from services.validation_service import call_llm_for_validation

user_query_bp = Blueprint("userQuery", __name__)

@user_query_bp.route('/query-insights', methods=['POST'])
def query_insights():
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


@user_query_bp.route('/generate-sql-v2', methods=['POST'])
def generate_sql_v2():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400

        final_prompt = generate_sql_prompt_v2(query)
        result = call_llm_for_sql(final_prompt)
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

@user_query_bp.route("/show-results", methods=["POST"])
def show_results():
    data = request.get_json()
    sql_statement = data.get("query")

    if not sql_statement:
        return jsonify({"error": "Missing SQL query"}), 400

    try:
        result = execute_sql(sql_statement)
        print("Execution Result:", result.get("result"))
        return jsonify({"result": result.get("result")})
    except Exception as e:
        print("Error during execution:", str(e))
        return jsonify({"error": str(e)}), 500
