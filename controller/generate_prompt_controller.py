from flask import Blueprint, jsonify
from services.validation_service import generate_validation_prompt
from services.insight_service import generate_insight_prompt

generate_prompt_bp = Blueprint("generate_prompt", __name__)

@generate_prompt_bp.route("/generate-validation-prompt", methods=["POST"])
def validation_prompt():
    """API endpoint to generate validation prompt."""
    result = generate_validation_prompt()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@generate_prompt_bp.route("/generate-insight-prompt", methods=["POST"])
def insight_prompt():
    """API endpoint to generate insight prompt."""
    result = generate_insight_prompt()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200