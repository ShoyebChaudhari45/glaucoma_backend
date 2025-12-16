from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.predict_service import run_prediction

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    user_email = get_jwt_identity()

    if "image" not in request.files:
        return jsonify({"error": "Image file required"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Invalid file"}), 400

    try:
        label, confidence = run_prediction(file, user_email)

        return jsonify({
            "prediction": label,
            "confidence": f"{confidence}%"
        }), 200

    # except ValueError as e:
    #     return jsonify({"error": str(e)}), 400
    # except Exception:
    #     return jsonify({"error": "Prediction failed"}), 500





    except Exception as e:
        print("❌ PREDICTION ERROR:", str(e))
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500