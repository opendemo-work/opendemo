# Async Demo

Spring Boot异步处理演示项目，演示如何使用@Async进行异步编程。

## 技术栈

- Spring Boot 2.7
- Spring Async
- CompletableFuture

## 项目结构

```
async-demo/
├── src/main/java/com/example/demo/
│   ├── AsyncDemoApplication.java          # 应用入口
│   ├── config/
│   │   └── AsyncConfig.java               # 异步配置
│   ├── controller/
│   │   └── AsyncController.java           # 异步控制器
│   └── service/
│       └── AsyncService.java              # 异步服务
├── pom.xml
└── README.md
```

## 核心概念

### 什么是异步处理

异步处理允许方法在后台线程中执行，不阻塞调用线程。适用于：
- 耗时操作（发送邮件、文件上传）
- 并行处理（批量任务）
- 提高系统吞吐量

### 同步 vs 异步

```
同步处理:
调用者 ──▶ 任务1(1s) ──▶ 任务2(1s) ──▶ 任务3(1s) ──▶ 总计: 3s

异步处理:
调用者 ──▶ 提交任务1
     ──▶ 提交任务2
     ──▶ 提交任务3
     ──▶ 等待结果 ──▶ 总计: ~1s
```

## 快速开始

### 1. 启用异步支持

```java
@SpringBootApplication
@EnableAsync
public class AsyncDemoApplication { }
```

### 2. 创建异步方法

```java
@Service
public class AsyncService {
    
    @Async
    public void asyncMethod() {
        // 异步执行
    }
    
    @Async
    public CompletableFuture<String> asyncMethodWithResult() {
        return CompletableFuture.completedFuture("result");
    }
}
```

### 3. 配置线程池

```java
@Configuration
public class AsyncConfig {
    
    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-task-");
        executor.initialize();
        return executor;
    }
}
```

## 测试接口

```bash
# 异步方法 - 无返回值
curl http://localhost:8080/api/async/without-return

# 异步方法 - 使用Future
curl http://localhost:8080/api/async/with-future

# 异步方法 - 使用CompletableFuture
curl http://localhost:8080/api/async/with-completable

# 对比同步vs异步
curl http://localhost:8080/api/async/compare
```

## 注意事项

### 1. 同类方法调用

@Async方法必须通过代理调用：

```java
// 错误 - 同类调用不会走代理
public void methodA() {
    asyncMethod();  // 同步执行
}

// 正确 - 使用注入的实例
@Autowired
private AsyncService asyncService;

public void methodA() {
    asyncService.asyncMethod();  // 异步执行
}
```

### 2. 返回值处理

```java
// CompletableFuture推荐
@Async
public CompletableFuture<String> asyncMethod() {
    return CompletableFuture.completedFuture("result");
}

// 获取结果
CompletableFuture<String> future = asyncService.asyncMethod();
String result = future.get();  // 阻塞等待
```

### 3. 异常处理

```java
@Async
public CompletableFuture<String> asyncMethod() {
    try {
        // 业务逻辑
        return CompletableFuture.completedFuture("success");
    } catch (Exception e) {
        return CompletableFuture.failedFuture(e);
    }
}
```

## 学习要点

1. @Async注解的使用
2. 线程池配置
3. CompletableFuture异步编程
4. 异步方法的异常处理
5. 性能优化技巧
