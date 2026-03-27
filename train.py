from ultralytics import YOLO

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt")

# Train the model on pothole dataset
model.train(
    data="dataset/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16
)
