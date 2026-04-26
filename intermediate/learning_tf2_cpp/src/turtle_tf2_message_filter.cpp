// Copyright 2021 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// 标准库头文件
#include <chrono>      // 时间库
#include <memory>       // 智能指针库
#include <string>       // 字符串库

// ROS 2 消息类型
#include "geometry_msgs/msg/point_stamped.hpp"  // 带时间戳的点坐标消息

// message_filters 消息过滤器库
#include "message_filters/subscriber.h"

// ROS 2 C++ 客户端库
#include "rclcpp/rclcpp.hpp"

// TF2 相关头文件
#include "tf2_ros/buffer.h"  // TF2 缓冲区
#include "tf2_ros/create_timer_ros.h"  // 创建定时器接口
#include "tf2_ros/message_filter.h"  // 消息过滤器
#include "tf2_ros/transform_listener.h"  // 变换监听器

// TF2 几何消息转换头文件
#ifdef TF2_CPP_HEADERS
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#else
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#endif

// 使用 std::chrono_literals 命名空间
using namespace std::chrono_literals;

// PoseDrawer 类：继承自 rclcpp::Node
// 功能：使用 TF2 MessageFilter 接收海龟的位置点，并将其转换到目标坐标系
class PoseDrawer : public rclcpp::Node
{
public:
  // 构造函数
  PoseDrawer()
      : Node("turtle_tf2_pose_drawer")  // 调用父类构造函数，设置节点名称
  {
    // 声明并获取 target_frame 参数（目标坐标系，默认是 turtle1）
    target_frame_ = this->declare_parameter<std::string>("target_frame", "turtle1");

    // 设置缓冲区超时时间（秒）
    std::chrono::duration<int> buffer_timeout(1);

    // 创建 TF2 缓冲区
    tf2_buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
    
    // 在调用 waitForTransform 之前创建定时器接口
    // 以避免 tf2_ros::CreateTimerInterfaceException 异常
    auto timer_interface = std::make_shared<tf2_ros::CreateTimerROS>(
        this->get_node_base_interface(),
        this->get_node_timers_interface());
    tf2_buffer_->setCreateTimerInterface(timer_interface);
    
    // 创建 TF2 变换监听器
    tf2_listener_ =
        std::make_shared<tf2_ros::TransformListener>(*tf2_buffer_);

    // 订阅带时间戳的点坐标话题
    point_sub_.subscribe(this, "/turtle3/turtle_point_stamped");
    
    // 创建 TF2 消息过滤器
    // 当目标坐标系可变换时，消息才会被传递到回调函数
    tf2_filter_ = std::make_shared<tf2_ros::MessageFilter<geometry_msgs::msg::PointStamped>>(
        point_sub_,  // 消息订阅器
        *tf2_buffer_,  // TF2 缓冲区
        target_frame_,  // 目标坐标系
        100,  // 队列大小
        this->get_node_logging_interface(),  // 日志接口
        this->get_node_clock_interface(),  // 时钟接口
        buffer_timeout);  // 超时时间
    
    // 注册回调函数，当变换可用时会被调用
    tf2_filter_->registerCallback(&PoseDrawer::msgCallback, this);
  }

private:
  // 消息回调函数
  void msgCallback(const geometry_msgs::msg::PointStamped::SharedPtr point_ptr)
  {
    // 创建输出点消息
    geometry_msgs::msg::PointStamped point_out;
    try
    {
      // 将点从原始坐标系变换到目标坐标系
      tf2_buffer_->transform(*point_ptr, point_out, target_frame_);
      
      // 打印变换后的点坐标
      RCLCPP_INFO(
          this->get_logger(), "Point of turtle3 in frame of turtle1: x:%f y:%f z:%f\n",
          point_out.point.x,
          point_out.point.y,
          point_out.point.z);
    }
    catch (const tf2::TransformException &ex)
    {
      // 打印捕获的异常
      RCLCPP_WARN(
          this->get_logger(), "Failure %s\n", ex.what());
    }
  }

  // 成员变量
  std::string target_frame_;  // 目标坐标系名称
  std::shared_ptr<tf2_ros::Buffer> tf2_buffer_;  // TF2 缓冲区指针
  std::shared_ptr<tf2_ros::TransformListener> tf2_listener_;  // TF2 监听器指针
  message_filters::Subscriber<geometry_msgs::msg::PointStamped> point_sub_;  // 消息订阅器
  std::shared_ptr<tf2_ros::MessageFilter<geometry_msgs::msg::PointStamped>> tf2_filter_;  // 消息过滤器指针
};

// 主函数：程序入口点
int main(int argc, char *argv[])
{
  // 初始化 ROS 2 客户端库
  rclcpp::init(argc, argv);
  
  // 创建 PoseDrawer 节点并 spin（处理回调）
  rclcpp::spin(std::make_shared<PoseDrawer>());
  
  // 关闭 ROS 2 客户端库
  rclcpp::shutdown();
  return 0;
}
