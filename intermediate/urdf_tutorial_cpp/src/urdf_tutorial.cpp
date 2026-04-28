#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <cmath>
#include <thread>
#include <chrono>

using namespace std::chrono;

class StatePublisher : public rclcpp::Node
{
public:
    StatePublisher(rclcpp::NodeOptions options = rclcpp::NodeOptions()) : Node("state_publisher", options)
    {
        joint_pub_ = this->create_publisher<sensor_msgs::msg::JointState>("joint_states", 10);
        // 创建一个发布者，用于告诉 robot_state_publisher 关节状态信息
        // robot_state_publisher 会处理这个变换
        broadcaster = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        // 创建一个广播器，用于告诉 tf2 状态信息
        // 这个广播器会确定坐标系 'axis' 在坐标系 'odom' 中的位置
        RCLCPP_INFO(this->get_logger(), "Starting state publisher");

        loop_rate_ = std::make_shared<rclcpp::Rate>(33ms);

        timer_ = this->create_wall_timer(33ms, std::bind(&StatePublisher::publish, this));
    }

    void publish();

private:
    rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_pub_;
    std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster;
    rclcpp::Rate::SharedPtr loop_rate_;
    rclcpp::TimerBase::SharedPtr timer_;

    // 机器人状态变量
    // degree 表示 1 度
    const double degree = M_PI / 180.0;
    double tilt = 0.;
    double tinc = degree;
    double swivel = 0.;
    double angle = 0.;
    double height = 0.;
    double hinc = 0.005;
};

void StatePublisher::publish()
{
    // 创建必要的消息
    geometry_msgs::msg::TransformStamped t;
    sensor_msgs::msg::JointState joint_state;

    // 添加时间戳
    joint_state.header.stamp = this->get_clock()->now();
    // 指定在 r2d2.urdf.xml 中定义的关芓名称及其内容
    joint_state.name = {"swivel", "tilt", "periscope"};
    joint_state.position = {swivel, tilt, height};

    // 添加时间戳
    t.header.stamp = this->get_clock()->now();
    // 指定父坐标系和子坐标系
    // odom 是 tf2 的基础坐标系
    t.header.frame_id = "odom";
    // axis 在 r2d2.urdf.xml 文件中定义，它是模型的基础坐标系
    t.child_frame_id = "axis";

    // 添加平移变换
    t.transform.translation.x = cos(angle) * 2;
    t.transform.translation.y = sin(angle) * 2;
    t.transform.translation.z = 0.7;
    tf2::Quaternion q;
    // 将欧拉角转换为四元数并添加旋转变换
    q.setRPY(0, 0, angle + M_PI / 2);
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    // 更新下一次的状态
    tilt += tinc;
    if (tilt < -0.5 || tilt > 0.0)
    {
        tinc *= -1;
    }
    height += hinc;
    if (height > 0.2 || height < 0.0)
    {
        hinc *= -1;
    }
    swivel += degree; // 增加 1 度（以弧度为单位）
    angle += degree;  // 以较慢的节奏改变角度

    // 发送消息
    broadcaster->sendTransform(t);
    joint_pub_->publish(joint_state);

    RCLCPP_INFO(this->get_logger(), "Publishing joint state");
}

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<StatePublisher>());
    rclcpp::shutdown();
    return 0;
}