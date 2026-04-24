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

# 从 geometry_msgs 包导入 TransformStamped 消息类型
# TransformStamped 用于表示带时间戳的坐标变换
from geometry_msgs.msg import TransformStamped

# 导入 NumPy 库，用于数组操作
import numpy as np

# 导入 ROS 2 Python 客户端库
import rclpy

# 从 rclpy 导入 Node 基类
from rclpy.node import Node

# 从 tf2_ros 导入坐标变换广播器
# 用于发布动态坐标变换（持续更新）
from tf2_ros import TransformBroadcaster

# 从 turtlesim 包导入 Pose 消息类型
# Pose 用于表示海龟的位置和姿态
from turtlesim.msg import Pose


# 这个函数是 transforms3d 库的简化版本
# 原代码位于: https://github.com/matthew-brett/transforms3d/blob/f185e866ecccb66c545559bc9f2e19cb5025e0ab/transforms3d/euler.py
# 除了简化之外，这个版本还调整了返回顺序为 x,y,z,w，这是 ROS 偏好的格式
def quaternion_from_euler(ai, aj, ak):
    """
    将欧拉角转换为四元数

    参数:
        ai: 绕 X 轴的旋转角度（弧度）
        aj: 绕 Y 轴的旋转角度（弧度）
        ak: 绕 Z 轴的旋转角度（弧度）

    返回:
        q: 四元数数组 [x, y, z, w]
    """
    # 将角度除以 2（欧拉角到四元数公式需要）
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0

    # 计算各个角度的三角函数值
    ci = math.cos(ai)  # cos(ai/2)
    si = math.sin(ai)  # sin(ai/2)
    cj = math.cos(aj)  # cos(aj/2)
    sj = math.sin(aj)  # sin(aj/2)
    ck = math.cos(ak)  # cos(ak/2)
    sk = math.sin(ak)  # sin(ak/2)

    # 计算组合值
    cc = ci * ck  # cos(ai/2) * cos(ak/2)
    cs = ci * sk  # cos(ai/2) * sin(ak/2)
    sc = si * ck  # sin(ai/2) * cos(ak/2)
    ss = si * sk  # sin(ai/2) * sin(ak/2)

    # 创建四元数数组
    q = np.empty((4,))

    # 计算四元数的各个分量
    q[0] = cj * sc - sj * cs  # x
    q[1] = cj * ss + sj * cc  # y
    q[2] = cj * cs - sj * sc  # z
    q[3] = cj * cc + sj * ss  # w

    # 返回四元数 [x, y, z, w]
    return q


class FramePublisher(Node):
    """
    订阅海龟姿态并广播坐标变换

    这个类订阅海龟的姿态信息，将其转换为从 world 坐标系到海龟坐标系的坐标变换，
    并通过 TF2 广播出去。
    """

    def __init__(self):
        """
        构造函数
        """
        # 调用父类构造函数，设置节点名称
        super().__init__("turtle_tf2_frame_publisher")

        # 声明并获取 `turtlename` 参数（默认为 'turtle'）
        self.turtlename = (
            self.declare_parameter("turtlename", "turtle")
            .get_parameter_value()
            .string_value
        )

        # 初始化坐标变换广播器
        self.tf_broadcaster = TransformBroadcaster(self)

        # 订阅海龟的姿态话题，并在收到消息时调用 handle_turtle_pose 回调函数
        self.subscription = self.create_subscription(
            Pose,  # 消息类型
            f"/{self.turtlename}/pose",  # 话题名称（基于海龟名称）
            self.handle_turtle_pose,  # 回调函数
            1,
        )  # 队列大小
        self.subscription  # 防止未使用变量警告

    def handle_turtle_pose(self, msg):
        """
        处理海龟姿态消息的回调函数

        参数:
            msg: 海龟的姿态消息（包含位置和角度）
        """
        # 创建 TransformStamped 消息
        t = TransformStamped()

        # 设置消息头
        t.header.stamp = self.get_clock().now().to_msg()  # 当前时间戳
        t.header.frame_id = "world"  # 父坐标系名称
        t.child_frame_id = self.turtlename  # 子坐标系名称（海龟名称）

        # 海龟只在 2D 平面存在，因此我们从消息中获取 x 和 y 平移坐标，
        # 并将 z 坐标设置为 0
        t.transform.translation.x = msg.x  # X 坐标
        t.transform.translation.y = msg.y  # Y 坐标
        t.transform.translation.z = 0.0  # Z 坐标（固定为 0）

        # 同样，海龟只能绕一个轴旋转，
        # 因此我们将 x 和 y 方向的旋转设置为 0，
        # 并从消息中获取 z 轴的旋转
        q = quaternion_from_euler(0, 0, msg.theta)  # 转换欧拉角到四元数
        t.transform.rotation.x = q[0]  # 四元数 x
        t.transform.rotation.y = q[1]  # 四元数 y
        t.transform.rotation.z = q[2]  # 四元数 z
        t.transform.rotation.w = q[3]  # 四元数 w

        # 发送坐标变换
        self.tf_broadcaster.sendTransform(t)


def main():
    """
    主函数：程序入口点
    """
    # 初始化 ROS 2 客户端库
    rclpy.init()

    # 创建海龟坐标变换广播器节点
    node = FramePublisher()

    try:
        # 开始处理回调（保持节点运行）
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断
        pass

    # 关闭 ROS 2 客户端库
    rclpy.shutdown()
