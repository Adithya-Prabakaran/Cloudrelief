"""
ClassifierService interface. Route handlers must depend on this ABC only —
never import MockClassifierService (or a future RekognitionClassifierService)
directly. Get an instance via app.services.factory.get_classifier_service().
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    label: str
    confidence: float


class ClassifierService(ABC):
    @abstractmethod
    def classify_image(self, image_path: str) -> ClassificationResult:
        raise NotImplementedError
