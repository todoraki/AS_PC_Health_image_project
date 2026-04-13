from io import BytesIO
from PIL import Image
import numpy as np
from app.config.settings import IMAGE_SIZE


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """Load a PIL Image from raw bytes and convert to RGB."""
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def resize_image(image: Image.Image, size: tuple = IMAGE_SIZE) -> Image.Image:
    """Resize image to the target dimensions."""
    return image.resize(size, Image.LANCZOS)


def image_to_array(image: Image.Image) -> np.ndarray:
    """Convert PIL Image to a normalized [0,1] float32 numpy array."""
    return np.array(image, dtype=np.float32) / 255.0


def flatten_image(image_array: np.ndarray) -> np.ndarray:
    """Flatten a multi-dimensional image array into a 1-D feature vector."""
    return image_array.flatten()


def to_grayscale_cnn_input(image: Image.Image) -> np.ndarray:
    """Convert a PIL Image to a 4-D float32 array ready for the CNN.

    Steps:
      - Convert to grayscale (L mode)
      - Resize to IMAGE_SIZE (224×224)
      - Normalize pixels to [0, 1]
      - Expand dims → shape (1, 224, 224, 1)  for model.predict()

    Returns
    -------
    np.ndarray  shape (1, 224, 224, 1)
    """
    gray = image.resize(IMAGE_SIZE, Image.LANCZOS).convert("L")
    arr = np.array(gray, dtype=np.float32) / 255.0       # (224, 224)
    arr = arr[..., np.newaxis]                            # (224, 224, 1)
    return np.expand_dims(arr, axis=0)                    # (1, 224, 224, 1)
