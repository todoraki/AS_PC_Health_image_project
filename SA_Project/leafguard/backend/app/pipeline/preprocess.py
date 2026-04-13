from app.pipeline.base import BaseFilter
from app.utils.image_utils import (
    load_image_from_bytes,
    to_grayscale_cnn_input,
)


class ImagePreprocessor(BaseFilter):
    """Filter 1 – Image Preprocessing.

    Loads the raw bytes, converts to a PIL Image, and produces
    two representations:

    1. ``pil_image``          – original PIL Image (RGB, resized) for display.
    2. ``grayscale_cnn_input``– float32 array of shape (1, 224, 224, 1),
                                 normalized to [0, 1], ready for CNN.predict().

    Reads:  data["image_bytes"]
    Writes: data["pil_image"], data["grayscale_cnn_input"]
    """

    def process(self, data: dict) -> dict:
        image_bytes = data["image_bytes"]

        image = load_image_from_bytes(image_bytes)
        grayscale_input = to_grayscale_cnn_input(image)

        data["pil_image"] = image
        data["grayscale_cnn_input"] = grayscale_input
        return data
