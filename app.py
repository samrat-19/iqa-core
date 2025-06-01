from flask import Flask
from controller.user_query_controller import user_query_bp
from controller.db_metadata_controller import db_metadata_bp
from controller.generate_prompt_controller import generate_prompt_bp
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(user_query_bp)
app.register_blueprint(db_metadata_bp)
app.register_blueprint(generate_prompt_bp)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)