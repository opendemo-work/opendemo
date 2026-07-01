<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 观察者模式（Observer Pattern）

## 1. 模式定义

观察者模式（Observer Pattern）是一种**行为型设计模式**，它定义了对象之间的一对多依赖关系。当一个对象的状态发生改变时，所有依赖于它的对象都会得到通知并自动更新。

也称为**发布-订阅模式（Publish-Subscribe Pattern）**。

**核心要点：**
- Subject（被观察者）维护一组 Observer（观察者）列表
- Subject 状态变化时自动通知所有 Observer
- Observer 可以动态地注册和注销

## 2. UML 类图

```
┌──────────────────┐        ┌──────────────────┐
│     Subject      │        │     Observer     │
│   (interface)    │        │   (interface)    │
├──────────────────┤        ├──────────────────┤
│ +attach(o)       │───────▶│ +update(data)    │
│ +detach(o)       │        └──────────────────┘
│ +notifyObservers()│              ▲
└──────────────────┘               │
        ▲                          │
        │                ┌─────────┴────────┐
        │                │                  │
┌───────────────┐  ┌──────────────┐ ┌──────────────┐
│NewsPublisher  │  │NewsSubscriber│ │WeatherDisplay│
├───────────────┤  ├──────────────┤ ├──────────────┤
│-subscribers   │  │-name         │ │-location     │
│-latestNews    │  │-lastReceived │ │-temperature  │
├───────────────┤  ├──────────────┤ ├──────────────┤
│+publishNews() │  │+update()     │ │+update()     │
└───────────────┘  └──────────────┘ └──────────────┘
```

## 3. 代码示例

### 3.1 Subject 接口

```java
public interface Subject {
    void attach(Observer observer);
    void detach(Observer observer);
    void notifyObservers();
}
```

### 3.2 Observer 接口

```java
public interface Observer {
    void update(Object data);
}
```

### 3.3 具体被观察者

```java
public class NewsPublisher implements Subject {
    private List<Observer> subscribers = new ArrayList<>();
    private String latestNews;

    public void publishNews(String news) {
        this.latestNews = news;
        notifyObservers();
    }

    @Override
    public void notifyObservers() {
        for (Observer o : subscribers) {
            o.update(latestNews);
        }
    }
}
```

### 3.4 具体观察者

```java
public class NewsSubscriber implements Observer {
    private String name;

    @Override
    public void update(Object data) {
        System.out.println(name + " received: " + data);
    }
}
```

## 4. 推模式 vs 拉模式

| 特性 | 推模式（Push） | 拉模式（Pull） |
|------|---------------|---------------|
| 数据传递 | Subject 主动推送数据 | Observer 主动拉取数据 |
| 耦合度 | 较高（Subject 知道 Observer 需要什么） | 较低（Observer 自己决定获取什么） |
| 性能 | 可能推送不必要的数据 | Observer 可能多次访问 Subject |
| 本 demo 使用 | ✅ 推模式 | |

## 5. 真实应用场景

### 5.1 Java 标准库

- `java.util.Observable` / `java.util.Observer`（已废弃，Java 9+）
- `java.beans.PropertyChangeListener` — JavaBeans 属性变化监听
- `java.util.EventListener` — Swing/AWT 事件机制
- `java.util.concurrent.Flow` — 响应式流（Java 9+）

### 5.2 Spring 框架

- `ApplicationEvent` + `ApplicationListener` — Spring 事件机制
- `@EventListener` 注解 — 简化事件监听
- Spring Cloud Stream — 消息驱动

### 5.3 其他常见场景

- **GUI 事件处理**：按钮点击、鼠标移动等事件监听
- **消息队列**：RabbitMQ、Kafka 等消息中间件
- **响应式编程**：RxJava、Project Reactor
- **MVC 架构**：Model 变化通知 View 更新
- **实时数据推送**：WebSocket、SSE
- **日志系统**：日志事件通知多个 Appender

## 6. 文件说明

| 文件 | 说明 |
|------|------|
| `ObserverDemo.java` | 主入口，演示新闻发布和气象站两个场景 |
| `Subject.java` | 被观察者接口 |
| `Observer.java` | 观察者接口 |
| `NewsPublisher.java` | 新闻发布者（具体被观察者） |
| `NewsSubscriber.java` | 新闻订阅者（具体观察者） |
| `WeatherStation.java` | 气象站（具体被观察者） |
| `WeatherDisplay.java` | 天气显示器（具体观察者） |
| `ObserverPatternTest.java` | 单元测试 |

## 7. 与其他模式的关系

### 7.1 与中介者模式（Mediator）
- 观察者模式中 Subject 直接通知 Observer
- 中介者模式通过中介者间接通信，降低对象间的直接依赖

### 7.2 与策略模式
- 策略模式改变对象的行为，观察者模式改变对象的状态通知

### 7.3 与责任链模式
- 责任链模式沿链传递请求直到被处理
- 观察者模式广播通知给所有观察者

### 7.4 与装饰器模式
- 可以用装饰器模式动态增强观察者的功能

## 8. 注意事项

### 8.1 内存泄漏

观察者注册后如果忘记注销，可能导致内存泄漏。解决方案：

```java
// 使用 WeakReference
private List<WeakReference<Observer>> observers = new ArrayList<>();
```

### 8.2 线程安全

多线程环境下，Subject 的观察者列表需要同步处理：

```java
// 使用线程安全的集合
private List<Observer> observers = new CopyOnWriteArrayList<>();
```

### 8.3 通知顺序

观察者的通知顺序通常不应影响业务逻辑。如果顺序重要，需要使用 `LinkedHashSet` 等有序集合。

### 8.4 循环依赖

避免 Subject 和 Observer 之间的循环更新，可能导致无限递归。

## 9. 运行方式

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 编译
mvn clean compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.patterns.observer.ObserverDemo"

# 运行测试
mvn test
```

## 10. 总结

观察者模式是实现分布式事件处理系统的核心模式，广泛应用于 GUI 事件处理、消息中间件、响应式编程等领域。在使用时需要注意内存泄漏和线程安全问题。Java 9+ 推荐使用 `Flow` API 或第三方库（如 RxJava、Project Reactor）替代传统的 Observer 实现。

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
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
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
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
# 请根据实际案例替换
./scripts/demo.sh
```
