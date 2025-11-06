#!/usr/bin/env python3
# coding: UTF-8

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CompressedImage  # ← CompressedImageに変更
from std_msgs.msg import Int32MultiArray

import cv2
import numpy as np
from ultralytics import YOLO


class YoloPublisher(Node):
    def __init__(self):
        super().__init__("yolo_publisher")

        # --- Publisher & Subscriber 設定 ---
        self.subscription = self.create_subscription(
            CompressedImage,  # ← ここを CompressedImage に変更
            "/image_raw/compressed",
            self.image_callback,
            qos_profile_sensor_data,
        )
        self.publisher_ = self.create_publisher(Int32MultiArray, "cig_pub", 10)

        # --- YOLO モデル読込（OpenVINO版） ---
        self.get_logger().info("Loading YOLO model...")
        model_path = "/home/dev/robosou_ws/src/yolo_ws/best_openvino_model/"
        self.model = YOLO(model_path)
        self.get_logger().info("YOLO model loaded successfully.")

        # --- 送信用メッセージバッファ ---
        self.msg = Int32MultiArray()

    def image_callback(self, data: CompressedImage):
        try:
            # CompressedImage → OpenCV画像に変換
            np_arr = np.frombuffer(data.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                self.get_logger().warn("Failed to decode compressed image.")
                return

            # --- YOLOv8 推論 ---
            results = self.model.predict(frame, verbose=False, conf=0.75)
            annotated_frame = results[0].plot()

            # --- 結果の送信 ---
            self.msg.data = [-1, -1, -1, -1, -1]

            # 最初の検出物体のクラスIDを送信
            if len(results[0].boxes.cls) > 0:
                self.msg.data[0] = int(results[0].boxes.cls[0])

            self.publisher_.publish(self.msg)

            # --- 結果の表示 ---
            cv2.imshow("YOLOv8 Detection", annotated_frame)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"YOLO callback error: {e}")
            self.msg.data = [-1, -1, -1, -1, -1]
            self.publisher_.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)
    node = YoloPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
