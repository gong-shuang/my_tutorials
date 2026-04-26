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
#include <functional>  // 函数库，用于 std::bind
#include <memory>      // 智能指针库
#include <sstream>     // 字符串流库
#include <string>      // 字符串库

// ROS 2 消息类型
#include "geometry_msgs/msg/transform_stamped.hpp"  // 坐标变换消息类型

// ROS 2 C++ 客户端库
#include "rclcpp/rclcpp.hpp"

// TF2 四元数数学库
#include "tf2/LinearMath/Quaternion.h"

// TF2 坐标变换广播器
#include "tf2_ros/transform_broadcaster.h"

// turtlesim 海龟位置消息
#include "turtlesim/msg/pose.hpp"

// FramePublisher 类：继承自 rclcpp::Node
// 功能：订阅海龟的位置话题，并将海龟的位置信息广播为 TF2 坐标变换
class FramePublisher : public rclcpp::Node
{
public:
  // 构造函数
  FramePublisher()
  : Node("turtle_tf2_frame_publisher")  // 调用父类构造函数，设置节点名称
  {
    // 声明并获取 turtlename 参数（默认值是 "turtle"）
    turtlename_ = this->declare_parameter<std::string>("turtlename", "turtle");

    // 初始化 TF2 变换广播器
    tf_broadcaster_ =
      std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    // 订阅海龟位置话题，并在收到消息时调用 handle_turtle_pose 回调函数
    // 构建话题名称："/turtle1/pose" 或 "/turtle2/pose"
    std::ostringstream stream;
    stream << "/" << turtlename_.c_str() << "/pose";
    std::string topic_name = stream.str();

    // 定义处理海龟位置的回调函数
    auto handle_turtle_pose = [this](const std::shared_ptr<turtlesim::msg::Pose> msg) {
        // 创建坐标变换消息
        geometry_msgs::msg::TransformStamped t;

        // 读取消息内容并赋值给对应的 TF 变量
        t.header.stamp = this->get_clock()->now();  // 设置时间戳
        t.header.frame_id = "world";  // 父坐标系是 world
        t.child_frame_id = turtlename_.c_str();  // 子坐标系是海龟名称

        // 海龟只存在于 2D 平面，因此只获取 x 和 y 的平移坐标
        // z 坐标设置为 0
        t.transform.translation.x = msg->x;
        t.transform.translation.y = msg->y;
        t.transform.translation.z = 0.0;

        // 同样，海龟只能绕一个轴旋转
        // 因此将 x 和 y 的旋转分量设置为 0，只从消息中获取 z 轴的旋转角度
        tf2::Quaternion q;
        q.setRPY(0, 0, msg->theta);  // 设置欧拉角（roll=0, pitch=0, yaw=theta）
        
        // 设置四元数的四个分量
        t.transform.rotation.x = q.x();
        t.transform.rotation.y = q.y();
        t.transform.rotation.z = q.z();
        t.transform.rotation.w = q.w();

        // 发送坐标变换
        tf_broadcaster_->sendTransform(t);
      };
    
    // 创建订阅者
    subscription_ = this->create_subscription<turtlesim::msg::Pose>(
      topic_name,  // 话题名称
      10,  // 队列大小
      handle_turtle_pose);  // 回调函数
  }

private:
  // 成员变量
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_;  // 订阅者指针
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;  // TF2 广播器指针（独占拥有权）
  std::string turtlename_;  // 海龟名称
};

// 主函数：程序入口点
int main(int argc, char * argv[])
{
  // 初始化 ROS 2 客户端库
  rclcpp::init(argc, argv);
  
  // 创建 FramePublisher 节点并 spin（处理回调）
  rclcpp::spin(std::make_shared<FramePublisher>());
  
  // 关闭 ROS 2 客户端库
  rclcpp::shutdown();
  return 0;
}
