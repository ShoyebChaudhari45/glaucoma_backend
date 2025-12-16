# from flask import Blueprint, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity

# from extensions import mongo
# from utils.gridfs_utils import delete_image_from_gridfs
# from models.user_model import UserModel

# user_bp = Blueprint("user", __name__)


# # ----------------------------
# # Get Prediction History
# # ----------------------------
# @user_bp.route("/history", methods=["GET"])
# @jwt_required()
# def get_history():
#     user_email = get_jwt_identity()

#     predictions = mongo.db.predictions.find(
#         {"user_email": user_email},
#         {"_id": 0}
#     ).sort("timestamp", -1)

#     history = []
#     for p in predictions:
#         history.append({
#             "prediction": p["prediction"],
#             "confidence": f'{p["confidence"]}%',
#             "timestamp": p["timestamp"],
#             "image_file_id": str(p["image_file_id"])
#         })

#     return jsonify(history), 200


# # ----------------------------
# # Delete Account
# # ----------------------------
# @user_bp.route("/delete", methods=["DELETE"])
# @jwt_required()
# def delete_account():
#     user_email = get_jwt_identity()

#     # ----------------------------
#     # Fetch predictions
#     # ----------------------------
#     predictions = mongo.db.predictions.find({"user_email": user_email})

#     # ----------------------------
#     # Delete images from GridFS
#     # ----------------------------
#     for p in predictions:
#         try:
#             delete_image_from_gridfs(p["image_file_id"])
#         except Exception:
#             pass

#     # ----------------------------
#     # Delete prediction history
#     # ----------------------------
#     mongo.db.predictions.delete_many({"user_email": user_email})

#     # ----------------------------
#     # Delete user
#     # ----------------------------
#     UserModel.delete_user(user_email)

#     return jsonify({"message": "Account deleted successfully"}), 200




from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import mongo, get_fs
from models.user_model import UserModel
import base64
from extensions import get_fs



user_bp = Blueprint("user", __name__)

@user_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    user_email = get_jwt_identity()
    
    fs = get_fs()

    predictions = mongo.db.predictions.find(
        {"user_email": user_email}
    ).sort("timestamp", -1)

    history = []

    for p in predictions:
        image_base64 = None

        try:
            grid_out = fs.get(p["image_file_id"])
            image_bytes = grid_out.read()

            # Convert binary → base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        except Exception:
            pass

        history.append({
            "prediction": p["prediction"],
            "confidence": f'{p["confidence"]}%',
            "timestamp": p["timestamp"],
            "image_base64": image_base64,  
            "image_content_type": grid_out.content_type if image_base64 else None
        })

    return jsonify(history), 200



@user_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_email = get_jwt_identity()

    fs = get_fs()

    predictions = mongo.db.predictions.find({"user_email": user_email})

    # Delete images
    for p in predictions:
        try:
            fs.delete(p["image_file_id"])
        except Exception:
            pass

    # Delete predictions
    mongo.db.predictions.delete_many({"user_email": user_email})

    # Delete user
    UserModel.delete_user(user_email)

    return jsonify({"message": "Account deleted successfully"}), 200
