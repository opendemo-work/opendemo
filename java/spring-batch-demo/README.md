# Spring Batch 演示

## 学习目标

1. 掌握 Spring Batch 核心组件
2. 理解 Job、Step、Chunk 概念
3. 学会实现数据批处理任务
4. 掌握 Job 启动和监控

## 环境要求

- JDK 17+
- Maven 3.9+
- 数据库 (H2 内存数据库)

## 核心组件

```
Job
├── Step 1 (ItemReader → ItemProcessor → ItemWriter)
├── Step 2
└── Step 3
```

## 快速开始

```bash
cd spring-batch-demo
mvn spring-boot:run
# 触发 Job: POST /jobs/run
```

## 使用场景

- 数据迁移
- 报表生成
- 定时同步任务
- 大文件处理

---

**技术栈**: Spring Boot 3.2 | Spring Batch 5.x

**版本**: 1.0.0