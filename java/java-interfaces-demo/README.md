# Java接口设计完整示例

## 🎯 案例概述

这是一个全面展示Java接口设计的完整示例，涵盖了接口定义、实现、继承、默认方法、函数式接口、Lambda表达式等现代Java接口特性的应用。

## 📚 学习目标

通过本示例你将掌握：
- 接口的基本定义和实现
- 默认方法和静态方法的使用
- 函数式接口和Lambda表达式
- 接口继承和多接口实现
- 回调机制和事件处理
- 异步处理接口设计

## 🔧 核心知识点

### 1. 接口基础
- 接口定义和抽象方法
- 接口实现和多实现
- 标记接口的作用

### 2. 现代接口特性
- 默认方法（Java 8+）
- 静态方法（Java 8+）
- 私有方法（Java 9+）
- 函数式接口注解

### 3. 接口应用模式
- 回调接口设计
- 事件处理机制
- 异步处理接口
- 服务提供者接口

## 🚀 运行示例

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.interfaces.InterfacesDemo"

# 运行测试
mvn test
```

## 📖 代码详解

### 主要组件

```java
// 基础接口
interface Vehicle { }
interface FlyingVehicle extends Vehicle { }

// 函数式接口
@FunctionalInterface
interface PaymentProcessor { }

// 实现类
class Car implements Vehicle, SerializableMarker { }
class Airplane implements Vehicle, FlyingVehicle { }

// 服务类
class PaymentService { }
class EventManager { }
```

### 关键技术点

#### 1. 接口定义和实现
```java
interface Vehicle {
    void start();
    void stop();
    void accelerate(int speed);
    
    default void honk() {
        logger.info("车辆鸣笛");
    }
}

class Car implements Vehicle {
    @Override
    public void start() { }
    @Override
    public void stop() { }
    @Override
    public void accelerate(int speed) { }
}
```

#### 2. 函数式接口和Lambda
```java
@FunctionalInterface
interface PaymentProcessor {
    boolean processPayment(double amount);
    String getProcessorName();
}

// Lambda表达式实现
PaymentProcessor unionPay = amount -> {
    logger.info("银联支付: ¥{}", amount);
    return true;
};
```

#### 3. 回调机制
```java
interface EventHandler {
    void handleEvent(String event);
    default void onError(Exception e) { }
}

// 使用Lambda回调
eventManager.fireEvent("登录", event -> logger.info("处理: {}", event));
```

## 🧪 测试覆盖

✅ 基础接口实现测试  
✅ 多接口实现测试  
✅ 函数式接口测试  
✅ 默认方法测试  
✅ 回调机制测试  
✅ 异步处理测试  
✅ 接口继承测试  
✅ 支付服务测试  

## 🎯 实际应用场景

### 1. 支付系统
```java
interface PaymentGateway {
    boolean processPayment(PaymentRequest request);
    PaymentStatus checkStatus(String transactionId);
}
```

### 2. 事件驱动架构
```java
interface EventListener<T> {
    void onEvent(T event);
    default void onError(Exception e) { }
}
```

### 3. 数据访问层
```java
interface Repository<T, ID> {
    T findById(ID id);
    List<T> findAll();
    T save(T entity);
}
```

## ⚡ 最佳实践

✅ 优先使用接口而非抽象类定义契约  
✅ 合理使用默认方法提供便利实现  
✅ 函数式接口配合Lambda表达式简化代码  
✅ 接口设计遵循单一职责原则  

## 📚 扩展学习

- Java 8+ 新特性
- 设计模式中的接口应用
- 微服务架构中的接口设计
- API设计最佳实践

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本