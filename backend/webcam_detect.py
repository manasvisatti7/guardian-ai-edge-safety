import cv2
import requests
from ultralytics import YOLO

model = YOLO("models/yolov8n.pt")

cap = cv2.VideoCapture(0)

restricted_alert_sent = False

RESTRICTED_ZONE_TOP_LEFT = (180, 120)
RESTRICTED_ZONE_BOTTOM_RIGHT = (460, 420)


def send_alert(alert_type, location, severity, message):
    alert_data = {
        "alert_type": alert_type,
        "location": location,
        "severity": severity,
        "message": message
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/alerts",
            json=alert_data,
            timeout=3
        )

        if response.status_code == 200:
            print("ALERT CREATED:", message)
        else:
            print("Alert failed with status:", response.status_code)

    except Exception as e:
        print("Alert Error:", e)


def is_inside_restricted_zone(x_center, y_center):
    x1, y1 = RESTRICTED_ZONE_TOP_LEFT
    x2, y2 = RESTRICTED_ZONE_BOTTOM_RIGHT

    return x1 <= x_center <= x2 and y1 <= y_center <= y2


while True:
    success, frame = cap.read()

    if not success:
        break

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.rectangle(
        annotated_frame,
        RESTRICTED_ZONE_TOP_LEFT,
        RESTRICTED_ZONE_BOTTOM_RIGHT,
        (0, 0, 255),
        3
    )

    cv2.putText(
        annotated_frame,
        "RESTRICTED ZONE",
        (RESTRICTED_ZONE_TOP_LEFT[0], RESTRICTED_ZONE_TOP_LEFT[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name == "person":
                x1, y1, x2, y2 = box.xyxy[0]

                x_center = int((x1 + x2) / 2)
                y_center = int((y1 + y2) / 2)

                cv2.circle(
                    annotated_frame,
                    (x_center, y_center),
                    6,
                    (0, 255, 255),
                    -1
                )

                if is_inside_restricted_zone(x_center, y_center) and not restricted_alert_sent:
                    send_alert(
                        "restricted_zone_violation",
                        "Live Webcam",
                        "high",
                        "Person entered restricted zone"
                    )

                    restricted_alert_sent = True

    cv2.imshow("GuardianAI Restricted Zone Monitoring", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()