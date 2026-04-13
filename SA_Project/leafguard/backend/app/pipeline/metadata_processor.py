from app.pipeline.base import BaseFilter
from app.utils.metadata_utils import validate_and_encode_metadata, encode_to_array


class MetadataPreprocessor(BaseFilter):
    """Filter 2 – Metadata Preprocessing.

    Validates all 10 tabular fields, encodes binary fields to 0.0/1.0,
    handles Damage_missing derivation, and produces a float32 feature
    vector in the exact column order expected by the SVM.

    Reads:  data["metadata"]
    Writes: data["validated_metadata"], data["metadata_features"]

    ``metadata_features`` layout (10 floats):
      [Artefacts, Control, Heat, Drought, Heat_Drought,
       Decolourization, Spots, Damage, Damage_missing, Week]
    Note: Week is still the raw integer float here.
    DiseaseClassifier applies tabular_scaler to index 9 before the SVM.
    """

    def process(self, data: dict) -> dict:
        validated = validate_and_encode_metadata(data["metadata"])
        features = encode_to_array(validated)

        data["validated_metadata"] = validated
        data["metadata_features"] = features
        return data
