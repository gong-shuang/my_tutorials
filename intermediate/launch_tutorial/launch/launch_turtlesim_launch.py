# /**
#  * @file launch_turtlesim_launch.py
#  * @brief 启动完整的 turtlesim 演示系统
#  * 
#  * 本文件用于启动完整的 turtlesim 演示系统，包含多个 launch 文件的组合，
#  * 演示了如何组织复杂的 launch 系统。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 IncludeLaunchDescription 动作，用于包含其他 launch 文件
from launch.actions import IncludeLaunchDescription

# 导入 PathJoinSubstitution 类，用于构建路径
from launch.substitutions import PathJoinSubstitution

# 导入 FindPackageShare 类，用于查找包的共享目录
from launch_ros.substitutions import FindPackageShare

# 导入 GroupAction 动作，用于将多个动作组合在一起
from launch.actions import GroupAction

# 导入 PushRosNamespace 动作，用于设置 ROS 命名空间
from launch_ros.actions import PushRosNamespace


# 生成 launch 描述的函数
def generate_launch_description():
    # 构建 launch 目录路径
    launch_dir = PathJoinSubstitution([FindPackageShare("launch_tutorial"), "launch"])
    
    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 1. 包含 turtlesim_world_1.launch.py 文件
            IncludeLaunchDescription(
                PathJoinSubstitution([launch_dir, "turtlesim_world_1.launch.py"])
            ),

            # 2. 包含 turtlesim_world_1.launch.py 文件
            # IncludeLaunchDescription(
            #     PathJoinSubstitution([launch_dir, "turtlesim_world_2.launch.py"])
            # ),
            
            # 3. 使用 GroupAction 为 turtlesim2 命名空间包含 turtlesim_world_2.launch.py
            GroupAction(
                actions=[
                    PushRosNamespace("turtlesim2"),  # 设置命名空间为 turtlesim2
                    IncludeLaunchDescription(
                        PathJoinSubstitution(
                            [launch_dir, "turtlesim_world_2.launch.py"]
                        )
                    ),
                ]
            ),
            
            # 4. 包含 broadcaster_listener.launch.py 文件，并覆盖 target_frame 参数
            IncludeLaunchDescription(
                PathJoinSubstitution([launch_dir, "broadcaster_listener.launch.py"]),
                launch_arguments={"target_frame": "carrot1"}.items(),  # 覆盖目标坐标系为 carrot1
            ),
            
            # 5. 包含 mimic.launch.py 文件
            IncludeLaunchDescription(
                PathJoinSubstitution([launch_dir, "mimic.launch.py"])
            ),
            
            # 6. 包含 fixed_broadcaster.launch.py 文件
            IncludeLaunchDescription(
                PathJoinSubstitution([launch_dir, "fixed_broadcaster.launch.py"])
            ),
            
            # 7. 包含 turtlesim_rviz.launch.py 文件
            IncludeLaunchDescription(
                PathJoinSubstitution([launch_dir, "turtlesim_rviz.launch.py"])
            ),
        ]
    )
