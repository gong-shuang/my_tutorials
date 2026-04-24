# /**
#  * @file turtlesim_rviz.launch.py
#  * @brief 启动 RViz2 并加载海龟 TF2 配置
#  * 
#  * 本文件用于启动 RViz2 并加载预配置的海龟 TF2 可视化配置文件。
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
            # 启动 RViz2 节点
            Node(
                package="rviz2",  # 包名
                executable="rviz2",  # 可执行文件名
                name="rviz2",  # 节点名称
                arguments=[  # 命令行参数
                    "-d",  # 指定配置文件
                    PathJoinSubstitution(
                        [
                            FindPackageShare("turtle_tf2_py"),  # 查找 turtle_tf2_py 包的共享目录
                            "rviz",  # rviz 子目录
                            "turtle_rviz.rviz"  # 配置文件名
                        ]
                    ),
                ],
            ),
        ]
    )
