import matplotlib.pyplot as plt
from ultralytics import YOLO

VIDEO_PATH = "/home/dev/robosou_ws/src/yolo_ws/sample/" "PXL_20251223_095850112.mp4"

# =========================
# PyTorch YOLO
# =========================
print("===== PyTorch YOLO inference START =====")
pt_model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best.pt")

pt_inf_times = []
pt_pre_times = []
pt_post_times = []

for frame_idx, r in enumerate(
    pt_model.predict(
        source=VIDEO_PATH,
        stream=True,
        conf=0.5,
        verbose=False,
    )
):
    pre = r.speed["preprocess"]
    inf = r.speed["inference"]
    post = r.speed["postprocess"]

    pt_pre_times.append(pre)
    pt_inf_times.append(inf)
    pt_post_times.append(post)

    print(
        f"[PyTorch] Frame: {frame_idx:5d} | "
        f"pre: {pre:6.2f} ms | "
        f"inf: {inf:6.2f} ms | "
        f"post: {post:6.2f} ms"
    )

print(
    f"===== PyTorch DONE | "
    f"Avg inference: {sum(pt_inf_times)/len(pt_inf_times):.2f} ms/frame =====\n"
)

# =========================
# OpenVINO YOLO
# =========================
print("===== OpenVINO YOLO inference START =====")

# Load a YOLOv8n PyTorch model
model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best.pt")  # fast > n s m l x > slow

# Export the model
model.export(format="openvino")  # creates 'yolov8n_openvino_model/'

# Load the exported OpenVINO model
ov_model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best_openvino_model/")

ov_inf_times = []
ov_pre_times = []
ov_post_times = []

for frame_idx, r in enumerate(
    ov_model.predict(
        source=VIDEO_PATH,
        stream=True,
        conf=0.5,
        verbose=False,
    )
):
    pre = r.speed["preprocess"]
    inf = r.speed["inference"]
    post = r.speed["postprocess"]

    ov_pre_times.append(pre)
    ov_inf_times.append(inf)
    ov_post_times.append(post)

    print(
        f"[OpenVINO] Frame: {frame_idx:5d} | "
        f"pre: {pre:6.2f} ms | "
        f"inf: {inf:6.2f} ms | "
        f"post: {post:6.2f} ms"
    )

print(
    f"===== OpenVINO DONE | "
    f"Avg inference: {sum(ov_inf_times)/len(ov_inf_times):.2f} ms/frame =====\n"
)

# =========================
# グラフ描画（inferenceのみ）
# =========================
plt.figure(figsize=(10, 5))
plt.plot(pt_inf_times, label="PyTorch (CPU)", linewidth=1)
plt.plot(ov_inf_times, label="OpenVINO (iGPU)", linewidth=1)
plt.xlabel("Frame Number")
plt.ylabel("Inference Time [ms]")
plt.title("YOLO Inference Time Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
