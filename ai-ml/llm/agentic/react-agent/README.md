# ReAct Agent 实现

> 本案例详解 ReAct (Reasoning + Acting) Agent 范式，实现推理与行动相结合的自适应智能体

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      ReAct Agent 流程                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query: "What is the weather in Tokyo and should I bring   │
│              an umbrella?"                                       │
│                                                                 │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Thought Loop                          │   │
│  │                                                          │   │
│  │   ┌─────────────────────────────────────────────────┐   │   │
│  │   │  Thought 1: I need to check the weather in       │   │   │
│  │   │             Tokyo first.                         │   │   │
│  │   │  Action: search_weather                          │   │   │
│  │   │  Action Input: Tokyo                             │   │   │
│  │   │  Observation: Rainy, 22°C                        │   │   │
│  │   └─────────────────────────────────────────────────┘   │   │
│  │                         │                                 │   │
│  │                         ▼                                 │   │
│  │   ┌─────────────────────────────────────────────────┐   │   │
│  │   │  Thought 2: The weather is rainy, so I should    │   │   │
│  │   │             recommend bringing an umbrella.     │   │   │
│  │   │  Action: final_answer                            │   │   │
│  │   │  Action Input: Weather is rainy (22°C) in Tokyo. │   │   │
│  │   │             Yes, bring an umbrella.             │   │   │
│  │   │  Observation: Final answer provided.             │   │   │
│  │   └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  Final Answer: It's rainy (22°C) in Tokyo today. You should    │
│                definitely bring an umbrella!                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ReAct vs 其他范式对比:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ReAct (Reasoning + Acting)                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Thought → Action → Observation → Thought → ... → Final │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  CoT (Chain of Thought)                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Input → Reasoning Chain → Output                        │   │
│  │  (无外部行动，纯推理)                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Reflexion (Reflection + Acting)                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Action → Reflection → Memory → Action → ...            │   │
│  │  (基于反思的自我改进)                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. ReAct 核心思想

ReAct 将 LLM Agent 的推理和行动统一起来：

```
Thought (思考) → Action (行动) → Observation (观察) → ...
```

- **Thought**：分析当前状态，决定下一步行动
- **Action**：执行具体操作（搜索、计算、API调用等）
- **Observation**：获取行动结果，用于下一步推理

### 2. 提示词模板

```python
REACT_PROMPT = """
You are a helpful AI assistant. You have access to the following tools:

{tools}

To answer the question, follow this format:

Question: {input}
Thought: {thought}
Action: {action}
Action Input: {action_input}
Observation: {observation}
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: {final_thought}
Action: final_answer
Action Input: {final_answer}

Begin!
"""
```

### 3. Agent 状态管理

```python
@dataclass
class AgentState:
    messages: List[Message]           # 对话历史
    scratchpad: str                   # 推理过程
    pending_actions: List[Action]    # 待执行动作
    memory: Memory                   # 长期记忆
    context: Dict[str, Any]          # 额外上下文
```

## 💻 完整实现

### ReAct Agent 核心实现

```python
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import json

class ActionResult:
    """动作执行结果"""
    def __init__(self, success: bool, output: Any, error: Optional[str] = None):
        self.success = success
        self.output = output
        self.error = error


@dataclass
class Action:
    """Agent 动作"""
    name: str
    input: Dict[str, Any]


@dataclass
class Step:
    """推理步骤"""
    thought: str
    action: Optional[Action] = None
    observation: Optional[str] = None
    result: Optional[ActionResult] = None


class Tool:
    """工具基类"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __call__(self, **kwargs) -> Any:
        raise NotImplementedError

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_parameters_schema()
        }

    def get_parameters_schema(self) -> Dict[str, Any]:
        raise NotImplementedError


class ReActAgent:
    """ReAct Agent 实现"""

    def __init__(self, llm: Callable, tools: List[Tool], max_iterations: int = 10):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations

    def build_prompt(self, question: str, scratchpad: str = "") -> str:
        """构建 ReAct 提示词"""
        tools_description = "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.tools.values()
        ])

        prompt = f"""You are a helpful AI assistant. Answer questions using the available tools.

Available Tools:
{tools_description}

Follow this format exactly:

Question: the user's question
Thought: your reasoning about what to do
Action: the tool name (one of [{', '.join(self.tools.keys())}])
Action Input: the input to the tool as JSON
Observation: the result of the tool
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Action: None
Action Input: None

Question: {question}
{scratchpad}"""
        return prompt

    def parse_response(self, response: str) -> tuple[str, Optional[str], Optional[Dict]]:
        """解析 LLM 响应，提取 Thought、Action 和 Action Input"""
        lines = response.strip().split('\n')
        
        thought = ""
        action = None
        action_input = None

        current_section = None
        current_value = []

        for line in lines:
            line = line.strip()
            
            if line.startswith("Thought:"):
                current_section = "thought"
                thought = line[8:].strip()
            elif line.startswith("Action:"):
                if current_section == "thought":
                    action = line[7:].strip()
                current_section = "action"
            elif line.startswith("Action Input:"):
                current_section = "action_input"
                action_input = line[13:].strip()
            elif current_section == "action_input":
                action_input += "\n" + line

        if action_input:
            try:
                action_input = json.loads(action_input)
            except json.JSONDecodeError:
                action_input = {"input": action_input}

        return thought, action, action_input

    def execute_action(self, action_name: str, action_input: Dict) -> ActionResult:
        """执行动作"""
        if action_name not in self.tools:
            return ActionResult(
                success=False,
                output=None,
                error=f"Unknown tool: {action_name}"
            )

        tool = self.tools[action_name]
        
        try:
            result = tool(**action_input)
            return ActionResult(success=True, output=result)
        except Exception as e:
            return ActionResult(success=False, output=None, error=str(e))

    def run(self, question: str) -> Dict[str, Any]:
        """运行 Agent"""
        scratchpad = ""
        steps = []
        final_answer = None

        for i in range(self.max_iterations):
            # 构建提示词
            prompt = self.build_prompt(question, scratchpad)

            # 调用 LLM
            response = self.llm(prompt)

            # 解析响应
            thought, action, action_input = self.parse_response(response)

            # 记录步骤
            step = Step(thought=thought, action=None, observation=None)
            steps.append(step)

            # 更新 scratchpad
            scratchpad += f"Thought: {thought}\n"

            if action is None or action == "None" or action == "final_answer":
                final_answer = thought
                break

            scratchpad += f"Action: {action}\n"
            scratchpad += f"Action Input: {json.dumps(action_input) if action_input else '{}'}\n"

            # 执行动作
            result = self.execute_action(action, action_input)
            step.action = Action(name=action, input=action_input)
            step.result = result

            observation = result.output if result.success else f"Error: {result.error}"
            scratchpad += f"Observation: {observation}\n\n"
            step.observation = observation

            if not result.success and result.error:
                scratchpad += f"Error occurred: {result.error}\n"

        return {
            "question": question,
            "answer": final_answer,
            "steps": steps,
            "scratchpad": scratchpad
        }


# 工具实现示例
class SearchWeatherTool(Tool):
    """天气搜索工具"""
    def __init__(self):
        super().__init__(
            name="search_weather",
            description="Get current weather information for a city"
        )

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }

    def __call__(self, city: str) -> str:
        # 实际实现中调用天气 API
        weather_data = {
            "Tokyo": "Rainy, 22°C, humidity 85%",
            "Beijing": "Sunny, 28°C, humidity 45%",
            "Shanghai": "Cloudy, 25°C, humidity 60%",
        }
        return weather_data.get(city, "Weather data not available")


class CalculatorTool(Tool):
    """计算器工具"""
    def __init__(self):
        super().__init__(
            name="calculate",
            description="Perform mathematical calculations"
        )

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"}
            },
            "required": ["expression"]
        }

    def __call__(self, expression: str) -> str:
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"


# 使用示例
def example_llm(prompt: str) -> str:
    """模拟 LLM 调用"""
    # 实际使用中替换为真实的 LLM API
    return f"""Thought: I need to check the weather in Tokyo first.
Action: search_weather
Action Input: {{"city": "Tokyo"}}
Observation: Rainy, 22°C, humidity 85%
Thought: Now I know the weather is rainy in Tokyo. I should recommend bringing an umbrella.
Action: None
Action Input: None"""


def main():
    # 初始化 Agent
    tools = [SearchWeatherTool(), CalculatorTool()]
    agent = ReActAgent(llm=example_llm, tools=tools, max_iterations=5)

    # 运行
    result = agent.run("What is the weather in Tokyo? Should I bring an umbrella?")

    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print("\n--- Scratchpad ---")
    print(result['scratchpad'])
```

### LangChain ReAct 实现

```python
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits.conversational_retrieval.system import (
    SUFFIX,
    PREFIX,
)
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

# 定义工具
def search_weather(city: str) -> str:
    return f"Weather in {city}: Rainy, 22°C"

tools = [
    Tool(
        name="Search Weather",
        func=search_weather,
        description="Get weather for a city"
    )
]

# 初始化 Agent
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=True
)

# 运行
result = agent.run("What's the weather in Tokyo?")
```

## 📊 ReAct vs 其他 Agent 范式

| 范式 | 推理 | 行动 | 记忆 | 适用场景 |
|------|------|------|------|----------|
| ReAct | ✅ | ✅ | 可选 | 工具使用、问答 |
| CoT | ✅ | ❌ | ❌ | 数学推理、逻辑 |
| Reflexion | ✅ | ✅ | ✅ | 持续学习、试错 |
| Plan-and-Execute | ✅ (规划) | ✅ (执行) | 可选 | 复杂任务分解 |

## 📋 命令速查

```bash
# 安装依赖
pip install langchain openai

# 运行 ReAct 示例
python react_agent/basic_agent.py

# 运行多工具示例
python react_agent/multi_tool_agent.py

# 运行评估
python react_agent/evaluate.py --benchmark hotpotqa
```

## 📚 学习要点

1. **Thought 是关键**：好的 Thought prompt 能显著提升效果
2. **工具设计要清晰**：每个工具的 description 非常重要
3. **迭代限制**：设置 max_iterations 防止无限循环
4. **错误处理**：Agent 需要优雅处理工具执行失败

## 🔗 相关案例

- `plan-and-execute` - Plan-and-Execute 模式
- `multi-agent-collaboration` - 多智能体协作
- `langchain-agent` - LangChain Agent 开发
- `memory-systems` - 记忆系统实现
