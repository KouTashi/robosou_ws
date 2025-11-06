#!/usr/bin/env python3
# coding: UTF-8

# カメラ用無線化ノードの立ち上げコマンド↓
# ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:=/dev/video2

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray

import cv2
import numpy as np
from cv_bridge import CvBridge
from ultralytics import YOLO


class YoloPublisher(Node):
    def __init__(self):
        super().__init__("yolo_publisher")

        # --- Publisher & Subscriber 設定 ---
        self.subscription = self.create_subscription(
            Image, "/image_raw", self.image_callback, qos_profile_sensor_data
        )
        self.publisher_ = self.create_publisher(Int32MultiArray, "cig_pub", 10)

        # --- 画像変換用 CvBridge ---
        self.br = CvBridge()

        # --- YOLO モデル読込（OpenVINO版） ---
        self.get_logger().info("Loading YOLO model...")
        model_path = "/home/dev/robosou_ws/src/yolo_ws/best_openvino_model/"
        self.model = YOLO(model_path)
        self.get_logger().info("YOLO model loaded successfully.")

        # --- 送信用メッセージバッファ ---
        self.msg = Int32MultiArray()

    def image_callback(self, data: Image):
        # ROS Image → OpenCV画像に変換
        frame = self.br.imgmsg_to_cv2(data, "bgr8")

        # --- YOLOv8 推論 ---
        results = self.model.predict(frame, verbose=False, conf=0.6)
        annotated_frame = results[0].plot()

        try:
            self.msg.data = [-1, -1, -1, -1, -1]

            # 最初の検出物体のクラスIDを送信
            if len(results[0].boxes.cls) > 0:
                self.msg.data[0] = int(results[0].boxes.cls[0])

            self.publisher_.publish(self.msg)

        except Exception as e:
            self.get_logger().error(f"YOLO publish error: {e}")
            self.msg.data = [-1, -1, -1, -1, -1]
            self.publisher_.publish(self.msg)

        # --- 結果の表示 ---
        cv2.imshow("YOLOv8 Detection", annotated_frame)
        cv2.waitKey(1)


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
