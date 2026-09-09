"""
ConsoleNotifyService — stands in for SNS. Logs the alert to stdout and
writes an `alerts` row for the admin dashboard / audit trail.

To swap in real SNS later: implement SnsNotifyService(NotifyService) using
boto3's sns client (publish to a topic ARN read from env), then flip
NOTIFY_PROVIDER=sns in .env.
"""
import logging

from sqlalchemy.orm import Session

from app.models.db import Alert
from app.services.notify.base import NotifyService

logger = logging.getLogger("cloudrelief.alerts")


class ConsoleNotifyService(NotifyService):
    def publish_alert(self, db: Session, incident_id: str, severity_score: float, message: str) -> None:
        logger.warning("[ALERT] incident=%s severity=%.3f message=%s", incident_id, severity_score, message)

        alert = Alert(incident_id=incident_id, severity_score=severity_score, message=message)
        db.add(alert)
        db.commit()
