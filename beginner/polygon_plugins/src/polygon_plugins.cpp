#include <polygon_base/regular_polygon.hpp>
#include <cmath>

/**
 * @file polygon_plugins.cpp
 * @brief 多边形插件的实现文件
 * @author ROS 2 官方教程
 * @version 0.1
 */

namespace polygon_plugins
{
  /**
   * @class Square
   * @brief 正方形插件实现
   * 
   * 继承自 polygon_base::RegularPolygon 抽象基类，实现了正方形的面积计算。
   */
  class Square : public polygon_base::RegularPolygon
  {
    public:
      /**
       * @brief 初始化正方形
       * @param side_length 边长
       * 
       * 重写基类的纯虚函数，设置正方形的边长。
       */
      void initialize(double side_length) override
      {
        side_length_ = side_length;
      }

      /**
       * @brief 计算正方形的面积
       * @return 正方形的面积
       * 
       * 重写基类的纯虚函数，计算并返回正方形的面积。
       * 面积计算公式：边长 * 边长
       */
      double area() override
      {
        return side_length_ * side_length_;
      }

    protected:
      double side_length_;  ///< 正方形的边长
  };

  /**
   * @class Triangle
   * @brief 正三角形插件实现
   * 
   * 继承自 polygon_base::RegularPolygon 抽象基类，实现了正三角形的面积计算。
   */
  class Triangle : public polygon_base::RegularPolygon
  {
    public:
      /**
       * @brief 初始化正三角形
       * @param side_length 边长
       * 
       * 重写基类的纯虚函数，设置正三角形的边长。
       */
      void initialize(double side_length) override
      {
        side_length_ = side_length;
      }

      /**
       * @brief 计算正三角形的面积
       * @return 正三角形的面积
       * 
       * 重写基类的纯虚函数，计算并返回正三角形的面积。
       * 面积计算公式：0.5 * 边长 * 高
       */
      double area() override
      {
        return 0.5 * side_length_ * getHeight();
      }

      /**
       * @brief 计算正三角形的高
       * @return 正三角形的高
       * 
       * 使用勾股定理计算正三角形的高：h = √(a² - (a/2)²)
       */
      double getHeight()
      {
        return sqrt((side_length_ * side_length_) - ((side_length_ / 2) * (side_length_ / 2)));
      }

    protected:
      double side_length_;  ///< 正三角形的边长
  };
}

#include <pluginlib/class_list_macros.hpp>

/**
 * @brief 导出 Square 插件
 * 
 * 将 Square 类导出为 polygon_base::RegularPolygon 类型的插件
 * 插件名称：polygon_plugins::Square
 */
PLUGINLIB_EXPORT_CLASS(polygon_plugins::Square, polygon_base::RegularPolygon)

/**
 * @brief 导出 Triangle 插件
 * 
 * 将 Triangle 类导出为 polygon_base::RegularPolygon 类型的插件
 * 插件名称：polygon_plugins::Triangle
 * 注意：在 area_node.cpp 中使用的是 "awesome_triangle" 名称，这是在 plugins.xml 中定义的别名
 */
PLUGINLIB_EXPORT_CLASS(polygon_plugins::Triangle, polygon_base::RegularPolygon)