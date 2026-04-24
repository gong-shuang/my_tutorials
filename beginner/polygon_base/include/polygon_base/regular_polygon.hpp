#ifndef POLYGON_BASE_REGULAR_POLYGON_HPP
#define POLYGON_BASE_REGULAR_POLYGON_HPP

/**
 * @file regular_polygon.hpp
 * @brief 正多边形抽象基类定义
 * @author ROS 2 官方教程
 * @version 0.1
 */

namespace polygon_base
{
  /**
   * @class RegularPolygon
   * @brief 正多边形抽象基类，定义了所有正多边形插件必须实现的接口
   * 
   * 这是一个抽象类，用于插件系统。所有具体的正多边形实现（如三角形、正方形等）
   * 都必须继承这个类并实现其纯虚函数。
   */
  class RegularPolygon
  {
    public:
      /**
       * @brief 初始化正多边形
       * @param side_length 边长
       * 
       * 纯虚函数，子类必须实现。用于设置正多边形的边长。
       */
      virtual void initialize(double side_length) = 0;
      
      /**
       * @brief 计算正多边形的面积
       * @return 正多边形的面积
       * 
       * 纯虚函数，子类必须实现。用于计算并返回正多边形的面积。
       */
      virtual double area() = 0;
      
      /**
       * @brief 虚析构函数
       * 
       * 确保子类析构函数能够被正确调用。
       */
      virtual ~RegularPolygon() {}

    protected:
      /**
       * @brief 保护构造函数
       * 
       * 防止直接实例化抽象基类，只能通过子类构造。
       */
      RegularPolygon() {}
  };
}  // namespace polygon_base

#endif  // POLYGON_BASE_REGULAR_POLYGON_HPP

