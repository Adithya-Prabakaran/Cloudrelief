"""
Explainable (non-ML) severity scoring for incidents.

severity = (classifier_score * 0.5) + (keyword_score * 0.25) + (density_score * 0.25)

- classifier_score: the classifier's confidence, but only if the predicted
  label is one of SEVERITY_RELEVANT_LABELS (flood/fire/structural_damage).
  A "normal" label contributes 0 regardless of confidence.
- keyword_score: count of urgent keywords found in the description,
  multiplied by URGENCY_WEIGHT.
- density_score: how many other incidents were reported nearby (within
  DENSITY_RADIUS_KM, in the last DENSITY_WINDOW_HOURS), normalized against
  DENSITY_CAP and scaled by DENSITY_WEIGHT.
"""
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.constants import SEVERITY_RELEVANT_LABELS, URGENT_KEYWORDS


@dataclass
class SeverityResult:
    severity_score: float
    classifier_score: float
    keyword_score: float
    density_score: float
    nearby_report_count: int
    should_alert: bool


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lng points, in kilometers."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def compute_classifier_score(label: str, confidence: float) -> float:
    if label in SEVERITY_RELEVANT_LABELS:
        return confidence
    return 0.0


def compute_keyword_score(description: str) -> float:
    text = (description or "").lower()
    count = sum(1 for kw in URGENT_KEYWORDS if kw in text)
    return count * settings.URGENCY_WEIGHT


def count_nearby_recent_reports(
    latitude: float,
    longitude: float,
    existing_incidents: list[tuple[float, float, datetime]],
) -> int:
    """
    existing_incidents: list of (latitude, longitude, created_at) for other
    incidents already in the DB. Kept as a plain function (no DB session) so
    it's trivially unit-testable and independent of the ORM.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=settings.DENSITY_WINDOW_HOURS)
    nearby = 0
    for lat, lng, created_at in existing_incidents:
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if created_at < cutoff:
            continue
        if haversine_km(latitude, longitude, lat, lng) <= settings.DENSITY_RADIUS_KM:
            nearby += 1
    return nearby


def compute_density_score(nearby_report_count: int) -> float:
    normalized = min(nearby_report_count / settings.DENSITY_CAP, 1.0)
    return normalized * settings.DENSITY_WEIGHT


def compute_severity(
    classifier_label: str,
    classifier_confidence: float,
    description: str,
    latitude: float,
    longitude: float,
    existing_incidents: list[tuple[float, float, datetime]],
) -> SeverityResult:
    classifier_score = compute_classifier_score(classifier_label, classifier_confidence)
    keyword_score = compute_keyword_score(description)
    nearby_count = count_nearby_recent_reports(latitude, longitude, existing_incidents)
    density_score = compute_density_score(nearby_count)

    severity = (classifier_score * 0.5) + (keyword_score * 0.25) + (density_score * 0.25)

    return SeverityResult(
        severity_score=round(severity, 4),
        classifier_score=classifier_score,
        keyword_score=keyword_score,
        density_score=density_score,
        nearby_report_count=nearby_count,
        should_alert=severity >= settings.ALERT_THRESHOLD,
    )
