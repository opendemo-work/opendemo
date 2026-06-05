# Promptfoo 自动化评估

> 本案例详解 Promptfoo 工具，自动化 Prompt 评估与优化

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Promptfoo 工作流                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  promptfooconfig.yaml                                           │
│       │                                                         │
│       ├── Providers (OpenAI, Anthropic, Local)                 │
│       ├── Prompts (多个 prompt 变体)                           │
│       ├── Tests (评估用例)                                      │
│       └── Asserts (断言)                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心配置

```yaml
# promptfooconfig.yaml
prompts:
  - "Prompt A: {query}"
  - "Prompt B: {query}"

providers:
  - openai:gpt-4

tests:
  - vars:
      query: "What is Python?"
    assert:
      - type: contains
        value: "programming"

  - vars:
      query: "Hello"
    assert:
      - type: not-contains
        value: "Sorry"
```

## 🔗 相关案例

- `lm-evaluation-harness` - LM-Eval Harness
- `llm-testing-framework` - 测试框架
