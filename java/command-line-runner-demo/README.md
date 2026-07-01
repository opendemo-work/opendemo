<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# CommandLineRunner 启动任务演示

> 深入理解 Spring Boot CommandLineRunner 接口，掌握启动任务、参数解析和退出码控制

## 🎯 学习目标

- ✅ 理解 CommandLineRunner 的执行时机
- ✅ 掌握 @Order 控制多个 Runner 执行顺序
- ✅ 学会命令行参数的接收和解析
- ✅ 了解 CommandLineRunner 与 ApplicationRunner 的区别

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **CommandLineRunner** | Spring Boot 启动完成后执行的函数式接口 |
| **run(String... args)** | 接收原始命令行参数字符串数组 |
| **@Order** | 控制多个 Runner 的执行优先级 |
| **ExitCodeGenerator** | 自定义应用退出码接口 |

---

## 🛠️ CommandLineRunner 执行流程

```
┌──────────────────────────────────────────────┐
│           Spring Boot 启动流程                │
├──────────────────────────────────────────────┤
│                                              │
│  1. 创建 SpringApplication                   │
│       ↓                                      │
│  2. 准备 Environment                         │
│       ↓                                      │
│  3. 创建 ApplicationContext                  │
│       ↓                                      │
│  4. Bean 创建和依赖注入                       │
│       ↓                                      │
│  5. ★ 执行 CommandLineRunner                 │
│       ↓                                      │
│  6. 应用就绪 (ApplicationReadyEvent)          │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. StartupRunner - 参数打印

```java
@Component
@Order(1)
public class StartupRunner implements CommandLineRunner {

    @Override
    public void run(String... args) {
        logger.info("=== CommandLineRunner 启动任务 ===");
        logger.info("参数数量: {}", args.length);
        for (String arg : args) {
            logger.info("参数: {}", arg);
        }
    }
}
```

### 2. TaskRunner - 系统检查

```java
@Component
@Order(2)
public class TaskRunner implements CommandLineRunner {

    @Override
    public void run(String... args) {
        logger.info("=== 系统检查任务开始 ===");
        checkSystemProperties();
        checkRuntimeInfo();

        if (args.length > 0 && "--health-check".equals(args[0])) {
            performHealthCheck();
        }
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/command-line-runner-demo
mvn spring-boot:run
```

### 2. 带参数启动

```bash
# 传递命令行参数
mvn spring-boot:run -Dspring-boot.run.arguments="--env=prod input.txt --debug"

# 指定健康检查
mvn spring-boot:run -Dspring-boot.run.arguments="--health-check"

# 打包后运行
java -jar target/command-line-runner-demo-1.0-SNAPSHOT.jar arg1 arg2
```

### 3. 观察启动日志

```
=== CommandLineRunner 启动任务 ===
参数数量: 2
参数: --env=prod
参数: input.txt
=== 启动任务完成 ===
=== 系统检查任务开始 ===
Java版本: 11.0.20
操作系统: Mac OS X 13.5.2
可用处理器: 8
总内存: 256MB
已用内存: 32MB
=== 系统检查任务完成 ===
```

---

## 📁 项目结构

```
command-line-runner-demo/
├── src/main/java/com/example/demo/
│   ├── CommandLineApplication.java     # 应用入口
│   ├── StartupRunner.java              # 启动参数打印 (Order=1)
│   └── TaskRunner.java                 # 系统检查任务 (Order=2)
├── src/test/java/com/example/demo/
│   └── CommandLineRunnerDemoTest.java  # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 CommandLineRunner vs ApplicationRunner

| 特性 | CommandLineRunner | ApplicationRunner |
|------|-------------------|-------------------|
| 参数类型 | `String...` | `ApplicationArguments` |
| 参数解析 | 需手动解析 | 自动区分选项/普通参数 |
| 适用场景 | 简单参数处理 | 需要参数类型区分 |
| 复杂度 | 简单 | 稍复杂 |

---

## 🔧 常见使用场景

| 场景 | 说明 |
|------|------|
| 系统信息打印 | 启动时打印 Java 版本、内存等信息 |
| 健康检查 | 启动后验证外部服务可用性 |
| 数据导入 | 从文件导入初始数据 |
| 参数模式 | 根据参数执行不同逻辑 |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [ApplicationRunner Demo](../application-runner-demo/) - 更强大的启动任务接口

---

*最后更新：2026年4月*

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
