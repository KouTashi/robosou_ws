from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
    #results = model.train(data="https://universe.roboflow.com/ds/gsey9YKqQj?key=IjLpzOJwLp", epochs=500, imgsz=640)
    results = model.train(data="https://universe.roboflow.com/ds/Zbe7ZzBtZ3?key=O3bRLXT1RB", epochs=500, imgsz=640 , device='0') #cudaを使う場合