#-------------------------------------------------------------------------------
# polygon_base 包的 CMake 配置文件
#-------------------------------------------------------------------------------

# 1.要求的 CMake 最低版本
cmake_minimum_required(VERSION 3.8)


# 2. 项目名称
project(polygon_base)  #  PROJECT_NAME 将自动设置为 "polygon_base"

# 编译器设置：启用额外的警告选项
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖项
find_package(ament_cmake REQUIRED)  # ROS 2 的构建系统
find_package(pluginlib REQUIRED)     # 插件库，用于加载动态插件

# 3. add_executable() 指定要生成的可执行文件和其源文件：
# 构建 area_node 可执行文件
add_executable(area_node src/area_node.cpp)

# ------------------------------------------------------

# 4. add_library() 创建一个库（静态库或动态库）及其源文件：
# 构建库（作为插件的基类）
# 使用 INTERFACE 库类型，因为这只是一个头文件库
add_library(${PROJECT_NAME} INTERFACE)
add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

# 设置编译特性
target_compile_features(${PROJECT_NAME} INTERFACE c_std_99 cxx_std_17)

# ------------------------------------------------------

# 5. target_link_libraries() 链接目标文件与其他库：
# 链接依赖项
target_link_libraries(${PROJECT_NAME} INTERFACE ${pluginlib_TARGETS})

# ------------------------------------------------------

# 6. 设置目标属性 , target_include_directories() 为指定的目标（target）添加头文件搜索路径（相当于 -I 或 /I 编译选项）
# BUILD_INTERFACE: 构建时使用的路径
# INSTALL_INTERFACE: 安装后使用的路径
target_include_directories(area_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

# 设置 include 目录
target_include_directories(${PROJECT_NAME} INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
)

# ------------------------------------------------------

# 7. install() 指定在运行 cmake --install 或 make install 时，将哪些文件复制到目标位置
# 相当于： 在运行 cmake --install 或 make install 时，将哪些文件复制到目标位置
# 安装可执行文件
install(TARGETS area_node
  DESTINATION lib/${PROJECT_NAME}
)
# CMake 目标（可执行文件、库）

# 安装头文件
install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)
# 文件系统中的目录

# 安装库和导出目标
install(TARGETS ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)
# 第一个命令：install(TARGETS ... EXPORT ...)
# 含义：导出一个目标集合的名称（相当于给这个集合起个名字）
# 作用：
#   将指定的目标（${PROJECT_NAME}）加入到一个名为 export_${PROJECT_NAME} 的导出集合中
#   这个集合稍后可以被 install(EXPORT ...) 命令使用
#   用于生成供其他 CMake 项目使用的 CMake 配置文件（如 MyLibraryConfig.cmake）
# 本质：它不安装文件，而是记录信息，告诉 CMake："这些目标（库、可执行文件等）要被打包成一个导出集"

# 安装导出目标
install(EXPORT export_${PROJECT_NAME}
  NAMESPACE ${PROJECT_NAME}::
  DESTINATION share/${PROJECT_NAME}/cmake
)
# 第二个命令：install(EXPORT ...)
# 含义：指定要安装哪个导出集合
# 作用：引用第一个命令中定义的导出集名称 export_${PROJECT_NAME}
# 结果：生成一个 CMake 文件（通常是 <export-name>.cmake），其中包含所有目标的导入信息

# ------------------------------------------------------

# 设置依赖项
ament_target_dependencies(
  area_node
  "pluginlib"
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


# 导出现代 CMake 目标
ament_export_targets(
  export_${PROJECT_NAME}
)




# 生成包配置文件和导出设置
ament_package()
