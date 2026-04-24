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

# 导入数学库，用于三角函数计算
import math

# 从 geometry_msgs 包导入 Twist 消息类型
# Twist 用于表示速度命令（线速度和角速度）
from geometry_msgs.msg import Twist

# 导入 ROS 2 Python 客户端库
import rclpy

# 从 rclpy 导入 Node 基类
from rclpy.node import Node

# 从 tf2_ros 导入异常类、缓冲区和监听器
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

# 从 turtlesim 包导入 Spawn 服务类型
# Spawn 用于生成新的海龟
from turtlesim.srv import Spawn


class FrameListener(Node):
    """
    监听坐标变换并控制海龟运动

    这个类监听从目标坐标系到 turtle2 坐标系的变换，
    并根据变换信息控制 turtle2 向目标坐标系移动。
    """

    def __init__(self):
        """
        构造函数
        """
        # 调用父类构造函数，设置节点名称
        super().__init__('turtle_tf2_frame_listener')

        # 声明并获取 `target_frame` 参数（默认为 'turtle1'）
        self.target_frame = self.declare_parameter(
            'target_frame', 'turtle1').get_parameter_value().string_value

        # 创建 TF2 缓冲区，用于存储坐标变换
        self.tf_buffer = Buffer()
        
        # 创建 TF2 监听器，用于监听坐标变换并存储到缓冲区
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 创建生成海龟的服务客户端
        self.spawner = self.create_client(Spawn, 'spawn')
        
        # 布尔值，用于存储服务状态信息
        self.turtle_spawning_service_ready = False  # 生成海龟的服务是否可用
        self.turtle_spawned = False  # 海龟是否成功生成

        # 创建 turtle2 的速度命令发布者
        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)

        # 创建定时器，每秒调用一次 on_timer 方法
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        """
        定时器回调函数，用于监听坐标变换并控制海龟运动
        """
        # 存储坐标系名称，用于计算变换
        from_frame_rel = self.target_frame  # 源坐标系（目标坐标系）
        to_frame_rel = 'turtle2'  # 目标坐标系（turtle2）

        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                # 查找从目标坐标系到 turtle2 坐标系的变换
                # 并发送速度命令让 turtle2 到达目标坐标系
                try:
                    t = self.tf_buffer.lookup_transform(
                        to_frame_rel,  # 目标坐标系
                        from_frame_rel,  # 源坐标系
                        rclpy.time.Time())  # 时间点（使用当前时间）
                except TransformException as ex:
                    # 处理变换异常
                    self.get_logger().info(
                        f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
                    return

                # 创建速度命令消息
                msg = Twist()
                
                # 计算角速度：朝向目标方向
                scale_rotation_rate = 1.0
                msg.angular.z = scale_rotation_rate * math.atan2(
                    t.transform.translation.y,  # 目标相对于 turtle2 的 y 坐标
                    t.transform.translation.x)  # 目标相对于 turtle2 的 x 坐标

                # 计算线速度：与目标距离成正比
                scale_forward_speed = 0.5
                msg.linear.x = scale_forward_speed * math.sqrt(
                    t.transform.translation.x ** 2 +  # x 坐标平方
                    t.transform.translation.y ** 2)  # y 坐标平方，计算距离

                # 发布速度命令
                self.publisher.publish(msg)
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
                request.name = 'turtle2'  # 海龟名称
                request.x = 4.0  # 初始 x 坐标
                request.y = 2.0  # 初始 y 坐标
                request.theta = 0.0  # 初始角度
                
                # 异步调用服务
                self.result = self.spawner.call_async(request)
                self.turtle_spawning_service_ready = True
            else:
                # 服务不可用
                self.get_logger().info('Service is not ready')


def main():
    """
    主函数：程序入口点
    """
    # 初始化 ROS 2 客户端库
    rclpy.init()
    
    # 创建坐标变换监听器节点
    node = FrameListener()
    
    try:
        # 开始处理回调（保持节点运行）
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断
        pass

    # 关闭 ROS 2 客户端库
    rclpy.shutdown()
