from ultralytics import YOLO

model = YOLO("models/yolov8n.pt")

image_path = "test-images/sample.jpg"

print("Running GuardianAI object detection...")
results = model(image_path)

for result in results:
    print("Detected objects:")
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]

        print(f"- {class_name}: {confidence:.2f}")

print("Detection complete.")