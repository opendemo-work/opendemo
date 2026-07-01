<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 模板方法模式（Template Method Pattern）

## 1. 模式定义

模板方法模式（Template Method Pattern）是一种**行为型设计模式**，它在父类中定义一个算法的骨架（框架），将某些步骤延迟到子类中实现。子类可以在不改变算法结构的情况下重写算法的特定步骤。

**核心要点：**
- 父类定义算法骨架（模板方法）
- 子类实现具体步骤（抽象方法）
- 模板方法通常用 `final` 修饰，防止子类覆盖
- 通过钩子方法（Hook）提供扩展点

## 2. UML 类图

### 2.1 数据处理器

```
┌──────────────────────────────┐
│      DataProcessor           │
│      (abstract)              │
├──────────────────────────────┤
│+ process(data): void [final] │  ← 模板方法
│# validate(data): String      │  ← 抽象方法
│# transform(data): String     │  ← 抽象方法
│# save(data): void            │  ← 抽象方法
│# shouldLog(): boolean        │  ← 钩子方法
└──────────────────────────────┘
            ▲
    ┌───────┼────────┐
    │       │        │
┌────────┐┌────────┐┌────────┐
│  CSV   ││  JSON  ││  XML   │
│Processor││Processor││Processor│
└────────┘└────────┘└────────┘
```

### 2.2 游戏模拟

```
┌──────────────────────────┐
│    AbstractGame           │
│    (abstract)             │
├──────────────────────────┤
│+ play(): void [final]     │  ← 模板方法
│# initialize(): void       │  ← 抽象方法
│# startPlay(): void        │  ← 抽象方法
│# endPlay(): void          │  ← 抽象方法
└──────────────────────────┘
            ▲
    ┌───────┴───────┐
    │               │
┌─────────┐  ┌──────────┐
│ChessGame│  │FootballGame│
└─────────┘  └──────────┘
```

## 3. 代码示例

### 3.1 模板方法（抽象类）

```java
public abstract class DataProcessor {

    public final void process(String data) {
        String validated = validate(data);
        String transformed = transform(validated);
        save(transformed);
    }

    protected abstract String validate(String data);
    protected abstract String transform(String data);
    protected abstract void save(String data);
}
```

### 3.2 具体实现

```java
public class CsvDataProcessor extends DataProcessor {
    @Override
    protected String validate(String data) {
        if (data == null || data.trim().isEmpty()) {
            throw new IllegalArgumentException("CSV data is empty");
        }
        return data;
    }

    @Override
    protected String transform(String data) {
        return data.replace(",", " | ");
    }

    @Override
    protected void save(String data) {
        System.out.println("Saving to CSV file: " + data);
    }
}
```

## 4. 模板方法中的方法类型

| 方法类型 | 说明 | 示例 |
|---------|------|------|
| 模板方法 | 定义算法骨架，用 `final` 修饰 | `process()` |
| 抽象方法 | 子类必须实现 | `validate()`, `transform()`, `save()` |
| 钩子方法 | 子类可选重写，提供默认实现 | `shouldLog()` |
| 具体方法 | 通用逻辑，子类共享 | 通用工具方法 |

## 5. 真实应用场景

### 5.1 Java 标准库

- `java.util.AbstractList` — 定义列表操作的骨架
- `java.util.AbstractMap` — 定义 Map 操作的骨架
- `java.io.InputStream` — `read(byte[], int, int)` 调用 `read()`
- `javax.servlet.http.HttpServlet` — `doGet()`, `doPost()` 由子类实现
- `java.util.Arrays#sort()` — 排序骨架，比较逻辑由 `Comparator` 提供

### 5.2 Spring 框架

- `AbstractApplicationContext#refresh()` — Spring 容器刷新的模板方法
- `JdbcTemplate` — 数据库操作的模板方法
- `RestTemplate` — REST 请求的模板方法
- `AbstractView#render()` — 视图渲染的模板方法

### 5.3 其他常见场景

- **数据库操作**：打开连接 → 执行查询 → 处理结果 → 关闭连接
- **文件处理**：打开文件 → 读取/写入 → 关闭文件
- **报表生成**：收集数据 → 格式化 → 生成 → 导出
- **测试框架**：setUp() → test() → tearDown()
- **构建工具**：Maven 的生命周期阶段
- **Servlet**：init() → service() → destroy()

## 6. 文件说明

| 文件 | 说明 |
|------|------|
| `TemplateMethodDemo.java` | 主入口 |
| `DataProcessor.java` | 数据处理器（抽象类，含模板方法） |
| `CsvDataProcessor.java` | CSV 处理器 |
| `JsonDataProcessor.java` | JSON 处理器 |
| `XmlDataProcessor.java` | XML 处理器 |
| `AbstractGame.java` | 游戏抽象类 |
| `ChessGame.java` | 国际象棋游戏 |
| `FootballGame.java` | 足球游戏 |
| `TemplateMethodPatternTest.java` | 单元测试 |

## 7. 与其他模式的关系

### 7.1 与策略模式
- 模板方法使用继承改变行为
- 策略模式使用组合改变行为
- 策略模式更灵活，模板方法更简洁

### 7.2 与工厂方法
- 工厂方法是模板方法的一种特殊应用
- 模板方法通常包含工厂方法调用

### 7.3 与建造者模式
- 建造者关注对象的逐步构造
- 模板方法关注算法的步骤执行

### 7.4 与回调模式
- 回调是模板方法的一种替代方案
- 回调使用组合代替继承，更灵活

## 8. 最佳实践

### 8.1 最小化抽象方法

抽象方法过多会增加子类的实现负担：

```java
// 好的设计：少量抽象方法
public abstract class DataProcessor {
    public final void process(String data) {
        String validated = validate(data);
        String transformed = transform(validated);
        save(transformed);
    }
    protected abstract String validate(String data);
    protected abstract String transform(String data);
    protected abstract void save(String data);
}
```

### 8.2 使用 final 保护模板方法

模板方法应该用 `final` 修饰，防止子类破坏算法结构。

### 8.3 提供钩子方法

钩子方法提供可选的扩展点：

```java
protected boolean shouldLog() {
    return true; // 默认行为
}
```

### 8.4 好莱坞原则

"不要调用我们，我们会调用你" — 父类调用子类的方法，而非反之。

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
mvn exec:java -Dexec.mainClass="com.opendemo.java.patterns.templatemethod.TemplateMethodDemo"

# 运行测试
mvn test
```

## 10. 总结

模板方法模式是最基础的行为型模式之一，它通过在父类中定义算法骨架，将具体实现延迟到子类，实现了代码复用和扩展性。Java 的很多框架和类库都大量使用了模板方法模式。理解该模式有助于更好地使用 Spring、Servlet 等框架，以及设计自己的可扩展框架。

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
