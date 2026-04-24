# /**
#  * @file turtle_tf2_dynamic_frame_demo_launch.py
#  * @brief 启动动态坐标系的海龟 TF2 演示
#  *
#  * 本文件用于启动动态坐标系的海龟 TF2 演示系统，包括：
#  * - 包含基础的海龟 TF2 演示
#  * - 启动动态坐标系广播器（carrot1）
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 IncludeLaunchDescription 动作，用于包含其他 launch 文件
from launch.actions import IncludeLaunchDescription

# 导入 PathJoinSubstitution 类，用于构建路径
from launch.substitutions import PathJoinSubstitution

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node

# 导入 FindPackageShare 类，用于查找包的共享目录
from launch_ros.substitutions import FindPackageShare


# 生成 launch 描述的函数
def generate_launch_description():
    # 返回 LaunchDescription 对象，包含所有要执行的动作
    return LaunchDescription(
        [
            # 1. 包含基础的海龟 TF2 演示 launch 文件
            # 并覆盖 target_frame 参数为 "carrot1"
            IncludeLaunchDescription(
                # 构建被包含文件的路径
                PathJoinSubstitution(
                    [
                        FindPackageShare(
                            "learning_tf2_py"
                        ),  # 查找 learning_tf2_py 包的共享目录
                        "launch",  # 子目录
                        "turtle_tf2_demo_launch.py",  # 要包含的文件
                    ]
                ),
                # 传递启动参数给被包含的 launch 文件
                launch_arguments={
                    "target_frame": "carrot1"
                }.items(),  # 目标坐标系为 carrot1
            ),
            # 2. 启动动态坐标系广播器
            # 这个广播器会创建一个随时间变化的 carrot1 坐标系
            Node(
                package="learning_tf2_py",  # 包名
                executable="dynamic_frame_tf2_broadcaster",  # 可执行文件名
                name="dynamic_broadcaster",  # 节点名称
            ),
        ]
    )
