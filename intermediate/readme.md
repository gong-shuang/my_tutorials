
# intermediate 目录
对应官网教程的 intermediate 章节

## 1. action_tutorials_interfaces
| 备注 | 说明 |
|------|------|
| 创建action | 包含 Fibonacci 动作类型 |

## 2. action_tutorials_cpp
| 备注 | 说明 |
|------|------|
| C++ action服务与客户 | 展示动作系统的使用 |

## 3. action_tutorials_python （未完成）
| 备注 | 说明 |
|------|------|
| python action服务与客户 | 展示动作系统的使用 |

## 4. composable_node_cpp （未完成）
| 备注 | 说明 |
|------|------|
| C++ 可组合的节点| 未完成 |

## 5. node_interfaces_template_class_cpp （未完成）
| 备注 | 说明 |
|------|------|
| C++ 节点接口模版类 | 未完成 |

## 6. cpp_parameter_event_handler
| 备注 | 说明 |
|------|------|
| C++ 监控参数变化 | 展示如何监听参数变化 |

-------------launch 部分------------

## 7. launch
| 备注 | 说明 |
|------|------|
| Creating a launch file | 这个文件夹不是ros2的package，直接使用ros2 launch命令启动py文件 |
```
# 直接当做普通的python文件运行，例如：
ros2 launch my_launch_file.launch.py

# 通过软件包启动文件
ros2 launch <package_name> <launch_file_name>
```

## 8. py_launch_example
| 备注 | 说明 |
|------|------|
| 集成launch文件 | 该小节提供了python或者C++两种方式，如何添加launch文件，修改setup.py文件，或者CMakeLists.txt文件 |


## 9. launch_tutorial
| 备注 | 说明 |
|------|------|
| Using substitutions | 如何启动 子launch文件，并给其传递参数 ，可以提高程序的灵活性。|
|-|example_substitutions.launch.py 文件，是非常好的示例文件，接受父launch文件传递过来的参数，执行普通的命令，延时执行。|
| Using event handlers | 如何在 launch文件中使用事件处理函数，监控进程的状态，并执行相应的动作，例如：当节点启动时，输出打印信息等。这也是非常有用的调试手段。 |
| Managing large projects | 展示如何管理大型项目，顶层launch文件，加各个子launch文件，提高项目的可重用性，比如真实Robot与模拟Robot相互切换。 |
|-|1.从YAML文件中加载参数。2.设置全局命名空间。3.重用节点。4.给子launch文件传递参数。5.话题重映射。6.启动RViz。7.使用系统的环境变量。|

-------------tf2 部分------------

## 10. learning_tf2_py
| 备注 | 说明 |
|------|------|
| static broadcaster | 静态广播只发送一次tf广播 |
| broadcaster | 将话题（/turtle1/pose）转换成tf2的广播，这将触发 TF2 中的坐标变换更新，话题（/turtle1/pose）的默认频率是62，那么tf_broadcaster.sendTransform(t) 的次数也是62|
| listener | 监听 target_frame 和 source_frame 之间的坐标变换，这是TF2的核心功能，用于在不同坐标系之间进行转换。用户只需要发送每个物体的TF2的广播，由ROS2 的TF2框架自动处理坐标变换，然后在使用的时候，只需要告知目标坐标系和源坐标系，即可获取到两个坐标系之间的坐标变换。 |
| 添加frame | 添加frame与创建tf2广播器非常相似， 添加frame可以没有实物，直接需要发送tf2的广播即可，添加frame分两种，一种是静态添加，一种是动态添加，静态frame每次发送的坐标变换是固定，动态frame每次发送的坐标变换是变化的。|

## 11. learning_tf2_cpp
| 备注 | 说明 |
|------|------|
| static broadcaster | 同上 |
| broadcaster | 同上 |
| listener | 同上 |
| 添加frame | 同上 |
| Using time | 调用tf_buffer_->lookupTransform()函数，1.如果参数time设置为0，表示获取最新可用的变换，正常。2.如果参数time设置为当前时间，不正常，因为tf广播还没有到来。此时，还需要设置timeout参数，等待tf广播到来，一般timeout设置为50ms。 |
| Traveling time（时间旅行） | 时间旅行的意思是，可以获取过去的时间点的变换，但是此时需要注意的是，对于tf_buffer_->lookupTransform()函数，不能简单的设置time参数为过去的时间点（比如5秒前，new-5s），需要指定固定不变的参考坐标系，比如"world"，才能正常获取到过去的时间点的变换。 |
| tf2_ros::MessageFilter | 将普通的话题（/turtle3/pose）转换成PointStamped（用于表示带时间戳和坐标系的点），并发布到话题（/turtle3/pose_stamped），然后使用tf2_ros::MessageFilter创建消息过滤器，并注册回调函数（当目标坐标系可变换时，消息才会被传递到回调函数）。 |

-------------Testing 部分------------

## 12. my_math
| 备注 | 说明 |
|------|------|
| Testing | 展示如何测试自定义库的功能 |

-------------URDF 部分------------

## 13. urdf_tutorial
代码来自github：https://github.com/ros/urdf_tutorial
| 备注 | 说明 |
|------|------|
| Building a visual robot model | 通过6个例子展示如何创建和使用机器人模型，这6个人例子，从零开始搭建机器人模型，循序渐进。连杆（Link）和关节（Joint），连杆（Link）有外观和物理属性，外观属性（尺寸，颜色，形状），物理属性（质量，惯性矩阵，碰撞参数），关节（Joint）有6种连接类型，关节的原点。以及如何引用外部的 3D 模型文件。 |
| Building a movable robot model | 三种常用的有可移动关节：continuous、revolute and prismatic，如何通过RViz软件控制并展示关节的运动 |
| Adding physical and collision properties | 如何添加关节（link）的碰撞和惯性属性 |
| Using Xacro to clean up your code | 如何使用Xacro包来简化代码，提高可维护性 |

```
对于章节Building a movable robot model，教程中的示例：
ros2 launch urdf_tutorial display.launch.py model:=urdf/06-flexible.urdf

会创建3个关键node：
/joint_state_publisher
/robot_state_publisher
/rviz

关键的话题：
/joint_states
/parameter_events
/robot_description
/rosout
/tf

初始流程是：
1. 启动joint_state_publisher node，发布关节状态话题（/joint_states）。
2. 启动robot_state_publisher node，发布机器人状态话题（/robot_description）。
3. 启动rviz node，显示机器人模型和关节状态。

在窗口 Joint State Publisher 中，控制滑动条可以改变RViz中机器人的关节角度，流程如下：
节点/joint_state_publisher定期发送/joint_states话题，节点/robot_state_publisher收到该话题后，计算正运动学，然后发布tf2广播，节点/rviz收到新 TF2 消息 → rviz 更新对应连杆的位置 → 显示变化。

```


## 14. urdf_sim_tutorial
代码来自github：https://github.com/ros/urdf_sim_tutorial
| 备注 | 说明 |
|------|------|
| Using a URDF in Gazebo | 要让Gazebo里的机器人“活”起来，必须为它添加两样东西：插件（Plugins）和控制器（Controllers），“插件”作为Gazebo和ROS 2沟通的桥梁，“控制器”则负责根据用户输入的指令，控制机器人的运动。 |


```
章节 Using a URDF in Gazebo，最后的一个例子，控制小车车轮：ros2 launch urdf_sim_tutorial 13-diffdrive.launch.py
在窗口 rqt_robot_steering__RobotSteering 中，控制滑动条机器人的车轮没有动，这是因为 rqt_robot_steering 自身的bug，此时改用命令：
ros2 topic pub /diff_drive_base_controller/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
也是可以控制小车前进

```

## 15. urdf_tutorial_cpp
| 备注 | 说明 |
|------|------|
| Using URDF with robot_state_publisher(C++) | robot_state_publisher 是 ROS 2 中的核心功能包 ，负责将机器人的关节状态转换为 TF（坐标变换）信息， 工作流程为：1. 读取URDF文件。 2. 订阅/joint_states话题，获取关节状态。2. 计算正运动学，将关节状态转换为 TF（坐标变换）信息。3. 将计算结果发布到 /tf 和 /tf_static 话题。 |

```
URDF 文件 → robot_state_publisher ← /joint_states
                                     ↓
                                正运动学计算
                                     ↓
                                /tf (坐标变换)
                                     ↓
                                RViz / Gazebo

```


## 16. urdf_tutorial_r2d2
| 备注 | 说明 |
|------|------|
| Using URDF with robot_state_publisher(Python) | 要使用Python版本的robot_state_publisher，必须在Python代码中添加两行东西：1. 导入robot_state_publisher包，2. 初始化robot_state_publisher。 |


