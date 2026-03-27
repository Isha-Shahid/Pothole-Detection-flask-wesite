import cv2
from ultralytics import YOLO

# 1. Load your custom trained model
# Replace with the actual path to your best.pt
model = YOLO("runs/detect/train/weights/best.pt")

# 2. Load the image
image_path = "download.jpg"
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not find image at {image_path}")
else:
    h, w, _ = img.shape
    total_frame_area = h * w

    # Define the Danger Zone line (60% down the image)
    danger_line_y = int(h * 0.6)

    # 3. Run Inference
    # Adjust conf to catch more/fewer potholes
    results = model(img, conf=0.25)

    total_weighted_area = 0
    pothole_count = 0

    # 4. Process Detections
    for result in results:
        for box in result.boxes:
            pothole_count += 1
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Calculate box area
            box_area = (x2 - x1) * (y2 - y1)

            # PROXIMITY WEIGHTING Logic
            if y2 > danger_line_y:
                # Pothole is in the Danger Zone (Immediate Risk)
                total_weighted_area += box_area * 1.5
                box_color = (0, 0, 255)  # Red box for close potholes
            else:
                # Pothole is in the distance
                total_weighted_area += box_area
                box_color = (0, 255, 0)  # Green box for distant potholes

            # Draw individual bounding boxes
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), box_color, 2)

    # 5. Calculate Road-Wide Hazard Density (%)
    hazard_density = (total_weighted_area / total_frame_area) * 100

    # 6. Severity & Congestion Logic
    if hazard_density > 15:
        status, color = "CRITICAL: HIGH CONGESTION", (0, 0, 255)  # Red
    elif hazard_density > 7:
        status, color = "HIGH: TRAFFIC SLOWDOWN", (0, 165, 255)  # Orange
    elif hazard_density > 3:
        status, color = "MEDIUM: CAUTION", (0, 255, 255)  # Yellow
    else:
        status, color = "LOW: MINIMAL IMPACT", (0, 255, 0)  # Green

    # 7. FINAL UI OVERLAY (Fixed Overlap)
    # Draw Danger Zone Line
    cv2.line(img, (0, danger_line_y), (w, danger_line_y), (255, 255, 0), 2)
    cv2.putText(img, "DANGER ZONE (WEIGHTED)", (10, danger_line_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

    # Create a translucent black header bar (Tall enough for 3 lines)
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (w, 130), (0, 0, 0), -1)
    img = cv2.addWeighted(overlay, 0.7, img, 0.3, 0)

    # Text Placement (Vertically Stacked)
    # Line 1: Road Status
    cv2.putText(img, f"STATUS: {status}", (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Line 2: Hazard Density
    cv2.putText(img, f"Hazard Density: {hazard_density:.1f}%", (15, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Line 3: Potholes Detected
    cv2.putText(img, f"Potholes Detected: {pothole_count}", (15, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # 8. Show and Save
    cv2.imshow("Whole Road Severity Analysis", img)
    cv2.imwrite("pothole_analysis_report.jpg", img)

    print(f"Report: {pothole_count} potholes. Density: {hazard_density:.2f}%")

    cv2.waitKey(0)
    cv2.destroyAllWindows()