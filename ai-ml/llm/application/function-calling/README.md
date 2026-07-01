<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Function Calling 工具调用

> 本案例详解 LLM Function Calling 能力，实现模型调用外部工具和 API

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Function Calling 流程                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User: "What's the weather in Tokyo and should I take an umbrella?"
│                                                                 │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   LLM Decision                            │   │
│  │                                                          │   │
│  │   分析用户意图 → 需要调用天气 API                           │   │
│  │                                                          │   │
│  │   决定调用: get_weather(city="Tokyo")                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Function Call Output                         │   │
│  │                                                          │   │
│  │   {                                                      │   │
│  │     "name": "get_weather",                              │   │
│  │     "arguments": {"city": "Tokyo"}                      │   │
│  │   }                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               External Execution                          │   │
│  │                                                          │   │
│  │   执行 get_weather(city="Tokyo")                        │   │
│  │   返回: {"temperature": 22, "condition": "rainy"}       │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Final Response                              │   │
│  │                                                          │   │
│  │   "Tokyo is rainy with a temperature of 22°C.            │   │
│  │    Yes, you should bring an umbrella!"                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Function Calling vs 普通 Prompt:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  普通 Prompt (不可靠):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  User: What weather in Tokyo?                           │   │
│  │  LLM: I don't have real-time weather data...            │   │
│  │  (可能编造或拒绝)                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Function Calling (可靠):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  User: What weather in Tokyo?                           │   │
│  │  LLM: get_weather(city="Tokyo")  ← 结构化输出           │   │
│  │                                                          │   │
│  │  [执行函数] → 结果                                        │   │
│  │                                                          │   │
│  │  LLM: Tokyo is rainy, 22°C. Take an umbrella!            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. Function Calling 工作流程

```
1. User Query → LLM 分析意图
2. LLM → 选择函数并生成参数 (JSON)
3. 执行函数 → 获取结果
4. 结果 + 原问题 → LLM 生成最终回答
```

### 2. Function Schema 定义

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "City name"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "default": "celsius"
      }
    },
    "required": ["city"]
  }
}
```

### 3. 支持的模型

| 模型 | Function Calling | 多函数调用 |
|------|-----------------|------------|
| GPT-4 | ✅ | ✅ |
| GPT-3.5 | ✅ | ❌ |
| Claude 3 | ✅ | ✅ |
| Gemini Pro | ✅ | ✅ |
| Mistral | ✅ | ✅ |
| Qwen | ✅ | ✅ |

## 💻 完整实现

### OpenAI Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "celsius"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol"
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

def call_function(name: str, arguments: dict) -> str:
    """执行函数调用"""
    if name == "get_weather":
        return get_weather(**arguments)
    elif name == "get_stock_price":
        return get_stock_price(**arguments)
    else:
        return f"Unknown function: {name}"

def get_weather(city: str, unit: str = "celsius") -> str:
    """模拟天气 API"""
    weather_data = {
        "Tokyo": {"temp": 22, "condition": "rainy"},
        "Beijing": {"temp": 28, "condition": "sunny"},
        "Shanghai": {"temp": 25, "condition": "cloudy"}
    }
    data = weather_data.get(city, {"temp": 20, "condition": "unknown"})
    return json.dumps(data)

def get_stock_price(symbol: str) -> str:
    """模拟股票 API"""
    prices = {"AAPL": 175.5, "GOOGL": 140.2, "MSFT": 380.0}
    price = prices.get(symbol, 100.0)
    return json.dumps({"symbol": symbol, "price": price})

def chat_with_functions(user_message: str):
    """带 Function Calling 的对话"""
    
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        # 第一次调用 - LLM 决定调用函数
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        messages.append(assistant_message)
        
        # 检查是否需要调用函数
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # 执行函数
                result = call_function(function_name, arguments)
                
                # 添加函数结果
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # 第二次调用 - LLM 生成最终回答
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                tools=tools
            )
            
            return response.choices[0].message.content
        
        else:
            # 没有函数调用，直接返回
            return assistant_message.content


# 使用示例
result = chat_with_functions("What's the weather in Tokyo? Should I bring an umbrella?")
print(result)
```

### LangChain Function Calling

```python
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentType, initialize_agent

# 定义工具
@tool
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return f"Weather in {city}: 22°C, rainy"

@tool
def get_stock(symbol: str) -> str:
    """Get stock price"""
    return f"{symbol}: $175.50"

# 初始化 agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [get_weather, get_stock]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 运行
result = agent.run("What's the weather in Tokyo and AAPL stock price?")
```

### 多函数调用

```python
# GPT-4 可以一次调用多个函数
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages,
    tools=tools,
)

# 处理多个函数调用
for tool_call in response.choices[0].message.tool_calls:
    # 并行执行所有函数
    pass
```

## 📊 Function Calling 评估

| 指标 | 说明 |
|------|------|
| Function Selection Accuracy | 正确选择函数的准确率 |
| Argument Accuracy | 参数提取的准确率 |
| Execution Success | 函数执行成功率 |
| End-to-End Accuracy | 端到端任务完成率 |

## 📋 命令速查

```bash
# 测试 OpenAI Function Calling
python function_calling/openai_example.py

# 测试 LangChain
python function_calling/langchain_example.py

# 运行评估
python function_calling/evaluate.py --benchmark function_calls
```

## 📚 学习要点

1. **Schema 设计**：清晰描述函数功能，帮助 LLM 理解
2. **参数验证**：LLM 可能生成无效参数，需要验证
3. **错误处理**：函数执行可能失败，需要优雅处理
4. **多轮对话**：复杂任务可能需要多次函数调用

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础架构
- `react-agent` - ReAct Agent
- `tool-schema-design` - 工具 Schema 设计
- `multi-tool-orchestration` - 多工具编排

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
