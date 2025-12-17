from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from services.auth_service import signup_user, login_user

auth_bp = Blueprint("auth", __name__)



@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # ⬇️ REQUIRED SEQUENCE
    name = data.get("name")
    email = data.get("email")
    mobile = data.get("mobile")
    dob = data.get("dob")
    password = data.get("password")

    if not all([name, email, mobile, dob, password]):
        return jsonify({
            "error": "name, email, mobile, dob, password are required"
        }), 400

    try:
        signup_user(name, email, mobile, dob, password)

        # ⬇️ ORDERED RESPONSE
        return jsonify({
            "name": name,
            "email": email,
            "mobile": mobile,
            "dob": dob,
            "message": "User registered successfully"
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

# ----------------------------
# Login
# ----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        user = login_user(email, password)

        # JWT identity
        access_token = create_access_token(identity=user["email"])

        return jsonify({
            "access_token": access_token,
            "user": {
                "name": user.get("name"),
                "email": user.get("email"),
                "mobile": user.get("mobile"),
                "dob": user.get("dob"),
                # "id": user.get("id"),
                # "created_at": user.get("created_at")
            }
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception:
        return jsonify({"error": "Internal server error"}), 500