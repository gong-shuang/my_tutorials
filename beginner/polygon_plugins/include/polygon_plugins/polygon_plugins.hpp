#ifndef POLYGON_PLUGINS__POLYGON_PLUGINS_HPP_
#define POLYGON_PLUGINS__POLYGON_PLUGINS_HPP_

#include "polygon_plugins/visibility_control.h"

/**
 * @file polygon_plugins.hpp
 * @brief 多边形插件的头文件
 * @author ROS 2 官方教程
 * @version 0.1
 */

namespace polygon_plugins
{

/**
 * @class PolygonPlugins
 * @brief 多边形插件的基类（未使用）
 * 
 * 注意：此类目前未被使用，实际的插件实现直接在 polygon_plugins.cpp 中继承
 * polygon_base::RegularPolygon 基类。
 */
class PolygonPlugins
{
public:
  /**
   * @brief 构造函数
   */
  PolygonPlugins();

  /**
   * @brief 虚析构函数
   */
  virtual ~PolygonPlugins();
};

}  // namespace polygon_plugins

#endif  // POLYGON_PLUGINS__POLYGON_PLUGINS_HPP_
