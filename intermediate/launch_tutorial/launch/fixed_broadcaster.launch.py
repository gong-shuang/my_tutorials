# /**
#  * @file fixed_broadcaster.launch.py
#  * @brief 启动固定坐标系的 TF2 广播器
#  * 
#  * 本文件用于启动一个固定坐标系的 TF2 广播器，
#  * 节点名称会使用当前用户名作为前缀。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 DeclareLaunchArgument 动作，用于声明启动参数
from launch.actions import DeclareLaunchArgument

# 导入替换变量
from launch.substitutions import (
    EnvironmentVariable,   # 环境变量
    LaunchConfiguration,   # 启动配置（参数）
)

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node


# 生成 launch 描述的函数
def generate_launch_description():
    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 1. 声明启动参数
            DeclareLaunchArgument(
                "node_prefix",  # 参数名称
                default_value=[EnvironmentVariable("USER"), "_"],  # 默认值：当前用户名 + 下划线
                description="prefix for node name",  # 描述：节点名称前缀
            ),
            
            # 2. 启动固定坐标系的 TF2 广播器
            Node(
                package="turtle_tf2_py",  # 包名
                executable="fixed_frame_tf2_broadcaster",  # 可执行文件名
                name=[LaunchConfiguration("node_prefix"), "fixed_broadcaster"],  # 节点名称：前缀 + fixed_broadcaster
            ),
        ]
    )
