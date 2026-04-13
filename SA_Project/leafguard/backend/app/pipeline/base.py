from abc import ABC, abstractmethod


class BaseFilter(ABC):
    """Abstract base class for every pipeline filter.

    Each filter implements ``process(data) -> data`` and transforms
    a shared data dictionary.  This is the fundamental building block
    of the **Pipe-and-Filter** architectural pattern used in the
    ML inference subsystem.
    """

    @abstractmethod
    def process(self, data: dict) -> dict:
        """Accept a data dictionary, transform it, and return it."""

    @property
    def name(self) -> str:
        return self.__class__.__name__
