from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="GuardianAI Edge Safety API")

alerts_db = []


class Alert(BaseModel):
    alert_type: str
    location: str
    severity: str
    message: str


@app.get("/")
def home():
    return {
        "message": "GuardianAI backend is running",
        "project": "Real-time edge safety monitoring for Arm devices"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "online"
    }


@app.get("/alerts")
def get_alerts():
    return {
        "total_alerts": len(alerts_db),
        "alerts": alerts_db
    }


@app.post("/alerts")
def create_alert(alert: Alert):
    new_alert = {
        "id": len(alerts_db) + 1,
        "alert_type": alert.alert_type,
        "location": alert.location,
        "severity": alert.severity,
        "message": alert.message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    alerts_db.append(new_alert)

    return {
        "message": "Alert created successfully",
        "alert": new_alert
    }