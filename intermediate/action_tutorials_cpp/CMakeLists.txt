#-------------------------------------------------------------------------------
# action_tutorials_cpp 包的 CMake 配置文件
#-------------------------------------------------------------------------------

# 1. 设置 CMake 最低版本要求
cmake_minimum_required(VERSION 3.8)

# 2. 定义项目名称
project(action_tutorials_cpp)  # PROJECT_NAME 将自动设置为 "action_tutorials_cpp"

# 3. 编译器设置：启用额外的警告选项
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # 如果使用 GCC 或 Clang 编译器，添加额外的警告编译选项
  # -Wall: 启用所有常见警告
  # -Wextra: 启用额外的警告
  # -Wpedantic: 启用严格符合标准的警告
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

#-------------------------------------------------------------------------------
# 4. 查找依赖项
#-------------------------------------------------------------------------------
# find_package() 用于在系统中查找并加载外部依赖包
# REQUIRED 表示该依赖是必需的，如果找不到会报错

find_package(ament_cmake REQUIRED)                # ROS 2 的 CMake 构建系统
find_package(action_tutorials_interfaces REQUIRED) # action 接口定义包
find_package(rclcpp REQUIRED)                     # ROS 2 C++ 客户端库
find_package(rclcpp_action REQUIRED)              # ROS 2 action 客户端库
find_package(rclcpp_components REQUIRED)          # ROS 2 组件系统

#-------------------------------------------------------------------------------
# 5. 测试配置
#-------------------------------------------------------------------------------
if(BUILD_TESTING)
  # 如果启用了测试构建
  
  find_package(ament_lint_auto REQUIRED)  # ROS 2 自动代码检查工具
  
  # 跳过版权检查（当所有源文件添加了版权和许可证时注释此行）
  set(ament_cmake_copyright_FOUND TRUE)
  
  # 跳过 cpplint 检查（当包在 git 仓库中且所有源文件添加了版权和许可证时注释此行）
  set(ament_cmake_cpplint_FOUND TRUE)
  
  # 自动查找测试依赖项
  ament_lint_auto_find_test_dependencies()
endif()

#-------------------------------------------------------------------------------
# 6. 构建 action_server 库
#-------------------------------------------------------------------------------

# add_library() 创建一个库
# SHARED 表示创建动态共享库（.so 文件）
add_library(action_server SHARED
  src/fibonacci_action_server.cpp)  # 源文件：斐波那契 action 服务器实现

# target_include_directories() 为目标添加头文件搜索路径
# PRIVATE 表示这些包含目录仅对 action_server 目标本身可见
# BUILD_INTERFACE: 构建时使用的路径
# INSTALL_INTERFACE: 安装后使用的路径
target_include_directories(action_server PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

# target_compile_definitions() 添加编译定义
# PRIVATE 表示这些定义仅对 action_server 目标本身可见
# ACTION_TUTORIALS_CPP_BUILDING_DLL 用于控制动态库的导入/导出宏
target_compile_definitions(action_server
  PRIVATE "ACTION_TUTORIALS_CPP_BUILDING_DLL")

# ament_target_dependencies() 设置依赖的 ROS 包
ament_target_dependencies(action_server
  "action_tutorials_interfaces"  # action 接口定义
  "rclcpp"                      # ROS C++ 客户端库
  "rclcpp_action"               # ROS action 支持
  "rclcpp_components")          # ROS 组件系统

# rclcpp_components_register_node() 注册为 ROS 2 组件
# PLUGIN: 类的完全限定名
# EXECUTABLE: 可执行文件的名称
rclcpp_components_register_node(action_server PLUGIN "action_tutorials_cpp::FibonacciActionServer" EXECUTABLE fibonacci_action_server)

# install() 指定安装目标的位置
# ARCHIVE DESTINATION: 静态库安装位置
# LIBRARY DESTINATION: 动态库安装位置
# RUNTIME DESTINATION: 可执行文件安装位置
install(TARGETS
  action_server
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

#-------------------------------------------------------------------------------
# 7. 构建 action_client 库
#-------------------------------------------------------------------------------

# add_library() 创建第二个库（action 客户端）
add_library(action_client SHARED
  src/fibonacci_action_client.cpp)  # 源文件：斐波那契 action 客户端实现

# target_include_directories() 为 action_client 添加头文件搜索路径
target_include_directories(action_client PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

# target_compile_definitions() 添加编译定义
target_compile_definitions(action_client
  PRIVATE "ACTION_TUTORIALS_CPP_BUILDING_DLL")

# ament_target_dependencies() 设置依赖的 ROS 包
ament_target_dependencies(action_client
  "action_tutorials_interfaces"
  "rclcpp"
  "rclcpp_action"
  "rclcpp_components")

# rclcpp_components_register_node() 注册为 ROS 2 组件
rclcpp_components_register_node(action_client PLUGIN "action_tutorials_cpp::FibonacciActionClient" EXECUTABLE fibonacci_action_client)

# install() 安装 action_client 库
install(TARGETS
  action_client
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

#-------------------------------------------------------------------------------
# 8. 生成包配置文件
#-------------------------------------------------------------------------------

# ament_package() 生成包的安装配置文件
# 这是 ROS 2 包的最后一步，生成 package.xml 中定义的元数据
ament_package()
