"""
MockClassifierService — stands in for Rekognition. Returns a random label
and confidence so the severity pipeline is fully testable without any real
image classification.

To swap in real Rekognition later: implement
RekognitionClassifierService(ClassifierService) using boto3's rekognition
client (detect_labels against the uploaded S3 object), map its labels onto
CLASSIFIER_LABELS, then flip CLASSIFIER_PROVIDER=rekognition in .env.
"""
import random

from app.core.constants import CLASSIFIER_LABELS
from app.services.classifier.base import ClassificationResult, ClassifierService


class MockClassifierService(ClassifierService):
    def classify_image(self, image_path: str) -> ClassificationResult:
        label = random.choice(CLASSIFIER_LABELS)
        confidence = round(random.uniform(0.4, 0.99), 4)
        return ClassificationResult(label=label, confidence=confidence)
