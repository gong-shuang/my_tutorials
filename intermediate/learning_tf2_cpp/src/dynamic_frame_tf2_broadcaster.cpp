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
#include <chrono>      // 时间库，用于 duration
#include <functional>   // 函数库，用于 std::bind
#include <memory>       // 智能指针库

// ROS 2 消息类型
#include "geometry_msgs/msg/transform_stamped.hpp"  // 坐标变换消息类型

// ROS 2 C++ 客户端库
#include "rclcpp/rclcpp.hpp"

// TF2 坐标变换广播器
#include "tf2_ros/transform_broadcaster.h"

// 使用 std::chrono_literals 命名空间，允许使用 1s, 100ms 等字面量
using namespace std::chrono_literals;

// 定义圆周率常量
const double PI = 3.141592653589793238463;

// DynamicFrameBroadcaster 类：继承自 rclcpp::Node
// 功能：广播一个相对于 turtle1 坐标系不断变化的 carrot1 坐标系
class DynamicFrameBroadcaster : public rclcpp::Node
{
public:
  // 构造函数
  DynamicFrameBroadcaster()
  : Node("dynamic_frame_tf2_broadcaster")  // 调用父类构造函数，设置节点名称
  {
    // 创建 TF2 变换广播器
    tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    
    // 创建定时器，每 100 毫秒调用一次广播回调函数
    timer_ = this->create_wall_timer(
      100ms, std::bind(&DynamicFrameBroadcaster::broadcast_timer_callback, this));
  }

private:
  // 广播定时器回调函数
  void broadcast_timer_callback()
  {
    // 获取当前时间
    rclcpp::Time now = this->get_clock()->now();
    // 计算角度：使用时间的秒数乘以 PI
    double x = now.seconds() * PI;

    // 创建坐标变换消息
    geometry_msgs::msg::TransformStamped t;
    // 设置时间戳
    t.header.stamp = now;
    // 设置父坐标系（参考坐标系）
    t.header.frame_id = "turtle1";
    // 设置子坐标系（要广播的坐标系）
    t.child_frame_id = "carrot1";
    
    // 设置坐标变换的平移分量
    // 使用 sin 和 cos 函数使 carrot1 相对于 turtle1 做圆周运动
    // 运动半径为 10 个单位
    t.transform.translation.x = 10 * sin(x);
    t.transform.translation.y = 10 * cos(x);
    t.transform.translation.z = 0.0;
    
    // 设置坐标变换的旋转分量（四元数）
    // 这里设置为无旋转（单位四元数）
    t.transform.rotation.x = 0.0;
    t.transform.rotation.y = 0.0;
    t.transform.rotation.z = 0.0;
    t.transform.rotation.w = 1.0;

    // 发送坐标变换
    tf_broadcaster_->sendTransform(t);
  }

  // 成员变量
  rclcpp::TimerBase::SharedPtr timer_;  // 定时器指针
  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;  // TF2 广播器指针
};

// 主函数：程序入口点
int main(int argc, char * argv[])
{
  // 初始化 ROS 2 客户端库
  rclcpp::init(argc, argv);
  
  // 创建 DynamicFrameBroadcaster 节点并 spin（处理回调）
  rclcpp::spin(std::make_shared<DynamicFrameBroadcaster>());
  
  // 关闭 ROS 2 客户端库
  rclcpp::shutdown();
  return 0;
}
