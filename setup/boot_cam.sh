#ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:=/dev/video0 
ros2 run usb_cam usb_cam_node_exe \
  --ros-args \
  -p video_device:=/dev/video0 \
  -p pixel_format:=yuyv \
  -p io_method:=mmap
