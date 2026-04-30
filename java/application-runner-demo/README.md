# ApplicationRunner 启动任务演示

> 深入理解 Spring Boot ApplicationRunner 接口的使用，掌握启动初始化、顺序控制和参数解析

## 🎯 学习目标

- ✅ 理解 ApplicationRunner 的执行时机和作用
- ✅ 掌握 @Order 注解控制 Runner 执行顺序
- ✅ 学会解析 ApplicationArguments 的各类参数
- ✅ 了解 ApplicationRunner 与 CommandLineRunner 的区别

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **ApplicationRunner** | Spring Boot 启动后执行的接口，接收 ApplicationArguments |
| **@Order** | 控制多个 Runner 的执行顺序，数值越小优先级越高 |
| **ApplicationArguments** | 封装启动参数，提供类型安全的参数访问 |
| **NonOptionArgs** | 无选项前缀的普通参数 |
| **OptionArgs** | 带 `--` 前缀的选项参数 |

---

## 🛠️ ApplicationRunner vs CommandLineRunner

| 特性 | ApplicationRunner | CommandLineRunner |
|------|-------------------|-------------------|
| 参数类型 | ApplicationArguments | String... |
| 参数解析 | 区分选项参数和普通参数 | 原始字符串数组 |
| 推荐场景 | 需要参数解析的初始化任务 | 简单的启动任务 |
| 执行时机 | ApplicationContext 刷新后 | ApplicationContext 刷新后 |

---

## 💻 核心代码

### 1. 数据初始化 Runner

```java
@Component
@Order(1)
public class DataInitializationRunner implements ApplicationRunner {

    private final DataService dataService;

    @Override
    public void run(ApplicationArguments args) {
        logger.info("=== 数据初始化开始 ===");
        dataService.put("config.theme", "dark");
        dataService.put("config.language", "zh-CN");

        if (args.containsOption("env")) {
            String env = args.getOptionValues("env").get(0);
            dataService.put("config.env", env);
        }
        logger.info("=== 数据初始化完成 ===");
    }
}
```

### 2. 缓存预热 Runner

```java
@Component
@Order(2)
public class CacheWarmUpRunner implements ApplicationRunner {

    @Override
    public void run(ApplicationArguments args) {
        logger.info("=== 缓存预热开始 ===");
        for (Map.Entry<String, String> entry : dataService.getAll().entrySet()) {
            logger.info("缓存加载: {} = {}", entry.getKey(), entry.getValue());
        }

        // 解析并打印启动参数
        logger.info("普通参数: {}", args.getNonOptionArgs());
        logger.info("选项参数: {}", args.getOptionNames());
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/application-runner-demo
mvn spring-boot:run
```

### 2. 带参数启动

```bash
# 指定环境参数
mvn spring-boot:run -Dspring-boot.run.arguments="--env=prod --debug"

# 使用 jar 包带参数启动
java -jar target/application-runner-demo-1.0-SNAPSHOT.jar --env=prod input.txt
```

### 3. 观察启动日志

```
=== 数据初始化开始 ===
初始化数据条数: 5
环境参数设置: env=prod
=== 数据初始化完成 ===
=== 缓存预热开始 ===
缓存加载: config.theme = dark
缓存加载: config.language = zh-CN
缓存预热条数: 6
=== 缓存预热完成 ===
普通参数: [input.txt]
选项参数: [env, debug]
  --env = [prod]
  --debug = []
```

---

## 📁 项目结构

```
application-runner-demo/
├── src/main/java/com/example/demo/
│   ├── RunnerApplication.java              # 应用入口
│   ├── DataInitializationRunner.java       # 数据初始化 Runner (Order=1)
│   ├── CacheWarmUpRunner.java              # 缓存预热 Runner (Order=2)
│   └── service/
│       └── DataService.java                # 数据服务
├── src/test/java/com/example/demo/
│   └── ApplicationRunnerDemoTest.java      # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 ApplicationArguments API

| 方法 | 说明 | 示例 |
|------|------|------|
| `getOptionNames()` | 获取所有选项参数名 | `[env, debug]` |
| `getOptionValues(name)` | 获取指定选项的值 | `env → [prod]` |
| `getNonOptionArgs()` | 获取普通参数列表 | `[input.txt]` |
| `containsOption(name)` | 判断是否包含某选项 | `true/false` |
| `getSourceArgs()` | 获取原始参数数组 | `String[]` |

---

## 🔧 使用场景

| 场景 | 说明 |
|------|------|
| 数据预加载 | 启动时从数据库/文件加载基础数据 |
| 缓存预热 | 预先加载热点数据到缓存 |
| 配置校验 | 验证必要配置是否存在 |
| 资源初始化 | 初始化连接池、线程池等 |
| 健康检查 | 启动后检查外部依赖是否可用 |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [CommandLineRunner Demo](../command-line-runner-demo/) - 另一种启动任务方式
- [Spring Bean Lifecycle](../spring-bean-lifecycle-demo/) - Bean 生命周期

---

*最后更新：2026年4月*
