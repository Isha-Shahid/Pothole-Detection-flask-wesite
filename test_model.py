from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train/weights/best.pt")

results = model("test.jpg")

annotated_frame = results[0].plot()

cv2.imshow("Pothole Detection Test", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()