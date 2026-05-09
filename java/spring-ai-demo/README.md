# Spring AI 演示

## 学习目标

1. 掌握 Spring AI 核心概念
2. 理解 ChatClient 使用方法
3. 学会实现 RAG (检索增强生成)
4. 掌握多模态 AI 集成

## 环境要求

- JDK 17+
- Maven 3.9+
- OpenAI API Key 或兼容的 LLM

## 核心功能

### 1. ChatClient

```java
@Service
public class AiService {
    private final ChatClient chatClient;

    public AiService(ChatClient.Builder builder) {
        this.chatClient = builder.defaultSystem("你是OpenDemo的AI助手").build();
    }

    public String ask(String question) {
        return chatClient.prompt()
            .user(question)
            .call()
            .content();
    }
}
```

### 2. RAG (检索增强生成)

```
用户问题 → 向量数据库检索 → 上下文注入 → LLM → 回答
```

## 快速开始

```bash
# 设置 API Key
export OPENAI_API_KEY=sk-xxxx

cd spring-ai-demo
mvn spring-boot:run
```

## API 端点

```bash
# 聊天接口
POST /api/chat
{"message": "解释Spring Boot 3的新特性"}

# 文档问答
POST /api/rag
{"question": "Spring Boot 3有哪些新特性？", "documentId": "doc123"}
```

---

**技术栈**: Spring Boot 3.2 | Spring AI | OpenAI | Vector DB

**版本**: 1.0.0