<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Multi-Agent 协作系统

> 本案例详解 Multi-Agent 协作架构，实现多个智能体的协同工作

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent 协作模式                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  协作模式 (Collaboration):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │            Task                                          │   │
│  │              │                                           │   │
│  │       ┌─────┴─────┐                                     │   │
│  │       │           │                                     │   │
│  │       ▼           ▼                                     │   │
│  │   [Agent A]   [Agent B]   [Agent C]                      │   │
│  │       │           │           │                          │   │
│  │       └─────┬─────┴───────────┘                          │   │
│  │             │                                             │   │
│  │             ▼                                             │   │
│  │         [整合结果]                                        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  层级模式 (Hierarchy):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │              [Manager Agent]                              │   │
│  │                  │                                        │   │
│  │       ┌─────────┼─────────┐                              │   │
│  │       ▼         ▼         ▼                              │   │
│  │   [Worker]   [Worker]   [Worker]                          │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  辩论模式 (Debate):                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │       [Agent A] ←───────→ [Agent B]                      │   │
│  │           │                    │                         │   │
│  │           │         辩论       │                         │   │
│  │           │                    │                         │   │
│  │           └────────┬───────────┘                          │   │
│  │                    ▼                                      │   │
│  │              [Judge Agent]                                │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

代码生成 Multi-Agent 示例:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Task: "Create a web server that handles user authentication"   │
│                                                                 │
│       ┌─────────────────────────────────────────────────────┐   │
│       │               [Orchestrator Agent]                    │   │
│       │                     │                                 │   │
│       │  分解任务: 认证模块 + API 模块 + 数据库模块            │   │
│       └─────────────────────────────────────────────────────┘   │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                   │
│         ▼                 ▼                 ▼                   │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐              │
│  │   Auth     │   │    API    │   │    DB     │              │
│  │   Expert   │   │   Expert   │   │   Expert   │              │
│  └────────────┘   └────────────┘   └────────────┘              │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           ▼                                      │
│                  ┌────────────┐                                 │
│                  │ Code Review │                                 │
│                  │   Agent     │                                 │
│                  └────────────┘                                 │
│                           │                                      │
│                           ▼                                      │
│                    [Final Code]                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. Multi-Agent 协作模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **协作** | 多 Agent 共同解决子问题 | 复杂任务分解 |
| **竞争** | Agent 相互竞争 | 优化问题 |
| **层级** | Manager 分配任务给 Worker | 复杂流水线 |
| **辩论** | Agent 相互辩论，Judge 裁决 | 需要多角度分析 |

### 2. 通信协议

```python
@dataclass
class AgentMessage:
    """Agent 间消息"""
    sender: str
    receiver: str  # "all" for broadcast
    content: str
    type: str  # "request", "response", "broadcast"
    metadata: dict


class AgentCommunication:
    """Agent 通信协议"""
    
    def send(self, message: AgentMessage):
        """发送消息"""
        if message.receiver == "all":
            self.broadcast(message)
        else:
            self.direct_send(message)
    
    def broadcast(self, message: AgentMessage):
        """广播消息"""
        for agent in self.agents:
            if agent.id != message.sender:
                agent.receive(message)
    
    def receive(self, message: AgentMessage):
        """接收消息"""
        # 处理消息
        pass
```

### 3. 任务分配策略

```python
class TaskAllocator:
    """任务分配器"""
    
    def allocate(self, task: Task, agents: List[Agent]) -> Dict[Agent, SubTask]:
        """分配任务给 Agent"""
        
        # 评估 Agent 能力
        agent_capabilities = {
            agent.id: self.assess_capability(agent, task)
            for agent in agents
        }
        
        # 分解任务
        subtasks = self.decompose_task(task)
        
        # 贪心分配
        allocation = {}
        for subtask in subtasks:
            best_agent = max(
                agents,
                key=lambda a: agent_capabilities[a.id].get(subtask.type, 0)
            )
            allocation[best_agent] = subtask
        
        return allocation
```

## 💻 完整实现

### Multi-Agent 框架

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
import uuid

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    RESULT = "result"

@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    receiver: str = "all"
    content: str = ""
    type: MessageType = MessageType.REQUEST
    metadata: Dict = field(default_factory=dict)

class Agent(ABC):
    """Agent 基类"""
    
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.inbox: List[Message] = []
        self.memory: List[str] = []
    
    @abstractmethod
    def think(self, message: Message) -> str:
        """思考 - 处理消息并生成响应"""
        pass
    
    def receive(self, message: Message):
        """接收消息"""
        self.inbox.append(message)
    
    def send(self, content: str, receiver: str = "all", msg_type: MessageType = MessageType.REQUEST) -> Message:
        """发送消息"""
        return Message(
            sender=self.id,
            receiver=receiver,
            content=content,
            type=msg_type
        )
    
    def broadcast(self, content: str) -> Message:
        """广播消息"""
        return self.send(content, "all", MessageType.BROADCAST)


class MultiAgentSystem:
    """多智能体系统"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_history: List[Message] = []
    
    def register(self, agent: Agent):
        """注册 Agent"""
        self.agents[agent.id] = agent
    
    def send_message(self, message: Message):
        """发送消息"""
        self.message_history.append(message)
        
        if message.receiver == "all":
            for agent in self.agents.values():
                if agent.id != message.sender:
                    agent.receive(message)
        elif message.receiver in self.agents:
            self.agents[message.receiver].receive(message)
    
    def run(self, task: str, max_rounds: int = 5) -> str:
        """运行多 Agent 协作"""
        
        # 初始化任务
        init_message = Message(
            sender="system",
            content=task,
            type=MessageType.REQUEST
        )
        
        # 分发给所有 Agent
        self.send_message(init_message)
        
        # 消息循环
        for round in range(max_rounds):
            new_messages = []
            
            for agent in self.agents.values():
                if agent.inbox:
                    message = agent.inbox.pop(0)
                    response = agent.think(message)
                    
                    if response:
                        response_msg = agent.send(response, msg_type=MessageType.RESPONSE)
                        new_messages.append(response_msg)
            
            # 发送响应
            for msg in new_messages:
                self.send_message(msg)
        
        # 收集最终结果
        results = []
        for agent in self.agents.values():
            if agent.memory:
                results.extend(agent.memory)
        
        return "\n".join(results)
```

### 协作示例：代码生成

```python
class OrchestratorAgent(Agent):
    """编排 Agent"""
    
    def think(self, message: Message) -> str:
        if "Create" in message.content and "web server" in message.content:
            # 分解任务
            subtasks = [
                "auth_module: Implement JWT authentication",
                "api_module: Create REST API endpoints",
                "db_module: Set up database models"
            ]
            
            # 分发给专家 Agent
            for subtask in subtasks:
                self.send(subtask, receiver=subtask.split(":")[0])
            
            return "Task distributed to specialized agents"
        
        return ""


class CodeExpertAgent(Agent):
    """代码专家 Agent"""
    
    def think(self, message: Message) -> str:
        if message.type == MessageType.REQUEST:
            # 生成代码
            task = message.content.split(": ", 1)[1] if ": " in message.content else message.content
            
            code = self.generate_code(task)
            self.memory.append(f"{self.name}: {code}")
            
            # 发送回编排器
            return self.send(f"Completed: {task}\n\nCode:\n{code}", receiver="orchestrator")


class CodeReviewAgent(Agent):
    """代码审查 Agent"""
    
    def think(self, message: Message) -> str:
        if message.type == MessageType.RESPONSE:
            self.memory.append(f"Review feedback: {message.content}")
            return f"Code reviewed: {message.content[:100]}..."


def run_code_generation_system():
    """运行代码生成系统"""
    
    system = MultiAgentSystem()
    
    # 注册 Agent
    orchestrator = OrchestratorAgent("orchestrator", "Orchestrator")
    auth_expert = CodeExpertAgent("auth_module", "Auth Expert")
    api_expert = CodeExpertAgent("api_module", "API Expert")
    db_expert = CodeExpertAgent("db_module", "DB Expert")
    reviewer = CodeReviewAgent("reviewer", "Code Reviewer")
    
    for agent in [orchestrator, auth_expert, api_expert, db_expert, reviewer]:
        system.register(agent)
    
    # 运行
    result = system.run("Create a web server that handles user authentication")
    return result
```

### 使用 CrewAI

```python
from crewai import Agent, Task, Crew

# 定义 Agent
researcher = Agent(
    role="Researcher",
    goal="Research the latest AI developments",
    backstory="Expert AI researcher with 10 years experience"
)

writer = Agent(
    role="Writer",
    goal="Write engaging content about AI",
    backstory="Skilled content writer with expertise in AI"
)

# 定义任务
research_task = Task(
    description="Research the latest developments in LLM",
    agent=researcher
)

write_task = Task(
    description="Write a blog post about LLM developments",
    agent=writer,
    context=[research_task]
)

# 创建 Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process="sequential"  # 或 "hierarchical"
)

# 运行
result = crew.kickoff()
```

## 📊 Multi-Agent 应用场景

| 场景 | Agent 配置 | 效果 |
|------|-----------|------|
| 代码生成 | 分解 + 专家 + 审查 | 复杂任务分解 |
| 数据分析 | 多角色分析 + 汇总 | 多角度洞察 |
| 对话系统 | 个性化助手 + 专业顾问 | 更全面回答 |
| 游戏 | 多 NPC 智能体 | 更真实交互 |

## 📋 命令速查

```bash
# 安装 CrewAI
pip install crewai

# 运行示例
python multi_agent/crewai_example.py

# 运行自定义框架
python multi_agent/custom_framework.py
```

## 📚 学习要点

1. **任务分解**：复杂任务需要分解为子任务
2. **通信协议**：清晰的 Agent 间通信很重要
3. **层级管理**：Manager/Worker 模式适合流水线
4. **结果整合**：多个 Agent 结果需要整合

## 🔗 相关案例

- `react-agent` - ReAct Agent
- `agent-debate` - Agent 辩论系统
- `langchain-agent` - LangChain Agent
- `crewai-multi-agent` - CrewAI 多智能体框架

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
python code/main.py
```
