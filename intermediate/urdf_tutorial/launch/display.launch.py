from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 创建 LaunchDescription 对象，用于存储所有要执行的动作
    ld = LaunchDescription()

    # 获取 urdf_tutorial 包的共享目录路径
    urdf_tutorial_path = FindPackageShare('urdf_tutorial')
    # 设置默认的 URDF 模型文件路径（相对于包目录）
    default_model_path = PathJoinSubstitution(['urdf', '01-myfirst.urdf'])
    # 设置默认的 RViz 配置文件路径
    default_rviz_config_path = PathJoinSubstitution([urdf_tutorial_path, 'rviz', 'urdf.rviz'])

    # 这些参数是为了保持向后兼容性而保留的
    # 声明 gui 参数，用于控制是否启用 joint_state_publisher_gui
    gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    ld.add_action(gui_arg)
    # 声明 rvizconfig 参数，用于指定 RViz 配置文件的路径
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                     description='Absolute path to rviz config file')
    ld.add_action(rviz_arg)

    # 这个参数的含义与之前版本略有不同
    # 声明 model 参数，用于指定 URDF 文件的路径（相对于 urdf_tutorial 包）
    ld.add_action(DeclareLaunchArgument(name='model', default_value=default_model_path,
                                        description='Path to robot urdf file relative to urdf_tutorial package'))

    # 包含 urdf_launch 包的 display.launch.py 文件
    # 这是一个标准的 URDF 显示启动文件，包含了 robot_state_publisher、joint_state_publisher 等
    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_launch'), 'launch', 'display.launch.py']),
        # 向包含的启动文件传递参数
        launch_arguments={
            'urdf_package': 'urdf_tutorial',  # URDF 文件所在的包名
            'urdf_package_path': LaunchConfiguration('model'),  # URDF 文件的路径
            'rviz_config': LaunchConfiguration('rvizconfig'),  # RViz 配置文件路径
            'jsp_gui': LaunchConfiguration('gui')  # 是否启用 joint_state_publisher_gui
        }.items()
    ))

    # 返回完整的 LaunchDescription 对象
    return ld
