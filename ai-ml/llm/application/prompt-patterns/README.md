# Prompt Patterns 高级模式

> 本案例详解高级 Prompt Engineering 模式，提升 LLM 输出质量

## 📐 核心模式

### 1. Chain of Verification

```
Initial Response → Verification Questions → Refined Response
```

### 2. Template System

```python
class PromptTemplate:
    def __init__(self, template: str):
        self.template = template
    
    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

# 示例
template = PromptTemplate("""
You are a {role}.
Context: {context}
Task: {task}
Format: {format}
""")

prompt = template.format(
    role="Python expert",
    context="The user is learning programming",
    task="Explain decorators",
    format="Include code examples and explanation"
)
```

## 🔗 相关案例

- `chain-of-thought` - 思维链
- `prompt-engineering` - Prompt 工程基础
