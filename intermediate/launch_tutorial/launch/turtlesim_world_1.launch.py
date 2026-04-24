# /**
#  * @file turtlesim_world_1.launch.py
#  * @brief 启动带有自定义背景颜色的 turtlesim
#  * 
#  * 本文件用于启动一个带有蓝色背景的 turtlesim 节点。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 DeclareLaunchArgument 动作，用于声明启动参数
from launch.actions import DeclareLaunchArgument

# 导入 LaunchConfiguration 类，用于获取启动参数值
from launch.substitutions import LaunchConfiguration

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node


# 生成 launch 描述的函数
def generate_launch_description():
    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 1. 声明背景颜色参数
            DeclareLaunchArgument("background_r", default_value="0"),  # 背景红色值
            DeclareLaunchArgument("background_g", default_value="84"),  # 背景绿色值
            DeclareLaunchArgument("background_b", default_value="122"),  # 背景蓝色值
            
            # 2. 启动 turtlesim 节点
            Node(
                package="turtlesim",  # 包名
                executable="turtlesim_node",  # 可执行文件名
                name="sim",  # 节点名称
                parameters=[  # 参数设置
                    {
                        "background_r": LaunchConfiguration("background_r"),  # 使用红色参数
                        "background_g": LaunchConfiguration("background_g"),  # 使用绿色参数
                        "background_b": LaunchConfiguration("background_b"),  # 使用蓝色参数
                    }
                ],
            ),
        ]
    )
