#include <pluginlib/class_loader.hpp>
#include <polygon_base/regular_polygon.hpp>

/**
 * @file area_node.cpp
 * @brief 演示如何使用 pluginlib 加载和使用多边形插件
 * @author ROS 2 官方教程
 * @version 0.1
 */

/**
 * @brief 主函数，演示插件加载和使用
 * @param argc 命令行参数个数
 * @param argv 命令行参数数组
 * @return 执行状态码
 * 
 * 本函数展示了如何使用 pluginlib 加载不同的正多边形插件（三角形和正方形），
 * 初始化它们的边长，然后计算并打印它们的面积。
 */
int main(int argc, char** argv)
{
  // 避免未使用参数的警告
  (void) argc;
  (void) argv;

  /**
   * @brief 创建插件加载器
   * 
   * 参数1: 包名 "polygon_base"
   * 参数2: 基类类型 "polygon_base::RegularPolygon"
   */
  pluginlib::ClassLoader<polygon_base::RegularPolygon> poly_loader("polygon_base", "polygon_base::RegularPolygon");

  try
  {
    /**
     * @brief 加载三角形插件
     * 
     * 使用插件名称 "awesome_triangle" 创建实例
     */
    std::shared_ptr<polygon_base::RegularPolygon> triangle = poly_loader.createSharedInstance("awesome_triangle");
    triangle->initialize(10.0);  // 初始化边长为10.0

    /**
     * @brief 加载正方形插件
     * 
     * 使用插件名称 "polygon_plugins::Square" 创建实例
     */
    std::shared_ptr<polygon_base::RegularPolygon> square = poly_loader.createSharedInstance("polygon_plugins::Square");
    square->initialize(10.0);  // 初始化边长为10.0

    // 计算并打印三角形面积
    printf("Triangle area: %.2f\n", triangle->area());
    // 计算并打印正方形面积
    printf("Square area: %.2f\n", square->area());
  }
  catch(pluginlib::PluginlibException& ex)
  {
    // 处理插件加载失败的异常
    printf("The plugin failed to load for some reason. Error: %s\n", ex.what());
  }

  return 0;
}