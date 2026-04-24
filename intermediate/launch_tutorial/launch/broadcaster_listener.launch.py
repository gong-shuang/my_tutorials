# /**
#  * @file broadcaster_listener.launch.py
#  * @brief 启动 turtle_tf2 广播器和监听器
#  * 
#  * 本文件用于启动两个 TF2 广播器（分别对应两个海龟）
#  * 和一个 TF2 监听器，用于演示坐标变换功能。
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
    # 返回 LaunchDescription 对象，包含所有要执行的动作
    return LaunchDescription(
        [
            # 1. 声明启动参数
            DeclareLaunchArgument(
                "target_frame",  # 参数名称
                default_value="turtle1",  # 默认值
                description="Target frame name.",  # 描述
            ),
            
            # 2. 启动第一个 TF2 广播器（对应 turtle1）
            Node(
                package="turtle_tf2_py",  # 包名
                executable="turtle_tf2_broadcaster",  # 可执行文件名
                name="broadcaster1",  # 节点名称
                parameters=[{"turtlename": "turtle1"}],  # 参数：海龟名称
            ),
            
            # 3. 启动第二个 TF2 广播器（对应 turtle2）
            Node(
                package="turtle_tf2_py",  # 包名
                executable="turtle_tf2_broadcaster",  # 可执行文件名
                name="broadcaster2",  # 节点名称
                parameters=[{"turtlename": "turtle2"}],  # 参数：海龟名称
            ),
            
            # 4. 启动 TF2 监听器
            Node(
                package="turtle_tf2_py",  # 包名
                executable="turtle_tf2_listener",  # 可执行文件名
                name="listener",  # 节点名称
                parameters=[{"target_frame": LaunchConfiguration("target_frame")}],  # 参数：目标坐标系
            ),
        ]
    )
