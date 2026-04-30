# 工厂模式（Factory Pattern）

## 1. 模式定义

工厂模式是一种**创建型设计模式**，它将对象的创建过程封装在工厂类中，客户端无需知道具体的创建细节，只需通过工厂获取所需对象。

工厂模式分为三种：
- **简单工厂模式（Simple Factory）**：一个工厂类根据参数创建不同对象
- **工厂方法模式（Factory Method）**：定义创建对象的接口，让子类决定实例化哪个类
- **抽象工厂模式（Abstract Factory）**：创建一系列相关对象的接口

## 2. UML 类图

### 2.1 简单工厂模式

```
┌──────────────┐      ┌──────────────┐
│DocumentFactory│─────▶│  Document    │
└──────────────┘      │  (interface) │
                      └──────────────┘
                            ▲
              ┌─────────────┼─────────────┐
              │             │             │
      ┌───────────┐  ┌───────────┐  ┌───────────┐
      │PdfDocument│  │WordDocument│  │ExcelDocument│
      └───────────┘  └───────────┘  └───────────┘
```

### 2.2 工厂方法模式

```
┌─────────────────────────┐
│ AdvancedDocumentFactory  │
│  (interface)             │
│  + createDocument(): Doc │
└─────────────────────────┘
            ▲
            │
┌───────────┼───────────────┐
│                          │
┌──────────────────┐  ┌──────────────────┐
│PdfDocumentFactory │  │WordDocumentFactory│
│+createDocument() │  │+createDocument()  │
└──────────────────┘  └──────────────────┘
```

## 3. 代码结构

### 3.1 产品接口

```java
public interface Document {
    void open();
    void save();
    String getType();
}
```

### 3.2 具体产品

```java
public class PdfDocument implements Document {
    @Override
    public void open() {
        System.out.println("Opening PDF document...");
    }

    @Override
    public void save() {
        System.out.println("Saving PDF document...");
    }

    @Override
    public String getType() {
        return "PDF";
    }
}
```

### 3.3 简单工厂

```java
public class DocumentFactory {
    public static Document createDocument(DocumentType type) {
        switch (type) {
            case PDF: return new PdfDocument();
            case WORD: return new WordDocument();
            case EXCEL: return new ExcelDocument();
            default: throw new IllegalArgumentException("Unknown document type");
        }
    }
}
```

### 3.4 工厂方法

```java
public interface AdvancedDocumentFactory {
    Document createDocument();
}

public class PdfDocumentFactory implements AdvancedDocumentFactory {
    @Override
    public Document createDocument() {
        return new PdfDocument();
    }
}
```

## 4. 简单工厂 vs 工厂方法

| 特性 | 简单工厂 | 工厂方法 |
|------|---------|---------|
| 设计模式类型 | 不属于 GoF 23 种模式 | GoF 创建型模式 |
| 开闭原则 | 违反（新增类型需修改工厂类） | 遵循（新增类型只需新增工厂类） |
| 复杂度 | 低 | 中 |
| 灵活性 | 低 | 高 |
| 适用场景 | 产品种类少且稳定 | 产品种类可能频繁变化 |

## 5. 真实应用场景

### 5.1 Java 标准库

- `java.util.Calendar#getInstance()` — 根据时区和地区创建日历实例
- `java.text.NumberFormat#getInstance()` — 创建数字格式化器
- `java.sql.DriverManager#getConnection()` — 创建数据库连接
- `java.util.ResourceBundle#getBundle()` — 创建资源包

### 5.2 Spring 框架

- `BeanFactory` 和 `ApplicationContext` 都是工厂模式的实现
- `FactoryBean` 接口允许自定义 Bean 的创建逻辑
- Spring AOP 的 `ProxyFactory` 创建代理对象

### 5.3 其他常见场景

- **日志框架**：根据配置创建不同的 Logger 实例
- **连接池**：根据数据库类型创建对应的连接
- **消息队列**：根据协议创建对应的消息生产者/消费者
- **UI 组件**：根据平台创建对应的按钮、对话框等

## 6. 文件说明

| 文件 | 说明 |
|------|------|
| `FactoryDemo.java` | 主入口，演示工厂模式 |
| `Document.java` | 文档接口（产品） |
| `PdfDocument.java` | PDF 文档实现 |
| `WordDocument.java` | Word 文档实现 |
| `ExcelDocument.java` | Excel 文档实现 |
| `DocumentType.java` | 文档类型枚举 |
| `DocumentFactory.java` | 简单工厂 |
| `AdvancedDocumentFactory.java` | 工厂方法接口及实现 |
| `FactoryPatternTest.java` | 单元测试 |

## 7. 与其他模式的关系

### 7.1 与抽象工厂模式
- 工厂方法用于创建一种产品，抽象工厂用于创建一系列产品族
- 抽象工厂内部通常使用工厂方法来实现

### 7.2 与单例模式
- 工厂类本身通常是单例，确保全局只有一个工厂实例

### 7.3 与原型模式
- 工厂可以使用原型模式来创建对象（通过克隆而非新建）

### 7.4 与策略模式
- 工厂返回的对象可能是策略模式中的策略实现

## 8. 最佳实践

### 8.1 何时使用简单工厂
- 产品种类较少（通常不超过 5 种）
- 产品类型不常变化
- 快速原型开发

### 8.2 何时使用工厂方法
- 产品种类可能扩展
- 需要遵循开闭原则
- 框架或库的设计

### 8.3 何时使用抽象工厂
- 需要创建一系列相关产品
- 产品之间存在约束关系
- 需要支持多个产品族

## 9. 运行方式

```bash
# 编译
mvn clean compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.patterns.factory.FactoryDemo"

# 运行测试
mvn test
```

## 10. 总结

工厂模式是面向对象编程中最常用的创建型模式之一。它通过封装对象创建逻辑，使客户端代码与具体类解耦，提高了代码的可维护性和可扩展性。选择哪种工厂模式取决于具体场景的复杂度和扩展需求。
