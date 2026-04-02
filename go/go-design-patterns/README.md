# Go Design Patterns

Go语言设计模式实践，涵盖GoF经典模式和Go惯用模式。

## 设计模式分类

```
设计模式分类:
┌─────────────────────────────────────────────────────────┐
│ 创建型模式 (Creational)                                  │
│ ├── 单例模式 (Singleton)                                 │
│ ├── 工厂模式 (Factory)                                   │
│ ├── 建造者模式 (Builder)                                 │
│ └── 原型模式 (Prototype)                                 │
├─────────────────────────────────────────────────────────┤
│ 结构型模式 (Structural)                                  │
│ ├── 适配器模式 (Adapter)                                 │
│ ├── 装饰器模式 (Decorator)                               │
│ ├── 代理模式 (Proxy)                                     │
│ └── 外观模式 (Facade)                                    │
├─────────────────────────────────────────────────────────┤
│ 行为型模式 (Behavioral)                                  │
│ ├── 观察者模式 (Observer)                                │
│ ├── 策略模式 (Strategy)                                  │
│ └── 模板方法 (Template Method)                           │
├─────────────────────────────────────────────────────────┤
│ Go惯用模式 (Idiomatic)                                   │
│ ├── 函数选项模式 (Functional Options)                    │
│ └── 中间件模式 (Middleware)                              │
└─────────────────────────────────────────────────────────┘
```

## 单例模式
```go
package singleton

import "sync"

type Singleton struct {
    data string
}

var instance *Singleton
var once sync.Once

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{data: "initialized"}
    })
    return instance
}
```

## 工厂模式
```go
package factory

type PaymentMethod interface {
    Pay(amount float64) error
}

type PaymentFactory struct{}

func (f *PaymentFactory) CreatePayment(method string) PaymentMethod {
    switch method {
    case "creditcard":
        return &CreditCard{}
    case "paypal":
        return &PayPal{}
    default:
        return nil
    }
}
```

## 函数选项模式
```go
package options

type Server struct {
    host string
    port int
}

type Option func(*Server)

func WithHost(host string) Option {
    return func(s *Server) { s.host = host }
}

func NewServer(opts ...Option) *Server {
    s := &Server{host: "localhost", port: 8080}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

## 学习要点

1. Go语言设计模式的独特实现
2. 接口的组合使用
3. 函数作为一等公民的应用
4. 并发安全的设计考虑
