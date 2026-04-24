#-------------------------------------------------------------------------------
# polygon_plugins 包的 CMake 配置文件
#-------------------------------------------------------------------------------

# 要求的 CMake 最低版本
cmake_minimum_required(VERSION 3.8)

# 项目名称
project(polygon_plugins)

# 编译器设置：启用额外的警告选项
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖项
find_package(ament_cmake REQUIRED)          # ROS 2 的构建系统
find_package(ament_cmake_ros REQUIRED)      # ROS 2 扩展的构建系统
find_package(polygon_base REQUIRED)         # 多边形基类包
find_package(pluginlib REQUIRED)             # 插件库，用于加载动态插件

# 导出插件描述文件
# 这将把 plugins.xml 中的插件信息注册到 ROS 2 系统中
pluginlib_export_plugin_description_file(polygon_base plugins.xml)

# 构建插件库
add_library(polygon_plugins src/polygon_plugins.cpp)

# 设置编译特性：要求 C99 和 C++17
target_compile_features(polygon_plugins PUBLIC c_std_99 cxx_std_17)

# 设置 include 目录
target_include_directories(polygon_plugins PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

# 设置依赖项
ament_target_dependencies(
  polygon_plugins
  "polygon_base"  # 依赖多边形基类
  "pluginlib"     # 依赖插件库
)

# 设置编译定义
# 使可见性宏使用 dllexport 而不是 dllimport，
# 这在构建库时是合适的，而不是在使用它时。
target_compile_definitions(polygon_plugins PRIVATE "POLYGON_PLUGINS_BUILDING_LIBRARY")

# 安装头文件
install(
  DIRECTORY include/
  DESTINATION include
)

# 安装库
install(
  TARGETS polygon_plugins
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# 测试配置
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # 跳过版权检查（当所有源文件添加了版权和许可证时注释此行）
  set(ament_cmake_copyright_FOUND TRUE)
  # 跳过 cpplint 检查（当包在 git 仓库中且所有源文件添加了版权和许可证时注释此行）
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 导出 include 目录
ament_export_include_directories(
  include
)

# 导出库
ament_export_libraries(
  polygon_plugins
)

# 导出目标
ament_export_targets(
  export_${PROJECT_NAME}
)

# 生成包配置文件和导出设置
ament_package()
