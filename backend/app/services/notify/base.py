"""
NotifyService interface. Route handlers must depend on this ABC only —
never import ConsoleNotifyService (or a future SnsNotifyService) directly.
Get an instance via app.services.factory.get_notify_service().
"""
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class NotifyService(ABC):
    @abstractmethod
    def publish_alert(self, db: Session, incident_id: str, severity_score: float, message: str) -> None:
        """Publish a high-severity alert. Local impl logs + writes an `alerts` row.

        A future SnsNotifyService would additionally publish to an SNS topic
        here (e.g. sns.publish(TopicArn=..., Message=message)) while keeping
        the same DB write for audit history.
        """
        raise NotImplementedError
