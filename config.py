import os

class Config:
    # -------------------------
    # Flask
    # -------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-change-this")

    # -------------------------
    # JWT
    # -------------------------
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key-change-this")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day

    # -------------------------
    # MongoDB
    # -------------------------
    MONGO_URI = os.environ.get(
        "MONGO_URI",
        "mongodb://localhost:27017/glaucoma_db"
    )

    # -------------------------
    # Model
    # -------------------------
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "model",
        "best_inceptionv3_glaucoma.h5"
    )

    IMG_SIZE = (224, 224)
    PREDICTION_THRESHOLD = 0.5
