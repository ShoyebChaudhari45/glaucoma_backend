from datetime import datetime
from tensorflow.keras.models import load_model

from extensions import mongo, get_fs
from utils.image_utils import preprocess_image
from config import Config

_model = None


def load_glaucoma_model(model_path):
    global _model
    if _model is None:
        print("✅ Loading model:", model_path)
        _model = load_model(model_path)
        print("✅ Model loaded")


def run_prediction(file, user_email):
    if _model is None:
        raise RuntimeError("Model not loaded")

    image_bytes = file.read()
    if not image_bytes:
        raise ValueError("Empty image file")

    # ✅ GridFS (SAFE)
    fs = get_fs()
    file_id = fs.put(
        image_bytes,
        filename=file.filename,
        content_type=file.content_type,
        user_email=user_email
    )

    img = preprocess_image(image_bytes)

    raw_pred = _model.predict(img, verbose=0)

    # sigmoid or softmax safe
    if raw_pred.shape[-1] == 1:
        prediction = float(raw_pred[0][0])
    else:
        prediction = float(raw_pred[0][1])

    if prediction >= Config.PREDICTION_THRESHOLD:
        label = "GLAUCOMA"
        confidence = prediction
    else:
        label = "NORMAL"
        confidence = 1 - prediction

    confidence_percent = round(confidence * 100, 2)

    mongo.db.predictions.insert_one({
        "user_email": user_email,
        "image_file_id": file_id,
        "prediction": label,
        "confidence": confidence_percent,
        "timestamp": datetime.utcnow()
    })

    return label, confidence_percent
