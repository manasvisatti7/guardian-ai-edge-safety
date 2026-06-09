from ultralytics import YOLO

print("Loading YOLO model from models folder...")

model = YOLO("models/yolov8n.pt")

print("Model loaded successfully from models/yolov8n.pt")
print("GuardianAI AI stack is ready.")