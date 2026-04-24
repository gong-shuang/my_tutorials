# Software License Agreement (BSD License 2.0)
#
# Copyright (c) 2023, Metro Robots
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Metro Robots nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# 导入启动相关的模块
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 这些是你可以传递给这个启动文件的参数，例如 paused:=true
    # 声明 gui 参数，用于控制是否显示 Gazebo GUI
    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='true',
    )
    
    # 声明 urdf_package 参数，指定机器人描述所在的包
    package_arg = DeclareLaunchArgument('urdf_package',
                                        description='The package where the robot description is located',
                                        default_value='urdf_tutorial')
    
    # 声明 urdf_package_path 参数，指定机器人描述文件相对于包根目录的路径
    model_arg = DeclareLaunchArgument('urdf_package_path',
                                      description='The path to the robot description relative to the package root',
                                      default_value='urdf/08-macroed.urdf.xacro')

    # 包含 Gazebo 空世界启动文件
    empty_world_launch = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py']),
        # 传递参数给 Gazebo 启动文件
        launch_arguments={
            'gui': LaunchConfiguration('gui'),  # 是否显示 GUI
            'pause': 'true',  # 启动时暂停
        }.items(),
    )

    # 包含 urdf_launch 包的 description.launch.py 文件
    # 用于加载和发布机器人描述
    description_launch_py = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_launch'), 'launch', 'description.launch.py']),
        # 传递参数给 description 启动文件
        launch_arguments={
            'urdf_package': LaunchConfiguration('urdf_package'),
            'urdf_package_path': LaunchConfiguration('urdf_package_path')}.items()
    )

    # 将 robot_description 推送到工厂并在 Gazebo 中生成机器人
    urdf_spawner_node = Node(
        package='gazebo_ros',  # 包名
        executable='spawn_entity.py',  # 可执行文件名
        name='urdf_spawner',  # 节点名称
        arguments=['-topic', '/robot_description', '-entity', 'robot', '-z', '0.5', '-unpause'],
        # -topic: 机器人描述话题
        # -entity: 生成的实体名称
        # -z: 生成位置的 z 坐标（抬高 0.5 米）
        # -unpause: 生成后取消暂停
        output='screen',  # 输出到屏幕
    )

    # 返回完整的 LaunchDescription 对象
    return LaunchDescription([
        gui_arg,  # GUI 参数
        package_arg,  # 包参数
        model_arg,  # 模型参数
        empty_world_launch,  # 启动 Gazebo 空世界
        description_launch_py,  # 加载和发布机器人描述
        urdf_spawner_node,  # 在 Gazebo 中生成机器人
    ])
