# Go Domain-Driven Design (DDD)

Go语言领域驱动设计实践。

## DDD分层架构

```
DDD分层:
┌─────────────────────────────────────────────────────────┐
│  User Interface (接口层)                                  │
│  - HTTP Handler                                          │
│  - gRPC Service                                          │
├─────────────────────────────────────────────────────────┤
│  Application (应用层)                                     │
│  - Use Case                                              │
│  - Application Service                                   │
├─────────────────────────────────────────────────────────┤
│  Domain (领域层)                                          │
│  - Entity                                                │
│  - Value Object                                          │
│  - Domain Service                                        │
│  - Repository Interface                                  │
├─────────────────────────────────────────────────────────┤
│  Infrastructure (基础设施层)                              │
│  - Repository Implementation                             │
│  - Database                                              │
│  - External Services                                     │
└─────────────────────────────────────────────────────────┘
```

## 实体与值对象

```go
package domain

import "github.com/google/uuid"

// Order 聚合根
type Order struct {
    ID         OrderID
    CustomerID CustomerID
    Items      []OrderItem
    Status     OrderStatus
    Version    int // 用于乐观锁
}

type OrderID string

func NewOrderID() OrderID {
    return OrderID(uuid.New().String())
}

// OrderItem 值对象
type OrderItem struct {
    ProductID ProductID
    Quantity  int
    Price     Money
}

// Money 值对象
type Money struct {
    Amount   float64
    Currency string
}

func (m Money) Add(other Money) Money {
    return Money{
        Amount:   m.Amount + other.Amount,
        Currency: m.Currency,
    }
}
```

## 领域服务

```go
package domain

// OrderService 领域服务
type OrderService struct {
    orderRepo OrderRepository
}

func (s *OrderService) CreateOrder(customerID CustomerID, items []OrderItem) (*Order, error) {
    order := &Order{
        ID:         NewOrderID(),
        CustomerID: customerID,
        Items:      items,
        Status:     OrderStatusPending,
    }
    
    if err := s.orderRepo.Save(order); err != nil {
        return nil, err
    }
    
    return order, nil
}
```

## 学习要点

1. 领域建模
2. 聚合设计
3. 仓库模式
4. 领域事件
5. 限界上下文
