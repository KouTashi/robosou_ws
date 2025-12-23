from ultralytics import YOLO

model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best.pt")  # fast > n s m l x > slow

results = model.predict(
    source="/home/dev/robosou_ws/src/yolo_ws/sample/Screencast from 2025-10-09 11-41-59.webm",
    show=True,
)
