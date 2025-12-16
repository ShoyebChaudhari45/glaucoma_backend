import numpy as np
from PIL import Image
from io import BytesIO
from config import Config


def preprocess_image(file_stream):
    try:
        image = Image.open(BytesIO(file_stream)).convert("RGB")
    except Exception:
        raise ValueError("Invalid image file")

    image = image.resize(Config.IMG_SIZE)
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    return image_array
