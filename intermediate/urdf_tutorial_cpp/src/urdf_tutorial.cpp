/**
 * @file urdf_tutorial.cpp
 * @brief 状态发布器节点实现
 * 
 * 该节点负责发布机器人的关节状态和TF坐标变换，用于URDF模型的可视化演示。
 * 主要功能：
 * 1. 发布关节状态到 /joint_states 话题
 * 2. 发布TF变换到 /tf 话题
 * 3. 模拟机器人关节的周期性运动
 */

#include <rclcpp/rclcpp.hpp>                          // ROS 2 C++ 核心库
#include <geometry_msgs/msg/quaternion.hpp>           // 四元数消息类型
#include <sensor_msgs/msg/joint_state.hpp>            // 关节状态消息类型
#include <tf2_ros/transform_broadcaster.h>            // TF2 变换广播器
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>    // TF2 几何消息转换
#include <cmath>                                      // 数学函数库
#include <thread>                                     // 线程支持
#include <chrono>                                     // 时间支持

using namespace std::chrono;

/**
 * @class StatePublisher
 * @brief 状态发布器类，继承自 rclcpp::Node
 * 
 * 该类实现了一个ROS 2节点，用于发布机器人关节状态和TF坐标变换。
 * 通过定时器周期性更新并发布状态信息，模拟机器人的运动。
 */
class StatePublisher : public rclcpp::Node
{
public:
    /**
     * @brief 构造函数，初始化节点
     * @param options 节点选项参数
     */
    StatePublisher(rclcpp::NodeOptions options = rclcpp::NodeOptions()) : Node("state_publisher", options)
    {
        // 创建关节状态发布者，话题名称为 "joint_states"，队列大小为10
        joint_pub_ = this->create_publisher<sensor_msgs::msg::JointState>("joint_states", 10);
        
        // 创建TF变换广播器，用于发布坐标系变换信息
        broadcaster = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        
        // 输出日志信息，表示节点已启动
        RCLCPP_INFO(this->get_logger(), "Starting state publisher");

        // 创建速率对象，控制发布频率约为30Hz (33ms)
        loop_rate_ = std::make_shared<rclcpp::Rate>(33ms);

        // 创建定时器，每33ms调用一次publish()方法
        timer_ = this->create_wall_timer(33ms, std::bind(&StatePublisher::publish, this));
    }

    /**
     * @brief 发布方法，周期性调用
     * 
     * 该方法负责：
     * 1. 更新关节状态消息
     * 2. 更新TF变换消息
     * 3. 发布消息到相应话题
     * 4. 更新机器人状态变量，实现周期性运动
     */
    void publish();

private:
    // 成员变量声明
    
    /**
     * @brief 关节状态发布者指针
     * 用于发布 sensor_msgs::msg::JointState 类型消息到 /joint_states 话题
     */
    rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_pub_;
    
    /**
     * @brief TF变换广播器指针
     * 用于发布 tf2_msgs::msg::TFMessage 类型消息到 /tf 话题
     */
    std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster;
    
    /**
     * @brief 循环速率控制对象
     * 用于控制发布频率
     */
    rclcpp::Rate::SharedPtr loop_rate_;
    
    /**
     * @brief 定时器对象
     * 用于周期性触发 publish() 方法
     */
    rclcpp::TimerBase::SharedPtr timer_;

    // 机器人状态变量
    
    /**
     * @brief 角度转换因子，将角度转换为弧度
     * degree = π / 180.0，即1度对应的弧度值
     */
    const double degree = M_PI / 180.0;
    
    /**
     * @brief 倾斜角度（弧度）
     * 控制机器人头部的倾斜角度
     */
    double tilt = 0.;
    
    /**
     * @brief 倾斜角度增量（弧度）
     * 每次循环的倾斜角度变化量
     */
    double tinc = degree;
    
    /**
     * @brief 旋转角度（弧度）
     * 控制机器人头部的旋转角度
     */
    double swivel = 0.;
    
    /**
     * @brief 整体旋转角度（弧度）
     * 控制整个机器人在平面上的圆周运动角度
     */
    double angle = 0.;
    
    /**
     * @brief 高度位置（米）
     * 控制机器人潜望镜的伸缩高度
     */
    double height = 0.;
    
    /**
     * @brief 高度增量（米）
     * 每次循环的高度变化量
     */
    double hinc = 0.005;
};

/**
 * @brief StatePublisher::publish() 方法实现
 * 
 * 该方法执行以下步骤：
 * 1. 创建关节状态消息和TF变换消息
 * 2. 设置消息的时间戳
 * 3. 填充关节状态数据（关节名称和位置）
 * 4. 填充TF变换数据（平移和旋转）
 * 5. 更新机器人状态变量，实现周期性运动
 * 6. 发布关节状态和TF变换消息
 */
void StatePublisher::publish()
{
    // 创建TF变换消息和关节状态消息
    geometry_msgs::msg::TransformStamped t;
    sensor_msgs::msg::JointState joint_state;

    // 设置关节状态消息的时间戳为当前时间
    joint_state.header.stamp = this->get_clock()->now();
    
    // 设置关节名称列表，对应URDF中定义的关节
    // swivel: 旋转关节，tilt: 倾斜关节，periscope: 升降关节
    joint_state.name = {"swivel", "tilt", "periscope"};
    
    // 设置关节位置值，顺序与关节名称对应
    joint_state.position = {swivel, tilt, height};

    // 设置TF变换消息的时间戳为当前时间
    t.header.stamp = this->get_clock()->now();
    
    // 设置TF变换的父坐标系为 "odom"（里程计坐标系）
    t.header.frame_id = "odom";
    
    // 设置TF变换的子坐标系为 "axis"（机器人基座坐标系）
    t.child_frame_id = "axis";

    // 设置平移变换：机器人在半径为2的圆周上运动
    t.transform.translation.x = cos(angle) * 2;  // X坐标：cos(angle) * 半径
    t.transform.translation.y = sin(angle) * 2;  // Y坐标：sin(angle) * 半径
    t.transform.translation.z = 0.7;             // Z坐标：固定高度0.7米
    
    // 创建四元数对象，用于表示旋转变换
    tf2::Quaternion q;
    
    // 将欧拉角(roll, pitch, yaw)转换为四元数
    // roll=0, pitch=0, yaw=angle+π/2（初始方向偏移90度）
    q.setRPY(0, 0, angle + M_PI / 2);
    
    // 将四元数值赋值给TF变换消息
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    // 更新机器人状态变量，实现周期性运动
    
    // 更新倾斜角度，在[-0.5, 0.0]弧度范围内来回摆动
    tilt += tinc;
    if (tilt < -0.5 || tilt > 0.0)
    {
        tinc *= -1;  // 到达边界时反转方向
    }
    
    // 更新高度，在[0.0, 0.2]米范围内来回伸缩
    height += hinc;
    if (height > 0.2 || height < 0.0)
    {
        hinc *= -1;  // 到达边界时反转方向
    }
    
    // 更新旋转角度，每次增加1度（转换为弧度）
    swivel += degree;
    
    // 更新整体圆周运动角度，每次增加1度（转换为弧度）
    angle += degree;

    // 发布TF变换消息到 /tf 话题
    broadcaster->sendTransform(t);
    
    // 发布关节状态消息到 /joint_states 话题
    joint_pub_->publish(joint_state);

    // 输出日志信息，表示关节状态已发布
    RCLCPP_INFO(this->get_logger(), "Publishing joint state");
}

/**
 * @brief 主函数，程序入口
 * @param argc 命令行参数数量
 * @param argv 命令行参数数组
 * @return 程序退出码
 */
int main(int argc, char *argv[])
{
    // 初始化 ROS 2 节点
    rclcpp::init(argc, argv);
    
    // 创建 StatePublisher 节点并进入自旋循环
    rclcpp::spin(std::make_shared<StatePublisher>());
    
    // 关闭 ROS 2 节点
    rclcpp::shutdown();
    
    return 0;
}