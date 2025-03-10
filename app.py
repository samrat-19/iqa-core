from flask import Flask
from controller.user_query_controller import user_query_bp
from controller.db_metadata_controller import db_metadata_bp

app = Flask(__name__)
app.register_blueprint(user_query_bp)
app.register_blueprint(db_metadata_bp)

if __name__ == "__main__":
    app.run(debug=True)