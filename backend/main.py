from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    alert_rows = ""

    for alert in alerts_db:
        severity = alert["severity"].lower()

        if severity == "high":
            severity_class = "severity-high"
        elif severity == "medium":
            severity_class = "severity-medium"
        else:
            severity_class = "severity-low"

        alert_rows += f"""
        <tr>
            <td>{alert['id']}</td>
            <td>{alert['alert_type']}</td>
            <td>{alert['location']}</td>
            <td><span class="{severity_class}">{alert['severity']}</span></td>
            <td>{alert['message']}</td>
            <td>{alert['timestamp']}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GuardianAI Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                padding: 30px;
            }}

            h1 {{
                color: #38bdf8;
                margin-bottom: 5px;
            }}

            .subtitle {{
                color: #94a3b8;
                margin-bottom: 25px;
            }}

            .card {{
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
                border: 1px solid #334155;
            }}

            .count {{
                font-size: 36px;
                font-weight: bold;
                color: #38bdf8;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: #1e293b;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #334155;
                text-align: left;
            }}

            th {{
                color: #38bdf8;
            }}

            .severity-high {{
                color: #ef4444;
                font-weight: bold;
            }}

            .severity-medium {{
                color: #f59e0b;
                font-weight: bold;
            }}

            .severity-low {{
                color: #22c55e;
                font-weight: bold;
            }}

            .empty {{
                color: #94a3b8;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <h1>GuardianAI Edge Safety Dashboard</h1>
        <p class="subtitle">Real-time AI safety monitoring for edge devices</p>

        <div class="card">
            <p>Total Alerts</p>
            <div class="count">{len(alerts_db)}</div>
        </div>

        <div class="card">
            <h2>Alert History</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Location</th>
                    <th>Severity</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                </tr>
                {alert_rows if alert_rows else '<tr><td colspan="6" class="empty">No alerts generated yet.</td></tr>'}
            </table>
        </div>
    </body>
    </html>
    """