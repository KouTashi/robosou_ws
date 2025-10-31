from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best_m.pt")  # fast > n s m l x > slow

# Export the model
model.export(format="openvino")  # creates 'yolov8n_openvino_model/'

# Load the exported OpenVINO model
ov_model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best_openvino_model/")

results = ov_model.predict(
    source="2",
    conf=0.5,
    show=True,
)

# results = ov_model.predict(
#     source="/home/dev/robosou_ws/src/yolo_ws/sample/Screencast from 2025-10-09 11-41-59.webm",
#     conf=0.5,
#     show=True,
# )
