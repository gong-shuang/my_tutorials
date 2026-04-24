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

# 从 geometry_msgs 包导入 TransformStamped 消息类型
# TransformStamped 用于表示带时间戳的坐标变换
from geometry_msgs.msg import TransformStamped

# 导入 ROS 2 Python 客户端库
import rclpy

# 从 rclpy 导入 Node 基类
from rclpy.node import Node

# 从 tf2_ros 导入坐标变换广播器
# 用于发布动态坐标变换（持续更新）
from tf2_ros import TransformBroadcaster


class FixedFrameBroadcaster(Node):
    """
    广播固定的坐标变换

    这个类用于广播一个固定的坐标变换，
    从 'turtle1' 坐标系到 'carrot1' 坐标系的变换。
    变换是固定的，不随时间变化。
    """

    def __init__(self):
        """
        构造函数
        """
        # 调用父类构造函数，设置节点名称
        super().__init__('fixed_frame_tf2_broadcaster')
        
        # 创建坐标变换广播器
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # 创建定时器，每 0.1 秒调用一次 broadcast_timer_callback 方法
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)

    def broadcast_timer_callback(self):
        """
        定时器回调函数，用于广播固定坐标变换
        """
        # 创建 TransformStamped 消息
        t = TransformStamped()
        
        # 设置消息头
        t.header.stamp = self.get_clock().now().to_msg()  # 当前时间戳
        t.header.frame_id = 'turtle1'  # 父坐标系名称
        t.child_frame_id = 'carrot1'  # 子坐标系名称
        
        # 设置平移分量（位置）
        # 固定位置：在 turtle1 坐标系的 (0, 2, 0) 处
        t.transform.translation.x = 0.0  # X 坐标（固定）
        t.transform.translation.y = 2.0  # Y 坐标（固定）
        t.transform.translation.z = 0.0  # Z 坐标（固定）
        
        # 设置旋转分量（四元数）
        # 这里使用单位四元数，表示没有旋转
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        # 广播坐标变换
        self.tf_broadcaster.sendTransform(t)


def main():
    """
    主函数：程序入口点
    """
    # 初始化 ROS 2 客户端库
    rclpy.init()
    
    # 创建固定坐标变换广播器节点
    node = FixedFrameBroadcaster()
    
    try:
        # 开始处理回调（保持节点运行）
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断
        pass

    # 关闭 ROS 2 客户端库
    rclpy.shutdown()
