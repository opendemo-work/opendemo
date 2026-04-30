# 策略模式（Strategy Pattern）

## 1. 模式定义

策略模式（Strategy Pattern）是一种**行为型设计模式**，它定义了一系列算法，将每一个算法封装起来，并使它们可以互相替换。策略模式让算法的变化独立于使用算法的客户端。

**核心要点：**
- 将算法封装为独立的策略类
- Context 持有策略引用，可在运行时切换策略
- 客户端与具体算法解耦

## 2. UML 类图

### 2.1 支付策略

```
┌──────────────────┐      ┌──────────────────┐
│  PaymentContext   │─────▶│ PaymentStrategy  │
├──────────────────┤      │  (interface)     │
│-strategy         │      ├──────────────────┤
├──────────────────┤      │+pay(amount)      │
│+executePayment() │      │+getName()        │
│+setStrategy()    │      └──────────────────┘
└──────────────────┘             ▲
                    ┌────────────┼────────────┐
                    │            │            │
            ┌────────────┐┌────────────┐┌────────────┐
            │CreditCard  ││  Alipay    ││  WeChat    │
            │  Payment   ││  Payment   ││  Payment   │
            └────────────┘└────────────┘└────────────┘
```

### 2.2 排序策略

```
┌──────────┐      ┌──────────────────┐
│  Sorter   │─────▶│ SortingStrategy  │
├──────────┤      │  (interface)     │
│-strategy │      ├──────────────────┤
├──────────┤      │+sort(array)      │
│+sort()   │      │+getName()        │
└──────────┘      └──────────────────┘
                         ▲
              ┌──────────┼──────────┐
              │          │          │
      ┌──────────┐┌──────────┐┌──────────┐
      │BubbleSort││QuickSort ││MergeSort │
      └──────────┘└──────────┘└──────────┘
```

## 3. 代码示例

### 3.1 策略接口

```java
public interface PaymentStrategy {
    boolean pay(double amount);
    String getName();
}
```

### 3.2 具体策略

```java
public class CreditCardPayment implements PaymentStrategy {
    private String cardNumber;

    public CreditCardPayment(String cardNumber, String cardHolder, String expiryDate) {
        this.cardNumber = cardNumber;
    }

    @Override
    public boolean pay(double amount) {
        System.out.println("Paying ¥" + amount + " with Credit Card");
        return true;
    }
}
```

### 3.3 上下文

```java
public class PaymentContext {
    private PaymentStrategy strategy;

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    public boolean executePayment(double amount) {
        return strategy.pay(amount);
    }
}
```

## 4. 排序算法对比

| 算法 | 时间复杂度（平均） | 时间复杂度（最坏） | 空间复杂度 | 稳定性 |
|------|-------------------|-------------------|-----------|--------|
| Bubble Sort | O(n²) | O(n²) | O(1) | 稳定 |
| Quick Sort | O(n log n) | O(n²) | O(log n) | 不稳定 |
| Merge Sort | O(n log n) | O(n log n) | O(n) | 稳定 |

## 5. 真实应用场景

### 5.1 Java 标准库

- `java.util.Comparator` — 不同的比较策略实现不同的排序方式
- `java.util.Collections#sort(List, Comparator)` — 运行时指定排序策略
- `javax.swing.JTable` — 表格排序策略
- `java.util.concurrent.ThreadPoolExecutor` — 拒绝策略（RejectedExecutionHandler）

### 5.2 Spring 框架

- `Resource` 接口 — 不同的资源加载策略
- `HandlerMapping` — 不同的请求映射策略
- `ViewResolver` — 不同的视图解析策略

### 5.3 其他常见场景

- **支付系统**：信用卡、支付宝、微信等不同支付方式
- **压缩算法**：ZIP、RAR、7z 等不同压缩策略
- **路由算法**：最短路径、最少跳数等不同路由策略
- **折扣计算**：满减、打折、优惠券等不同折扣策略
- **数据导出**：CSV、Excel、PDF 等不同导出格式

## 6. 文件说明

| 文件 | 说明 |
|------|------|
| `StrategyDemo.java` | 主入口 |
| `PaymentStrategy.java` | 支付策略接口 |
| `CreditCardPayment.java` | 信用卡支付 |
| `AlipayPayment.java` | 支付宝支付 |
| `WeChatPayment.java` | 微信支付 |
| `PaymentContext.java` | 支付上下文 |
| `SortingStrategy.java` | 排序策略接口 |
| `BubbleSort.java` | 冒泡排序 |
| `QuickSort.java` | 快速排序 |
| `MergeSort.java` | 归并排序 |
| `Sorter.java` | 排序上下文 |
| `StrategyPatternTest.java` | 单元测试 |

## 7. 与其他模式的关系

### 7.1 与工厂模式
- 工厂模式可以用来创建策略对象
- 客户端通过工厂获取策略，再传给 Context

### 7.2 与状态模式（State）
- 结构相似，但目的不同
- 策略模式：客户端选择策略
- 状态模式：状态自动转换

### 7.3 与模板方法模式
- 模板方法使用继承来改变行为
- 策略模式使用组合来改变行为

### 7.4 与命令模式
- 命令模式关注请求的封装
- 策略模式关注算法的封装和替换

## 8. 最佳实践

### 8.1 策略枚举

当策略较少且简单时，可以使用枚举：

```java
public enum DiscountStrategy implements PaymentStrategy {
    REGULAR { public double apply(double price) { return price; } },
    VIP { public double apply(double price) { return price * 0.8; } },
    SVIP { public double apply(double price) { return price * 0.7; } };
}
```

### 8.2 策略工厂

结合工厂模式动态创建策略：

```java
public class StrategyFactory {
    private static final Map<String, PaymentStrategy> strategies = new HashMap<>();
    static {
        strategies.put("credit", new CreditCardPayment(...));
        strategies.put("alipay", new AlipayPayment(...));
    }
    public static PaymentStrategy getStrategy(String type) {
        return strategies.get(type);
    }
}
```

### 8.3 函数式接口

Java 8+ 可以使用 Lambda 表达式简化策略：

```java
sorter.setSortingStrategy(array -> Arrays.sort(array));
```

## 9. 运行方式

```bash
# 编译
mvn clean compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.patterns.strategy.StrategyDemo"

# 运行测试
mvn test
```

## 10. 总结

策略模式是最常用的行为型模式之一，它通过将算法封装为独立的策略类，实现了算法的灵活切换和扩展。在 Java 中，策略模式与函数式编程结合可以大幅简化代码。本 demo 通过支付方式和排序算法两个场景，展示了策略模式在实际开发中的应用。
