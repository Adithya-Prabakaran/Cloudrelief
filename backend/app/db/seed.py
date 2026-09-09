"""
Seeds a demo admin user, a demo citizen, and a handful of fake incidents so
the admin map/table has something to show on first run.

Usage: python -m app.db.seed
"""
import random
from datetime import datetime, timedelta, timezone

from app.core.security import hash_password
from app.db.session import SessionLocal, engine
from app.models.db import Base, Incident, IncidentStatus, IncidentType, User, UserRole

ADMIN_EMAIL = "admin@cloudrelief.local"
ADMIN_PASSWORD = "admin12345"
CITIZEN_EMAIL = "citizen@cloudrelief.local"
CITIZEN_PASSWORD = "citizen12345"

# Roughly centered on downtown San Francisco, for a believable demo map.
DEMO_INCIDENTS = [
    (37.7749, -122.4194, "flood", "Street flooding near the intersection, water rising fast, help needed"),
    (37.7849, -122.4094, "fire", "Fire spotted in an apartment building, people trapped on the 3rd floor"),
    (37.7649, -122.4294, "structural_damage", "Building wall collapsed after the storm, blocking the road"),
    (37.7799, -122.4144, "normal", "Minor pothole and debris on the sidewalk"),
    (37.7699, -122.4244, "flood", "Basement flooding reported, water levels rising"),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD),
                full_name="CloudRelief Admin",
                role=UserRole.admin,
            )
            db.add(admin)
            print(f"Created admin user: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

        citizen = db.query(User).filter(User.email == CITIZEN_EMAIL).first()
        if not citizen:
            citizen = User(
                email=CITIZEN_EMAIL,
                password_hash=hash_password(CITIZEN_PASSWORD),
                full_name="Demo Citizen",
                role=UserRole.citizen,
            )
            db.add(citizen)
            print(f"Created citizen user: {CITIZEN_EMAIL} / {CITIZEN_PASSWORD}")

        db.commit()
        db.refresh(citizen)

        existing_count = db.query(Incident).count()
        if existing_count == 0:
            for lat, lng, incident_type, description in DEMO_INCIDENTS:
                confidence = round(random.uniform(0.5, 0.95), 4)
                severity = round(random.uniform(0.2, 0.9), 4)
                status_choice = random.choice(list(IncidentStatus))
                incident = Incident(
                    citizen_id=citizen.user_id,
                    latitude=lat,
                    longitude=lng,
                    description=description,
                    incident_type=IncidentType(incident_type),
                    classifier_confidence=confidence,
                    severity_score=severity,
                    status=status_choice,
                    created_at=datetime.now(timezone.utc) - timedelta(hours=random.randint(0, 12)),
                )
                db.add(incident)
            db.commit()
            print(f"Seeded {len(DEMO_INCIDENTS)} demo incidents")
        else:
            print(f"Incidents already present ({existing_count}), skipping incident seed")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
