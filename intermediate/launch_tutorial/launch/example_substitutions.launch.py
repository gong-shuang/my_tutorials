# /**
#  * @file example_substitutions.launch.py
#  * @brief 演示 ROS 2 launch 系统中的替换变量和条件执行
#  * 
#  * 本文件展示了如何使用 LaunchConfiguration、PythonExpression 和条件执行，
#  * 以及如何在 launch 文件中执行外部命令。
#  */

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入各种 launch 动作
from launch.actions import (
    DeclareLaunchArgument,  # 声明启动参数
    ExecuteProcess,         # 执行外部进程
    TimerAction,           # 定时器动作
)

# 导入条件判断
from launch.conditions import IfCondition

# 导入替换变量
from launch.substitutions import (
    LaunchConfiguration,   # 启动配置（参数）
    PythonExpression,      # Python 表达式
)

# 导入 ROS 2 节点动作
from launch_ros.actions import Node


# 生成 launch 描述的函数
def generate_launch_description():
    # 声明启动配置（参数）
    turtlesim_ns = LaunchConfiguration("turtlesim_ns")  # turtlesim 的命名空间
    use_provided_red = LaunchConfiguration("use_provided_red")  # 是否使用提供的红色值
    new_background_r = LaunchConfiguration("new_background_r")  # 新的背景红色值

    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 1. 声明启动参数
            DeclareLaunchArgument("turtlesim_ns", default_value="turtlesim1"),  # 命名空间参数
            DeclareLaunchArgument("use_provided_red", default_value="False"),  # 使用提供的红色值
            DeclareLaunchArgument("new_background_r", default_value="200"),  # 新的背景红色值
            
            # 2. 启动 turtlesim 节点
            Node(
                package="turtlesim",          # 包名
                namespace=turtlesim_ns,        # 命名空间
                executable="turtlesim_node",  # 可执行文件名
                name="sim",                   # 节点名称
            ),
            
            # 3. 执行 spawn 海龟的命令
            ExecuteProcess(
                cmd=[
                    [
                        "ros2 service call ",  # 服务调用命令
                        turtlesim_ns,            # 命名空间
                        "/spawn ",              # 服务名称
                        "turtlesim/srv/Spawn ",  # 服务类型
                        '"{x: 2, y: 2, theta: 0.2}"',  # 服务参数（JSON 格式）
                    ]
                ],
                shell=True,  # 使用 shell 执行
            ),
            
            # 4. 修改背景红色为 120
            ExecuteProcess(
                cmd=[["ros2 param set ", turtlesim_ns, "/sim background_r ", "120"]],
                shell=True,  # 使用 shell 执行
            ),
            
            # 5. 2 秒后条件执行修改背景红色
            TimerAction(
                period=2.0,  # 2 秒后执行
                actions=[
                    ExecuteProcess(
                        condition=IfCondition(  # 条件执行
                            PythonExpression(
                                [new_background_r, " == 200", " and ", use_provided_red]
                                # 当 new_background_r 等于 200 且 use_provided_red 为真时执行
                            )
                        ),
                        cmd=[
                            [
                                "ros2 param set ",  # 参数设置命令
                                turtlesim_ns,        # 命名空间
                                "/sim background_r ",  # 参数路径
                                new_background_r,    # 使用启动参数中的值
                            ]
                        ],
                        shell=True,  # 使用 shell 执行
                    ),
                ],
            ),
        ]
    )
