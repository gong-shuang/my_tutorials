# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 从 geometry_msgs 包导入 PointStamped 消息类型
# PointStamped 用于表示带时间戳和坐标系的点
from geometry_msgs.msg import PointStamped

# 从 geometry_msgs 包导入 Twist 消息类型
# Twist 用于表示速度命令（线速度和角速度）
from geometry_msgs.msg import Twist

# 导入 ROS 2 Python 客户端库
import rclpy

# 从 rclpy 导入 Node 基类
from rclpy.node import Node

# 从 turtlesim 包导入 Pose 消息类型
# Pose 用于表示海龟的位置和姿态
from turtlesim.msg import Pose

# 从 turtlesim 包导入 Spawn 服务类型
# Spawn 用于生成新的海龟
from turtlesim.srv import Spawn


class PointPublisher(Node):
    """
    生成海龟并发布带时间戳的点消息

    这个类生成一个新的海龟（turtle3），控制它移动，
    并发布它在 world 坐标系中的位置作为 PointStamped 消息。
    """

    def __init__(self):
        """
        构造函数
        """
        # 调用父类构造函数，设置节点名称
        super().__init__('turtle_tf2_message_broadcaster')

        # 创建生成海龟的服务客户端
        self.spawner = self.create_client(Spawn, 'spawn')
        
        # 布尔值，用于存储服务和海龟状态信息
        self.turtle_spawning_service_ready = False  # 生成海龟的服务是否可用
        self.turtle_spawned = False  # 海龟是否成功生成
        self.turtle_pose_cansubscribe = False  # 是否可以订阅 turtle3 的话题

        # 创建定时器，每秒调用一次 on_timer 方法
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        """
        定时器回调函数，用于处理海龟生成和话题订阅
        """
        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                # 海龟已生成，设置可以订阅标志
                self.turtle_pose_cansubscribe = True
            else:
                # 检查生成海龟的请求是否完成
                if self.result.done():
                    # 海龟生成成功
                    self.get_logger().info(
                        f'Successfully spawned {self.result.result().name}')
                    self.turtle_spawned = True
                else:
                    # 海龟生成未完成
                    self.get_logger().info('Spawn is not finished')
        else:
            # 检查生成海龟的服务是否可用
            if self.spawner.service_is_ready():
                # 初始化生成海龟的请求
                request = Spawn.Request()
                request.name = 'turtle3'  # 海龟名称
                request.x = 4.0  # 初始 x 坐标
                request.y = 2.0  # 初始 y 坐标
                request.theta = 0.0  # 初始角度
                
                # 异步调用服务
                self.result = self.spawner.call_async(request)
                self.turtle_spawning_service_ready = True
            else:
                # 服务不可用
                self.get_logger().info('Service is not ready')

        # 如果海龟已生成且可以订阅话题
        if self.turtle_pose_cansubscribe:
            # 创建速度命令发布者
            self.vel_pub = self.create_publisher(Twist, 'turtle3/cmd_vel', 10)
            
            # 订阅海龟的姿态话题
            self.sub = self.create_subscription(Pose, 'turtle3/pose', self.handle_turtle_pose, 10)
            
            # 创建 PointStamped 消息发布者
            self.pub = self.create_publisher(PointStamped, 'turtle3/turtle_point_stamped', 10)

    def handle_turtle_pose(self, msg):
        """
        处理海龟姿态消息的回调函数

        参数:
            msg: 海龟的姿态消息（包含位置和角度）
        """
        # 创建速度命令消息
        vel_msg = Twist()
        vel_msg.linear.x = 1.0  # 线速度：1.0
        vel_msg.angular.z = 1.0  # 角速度：1.0
        
        # 发布速度命令，控制海龟移动
        self.vel_pub.publish(vel_msg)

        # 创建 PointStamped 消息
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()  # 当前时间戳
        ps.header.frame_id = 'world'  # 坐标系名称
        ps.point.x = msg.x  # 海龟的 x 坐标
        ps.point.y = msg.y  # 海龟的 y 坐标
        ps.point.z = 0.0  # 海龟的 z 坐标（固定为 0）
        
        # 发布带时间戳的点消息
        self.pub.publish(ps)


def main():
    """
    主函数：程序入口点
    """
    # 初始化 ROS 2 客户端库
    rclpy.init()
    
    # 创建点发布器节点
    node = PointPublisher()
    
    try:
        # 开始处理回调（保持节点运行）
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断
        pass

    # 关闭 ROS 2 客户端库
    rclpy.shutdown()
