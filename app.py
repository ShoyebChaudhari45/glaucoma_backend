import tensorflow as tf
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import init_extensions
from routes.auth_routes import auth_bp
from routes.predict_routes import predict_bp
from routes.user_routes import user_bp
from services.predict_service import load_glaucoma_model

# ----------------------------
# Suppress TensorFlow warnings
# ----------------------------
tf.get_logger().setLevel("ERROR")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    # ----------------------------
    # Init extensions
    # ----------------------------
    init_extensions(app)
    

    # ----------------------------
    # Load AI model once
    # ----------------------------
    load_glaucoma_model(app.config["MODEL_PATH"])
    
    # ----------------------------
    # Register blueprints
    # ----------------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(predict_bp)
    app.register_blueprint(user_bp, url_prefix="/user")

    # ----------------------------
    # Health check
    # ----------------------------
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "OK"}), 200

    return app
 
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)