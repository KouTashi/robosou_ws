sudo docker run -it --rm -v /dev:/dev --privileged --net=host microros/micro-ros-agent:jazzy serial --dev /dev/ttyUSB0 -v6 &
ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:=/dev/video0 