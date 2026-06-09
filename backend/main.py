from fastapi import FastAPI

app = FastAPI(title="GuardianAI Edge Safety API")


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
def alerts():
    return {
        "alerts": [
            {
                "type": "fire",
                "location": "Camera 1",
                "severity": "high"
            }
        ]
    }