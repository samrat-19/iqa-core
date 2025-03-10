from flask import Flask, request, jsonify
from services.prompt_runner import call_llm_for_insights, call_llm_for_sql, call_llm_for_validation

app = Flask(__name__)

@app.route('/answer', methods=['POST'])
def answer_query():
    """
    Endpoint to receive user query and fetch insights based on LLM processing
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        # Process query through LLM service
        result = call_llm_for_insights(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-sql', methods=['POST'])
def generate_sql():
    """
    Endpoint to receive user query and fetch insights based on LLM processing
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        # Process query through LLM service
        result = call_llm_for_sql(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/validate-query', methods=['POST'])
def validate_sql():
    """
    Endpoint to receive user query and fetch insights based on LLM processing
    """
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Query is required"}), 400
        # Process query through LLM service
        result = call_llm_for_validation(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)