# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node


# generate_launch_description 是 ROS 2 Python Launch 文件中的入口函数，有着 main 函数的作用。
# 主要作用：
# （1）定义启动逻辑的入口， 在加载 .py 格式的 launch 文件时，会自动寻找并调用名为 generate_launch_description 的函数。
# （2）返回 LaunchDescription 对象， 必须返回一个 LaunchDescription 实例。
# （3）支持动态配置，可以在其中使用 Python 的所有功能（如条件判断 if/else、循环、解析命令行参数 LaunchConfiguration 等）来动态生成启动配置。
def generate_launch_description():

    # LaunchDescription 是 ROS 2 Launch 系统中的核心容器类，它的主要作用是描述和封装一组需要启动的动作（Actions）。
    # 它接收一个列表（List），列表中包含各种“动作”对象。
    # 最常见的动作是 Node（启动一个 ROS 节点），但也包括 ExecuteProcess（执行普通命令行进程）、TimerAction（延迟执行）、
    # IncludeLaunchDescription（包含其他 launch 文件）等。
    return LaunchDescription(  # <--- 创建容器
        [
            # 第一个海龟模拟器节点
            Node(
                package="turtlesim",  # 包名
                namespace="turtlesim1",  # 命名空间，避免话题冲突
                executable="turtlesim_node",  # 可执行文件名
                name="sim1",  # 节点名称
                # 传递给节点的参数
                arguments=["--ros-args", "--log-level", "info"],  # 设置日志级别为 info
            ),
            # 第二个海龟模拟器节点
            Node(
                package="turtlesim",  # 包名
                namespace="turtlesim2",  # 命名空间
                executable="turtlesim_node",  # 可执行文件名
                name="sim2",  # 节点名称
                # 使用 ros_arguments 参数设置 ros 参数
                ros_arguments=[
                    "--log-level",
                    "warn",
                ],  # 设置日志级别为 warn（减少输出）
            ),
            # Mimic 节点：模仿第一个海龟的动作控制第二个海龟
            Node(
                package="turtlesim",  # 包名
                executable="mimic",  # 模仿节点的可执行文件
                name="mimic",  # 节点名称
                # 话题重映射：将 mimic 的输入输出重映射到实际的海龟话题
                remappings=[
                    # 将 /input/pose 重映射到第一个海龟的姿态话题
                    ("/input/pose", "/turtlesim1/turtle1/pose"),
                    # 将 /output/cmd_vel 重映射到第二个海龟的速度命令话题
                    ("/output/cmd_vel", "/turtlesim2/turtle1/cmd_vel"),
                ],
            ),
        ]
    )


# 使用标准的 ROS 2 重映射语法
# 用户可以在运行该节点时，使用 --ros-args 和 -r (remap) 参数来改变话题名称。

# 例如，假设你想让这只"模仿"海龟订阅名为 /turtle1/pose 的话题，并发布速度指令到 /turtle2/cmd_vel，你可以这样运行：
# ros2 run turtlesim mimic --ros-args -r input/pose:=/turtle1/pose -r output/cmd_vel:=/turtle2/cmd_vel
