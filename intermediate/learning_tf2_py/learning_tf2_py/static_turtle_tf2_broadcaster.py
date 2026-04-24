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

# 导入系统库，用于命令行参数处理
import sys

# 从 geometry_msgs 包导入 TransformStamped 消息类型
# TransformStamped 用于表示带时间戳的坐标变换
from geometry_msgs.msg import TransformStamped

# 导入 NumPy 库，用于数组操作
import numpy as np

# 导入 ROS 2 Python 客户端库
import rclpy

# 从 rclpy 导入 Node 基类
from rclpy.node import Node

# 从 tf2_ros 导入静态坐标变换广播器
# 用于发布静态坐标变换（只发布一次，不持续更新）
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


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
    cc = ci*ck  # cos(ai/2) * cos(ak/2)
    cs = ci*sk  # cos(ai/2) * sin(ak/2)
    sc = si*ck  # sin(ai/2) * cos(ak/2)
    ss = si*sk  # sin(ai/2) * sin(ak/2)

    # 创建四元数数组
    q = np.empty((4, ))

    # 计算四元数的各个分量
    q[0] = cj*sc - sj*cs  # x
    q[1] = cj*ss + sj*cc  # y
    q[2] = cj*cs - sj*sc  # z
    q[3] = cj*cc + sj*ss  # w

    # 返回四元数 [x, y, z, w]
    return q


class StaticFramePublisher(Node):
    """
    广播永不变化的坐标变换

    这个示例从 `world` 坐标系向静态海龟坐标系发布坐标变换。
    坐标变换只在启动时发布一次，并且在所有时间内保持不变。
    """

    def __init__(self, transformation):
        """
        构造函数

        参数:
            transformation: 包含变换参数的列表
                           [程序名, 子坐标系名, x, y, z, roll, pitch, yaw]
        """
        # 调用父类构造函数，设置节点名称
        super().__init__('static_turtle_tf2_broadcaster')

        # 创建静态坐标变换广播器
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)

        # 在启动时发布静态坐标变换（只执行一次）
        self.make_transforms(transformation)

    def make_transforms(self, transformation):
        """
        创建并发布坐标变换

        参数:
            transformation: 包含变换参数的列表
        """
        # 创建 TransformStamped 消息
        t = TransformStamped()

        # 设置消息头
        t.header.stamp = self.get_clock().now().to_msg()  # 当前时间戳
        t.header.frame_id = 'world'  # 父坐标系名称
        t.child_frame_id = transformation[1]  # 子坐标系名称（海龟名称）

        # 设置平移分量（位置）
        t.transform.translation.x = float(transformation[2])  # X 坐标
        t.transform.translation.y = float(transformation[3])  # Y 坐标
        t.transform.translation.z = float(transformation[4])  # Z 坐标

        # 将欧拉角转换为四元数（旋转）
        quat = quaternion_from_euler(
            float(transformation[5]),  # roll (绕 X 轴)
            float(transformation[6]),  # pitch (绕 Y 轴)
            float(transformation[7]))  # yaw (绕 Z 轴)

        # 设置旋转分量（四元数）
        t.transform.rotation.x = quat[0]  # 四元数 x
        t.transform.rotation.y = quat[1]  # 四元数 y
        t.transform.rotation.z = quat[2]  # 四元数 z
        t.transform.rotation.w = quat[3]  # 四元数 w

        # 广播静态坐标变换
        self.tf_static_broadcaster.sendTransform(t)


def main():
    """
    主函数：程序入口点
    """
    # 获取 ROS 2 日志记录器
    logger = rclpy.logging.get_logger('logger')

    # 从命令行参数获取参数
    # 期望的参数格式: 程序名 子坐标系名 x y z roll pitch yaw
    if len(sys.argv) != 8:
        # 参数数量不正确，打印使用说明
        logger.info('Invalid number of parameters. Usage: \n'
                    '$ ros2 run turtle_tf2_py static_turtle_tf2_broadcaster'
                    'child_frame_name x y z roll pitch yaw')
        sys.exit(1)  # 以错误码 1 退出

    # 检查子坐标系名称不能是 "world"（因为 world 是父坐标系）
    if sys.argv[1] == 'world':
        logger.info('Your static turtle name cannot be "world"')
        sys.exit(2)  # 以错误码 2 退出

    # 初始化 ROS 2 客户端库
    rclpy.init()

    # 创建静态坐标变换广播器节点，传入命令行参数
    node = StaticFramePublisher(sys.argv)

    try:
        # 开始处理回调（保持节点运行）
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断
        pass

    # 关闭 ROS 2 客户端库
    rclpy.shutdown()
