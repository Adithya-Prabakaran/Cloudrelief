"""
Locust load test for CloudRelief's citizen-facing flow: register/login once,
then repeatedly submit an incident report (with image upload) and poll
"my reports" status — the same round trip a real citizen makes during a
disaster surge.

Point this at AWS later with just a host change:
    locust -f benchmark/locustfile.py --host https://api.cloudrelief.example.com

Ramp stages (10 -> 50 -> 200 -> 500 concurrent users) are driven via a
LoadTestShape so a single `locust --headless -f locustfile.py` run walks
through all four stages automatically. Run `benchmark/analyze_results.py`
afterwards against the CSV Locust writes to get p50/p95/p99 + cost-per-1k.
"""
import io
import random
import uuid

from locust import HttpUser, LoadTestShape, task, between

DESCRIPTIONS = [
    "Flooding on Main St, water rising fast, need help",
    "Small fire near the market, spreading slowly",
    "Building wall looks cracked and unstable after the storm",
    "Just a downed tree branch, no injuries",
    "People trapped in a collapsed structure, urgent",
]

# 1x1 transparent PNG, kept tiny so upload throughput isn't the bottleneck
# being measured — the point here is API/backend latency under concurrency.
FAKE_IMAGE_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108020000009077"
    "5301000000097048597300000b1300000b1301009a9c1800000009fceb0000"
    "0d494441545847010000000005fe022fe702000000004945454e42600000"
)


class CitizenUser(HttpUser):
    """Simulates a citizen: log in once, then repeatedly report incidents."""

    wait_time = between(1, 3)

    def on_start(self):
        self.email = f"loadtest-{uuid.uuid4().hex[:10]}@cloudrelief.local"
        self.password = "loadtest12345"
        resp = self.client.post(
            "/api/auth/register",
            json={"email": self.email, "password": self.password, "full_name": "Load Test User"},
            name="/api/auth/register",
        )
        if resp.status_code == 200:
            self.token = resp.json()["access_token"]
        else:
            # Fall back to login in case this user id was already created in a prior run.
            login_resp = self.client.post(
                "/api/auth/login",
                json={"email": self.email, "password": self.password},
                name="/api/auth/login",
            )
            self.token = login_resp.json().get("access_token")

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def submit_incident(self):
        files = {"photo": ("incident.png", io.BytesIO(FAKE_IMAGE_BYTES), "image/png")}
        data = {
            "latitude": str(round(random.uniform(37.70, 37.80), 6)),
            "longitude": str(round(random.uniform(-122.50, -122.40), 6)),
            "description": random.choice(DESCRIPTIONS),
        }
        self.client.post(
            "/api/incidents",
            data=data,
            files=files,
            headers=self.auth_headers,
            name="/api/incidents [submit]",
        )

    @task(2)
    def poll_my_reports(self):
        self.client.get("/api/incidents/mine", headers=self.auth_headers, name="/api/incidents/mine [poll]")


class StagedLoadShape(LoadTestShape):
    """Ramps 10 -> 50 -> 200 -> 500 users, each stage held for 60s."""

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 5},
        {"duration": 120, "users": 50, "spawn_rate": 10},
        {"duration": 180, "users": 200, "spawn_rate": 20},
        {"duration": 240, "users": 500, "spawn_rate": 25},
    ]

    def tick(self):
        run_time = self.get_run_time()
        elapsed = 0
        for stage in self.stages:
            elapsed += stage["duration"]
            if run_time < elapsed:
                return stage["users"], stage["spawn_rate"]
        return None
