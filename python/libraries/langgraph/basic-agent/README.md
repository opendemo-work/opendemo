# LangGraph基础Agent演示

一个使用LangGraph框架构建的基础Agent示例，展示了如何创建一个简单的对话Agent。

##  功能说明

- **状态管理**: 使用TypedDict定义清晰的状态结构
- **节点定义**: 将复杂任务分解为独立的节点函数
- **条件边**: 根据状态决定下一步的执行路径
- **循环流程**: 支持复杂的循环和分支逻辑
- **消息传递**: 在节点间传递消息和数据
- **错误处理**: 可以捕获和处理各种异常情况

##  快速开始

### 1. 安装依赖

`ash
pip install -r requirements.txt
`

### 2. 运行Demo

`ash
python code/basic_agent.py
`

##  代码结构

`
basic-agent/
 README.md          # 说明文档
 requirements.txt   # 依赖项
 code/
    basic_agent.py # 主程序
 metadata.json      # 元数据
`

##  核心组件

### AgentState
定义了Agent的状态结构，包括：
- messages: 消息列表
- current_user_input: 当前用户输入
- gent_active: Agent是否活跃
- conversation_history: 对话历史

### 节点函数
- user_input_node: 处理用户输入
- gent_node: Agent逻辑处理
- should_continue: 决定是否继续

##  使用示例

运行程序后，你可以输入各种消息与Agent交互：
- 输入"你好"来打招呼
- 输入"帮助"来了解Agent功能
- 输入"再见"来结束对话

##  应用场景

LangGraph特别适合构建需要记忆、规划和工具使用的复杂AI应用，如：
- 多步骤任务处理Agent
- 需要长期记忆的对话系统
- 工作流自动化Agent
- 复杂决策流程

##  参考资料

- [LangGraph官方文档](https://langchain-ai.github.io/langgraph/)
- [LangChain Core](https://python.langchain.com/docs/langgraph)
