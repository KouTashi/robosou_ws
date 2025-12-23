

// 標準
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <thread>

// ROS
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"
#include <std_msgs/msg/float32_multi_array.hpp>
// #include "actuator_msg/msg/actuator_msg.hpp"
#include <vector>

#define MC_PRINTF 0 // マイコン側のprintfを無効化・有効化(0 or 1)

std::vector<int16_t> data(18, 0); // マイコンに送信される配列"data"

class YOLO_Listener : public rclcpp::Node {
public:
    YOLO_Listener()
        : Node("yolo_listener") {
        subscription_ = this->create_subscription<std_msgs::msg::Int32MultiArray>(
            "cig_pub", 10,
            std::bind(&YOLO_Listener::yolo_listener_callback, this,
                      std::placeholders::_1));

        publisher_ = this->create_publisher<std_msgs::msg::Int32MultiArray>("to_esp32_1", 10);

        RCLCPP_INFO(this->get_logger(),
                    "YOLO Listener initialized");
    }

private:
    void yolo_listener_callback(const std_msgs::msg::Int32MultiArray::SharedPtr msg) {

        int yolo_state = msg->data[0];

        if (yolo_state == 0) {
            data[1] = 127;
            publish_data();
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
        } else {
            data[1] = 0;
            publish_data();
        }

        // std::cout << data[1] << std::endl;
        RCLCPP_INFO(this->get_logger(),
                    "Published data[1]: %d", data[1]);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    void publish_data() {
        auto msg = std_msgs::msg::Int32MultiArray();
        msg.data.reserve(data.size());
        for (auto &v : data) {
            msg.data.push_back(static_cast<int32_t>(v));
        }
        publisher_->publish(msg);
    }

    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr subscription_;
    rclcpp::Publisher<std_msgs::msg::Int32MultiArray>::SharedPtr publisher_;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);

    rclcpp::executors::SingleThreadedExecutor exec;
    auto yolo_listener = std::make_shared<YOLO_Listener>();
    exec.add_node(yolo_listener);
    exec.spin();

    rclcpp::shutdown();
    return 0;
}