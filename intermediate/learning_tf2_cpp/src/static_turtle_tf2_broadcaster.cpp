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
#include <memory>  // 智能指针库

// ROS 2 消息类型
#include "geometry_msgs/msg/transform_stamped.hpp"  // 坐标变换消息类型

// ROS 2 C++ 客户端库
#include "rclcpp/rclcpp.hpp"

// TF2 四元数数学库
#include "tf2/LinearMath/Quaternion.h"

// TF2 静态坐标变换广播器
#include "tf2_ros/static_transform_broadcaster.h"

// StaticFramePublisher 类：继承自 rclcpp::Node
// 功能：广播一个静态坐标变换（只广播一次，不会随时间变化）
class StaticFramePublisher : public rclcpp::Node
{
public:
  // 构造函数，接收命令行参数
  explicit StaticFramePublisher(char * transformation[])
  : Node("static_turtle_tf2_broadcaster")  // 调用父类构造函数，设置节点名称
  {
    // 创建 TF2 静态变换广播器
    tf_static_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    // 在启动时发布一次静态变换
    this->make_transforms(transformation);
  }

private:
  // 创建并发送坐标变换
  void make_transforms(char * transformation[])
  {
    // 创建坐标变换消息
    geometry_msgs::msg::TransformStamped t;

    // 设置时间戳
    t.header.stamp = this->get_clock()->now();
    // 设置父坐标系（参考坐标系）
    t.header.frame_id = "world";
    // 设置子坐标系（从命令行参数获取）
    t.child_frame_id = transformation[1];

    // 设置坐标变换的平移分量（从命令行参数获取）
    t.transform.translation.x = atof(transformation[2]);  // x 坐标
    t.transform.translation.y = atof(transformation[3]);  // y 坐标
    t.transform.translation.z = atof(transformation[4]);  // z 坐标

    // 设置坐标变换的旋转分量（使用四元数）
    // 将欧拉角（roll, pitch, yaw）转换为四元数
    tf2::Quaternion q;
    q.setRPY(
      atof(transformation[5]),  // roll（绕 x 轴旋转）
      atof(transformation[6]),  // pitch（绕 y 轴旋转）
      atof(transformation[7]));  // yaw（绕 z 轴旋转）
    
    // 设置四元数的四个分量
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    // 发送静态坐标变换
    tf_static_broadcaster_->sendTransform(t);
  }

  // 成员变量
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_static_broadcaster_;  // TF2 静态广播器指针
};

// 主函数：程序入口点
int main(int argc, char * argv[])
{
  // 获取日志记录器
  auto logger = rclcpp::get_logger("logger");

  // 从命令行参数获取变换参数
  // 期望的参数格式：
  // ros2 run learning_tf2_cpp static_turtle_tf2_broadcaster child_frame_name x y z roll pitch yaw
  if (argc != 8) {
    // 参数数量不正确，打印使用说明
    RCLCPP_INFO(
      logger, "Invalid number of parameters\nusage: "
      "$ ros2 run learning_tf2_cpp static_turtle_tf2_broadcaster "
      "child_frame_name x y z roll pitch yaw");
    return 1;
  }

  // 由于变换的父坐标系是 'world'，需要检查传入的子坐标系名称不能是 'world'
  if (strcmp(argv[1], "world") == 0) {
    RCLCPP_INFO(logger, "Your static turtle name cannot be 'world'");
    return 2;
  }

  // 初始化 ROS 2 客户端库
  rclcpp::init(argc, argv);
  
  // 创建 StaticFramePublisher 节点并 spin（处理回调）
  rclcpp::spin(std::make_shared<StaticFramePublisher>(argv));
  
  // 关闭 ROS 2 客户端库
  rclcpp::shutdown();
  return 0;
}
