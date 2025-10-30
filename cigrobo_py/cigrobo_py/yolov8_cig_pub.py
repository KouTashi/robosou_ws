#!/usr/bin/env python3
## coding: UTF-8

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

import cv2
import numpy as np
from ultralytics import YOLO


# Load the YOLOv8 model
model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best.pt")  # 絶対パス
# Export the model
model.export(format="openvino")  # creates 'yolov8n_openvino_model/'
# Load the exported OpenVINO model
ov_model = YOLO("/home/dev/robosou_ws/src/yolo_ws/best_openvino_model/")  # 絶対パス

# Webカメラの設定
cap = cv2.VideoCapture(2)  # builtin_cam:0 ext_cam:2
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 16)
# cap.set(cv2.CAP_PROP_EXPOSURE, -16)  # 0 ~ -16

msg = Int32MultiArray()


class Cig_Pub(Node):

    def __init__(self):
        super().__init__("cig_pub")
        self.publisher_ = self.create_publisher(Int32MultiArray, "cig_pub", 10)
        freq = 0.00000001  # seconds
        self.timer = self.create_timer(freq, self.timer_callback)
        # self.i = 0

    def timer_callback(self):  # callback for publishing setoshio data

        # >>>>>>>>>>>>>>>>>>>>>>Write your code from here>>>>>>>>>>>>>>>>>>>>>>#
        # callbacked every freq[s]

        # -------------------------YOLOv8-------------------------#
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            # frame = cv2.convertScaleAbs(frame, alpha=0.2,beta=0)#画像の調整
            results = ov_model.predict(
                frame, verbose=False, conf=0.6
            )  # verbose: Option for show output to terminal
            annotatedFrame = results[0].plot()

            # cls_and_box = list(zip(np.int32(results[0].boxes.cls), np.int32(results[0].boxes.xyxy)))
            try:

                # -------------------------Publish-------------------------#
                msg.data = [-1, -1, -1, -1, -1]

                msg.data[0] = np.int32(results[0].boxes.cls[0])

                # msg.data = cls_and_x1_sorted
                self.publisher_.publish(msg)

                # self.get_logger().info('Publishing: "%s"' % msg)

                # -------------------------End-------------------------#

                # print(str(cls_and_x1_sorted))
            except IndexError as e:  # To avoid IndexError stops program
                # print(e)
                msg.data = [-1, -1, -1, -1, -1]
                self.publisher_.publish(msg)

            cv2.imshow("YOLOv8", annotatedFrame)
            # print(str(results[0].boxes))

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                # Release the video capture object and close the display window
                cap.release()
                cv2.destroyAllWindows()
                # break

        # -------------------------End-------------------------#

        # >>>>>>>>>>>>>>>>>>>>>>End>>>>>>>>>>>>>>>>>>>>>>#


def main(args=None):
    rclpy.init(args=args)
    cig_pub = Cig_Pub()
    rclpy.spin(cig_pub)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    cig_pub.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
