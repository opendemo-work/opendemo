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
