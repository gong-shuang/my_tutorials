# /**
#  * @file turtlesim_world_2.launch.py
#  * @brief 启动带有 YAML 配置文件的 turtlesim
#  * 
#  * 本文件用于启动一个使用 YAML 配置文件的 turtlesim 节点。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 PathJoinSubstitution 类，用于构建路径
from launch.substitutions import PathJoinSubstitution

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node

# 导入 FindPackageShare 类，用于查找包的共享目录
from launch_ros.substitutions import FindPackageShare


# 生成 launch 描述的函数
def generate_launch_description():
    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 启动 turtlesim 节点
            Node(
                package="turtlesim",  # 包名
                executable="turtlesim_node",  # 可执行文件名
                name="sim",  # 节点名称
                parameters=[  # 参数设置
                    PathJoinSubstitution(
                        [
                            FindPackageShare("launch_tutorial"),  # 查找 launch_tutorial 包的共享目录
                            "config",  # config 子目录
                            "turtlesim.yaml",  # YAML 配置文件名
                        ]
                    )
                ],
            ),
        ]
    )
