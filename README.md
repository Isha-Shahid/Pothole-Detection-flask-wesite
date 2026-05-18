RoadGuard AI is an automated, computer vision-driven smart city solution designed to transition municipal road maintenance from a reactive model to a proactive, 
data-driven framework. The system achieves its core objectives by leveraging a high-performance YOLOv8-Nano deep learning architecture fine-tuned on a comprehensive 
multi-class dataset of 6,951 images sourced from Kaggle. This setup allows the system to seamlessly detect structural failures such as potholes and surface cracks 
down to a 0.25 confidence threshold within a swift 0.84-second inference time.

Moving far beyond simple object detection, the project delivers on its advanced objectives by introducing a specialized Proximity-Weighted Hazard Density 
algorithmic layer. This logic establishes a spatial threshold at 60% of the camera's frame height, isolating a foreground "Danger Zone" where immediate structural 
hazards are multiplied by 1.5x. By calculating the total weighted area of these hazards relative to the overall frame, RoadGuard AI derives a road-wide density 
percentage mapped to a responsive, four-tier severity scale (Critical, High, Medium, Low).

To ensure this actionable intelligence is practically accessible, the backend is seamlessly integrated into a decoupled Three-Tier Web Architecture using Flask 
and SQLite. The system processes asymmetric asynchronous image streams via OpenCV, pairs them with real-time geographical metadata extracted using the HTML5 
Geolocation API, and dynamically pins localized damage clusters onto an interactive, municipal map powered by Leaflet.js. This approach successfully addresses a 
critical performance benchmark of a 2.42-second end-to-end pipeline latency, creating a scalable, evidence-based prototype for smart infrastructure oversight in 
Pakistan.
