# Java Refactoring Patterns

Java代码重构技巧与模式。

## 重构原则

```
重构定义: 在不改变外部行为的前提下，改进代码内部结构
```

## 常见重构手法

### 1. 提取方法
```java
// 重构前
public void printOwing() {
    double outstanding = 0.0;
    
    // 打印banner
    System.out.println("**************************");
    System.out.println("***** Customer Owes ******");
    System.out.println("**************************");
    
    // 计算总额
    for (Order order : orders) {
        outstanding += order.getAmount();
    }
    
    // 打印详情
    System.out.println("name: " + name);
    System.out.println("amount: " + outstanding);
}

// 重构后
public void printOwing() {
    printBanner();
    double outstanding = calculateOutstanding();
    printDetails(outstanding);
}

private void printBanner() {
    System.out.println("**************************");
    System.out.println("***** Customer Owes ******");
    System.out.println("**************************");
}

private double calculateOutstanding() {
    return orders.stream()
        .mapToDouble(Order::getAmount)
        .sum();
}

private void printDetails(double outstanding) {
    System.out.println("name: " + name);
    System.out.println("amount: " + outstanding);
}
```

### 2. 引入Null对象
```java
// 重构前
if (customer != null && customer.isActive()) {
    customer.placeOrder(order);
}

// 重构后
customer.placeOrder(order); // NullCustomer不执行任何操作
```

### 3. 替换条件表达式
```java
// 重构前
public double calculatePrice(Order order) {
    if (order.getType().equals("NORMAL")) {
        return order.getAmount() * 1.0;
    } else if (order.getType().equals("VIP")) {
        return order.getAmount() * 0.8;
    } else if (order.getType().equals("STAFF")) {
        return order.getAmount() * 0.5;
    }
    return 0;
}

// 重构后 (策略模式)
public interface PricingStrategy {
    double calculatePrice(double amount);
}

public class NormalPricing implements PricingStrategy {
    public double calculatePrice(double amount) {
        return amount;
    }
}

public class VipPricing implements PricingStrategy {
    public double calculatePrice(double amount) {
        return amount * 0.8;
    }
}
```

## 代码坏味道

| 坏味道 | 症状 | 重构手法 |
|--------|------|----------|
| 长方法 | 方法超过20行 | 提取方法 |
| 大类 | 类超过200行 | 提取类 |
| 长参数列表 | 参数超过4个 | 引入参数对象 |
| 重复代码 | 相同代码出现多次 | 提取方法 |
| 魔术数字 | 未命名的常量 | 提取常量 |

## 学习要点

1. 重构原则
2. 常见重构手法
3. 代码坏味道识别
4. 安全重构步骤
5. 自动化重构工具
