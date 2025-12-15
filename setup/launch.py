from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="cigrobo_py",
                executable="cig_pub_wl",
                output="screen",
            ),
            Node(
                package="cigrobo",
                executable="yolo_bridge",
                output="screen",
            ),
        ]
    )