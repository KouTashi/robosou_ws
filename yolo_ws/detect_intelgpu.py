from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best.pt")  # fast > n s m l x > slow

# Export the model
model.export(format="openvino")  # creates 'yolov8n_openvino_model/'

# Load the exported OpenVINO model
ov_model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best_openvino_model/")

results = ov_model.predict(
    source="0",
    conf=0.5,
    show=True,
)
