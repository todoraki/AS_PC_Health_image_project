from app.pipeline.base import BaseFilter
from app.pipeline.preprocess import ImagePreprocessor
from app.pipeline.metadata_processor import MetadataPreprocessor
from app.pipeline.feature_combiner import FeatureCombiner
from app.pipeline.species_classifier import SpeciesClassifier
from app.pipeline.disease_classifier import DiseaseClassifier
from app.pipeline.result_formatter import ResultFormatter
from app.pipeline.pipeline_runner import PipelineRunner


def create_pipeline() -> PipelineRunner:
    """Factory function – assembles the default disease-detection pipeline."""
    filters = [
        ImagePreprocessor(),       # Filter 1: image preprocessing
        MetadataPreprocessor(),    # Filter 2: metadata preprocessing
        FeatureCombiner(),         # Filter 3: combine features
        SpeciesClassifier(),       # Filter 4: AS / PC classification
        DiseaseClassifier(),       # Filter 5: healthy / unhealthy
        ResultFormatter(),         # Filter 6: format output
    ]
    return PipelineRunner(filters)
