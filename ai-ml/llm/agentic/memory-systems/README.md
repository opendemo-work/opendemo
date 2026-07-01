<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Memory Systems 记忆系统

> 本案例详解 Agent 记忆系统：短期记忆、长期记忆、语义记忆

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Memory 架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Working Memory                         │   │
│  │                   (当前上下文)                           │   │
│  │                                                          │   │
│  │   Conversation History ──▶ Current Session Context       │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Episodic Memory                           │   │
│  │                 (情景记忆)                                │   │
│  │                                                          │   │
│  │   [Episode 1] [Episode 2] [Episode 3] ...               │   │
│  │   每次重要交互作为一个 episode                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Semantic Memory                           │   │
│  │                 (语义记忆)                                │   │
│  │                                                          │   │
│  │   Facts ──▶ Concepts ──▶ Knowledge Graph                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### 记忆管理器

```python
class MemoryManager:
    def __init__(self):
        self.working_memory = []  # 当前上下文
        self.episodic_memory = []  # 历史 episodes
        self.semantic_memory = {}  # 知识图谱
    
    def add_working(self, item):
        self.working_memory.append(item)
        if len(self.working_memory) > MAX_WORKING_SIZE:
            # 压缩到 episodic
            self.compress_to_episode()
    
    def compress_to_episode(self):
        """将工作记忆压缩到情景记忆"""
        if self.working_memory:
            episode = {
                "content": self.working_memory.copy(),
                "timestamp": datetime.now()
            }
            self.episodic_memory.append(episode)
            self.working_memory = []
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Any]:
        """检索记忆"""
        # 结合 working + episodic + semantic
        pass
```

## 🔗 相关案例

- `react-agent` - ReAct Agent
- `plan-and-execute` - Plan-and-Execute
- `multi-agent-collaboration` - Multi-Agent

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/main.py
```
