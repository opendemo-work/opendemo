# Schedule Task Demo - Spring Boot 定时任务

> Spring Boot 定时任务实战：@Scheduled 注解、Cron 表达式、fixedRate/fixedDelay、SchedulingConfigurer 编程式调度

## 目录

- [核心概念](#核心概念)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [启用定时任务](#启用定时任务)
- [@Scheduled 注解详解](#scheduled-注解详解)
- [fixedRate vs fixedDelay](#fixedrate-vs-fixeddelay)
- [Cron 表达式详解](#cron-表达式详解)
- [SchedulingConfigurer 编程式配置](#schedulingconfigurer-编程式配置)
- [异步定时任务](#异步定时任务)
- [测试接口](#测试接口)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

## 核心概念

### 什么是 Spring 定时任务？

Spring 框架内置了定时任务调度功能，通过 `@Scheduled` 注解可以将方法标记为定时执行的任务，无需引入 Quartz 等外部框架。

### 适用场景

| 场景 | 示例 |
|------|------|
| 数据同步 | 每天凌晨同步第三方数据 |
| 缓存刷新 | 每5分钟刷新热门数据缓存 |
| 状态检查 | 每10秒检查服务健康状态 |
| 报表生成 | 每周一自动生成周报 |
| 数据清理 | 每月清理过期的临时文件 |
| 消息重试 | 每30秒重试失败的消息 |

### 调度模型对比

```
fixedRate:  |----任务----|  |----任务----|  |----任务----|
            ^            ^               ^
            |5000ms      |5000ms         |5000ms
            (从开始计时，不管任务是否完成)

fixedDelay: |----任务----|  |----任务----|  |----任务----|
                         ^^
                         ||
                    5000ms (等上一个任务完成后才开始计时)
```

## 技术栈

- Java 11+
- Spring Boot 2.7.14
- Spring Web (spring-boot-starter-web)
- JUnit 5 + Spring Boot Test

## 项目结构

```
schedule-task-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/main/java/com/example/demo/
    ├── ScheduleTaskApplication.java        # 启动类 (@EnableScheduling)
    ├── config/
    │   └── SchedulingConfig.java           # SchedulingConfigurer 编程式配置
    ├── task/
    │   ├── ScheduledTasks.java             # @Scheduled 定时任务集合
    │   └── DynamicScheduleTask.java        # 动态 Cron 定时任务
    └── controller/
        └── ScheduleController.java         # 手动触发/查询任务状态
```

## 快速开始

```bash
# 编译项目
mvn clean package

# 运行项目
mvn spring-boot:run

# 运行测试
mvn test
```

应用启动后，定时任务会自动开始执行，观察控制台日志输出。

## 启用定时任务

在启动类上添加 `@EnableScheduling` 注解：

```java
@SpringBootApplication
@EnableScheduling
public class ScheduleTaskApplication {
    public static void main(String[] args) {
        SpringApplication.run(ScheduleTaskApplication.class, args);
    }
}
```

> `@EnableScheduling` 会注册一个 `TaskScheduler` Bean，负责调度所有 `@Scheduled` 方法。

## @Scheduled 注解详解

### 支持的属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `fixedRate` | long | 固定频率（毫秒），从任务开始计时 |
| `fixedDelay` | long | 固定延迟（毫秒），从任务结束计时 |
| `fixedRateString` | String | 同 fixedRate，支持配置文件占位符 |
| `fixedDelayString` | String | 同 fixedDelay，支持配置文件占位符 |
| `cron` | String | Cron 表达式 |
| `initialDelay` | long | 首次执行前的延迟（毫秒） |
| `zone` | String | Cron 表达式使用的时区 |

### 属性互斥规则

`fixedRate`、`fixedDelay`、`cron` 三者只能选择其一，不能同时使用。

## fixedRate vs fixedDelay

### fixedRate（固定频率）

不管上一次任务是否执行完成，固定间隔时间后开始下一次执行。

```java
@Scheduled(fixedRate = 5000)
public void fixedRateTask() {
    // 每5秒执行一次（从开始时间计时）
}
```

**时间线**：
```
0s      5s      10s     15s
|执行|  |执行|  |执行|  |执行|
```

### fixedDelay（固定延迟）

上一次任务执行完成后，等待固定延迟时间再开始下一次执行。

```java
@Scheduled(fixedDelay = 10000)
public void fixedDelayTask() {
    // 任务完成后等待10秒再执行
}
```

**时间线**：
```
|执行3s| 等10s |执行2s| 等10s |执行4s|
```

### 对比总结

| 特性 | fixedRate | fixedDelay |
|------|-----------|------------|
| 计时起点 | 任务开始时间 | 任务结束时间 |
| 任务重叠 | 可能发生 | 不会发生 |
| 适用场景 | 轻量级周期任务 | 耗时不定的任务 |
| 精确性 | 频率精确 | 间隔精确 |

### initialDelay（初始延迟）

配合 `fixedRate` 或 `fixedDelay` 使用，首次执行前等待指定时间：

```java
@Scheduled(fixedRate = 5000, initialDelay = 10000)
public void delayedTask() {
    // 应用启动后等10秒首次执行，之后每5秒执行一次
}
```

## Cron 表达式详解

### 格式

Spring Cron 表达式由 6 个字段组成：

```
秒  分  时  日  月  周
 ┃   ┃   ┃   ┃   ┃   ┃
 ┃   ┃   ┃   ┃   ┃   └─ 星期几 (0-7, 0和7都是周日)
 ┃   ┃   ┃   ┃   └───── 月份 (1-12)
 ┃   ┃   ┃   └───────── 日期 (1-31)
 ┃   ┃   └───────────── 小时 (0-23)
 ┃   └───────────────── 分钟 (0-59)
 └───────────────────── 秒 (0-59)
```

### 特殊字符

| 字符 | 含义 | 示例 |
|------|------|------|
| `*` | 任意值 | `* * * * * ?` 每秒 |
| `?` | 不指定（日/周互斥） | 日和周不能同时指定 |
| `-` | 范围 | `1-5` 表示 1 到 5 |
| `,` | 枚举 | `MON,WED,FRI` |
| `/` | 步长 | `0/5` 从0开始每5单位 |
| `L` | 最后 | `L` 在日中表示月末 |
| `W` | 工作日 | `15W` 离15号最近的工作日 |
| `#` | 第几个 | `6#3` 第3个周五 |

### 常用 Cron 表达式

| 表达式 | 说明 |
|--------|------|
| `0 0 * * * ?` | 每小时整点 |
| `0 */5 * * * ?` | 每5分钟 |
| `0 0 */2 * * ?` | 每2小时 |
| `0 0 12 * * ?` | 每天12:00 |
| `0 0 0 * * ?` | 每天00:00 |
| `0 0 12 * * MON` | 每周一12:00 |
| `0 0 12 1 * ?` | 每月1号12:00 |
| `0 0 12 1 1 ?` | 每年1月1日12:00 |
| `0 0/30 9-17 * * ?` | 工作时间每30分钟 |

### 与 Unix Cron 的区别

Spring Cron 有 **6 个字段**（包含秒），Unix Cron 只有 **5 个字段**（最小粒度为分钟）。

## SchedulingConfigurer 编程式配置

当需要动态调整 Cron 表达式时，可以实现 `SchedulingConfigurer` 接口：

```java
@Configuration
public class SchedulingConfig implements SchedulingConfigurer {

    @Override
    public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
        taskRegistrar.addFixedRateTask(() -> {
            System.out.println("[编程式] 固定频率任务执行");
        }, Duration.ofSeconds(30));
    }
}
```

### 配置线程池

默认情况下，所有 `@Scheduled` 任务共用一个单线程执行器。如果某个任务执行时间较长，会阻塞其他任务。通过 `SchedulingConfigurer` 可以配置线程池：

```java
@Override
public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
    taskRegistrar.setScheduler(taskExecutor());
}

@Bean(destroyMethod = "shutdown")
public ScheduledExecutorService taskExecutor() {
    return Executors.newScheduledThreadPool(4);
}
```

## 异步定时任务

当定时任务执行时间较长时，建议使用 `@Async` 异步执行：

```java
@Async
@Scheduled(fixedRate = 5000)
public void asyncTask() {
    // 异步执行，不阻塞其他定时任务
}
```

> 使用 `@Async` 需要在启动类上添加 `@EnableAsync` 注解。

## 测试接口

```bash
# 查看定时任务状态
curl http://localhost:8080/schedule/status

# 手动触发任务
curl -X POST http://localhost:8080/schedule/trigger

# 查看任务执行历史
curl http://localhost:8080/schedule/history
```

## 最佳实践

1. **选择合适的调度方式**：
   - 简单固定间隔 → `fixedRate` / `fixedDelay`
   - 复杂时间规则 → `cron`
   - 动态调整 → `SchedulingConfigurer`

2. **配置线程池**：避免单线程阻塞

3. **异常处理**：定时任务中的异常不会传播，建议用 try-catch 包裹
   ```java
   @Scheduled(fixedRate = 5000)
   public void safeTask() {
       try {
           // 业务逻辑
       } catch (Exception e) {
           log.error("定时任务执行失败", e);
       }
   }
   ```

4. **幂等设计**：定时任务可能重复执行，确保操作幂等

5. **避免长时间运行**：超过调度间隔的任务考虑使用 `@Async`

6. **分布式环境注意**：多实例部署时同一任务会重复执行，考虑分布式锁

7. **使用配置文件管理 Cron**：
   ```java
   @Scheduled(cron = "${task.cron.expression}")
   public void configurableTask() {}
   ```

## 常见问题

### Q: @Scheduled 方法能带参数吗？

不能。`@Scheduled` 方法必须是无参方法，返回值会被忽略。

### Q: 多个定时任务的执行顺序？

默认使用单线程，按顺序执行。配置线程池后可以并行执行。

### Q: 应用重启后定时任务会重新开始吗？

是的。`@Scheduled` 是内存级的调度，不持久化。重启后从头开始计时。如果需要持久化调度，考虑使用 Quartz。

### Q: fixedRate 任务执行时间超过间隔怎么办？

任务会在当前执行完成后立即开始下一次执行（不会并发）。如果需要并发执行，使用 `@Async`。

### Q: 如何禁用某个定时任务？

使用 `@ConditionalOnProperty`：
```java
@Scheduled(fixedRate = 5000)
@ConditionalOnProperty(name = "task.enabled", havingValue = "true")
public void conditionalTask() {}
```

## 扩展阅读

- [Spring Task Scheduling 官方文档](https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#scheduling)
- [@Scheduled 注解 API](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/scheduling/annotation/Scheduled.html)
- [Cron 表达式生成器](https://crontab.guru/)
- [Spring Boot Scheduling Guide](https://spring.io/guides/gs/scheduling-tasks/)
