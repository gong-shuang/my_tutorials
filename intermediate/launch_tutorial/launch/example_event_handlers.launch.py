
#  * @file example_event_handlers.launch.py
#  * @brief 演示 ROS 2 launch 系统的事件处理功能
#  * 
#  * 本文件展示了如何在 launch 文件中使用各种事件处理程序，
#  * 包括：进程启动、进程 IO、执行完成、进程退出和系统关闭事件。

# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入各种 launch 动作
from launch.actions import (
    DeclareLaunchArgument,  # 声明启动参数
    EmitEvent,             # 发射事件
    ExecuteProcess,         # 执行外部进程
    LogInfo,               # 记录信息日志
    RegisterEventHandler,   # 注册事件处理器
    TimerAction,           # 定时器动作
)

# 导入条件判断
from launch.conditions import IfCondition

# 导入事件处理器
from launch.event_handlers import (
    OnExecutionComplete,  # 执行完成事件
    OnProcessExit,        # 进程退出事件
    OnProcessIO,          # 进程 IO 事件
    OnProcessStart,       # 进程启动事件
    OnShutdown,           # 关闭事件
)

# 导入关闭事件
from launch.events import Shutdown

# 导入替换变量
from launch.substitutions import (
    EnvironmentVariable,   # 环境变量
    FindExecutable,        # 查找可执行文件
    LaunchConfiguration,   # 启动配置（参数）
    LocalSubstitution,     # 本地替换
    PythonExpression,      # Python 表达式
)

# 导入 ROS 2 节点动作
from launch_ros.actions import Node


# 生成 launch 描述的函数
def generate_launch_description():
    # 声明启动配置（参数）
    turtlesim_ns = LaunchConfiguration("turtlesim_ns")  #  turtlesim 的命名空间
    use_provided_red = LaunchConfiguration("use_provided_red")  # 是否使用提供的红色值
    new_background_r = LaunchConfiguration("new_background_r")  # 新的背景红色值

    # 声明启动参数（带默认值）
    turtlesim_ns_launch_arg = DeclareLaunchArgument(
        "turtlesim_ns", default_value="turtlesim1"  # 默认命名空间为 turtlesim1
    )
    use_provided_red_launch_arg = DeclareLaunchArgument(
        "use_provided_red", default_value="False"  # 默认不使用提供的红色值
    )
    new_background_r_launch_arg = DeclareLaunchArgument(
        "new_background_r", default_value="200"  # 默认红色值为 200
    )

    # 创建 turtlesim 节点
    turtlesim_node = Node(
        package="turtlesim",          # 包名
        namespace=turtlesim_ns,        # 命名空间
        executable="turtlesim_node",  # 可执行文件名
        name="sim",                   # 节点名称
    )
    
    # 创建 spawn 海龟的进程
    spawn_turtle = ExecuteProcess(
        cmd=[
            [
                FindExecutable(name="ros2"),  # 查找 ros2 可执行文件
                " service call ",             # 服务调用命令
                turtlesim_ns,                  # 命名空间
                "/spawn ",                    # 服务名称
                "turtlesim/srv/Spawn ",        # 服务类型
                '"{x: 2, y: 2, theta: 0.2}"',  # 服务参数（JSON 格式）
            ]
        ],
        shell=True,  # 使用 shell 执行
    )
    
    # 创建修改背景红色的进程
    change_background_r = ExecuteProcess(
        cmd=[
            [
                FindExecutable(name="ros2"),  # 查找 ros2 可执行文件
                " param set ",                # 参数设置命令
                turtlesim_ns,                  # 命名空间
                "/sim background_r ",         # 参数路径
                "120",                        # 参数值
            ]
        ],
        shell=True,  # 使用 shell 执行
    )
    
    # 创建条件执行的修改背景红色进程
    change_background_r_conditioned = ExecuteProcess(
        condition=IfCondition(  # 条件执行
            PythonExpression([new_background_r, " == 200", " and ", use_provided_red])
            # 当 new_background_r 等于 200 且 use_provided_red 为真时执行
        ),
        cmd=[
            [
                FindExecutable(name="ros2"),  # 查找 ros2 可执行文件
                " param set ",                # 参数设置命令
                turtlesim_ns,                  # 命名空间
                "/sim background_r ",         # 参数路径
                new_background_r,              # 使用启动参数中的值
            ]
        ],
        shell=True,  # 使用 shell 执行
    )
    
    # 返回 LaunchDescription 对象
    return LaunchDescription(
        [
            # 1. 声明的启动参数
            turtlesim_ns_launch_arg,
            use_provided_red_launch_arg,
            new_background_r_launch_arg,
            
            # 2. 启动 turtlesim 节点
            turtlesim_node,
            
            # 3. 注册事件处理器：当 turtlesim 节点启动时
            RegisterEventHandler(
                OnProcessStart(
                    target_action=turtlesim_node,  # 目标动作
                    on_start=[  # 启动时执行的动作
                        LogInfo(msg="Turtlesim started, spawning turtle"),  # 记录信息
                        spawn_turtle,  # 执行 spawn 海龟的进程
                    ],
                )
            ),
            
            # 4. 注册事件处理器：当 spawn 进程有输出时
            RegisterEventHandler(
                OnProcessIO(
                    target_action=spawn_turtle,  # 目标动作
                    on_stdout=lambda event: LogInfo(  # 标准输出回调
                        msg='Spawn request says "{}"'.format(
                            event.text.decode().strip()  # 解码并去除首尾空白
                        )
                    ),
                )
            ),
            
            # 5. 注册事件处理器：当 spawn 进程执行完成时
            RegisterEventHandler(
                OnExecutionComplete(
                    target_action=spawn_turtle,  # 目标动作
                    on_completion=[  # 完成时执行的动作
                        LogInfo(msg="Spawn finished"),  # 记录信息
                        change_background_r,  # 修改背景红色为 120
                        TimerAction(
                            period=2.0,  # 2 秒后执行
                            actions=[change_background_r_conditioned],  # 执行条件修改
                        ),
                    ],
                )
            ),
            
            # 6. 注册事件处理器：当 turtlesim 节点退出时
            RegisterEventHandler(
                OnProcessExit(
                    target_action=turtlesim_node,  # 目标动作
                    on_exit=[  # 退出时执行的动作
                        LogInfo(
                            msg=(
                                EnvironmentVariable(name="USER"),  # 获取当前用户名
                                " closed the turtlesim window",  # 消息内容
                            )
                        ),
                        EmitEvent(event=Shutdown(reason="Window closed")),  # 发射关闭事件
                    ],
                )
            ),
            
            # 7. 注册事件处理器：当启动系统关闭时
            RegisterEventHandler(
                OnShutdown(
                    on_shutdown=[  # 关闭时执行的动作
                        LogInfo(
                            msg=[
                                "Launch was asked to shutdown: ",  # 消息前缀
                                LocalSubstitution("event.reason"),  # 关闭原因
                            ]
                        )
                    ]
                )
            ),
        ]
    )
