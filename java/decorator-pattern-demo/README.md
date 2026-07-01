<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 装饰器模式（Decorator Pattern）

## 1. 模式定义

装饰器模式（Decorator Pattern）是一种**结构型设计模式**，它允许在不改变对象结构的前提下，动态地给对象添加新的功能。装饰器模式通过创建包装对象（Wrapper）来包裹真实对象，并在保持接口不变的情况下扩展功能。

**核心要点：**
- 装饰器和被装饰对象实现相同的接口
- 装饰器持有被装饰对象的引用
- 可以通过多层嵌套实现功能叠加
- 遵循开闭原则（对扩展开放，对修改关闭）

## 2. UML 类图

### 2.1 咖啡配料系统

```
┌──────────────────┐
│     Coffee       │
│  (interface)     │
├──────────────────┤
│+getCost(): double│
│+getDescription() │
└──────────────────┘
        ▲
        │
┌───────┴────────┐
│                │
┌────────────┐  ┌──────────────────┐
│SimpleCoffee│  │ CoffeeDecorator  │
│            │  │   (abstract)     │
├────────────┤  ├──────────────────┤
│+getCost()  │  │#decoratedCoffee  │
│+getDescription()│+getCost()      │
└────────────┘  │+getDescription() │
                └──────────────────┘
                        ▲
            ┌───────────┼───────────┐
            │           │           │
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Milk    │ │  Sugar   │ │  Whip    │
    │Decorator │ │Decorator │ │Decorator │
    └──────────┘ └──────────┘ └──────────┘
```

## 3. 代码示例

### 3.1 组件接口

```java
public interface Coffee {
    double getCost();
    String getDescription();
}
```

### 3.2 基础组件

```java
public class SimpleCoffee implements Coffee {
    @Override
    public double getCost() { return 10.0; }

    @Override
    public String getDescription() { return "Simple Coffee"; }
}
```

### 3.3 抽象装饰器

```java
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee decoratedCoffee;

    public CoffeeDecorator(Coffee coffee) {
        this.decoratedCoffee = coffee;
    }

    @Override
    public double getCost() { return decoratedCoffee.getCost(); }

    @Override
    public String getDescription() { return decoratedCoffee.getDescription(); }
}
```

### 3.4 具体装饰器

```java
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double getCost() { return super.getCost() + 2.0; }

    @Override
    public String getDescription() { return super.getDescription() + ", Milk"; }
}
```

### 3.5 使用方式

```java
Coffee coffee = new WhipDecorator(
    new SugarDecorator(
        new MilkDecorator(
            new SimpleCoffee())));
// 结果: "Simple Coffee, Milk, Sugar, Whip" -> ¥16.5
```

## 4. 继承 vs 装饰器

| 特性 | 继承 | 装饰器 |
|------|------|--------|
| 扩展方式 | 编译时静态扩展 | 运行时动态扩展 |
| 功能组合 | 类爆炸问题 | 自由组合 |
| 修改源码 | 需要 | 不需要 |
| 灵活性 | 低 | 高 |
| 复杂度 | 低 | 中 |

使用继承实现所有咖啡组合需要 N 个子类，而装饰器只需要 N 个装饰器类。

## 5. 真实应用场景

### 5.1 Java 标准库（IO 流）

装饰器模式最经典的 Java 实现：

```java
// 装饰器模式的典型应用
InputStream in = new BufferedInputStream(
    new DataInputStream(
        new FileInputStream("data.txt")));
```

- `InputStream` = Component
- `FileInputStream` = ConcreteComponent
- `BufferedInputStream` / `DataInputStream` = Decorator

### 5.2 Java Collections

```java
Collections.unmodifiableList(list);   // 不可修改装饰器
Collections.synchronizedList(list);    // 同步装饰器
Collections.checkedList(list, type);   // 类型检查装饰器
```

### 5.3 Spring 框架

- `HttpServletRequestWrapper` — 请求对象装饰
- `BeanDefinitionDecorator` — Bean 定义装饰
- Spring Security 的 `SecurityContext` 包装
- Spring Cache 的缓存装饰器

### 5.4 其他常见场景

- **UI 组件**：滚动条装饰、边框装饰
- **Web 过滤器**：Servlet Filter 链
- **日志增强**：添加时间戳、格式化等
- **权限控制**：在方法调用前添加权限检查
- **缓存**：在数据访问前添加缓存层

## 6. 文件说明

| 文件 | 说明 |
|------|------|
| `DecoratorDemo.java` | 主入口 |
| `Coffee.java` | 咖啡接口（组件） |
| `SimpleCoffee.java` | 基础咖啡（具体组件） |
| `CoffeeDecorator.java` | 咖啡装饰器（抽象装饰器） |
| `MilkDecorator.java` | 牛奶装饰器 |
| `SugarDecorator.java` | 糖装饰器 |
| `WhipDecorator.java` | 奶油装饰器 |
| `Notifier.java` | 通知接口 |
| `NotifierDecorator.java` | 通知装饰器 |
| `EmailNotifier.java` | 邮件通知 |
| `SMSNotifier.java` | 短信通知 |
| `DecoratorPatternTest.java` | 单元测试 |

## 7. 与其他模式的关系

### 7.1 与代理模式（Proxy）
- 结构相似，但目的不同
- 装饰器：为对象添加功能
- 代理：控制对象的访问

### 7.2 与适配器模式（Adapter）
- 适配器改变接口
- 装饰器保持接口不变

### 7.3 与组合模式（Composite）
- 组合模式构建树形结构
- 装饰器构建线性包装链

### 7.4 与责任链模式
- 责任链沿链传递请求直到被处理
- 装饰器每层都处理请求

## 8. 注意事项

### 8.1 装饰器顺序

装饰器的叠加顺序可能影响结果：

```java
// 顺序 A
new A(new B(new SimpleCoffee()));
// 顺序 B
new B(new A(new SimpleCoffee()));
```

### 8.2 对象标识

装饰器会改变对象的引用，`equals()` 和 `hashCode()` 可能不按预期工作。

### 8.3 调试困难

多层装饰器嵌套可能使调试变得困难，建议限制装饰层数。

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
mvn exec:java -Dexec.mainClass="com.opendemo.java.patterns.decorator.DecoratorDemo"

# 运行测试
mvn test
```

## 10. 总结

装饰器模式是替代继承实现功能扩展的优雅方案。它通过包装机制实现了功能的动态组合，避免了类爆炸问题。Java IO 流是装饰器模式的经典实现，理解装饰器模式有助于更好地使用和设计 IO 相关的代码。

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
