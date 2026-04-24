/**
 * @file fibonacci_action_server.cpp
 * @brief 斐波那契 Action 服务器实现
 * 
 * 本文件实现了一个 ROS 2 Action 服务器，用于计算斐波那契数列。
 * 客户端可以发送一个包含 "order"（项数）的目标请求，
 * 服务器会返回斐波那契数列的前 N 项。
 */

#include <functional>                  // 标准库函数对象封装
#include <memory>                      // 智能指针支持
#include <thread>                      // 多线程支持

// ROS 2 Action 相关头文件
#include "action_tutorials_interfaces/action/fibonacci.hpp"  // Fibonacci action 定义
#include "rclcpp/rclcpp.hpp"                                 // ROS 2 节点基类
#include "rclcpp_action/rclcpp_action.hpp"                   // ROS 2 Action 客户端库
#include "rclcpp_components/register_node_macro.hpp"         // 组件注册宏

// 可见性控制头文件（用于控制符号导出）
#include "action_tutorials_cpp/visibility_control.h"

namespace action_tutorials_cpp
{
  /**
   * @class FibonacciActionServer
   * @brief 斐波那契 Action 服务器类
   * 
   * 继承自 rclcpp::Node，实现了 ROS 2 Action 服务器的所有必要回调。
   * 该服务器接收计算斐波那契数列的请求，并返回计算结果。
   */
  class FibonacciActionServer : public rclcpp::Node
  {
  public:
    /**
     * @brief 类型别名定义
     * 
     * 使用类型别名简化代码，提高可读性
     */
    using Fibonacci = action_tutorials_interfaces::action::Fibonacci;  // Fibonacci action 类型
    using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;  // 目标句柄类型

    /**
     * @brief 宏：导出类符号
     * 
     * ACTION_TUTORIALS_CPP_PUBLIC 确保该类符号可以被其他模块访问
     * 定义在 visibility_control.h 中，用于跨平台 DLL 导出/导入
     */
    ACTION_TUTORIALS_CPP_PUBLIC
    
    /**
     * @brief 构造函数
     * @param options 节点选项，默认为空
     * 
     * 创建 Action 服务器并注册三个回调函数：
     * - handle_goal: 处理新的目标请求
     * - handle_cancel: 处理取消请求
     * - handle_accepted: 处理被接受的目标
     */
    explicit FibonacciActionServer(const rclcpp::NodeOptions &options = rclcpp::NodeOptions())
        : Node("fibonacci_action_server", options)  // 调用基类构造函数，设置节点名称
    {
      using namespace std::placeholders;  // 使用占位符命名空间 _1, _2 等

      /**
       * @brief 创建 Action 服务器
       * 
       * template 参数：Action 类型 (Fibonacci)
       * 
       * @param this 指向当前节点的指针
       * @param "fibonacci" Action 的名称（话题和服务名）
       * @param handle_goal 回调：验证并接受/拒绝目标
       * @param handle_cancel 回调：处理取消请求
       * @param handle_accepted 回调：目标被接受后的处理
       */
      this->action_server_ = rclcpp_action::create_server<Fibonacci>(
          this,
          "fibonacci",
          std::bind(&FibonacciActionServer::handle_goal, this, _1, _2),    // 绑定目标处理函数
          std::bind(&FibonacciActionServer::handle_cancel, this, _1),      // 绑定取消处理函数
          std::bind(&FibonacciActionServer::handle_accepted, this, _1));  // 绑定接受处理函数
    }

  private:
    /**
     * @brief Action 服务器的智能指针
     * 
     * SharedPtr 是 rclcpp_action::Server 的共享指针类型
     * 使用智能指针自动管理内存
     */
    rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;

    /**
     * @brief 处理新目标请求的回调函数
     * @param uuid 目标的唯一标识符
     * @param goal 目标请求（包含要计算的斐波那契项数）
     * @return 目标响应（接受、拒绝或立即执行）
     * 
     * 当客户端发送新目标时调用此函数。
     * 此处简单地接受所有目标并开始执行。
     */
    rclcpp_action::GoalResponse handle_goal(
        const rclcpp_action::GoalUUID &uuid,        // 目标的 UUID（唯一标识）
        std::shared_ptr<const Fibonacci::Goal> goal)  // 目标的共享指针（只读）
    {
      // 日志输出：打印接收到的目标信息
      RCLCPP_INFO(this->get_logger(), "Received goal request with order %d", goal->order);
      
      // 避免未使用参数警告
      (void)uuid;
      
      // 返回目标响应：接受并立即执行
      return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }

    /**
     * @brief 处理取消请求的回调函数
     * @param goal_handle 要取消的目标句柄
     * @return 取消响应（接受或拒绝）
     * 
     * 当客户端发送取消请求时调用此函数。
     * 此处简单地接受所有取消请求。
     */
    rclcpp_action::CancelResponse handle_cancel(
        const std::shared_ptr<GoalHandleFibonacci> goal_handle)  // 目标的共享指针
    {
      // 日志输出：打印取消请求信息
      RCLCPP_INFO(this->get_logger(), "Received request to cancel goal");
      
      // 避免未使用参数警告
      (void)goal_handle;
      
      // 返回取消响应：接受取消
      return rclcpp_action::CancelResponse::ACCEPT;
    }

    /**
     * @brief 处理被接受目标的回调函数
     * @param goal_handle 被接受的目标句柄
     * 
     * 当目标被接受后调用此函数。
     * 由于需要在主线程快速返回以避免阻塞执行器，
     * 因此在新线程中执行实际的计算工作。
     */
    void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
      using namespace std::placeholders;  // 使用占位符命名空间
      
      // 注释：需要快速返回以避免阻塞执行器，所以启动新线程
      // 创建新线程执行 execute 函数，线程结束后自动分离
      std::thread{std::bind(&FibonacciActionServer::execute, this, _1), goal_handle}.detach();
    }

    /**
     * @brief 执行目标的具体逻辑
     * @param goal_handle 要执行的目标句柄
     * 
     * 在新线程中执行斐波那契数列计算。
     * 计算过程中会定期发布反馈（当前计算的序列），
     * 并检查是否有取消请求。
     */
    void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
      // 日志输出：开始执行目标
      RCLCPP_INFO(this->get_logger(), "Executing goal");
      
      // 创建 1Hz 的循环_rate（每秒一次）
      rclcpp::Rate loop_rate(1);
      
      // 获取目标中的请求参数（要计算的斐波那契项数）
      const auto goal = goal_handle->get_goal();
      
      // 创建反馈消息的共享指针
      auto feedback = std::make_shared<Fibonacci::Feedback>();
      
      // 获取反馈中的序列引用（用于快速访问）
      auto &sequence = feedback->partial_sequence;
      
      // 初始化斐波那契序列的前两项
      sequence.push_back(0);   // F(0) = 0
      sequence.push_back(1);   // F(1) = 1
      
      // 创建结果消息的共享指针
      auto result = std::make_shared<Fibonacci::Result>();

      /**
       * @brief 主循环：计算斐波那契数列
       * 
       * 循环条件：
       * - i < goal->order: 还没计算到指定的项数
       * - rclcpp::ok(): ROS 2 节点正常运行（未被关闭）
       */
      for (int i = 1; (i < goal->order) && rclcpp::ok(); ++i)
      {
        // 检查是否有取消请求
        if (goal_handle->is_canceling())
        {
          // 将当前计算结果设置为最终结果
          result->sequence = sequence;
          
          // 通知目标已被取消
          goal_handle->canceled(result);
          
          // 日志输出：目标已取消
          RCLCPP_INFO(this->get_logger(), "Goal canceled");
          
          // 返回，结束执行
          return;
        }
        
        // 计算下一个斐波那契数：F(i) = F(i-1) + F(i-2)
        sequence.push_back(sequence[i] + sequence[i - 1]);
        
        // 发布反馈：告诉客户端当前计算到的进度
        goal_handle->publish_feedback(feedback);
        
        // 日志输出：已发布反馈
        RCLCPP_INFO(this->get_logger(), "Publish feedback");

        // 等待直到下一次循环（1Hz）
        loop_rate.sleep();
      }

      // 检查目标是否完成（节点还在运行）
      if (rclcpp::ok())
      {
        // 将最终序列设置为结果
        result->sequence = sequence;
        
        // 通知目标已成功完成
        goal_handle->succeed(result);
        
        // 日志输出：目标成功
        RCLCPP_INFO(this->get_logger(), "Goal succeeded");
      }
    }
  }; // class FibonacciActionServer

} // namespace action_tutorials_cpp

/**
 * @brief ROS 2 组件注册宏
 * 
 * 将 FibonacciActionServer 类注册为 ROS 2 组件，
 * 使其可以通过 ROS 2 组件系统动态加载。
 * 
 * 宏展开后会将类导出为插件，供 rclcpp_components 加载
 */
RCLCPP_COMPONENTS_REGISTER_NODE(action_tutorials_cpp::FibonacciActionServer)
