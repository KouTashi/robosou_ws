from ultralytics import YOLO

model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best_m.pt")  # fast > n s m l x > slow

results = model.predict(
    source="2",
    show=True,
)
