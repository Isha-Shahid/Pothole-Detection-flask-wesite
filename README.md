RoadGuard AI: Smart Road Monitoring System

Overview
RoadGuard AI is an intelligent, computer vision-driven system designed for smart city infrastructure monitoring. By utilizing a YOLOv8n deep learning model, it detects potholes in real-time and analyzes the correlation between damage severity and traffic flow disruption.

Key Objectives
*   Detect road surface potholes from surveillance footage using a YOLO-based model.
*   Establish a correlation between pothole severity and traffic flow disruption (speed reduction/flow rate).
*   Store metadata in a relational database to support maintenance planning and trend monitoring.

Technical Stack
*   Language/Framework: Python, Flask
*   AI/ML: YOLOv8n (Ultralytics framework)
*   Tools: OpenCV, SQLite/PostgreSQL
*   Dataset: ~4,150 images (augmented).

Methodology
*   Training: Trained on 100 epochs with a batch size of 16.
*   Evaluation: Assessed using precision, recall, and mean average precision (mAP).
