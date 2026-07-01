<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Java DDD Aggregates

Java领域驱动设计聚合实践。

## 什么是聚合

聚合是DDD中的模式，用于封装实体和值对象：

```
订单聚合:
┌─────────────────────────────────────────┐
│           Order (聚合根)                 │
│  - orderId (ID)                         │
│  - customerId                           │
│  - status                               │
├─────────────────────────────────────────┤
│  OrderLine (实体)                       │
│  - productId                            │
│  - quantity                             │
│  - price                                │
├─────────────────────────────────────────┤
│  Address (值对象)                       │
│  - street                               │
│  - city                                 │
│  - zipCode                              │
└─────────────────────────────────────────┘
```

## 聚合实现

```java
// 聚合根
public class Order {
    private OrderId id;
    private CustomerId customerId;
    private List<OrderLine> orderLines;
    private Address shippingAddress;
    private OrderStatus status;
    
    // 业务规则在聚合根中实现
    public void addProduct(Product product, int quantity) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify submitted order");
        }
        orderLines.add(new OrderLine(product.getId(), quantity, product.getPrice()));
    }
    
    public Money getTotal() {
        return orderLines.stream()
            .map(line -> line.getPrice().multiply(line.getQuantity()))
            .reduce(Money.ZERO, Money::add);
    }
    
    public void submit() {
        if (orderLines.isEmpty()) {
            throw new IllegalStateException("Cannot submit empty order");
        }
        this.status = OrderStatus.SUBMITTED;
        // 发布领域事件
        registerEvent(new OrderSubmittedEvent(id));
    }
}

// 实体
public class OrderLine {
    private ProductId productId;
    private int quantity;
    private Money price;
    
    // 实体有ID，但无全局唯一性
}

// 值对象
public class Address {
    private final String street;
    private final String city;
    private final String zipCode;
    
    // 值对象不可变
    public Address(String street, String city, String zipCode) {
        this.street = street;
        this.city = city;
        this.zipCode = zipCode;
    }
}
```

## 仓库接口

```java
public interface OrderRepository {
    Order findById(OrderId id);
    void save(Order order);
    List<Order> findByCustomerId(CustomerId customerId);
}
```

## 学习要点

1. 聚合根设计原则
2. 实体与值对象区分
3. 事务边界
4. 领域事件
5.  eventual consistency

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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
