from typing import List
from app.pipeline.base import BaseFilter


class PipelineRunner:
    """Orchestrator for the Pipe-and-Filter pipeline.

    Chains an ordered list of ``BaseFilter`` instances and pushes
    a data dictionary through each one sequentially.
    """

    def __init__(self, filters: List[BaseFilter]):
        self.filters = filters

    def run(self, initial_data: dict) -> dict:
        """Execute every filter in order and return the final data dict."""
        data = initial_data
        for filt in self.filters:
            data = filt.process(data)
        return data

    def get_stage_names(self) -> List[str]:
        """Return the names of all registered pipeline stages."""
        return [f.name for f in self.filters]
