# /**
#  * @file mimic.launch.py
#  * @brief 启动 turtlesim 的 mimic 节点
#  * 
#  * 本文件用于启动 turtlesim 的 mimic 节点，
#  * 该节点用于让一个海龟模仿另一个海龟的运动。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node


# 生成 launch 描述的函数
def generate_launch_description():
    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 启动 mimic 节点
            Node(
                package="turtlesim",  # 包名
                executable="mimic",  # 可执行文件名
                name="mimic",  # 节点名称
                remappings=[  # 话题重映射
                    ("/input/pose", "/turtle2/pose"),  # 输入姿势：从 /turtle2/pose 接收
                    ("/output/cmd_vel", "/turtlesim2/turtle1/cmd_vel"),  # 输出速度命令：发送到 /turtlesim2/turtle1/cmd_vel
                ],
            )
        ]
    )
