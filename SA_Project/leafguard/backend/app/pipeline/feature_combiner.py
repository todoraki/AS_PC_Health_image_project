import numpy as np
from app.pipeline.base import BaseFilter


class FeatureCombiner(BaseFilter):
    """Filter 3 – Feature Combination.

    Currently passes ``metadata_features`` directly as
    ``combined_features`` for the SpeciesClassifier.

    The disease models (DiseaseClassifier) perform their own internal
    feature extraction (CNN embeddings + tabular) and do NOT use
    combined_features, so no image flattening is needed here.

    TODO: When the species classifier model is trained and its
          expected feature vector is known, update this filter to
          combine image and tabular features accordingly.

    Reads:  data["metadata_features"]
    Writes: data["combined_features"]
    """

    def process(self, data: dict) -> dict:
        data["combined_features"] = data["metadata_features"].copy()
        return data
