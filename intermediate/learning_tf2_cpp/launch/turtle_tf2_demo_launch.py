# 导入 LaunchDescription 类，用于构建 launch 描述
from launch import LaunchDescription

# 导入 DeclareLaunchArgument，用于声明启动参数
from launch.actions import DeclareLaunchArgument

# 导入 LaunchConfiguration，用于获取启动参数的值
from launch.substitutions import LaunchConfiguration

# 导入 Node 动作，用于启动 ROS 2 节点
from launch_ros.actions import Node


# generate_launch_description 是 ROS 2 Python Launch 文件中的入口函数
# 主要作用：
# （1）定义启动逻辑的入口，在加载 .py 格式的 launch 文件时，会自动寻找并调用该函数
# （2）返回 LaunchDescription 对象，必须返回一个 LaunchDescription 实例
# （3）支持动态配置，可以使用 Python 的所有功能（如条件判断、循环、解析命令行参数等）来动态生成启动配置
def generate_launch_description():
    """
    生成 TF2 海龟演示的 launch 描述

    该 launch 文件启动以下组件：
    - turtlesim 海龟模拟器节点
    - 两个 TF2 广播器节点（分别广播 turtle1 和 turtle2 的坐标变换）
    - 一个 TF2 监听器节点（用于查询坐标变换）

    返回:
        LaunchDescription: 包含所有要执行的动作
    """
    return LaunchDescription(
        [
            # 启动 turtlesim 海龟模拟器节点
            Node(
                package="turtlesim",  # 包名
                executable="turtlesim_node",  # 可执行文件名
                name="sim",  # 节点名称
            ),
            
            # 启动第一个 TF2 广播器节点，广播 turtle1 的坐标变换
            Node(
                package="learning_tf2_cpp",  # 包名
                executable="turtle_tf2_broadcaster",  # 可执行文件（TF2 广播器）
                name="broadcaster1",  # 节点名称
                # 传递参数给节点
                parameters=[{"turtlename": "turtle1"}],  # 参数：广播器对应的海龟名称
            ),
            
            # 声明 target_frame 启动参数，默认为 turtle1
            DeclareLaunchArgument(
                "target_frame",  # 参数名称
                default_value="turtle1",  # 默认值
                description="Target frame name.",  # 参数描述
            ),
            
            # 启动第二个 TF2 广播器节点，广播 turtle2 的坐标变换
            Node(
                package="learning_tf2_cpp",  # 包名
                executable="turtle_tf2_broadcaster",  # 可执行文件（TF2 广播器）
                name="broadcaster2",  # 节点名称
                # 传递参数给节点
                parameters=[{"turtlename": "turtle2"}],  # 参数：广播器对应的海龟名称
            ),
            
            # 启动 TF2 监听器节点，用于查询坐标变换
            Node(
                package="learning_tf2_cpp",  # 包名
                executable="turtle_tf2_listener",  # 可执行文件（TF2 监听器）
                name="listener",  # 节点名称
                # 传递参数给节点
                parameters=[{"target_frame": LaunchConfiguration("target_frame")}],  # 参数：目标坐标系
            ),
        ]
    )
