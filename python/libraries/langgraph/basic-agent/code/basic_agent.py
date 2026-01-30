#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangGraph基础Agent演示

这是一个简单的LangGraph Agent示例，展示如何构建一个基础的可执行Agent。
"""

import asyncio
from typing import Dict, TypedDict, Annotated, List
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END


# 定义状态结构
class AgentState(TypedDict):
    """Agent状态定义"""
    messages: Annotated[List[BaseMessage], operator.add]  # 使用operator.add来合并消息列表
    current_user_input: str
    agent_active: bool
    conversation_history: List[str]


def format_message(message: BaseMessage) -> str:
    """格式化消息以便显示"""
    if isinstance(message, HumanMessage):
        return f" 用户: {message.content}"
    elif isinstance(message, AIMessage):
        return f" Agent: {message.content}"
    else:
        return f" 系统: {message.content}"


def agent_node(state: AgentState) -> AgentState:
    """Agent节点：处理用户输入并生成响应"""
    print(f"
 Agent正在处理输入: {state['current_user_input'][:50]}...")
    
    # 这里是一个简化的Agent响应逻辑
    # 在实际应用中，这里会调用LLM或其他AI服务
    user_input = state['current_user_input'].lower()
    
    # 简单的响应逻辑
    if any(word in user_input for word in ['你好', 'hello', 'hi', 'hey']):
        response = "你好！我是LangGraph基础Agent，很高兴为你服务。我可以回答问题、提供建议或进行闲聊。你今天想聊些什么呢？"
    elif any(word in user_input for word in ['天气', 'temperature', 'weather']):
        response = "我目前无法获取实时天气信息，但建议你可以查看当地的天气预报应用或网站。如果你告诉我你的城市，我可以提供一些通用的天气建议。"
    elif any(word in user_input for word in ['再见', 'bye', 'goodbye', 'exit', 'quit']):
        response = "再见！感谢你与LangGraph基础Agent交流。如果你有其他问题，随时可以回来找我。祝你有美好的一天！"
    elif any(word in user_input for word in ['名字', 'name', '你是谁', 'who']):
        response = "我是LangGraph基础Agent，一个使用LangGraph框架构建的示例Agent。我被设计用来演示Agent的基本工作原理。"
    elif any(word in user_input for word in ['帮助', 'help', '功能', 'can you']):
        response = "我可以与你对话、回答问题、提些建议。试着问我一些问题，比如'你好'、'你能做什么？'或者告诉我你需要什么帮助。"
    else:
        response = f"我理解了你说的: '{state['current_user_input']}'。这是一个很好的话题！LangGraph是一个强大的框架，用于构建有状态的、多步骤的AI应用。我的内部使用了状态机来跟踪对话历史和上下文。"
    
    # 创建AI消息
    ai_message = AIMessage(content=response)
    
    # 更新状态
    updated_state = state.copy()
    updated_state['messages'] = [ai_message]  # 添加AI响应到消息列表
    
    # 更新对话历史
    updated_state['conversation_history'].append(f"User: {state['current_user_input']}")
    updated_state['conversation_history'].append(f"Agent: {response}")
    
    # 检查是否应该结束对话
    if any(word in user_input for word in ['再见', 'bye', 'goodbye', 'exit', 'quit']):
        updated_state['agent_active'] = False
    
    return updated_state


def user_input_node(state: AgentState) -> AgentState:
    """用户输入节点：获取用户输入"""
    print("
" + "="*50)
    user_input = input(" 请输入你的消息 (输入'quit'或'exit'退出): ")
    
    # 更新状态
    updated_state = state.copy()
    updated_state['current_user_input'] = user_input
    
    # 添加用户消息到状态
    human_message = HumanMessage(content=user_input)
    updated_state['messages'] = [human_message]
    
    # 检查是否应该结束
    if user_input.lower() in ['quit', 'exit', '再见', 'bye']:
        updated_state['agent_active'] = False
    
    return updated_state


def should_continue(state: AgentState) -> str:
    """决定下一步的函数"""
    if not state['agent_active']:
        print("
结尾 Agent会话结束。")
        return "end"
    return "agent"


def main():
    """主函数：构建并运行LangGraph Agent"""
    print(" 欢迎使用LangGraph基础Agent演示！")
    print("这个示例展示了如何使用LangGraph构建一个简单的对话Agent。")
    print("-" * 50)
    
    # 创建状态图
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("user_input", user_input_node)
    workflow.add_node("agent", agent_node)
    
    # 设置入口点
    workflow.set_entry_point("user_input")
    
    # 添加边
    workflow.add_conditional_edges(
        "user_input",  # 从用户输入节点
        should_continue,  # 条件函数
        {
            "agent": "agent",  # 如果继续，则转到agent节点
            "end": END  # 否则结束
        }
    )
    
    workflow.add_edge('agent', 'user_input')  # Agent响应后回到用户输入
    
    # 编译图形
    app = workflow.compile()
    
    # 初始状态
    initial_state = {
        "messages": [],
        "current_user_input": "",
        "agent_active": True,
        "conversation_history": []
    }
    
    # 运行Agent
    current_state = initial_state
    
    print("
🚀 启动LangGraph Agent...")
    print("提示：输入'quit'、'exit'、'再见'或'bye'来结束对话。")
    
    try:
        while current_state['agent_active']:
            # 运行直到下一个节点
            result = app.invoke(current_state)
            current_state = result
            
            # 显示最新的AI消息
            if current_state['messages']:
                last_message = current_state['messages'][-1]
                if isinstance(last_message, AIMessage):
                    print(f"
 Agent响应: {last_message.content}")

    except KeyboardInterrupt:
        print("
"
 + "
  用户中断了Agent会话。")
    except Exception as e:
        print(f"
 发生错误: {str(e)}")
    
    print(f"
 本次会话共进行了 {len(current_state['conversation_history'])} 轮对话。")
    print(" LangGraph基础Agent演示结束！")


def demo_features():
    """演示LangGraph的关键特性"""
    print("
" + "="*60)
    print(" LangGraph关键特性演示")
    print("="*60)
    
    features = [
        "1. 状态管理 - 使用TypedDict定义清晰的状态结构",
        "2. 节点定义 - 将复杂任务分解为独立的节点函数", 
        "3. 条件边 - 根据状态决定下一步的执行路径",
        "4. 循环流程 - 支持复杂的循环和分支逻辑",
        "5. 消息传递 - 在节点间传递消息和数据",
        "6. 错误处理 - 可以捕获和处理各种异常情况"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("
 提示：LangGraph特别适合构建需要记忆、规划和工具使用的复杂AI应用。")


if __name__ == "__main__":
    # 首先展示特性
    demo_features()
    
    # 然后运行主要的Agent
    main()
    
    print("
 感谢体验LangGraph基础Agent演示！")
