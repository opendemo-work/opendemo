<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
