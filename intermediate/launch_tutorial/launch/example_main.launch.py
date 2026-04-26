# /**
#  * @file example_main.launch.py
#  * @brief 演示如何包含其他 launch 文件
#  *
#  * 本文件（父 launch 文件）展示了如何使用 IncludeLaunchDescription 包含其他 launch 文件 （子 launch 文件）
#  * 并传递启动参数给被包含的 launch 文件。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 IncludeLaunchDescription 动作，用于包含其他 launch 文件
from launch.actions import IncludeLaunchDescription

# 导入 PathJoinSubstitution 类，用于构建路径
from launch.substitutions import PathJoinSubstitution

# 导入 FindPackageShare 类，用于查找包的共享目录
from launch_ros.substitutions import FindPackageShare


# 生成 launch 描述的函数
def generate_launch_description():
    # 定义颜色配置字典
    colors = {"background_r": "200"}  # 背景红色值

    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 包含 example_substitutions.launch.py 文件
            IncludeLaunchDescription(
                # 构建被包含文件的路径
                PathJoinSubstitution(
                    [
                        FindPackageShare(
                            "launch_tutorial"
                        ),  # 查找 launch_tutorial 包的共享目录
                        "launch",  # 子目录
                        "example_substitutions.launch.py",  # 要包含的文件
                    ]
                ),
                # 传递启动参数给被包含的 launch 文件
                launch_arguments={
                    "turtlesim_ns": "turtlesim2",  # 命名空间
                    "use_provided_red": "True",  # 使用提供的红色值
                    "new_background_r": colors["background_r"],  # 新的背景红色值
                }.items(),  # 转换为键值对列表
            )
        ]
    )
