# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 IncludeLaunchDescription，用于包含其他 launch 文件
from launch.actions import IncludeLaunchDescription

# 导入 PathJoinSubstitution，用于构建路径
from launch.substitutions import PathJoinSubstitution

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node

# 导入 FindPackageShare，用于查找包的共享目录
from launch_ros.substitutions import FindPackageShare


# generate_launch_description 是 ROS 2 Python Launch 文件中的入口函数
# 主要作用：
# （1）定义启动逻辑的入口，在加载 .py 格式的 launch 文件时，会自动寻找并调用该函数
# （2）返回 LaunchDescription 对象，必须返回一个 LaunchDescription 实例
# （3）支持动态配置，可以使用 Python 的所有功能（如条件判断、循环、解析命令行参数等）来动态生成启动配置
def generate_launch_description():
    """
    生成动态坐标系 TF2 演示的 launch 描述

    该 launch 文件在基础 TF2 演示的基础上，增加了一个动态坐标系广播器。
    动态坐标系广播器会创建一个名为 'carrot1' 的坐标系，该坐标系会随时间不断变化。

    返回:
        LaunchDescription: 包含所有要执行的动作
    """
    return LaunchDescription(
        [
            # 包含基础的海龟 TF2 演示 launch 文件
            IncludeLaunchDescription(
                # 构建被包含文件的路径
                PathJoinSubstitution(
                    [
                        FindPackageShare("learning_tf2_cpp"),  # 查找 learning_tf2_cpp 包的共享目录
                        "launch",  # 子目录
                        "turtle_tf2_demo_launch.py",  # 要包含的文件
                    ]
                ),
                # 向包含的 launch 文件传递参数
                # 将 target_frame 设置为 carrot1，这样监听器就会查询 turtle2 到 carrot1 的变换
                launch_arguments={"target_frame": "carrot1"}.items(),
            ),
            
            # 启动动态坐标系广播器节点
            Node(
                package="learning_tf2_cpp",  # 包名
                executable="dynamic_frame_tf2_broadcaster",  # 可执行文件（动态坐标系广播器）
                name="dynamic_broadcaster",  # 节点名称
            ),
        ]
    )
