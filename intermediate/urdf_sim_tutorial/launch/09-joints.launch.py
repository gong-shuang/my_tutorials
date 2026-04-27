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
from launch.actions import ExecuteProcess
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 声明 urdf_package 参数，指定机器人描述所在的包
    package_arg = DeclareLaunchArgument('urdf_package',
                                        description='The package where the robot description is located',
                                        default_value='urdf_sim_tutorial')
    
    # 声明 urdf_package_path 参数，指定机器人描述文件相对于包根目录的路径
    model_arg = DeclareLaunchArgument('urdf_package_path',
                                      description='The path to the robot description relative to the package root',
                                      default_value='urdf/09-publishjoints.urdf.xacro')

    # 声明 rvizconfig 参数，指定 RViz 配置文件的路径
    rvizconfig_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=PathJoinSubstitution([FindPackageShare('urdf_tutorial'), 'rviz', 'urdf.rviz']),
    )

    # 包含 gazebo 启动文件，用于启动 Gazebo 模拟器
    gazebo_launch = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_sim_tutorial'), 'launch', 'gazebo.launch.py']),
        # 传递参数给 gazebo 启动文件
        launch_arguments={
            'urdf_package': LaunchConfiguration('urdf_package'),
            'urdf_package_path': LaunchConfiguration('urdf_package_path')
        }.items(),
    )

    # 创建 RViz 节点，用于可视化机器人模型
    rviz_node = Node(
        package='rviz2',  # 包名
        executable='rviz2',  # 可执行文件名
        output='screen',  # 输出到屏幕
        arguments=['-d', LaunchConfiguration('rvizconfig')],  # 传递 RViz 配置文件路径
    )

    # 执行命令加载关节状态广播器控制器
    # load_joint_state_controller = ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'start',
    #          'joint_state_broadcaster'],  # 命令参数
    #     output='screen'  # 输出到屏幕
    # )

    # 这是 ROS 2 Control 中用于 加载并激活控制器 的节点配置
    load_joint_state_controller = Node(
        package="controller_manager",
        executable="spawner",      # spawner 会自动加载并激活控制器
        arguments=["joint_state_broadcaster"],  # 告诉 spawner 要加载哪个控制器
        output="screen"
    )

    # 返回完整的 LaunchDescription 对象
    return LaunchDescription([
        package_arg,  # 包参数
        model_arg,  # 模型参数
        rvizconfig_arg,  # RViz 配置参数
        gazebo_launch,  # Gazebo 启动
        rviz_node,  # RViz 节点
        load_joint_state_controller,  # 加载关节状态控制器
    ])
