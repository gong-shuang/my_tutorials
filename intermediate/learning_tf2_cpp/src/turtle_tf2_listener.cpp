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
#include <functional>   // 函数库
#include <memory>       // 智能指针库
#include <string>       // 字符串库

// ROS 2 消息类型
#include "geometry_msgs/msg/transform_stamped.hpp"  // 坐标变换消息
#include "geometry_msgs/msg/twist.hpp"  // 速度命令消息

// ROS 2 C++ 客户端库
#include "rclcpp/rclcpp.hpp"

// TF2 异常
#include "tf2/exceptions.h"

// TF2 监听器和缓冲区
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"

// turtlesim 生成海龟服务
#include "turtlesim/srv/spawn.hpp"

// 使用 std::chrono_literals 命名空间
using namespace std::chrono_literals;

// FrameListener 类：继承自 rclcpp::Node
// 功能：
// 1. 监听 TF2 坐标变换
// 2. 调用服务生成第二只海龟
// 3. 根据坐标变换计算速度命令，使第二只海龟追向第一只海龟
class FrameListener : public rclcpp::Node
{
public:
  // 构造函数
  FrameListener()
      : Node("turtle_tf2_frame_listener"),  // 调用父类构造函数
        turtle_spawning_service_ready_(false),  // 初始化：服务未就绪
        turtle_spawned_(false)  // 初始化：海龟未生成
  {
    // 声明并获取 target_frame 参数（目标坐标系，默认是 turtle1）
    target_frame_ = this->declare_parameter<std::string>("target_frame", "turtle1");

    // 创建 TF2 缓冲区
    tf_buffer_ =
        std::make_unique<tf2_ros::Buffer>(this->get_clock());
    // 创建 TF2 监听器
    tf_listener_ =
        std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

    // 创建生成海龟的服务客户端
    spawner_ =
        this->create_client<turtlesim::srv::Spawn>("spawn");

    // 创建 turtle2 的速度命令发布者
    publisher_ =
        this->create_publisher<geometry_msgs::msg::Twist>("turtle2/cmd_vel", 1);

    // 创建定时器，每秒调用一次 on_timer 函数
    timer_ = this->create_wall_timer(
        1s, [this]()
        { return this->on_timer(); });
  }

private:
  // 定时器回调函数
  void on_timer()
  {
    // 将坐标系名称存储在变量中
    std::string fromFrameRel = target_frame_.c_str();  // 源坐标系（目标海龟）
    std::string toFrameRel = "turtle2";  // 目标坐标系（追击海龟）

    // 如果服务就绪
    if (turtle_spawning_service_ready_)
    {
      // 如果海龟已生成
      if (turtle_spawned_)
      {
        geometry_msgs::msg::TransformStamped t;

        // 查询坐标变换：从 target_frame 到 turtle2 的变换
        // 并发送速度命令使 turtle2 到达 target_frame
        try
        {
          //1. 正常，turtle2紧跟着turtle1
          // t = tf_buffer_->lookupTransform(
          //   toFrameRel,
          //   fromFrameRel,
          //   tf2::TimePointZero); //时间 0 表示缓冲区中“最新可用”的变换

          //2. 获取当前时间的变换，不正常，终端会一直提示：请求变换的时间比最新数据的时间还要新，即数据位于未来，故要等几毫米才能收到信息
          // rclcpp::Time now = this->get_clock()->now();
          // t = tf_buffer_->lookupTransform(
          //   toFrameRel,
          //   fromFrameRel,
          //   now);

          //3. 通过添加超时参数来解决上面的问题
          // rclcpp::Time now = this->get_clock()->now();
          // t = tf_buffer_->lookupTransform(
          //   toFrameRel,
          //   fromFrameRel,
          //   now,
          //   50ms);

          //4. 时间旅行，获取 5 秒前的变换，不正常，原因没有指定固定不变的参考坐标系，导致坐标变换总在漂移
          // rclcpp::Time when = this->get_clock()->now() - rclcpp::Duration(5, 0);
          // t = tf_buffer_->lookupTransform(
          //     toFrameRel, fromFrameRel,  // 目标坐标系，源坐标系
          //     when, 100ms);  // 查询时间，超时时间

          //5. （正确的设置）时间旅行，获取5秒钱的变换，运行正常。
          rclcpp::Time now = this->get_clock()->now();
          rclcpp::Time when = now - rclcpp::Duration(5, 0);
          t = tf_buffer_->lookupTransform(
              toFrameRel,
              now,
              fromFrameRel,
              when,
              "world",
              50ms);
        }
        catch (const tf2::TransformException &ex)
        {
          // 如果查询失败，打印错误信息
          RCLCPP_INFO(
              this->get_logger(), "Could not transform %s to %s: %s",
              toFrameRel.c_str(), fromFrameRel.c_str(), ex.what());
          return;
        }

        // 创建速度命令消息
        geometry_msgs::msg::Twist msg;

        // 计算角速度：使 turtle2 朝向 target_frame
        static const double scaleRotationRate = 1.0;  // 旋转速度缩放因子
        msg.angular.z = scaleRotationRate * atan2(
                                                t.transform.translation.y,
                                                t.transform.translation.x);

        // 计算线速度：使 turtle2 向 target_frame 移动
        static const double scaleForwardSpeed = 0.5;  // 前进速度缩放因子
        msg.linear.x = scaleForwardSpeed * sqrt(
                                               pow(t.transform.translation.x, 2) +
                                               pow(t.transform.translation.y, 2));

        // 发布速度命令
        publisher_->publish(msg);
      }
      else
      {
        // 海龟生成成功
        RCLCPP_INFO(this->get_logger(), "Successfully spawned");
        turtle_spawned_ = true;
      }
    }
    else
    {
      // 检查服务是否就绪
      if (spawner_->service_is_ready())
      {
        // 初始化请求消息
        auto request = std::make_shared<turtlesim::srv::Spawn::Request>();
        request->x = 3.544445;  // 海龟初始 x 坐标
        request->y = 5.544445;  // 海龟初始 y 坐标
        request->theta = 0.0;  // 海龟初始朝向角度
        request->name = "turtle2";  // 海龟名称

        // 发送服务请求
        using ServiceResponseFuture =
            rclcpp::Client<turtlesim::srv::Spawn>::SharedFuture;
        auto response_received_callback = [this](ServiceResponseFuture future)
        {
          auto result = future.get();
          // 检查返回结果是否匹配
          if (strcmp(result->name.c_str(), "turtle2") == 0)
          {
            turtle_spawning_service_ready_ = true;  // 服务就绪
          }
          else
          {
            RCLCPP_ERROR(this->get_logger(), "Service callback result mismatch");
          }
        };
        auto result = spawner_->async_send_request(request, response_received_callback);
      }
      else
      {
        RCLCPP_INFO(this->get_logger(), "Service is not ready");
      }
    }
  }

  // 成员变量
  bool turtle_spawning_service_ready_;  // 海龟生成服务是否就绪
  bool turtle_spawned_;  // 海龟是否已生成
  rclcpp::Client<turtlesim::srv::Spawn>::SharedPtr spawner_;  // 服务客户端指针
  rclcpp::TimerBase::SharedPtr timer_;  // 定时器指针
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;  // 发布者指针
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;  // TF2 监听器指针
  std::unique_ptr<tf2_ros::Buffer> tf_buffer_;  // TF2 缓冲区指针
  std::string target_frame_;  // 目标坐标系名称
};

// 主函数：程序入口点
int main(int argc, char *argv[])
{
  // 初始化 ROS 2 客户端库
  rclcpp::init(argc, argv);
  
  // 创建 FrameListener 节点并 spin（处理回调）
  rclcpp::spin(std::make_shared<FrameListener>());
  
  // 关闭 ROS 2 客户端库
  rclcpp::shutdown();
  return 0;
}
