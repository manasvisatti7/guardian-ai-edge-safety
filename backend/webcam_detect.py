import cv2
import requests
from ultralytics import YOLO

model = YOLO("models/yolov8n.pt")

cap = cv2.VideoCapture(0)

person_alert_sent = False

while True:
    success, frame = cap.read()

    if not success:
        break

    results = model(frame)

    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name == "person" and not person_alert_sent:

                alert_data = {
                    "alert_type": "person_detected",
                    "location": "Live Webcam",
                    "severity": "medium",
                    "message": "Person detected by GuardianAI"
                }

                try:
                    requests.post(
                        "http://127.0.0.1:8000/alerts",
                        json=alert_data
                    )

                    print("ALERT CREATED")
                    person_alert_sent = True

                except Exception as e:
                    print("Alert Error:", e)

    annotated_frame = results[0].plot()

    cv2.imshow("GuardianAI Live Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()