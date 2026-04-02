# Distributed Transaction Seata Demo

Seata分布式事务演示项目，展示微服务架构下的分布式事务解决方案。

## 什么是分布式事务

在微服务架构中，业务操作可能涉及多个服务的数据库。分布式事务用于保证跨服务的操作要么全部成功，要么全部回滚。

```
下单场景:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  订单服务    │────▶│  库存服务    │────▶│  账户服务    │
│  (创建订单)  │     │  (扣减库存)  │     │  (扣减余额)  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                    分布式事务
         要么全部成功，要么全部回滚
```

## Seata介绍

Seata是阿里巴巴开源的分布式事务解决方案，提供4种模式：
- **AT模式** (Automatic Transaction)：自动补偿，侵入性小
- **TCC模式** (Try-Confirm-Cancel)：手动实现三阶段
- **Saga模式**：长事务，状态机驱动
- **XA模式**：基于XA协议的两阶段提交

## 技术栈

- Spring Boot 2.7
- Spring Cloud Alibaba Seata
- Spring Data JPA
- MySQL
- OpenFeign

## 项目结构

```
distributed-transaction-seata-demo/
├── Order Service (订单服务)
│   ├── 创建订单
│   └── 调用库存和账户服务
├── Storage Service (库存服务)
│   └── 扣减库存
└── Account Service (账户服务)
    └── 扣减余额
```

## 快速开始

### 1. 启动Seata Server

```bash
# 下载Seata Server
curl -O https://github.com/seata/seata/releases/download/v1.7.0/seata-server-1.7.0.tar.gz
tar -xzf seata-server-1.7.0.tar.gz
cd seata-server-1.7.0

# 启动 (单机模式)
sh bin/seata-server.sh -p 8091 -h 127.0.0.1 -m file
```

### 2. 配置数据库

```sql
-- 订单库
CREATE DATABASE seata_order;
USE seata_order;
CREATE TABLE t_order (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    product_id BIGINT,
    count INT,
    money DECIMAL(10,2),
    status INT
);

-- 库存库
CREATE DATABASE seata_storage;
USE seata_storage;
CREATE TABLE t_storage (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT,
    count INT
);
INSERT INTO t_storage VALUES (1, 1, 100);

-- 账户库
CREATE DATABASE seata_account;
USE seata_account;
CREATE TABLE t_account (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    balance DECIMAL(10,2)
);
INSERT INTO t_account VALUES (1, 1, 1000.00);
```

### 3. 启动应用

```bash
# 启动三个服务
mvn spring-boot:run -Dspring-boot.run.profiles=order
mvn spring-boot:run -Dspring-boot.run.profiles=storage  
mvn spring-boot:run -Dspring-boot.run.profiles=account
```

### 4. 测试分布式事务

```bash
# 正常下单 - 全部成功
curl -X POST "http://localhost:8080/order/create" \
  -H "Content-Type: application/json" \
  -d '{"userId":1,"productId":1,"count":2}'

# 模拟异常 - 触发回滚
# 修改账户余额为0，使扣减失败
curl -X POST "http://localhost:8080/order/create" \
  -H "Content-Type: application/json" \
  -d '{"userId":1,"productId":1,"count":20}'
# 结果：订单创建失败，库存未扣减，数据保持一致
```

## AT模式原理

### 一阶段：业务执行
```
1. 解析SQL，生成前镜像（Before Image）
2. 执行业务SQL
3. 生成后镜像（After Image）
4. 插入Undo Log
```

### 二阶段：事务提交/回滚
```
成功：删除Undo Log
失败：根据Undo Log生成反向SQL，执行回滚
```

```sql
-- 示例：扣减库存
UPDATE t_storage SET count = count - 10 WHERE product_id = 1;

-- Undo Log（自动生成的反向SQL）
UPDATE t_storage SET count = 90 WHERE product_id = 1;
```

## 核心注解

### @GlobalTransactional
```java
@Service
public class OrderService {
    
    @GlobalTransactional(name = "create-order", rollbackFor = Exception.class)
    public Order createOrder(Long userId, Long productId, Integer count) {
        // 1. 创建订单
        // 2. 扣减库存（远程调用）
        // 3. 扣减账户（远程调用）
        // 任一环节失败，全部回滚
    }
}
```

## Seata架构

```
┌─────────────────────────────────────────┐
│              TC (Transaction Coordinator)│
│              事务协调器                   │
│           (独立部署的服务)                │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│   TM      │ │    RM     │ │    RM     │
│事务管理器   │ │资源管理器   │ │资源管理器   │
│@Global    │ │(各服务DB)  │ │(各服务DB)  │
│Transactional│ │           │ │           │
└───────────┘ └───────────┘ └───────────┘

TM: Transaction Manager (事务管理器)
RM: Resource Manager (资源管理器)
TC: Transaction Coordinator (事务协调器)
```

## 事务模式对比

| 模式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| AT | 无侵入、自动补偿 | 需要Undo Log存储 | 简单CRUD |
| TCC | 性能高、控制精确 | 业务侵入大 | 复杂业务 |
| Saga | 长事务支持 | 无隔离性 | 业务流程长 |
| XA | 强一致性 | 性能差、阻塞 | 金融级一致 |

## 生产配置

### 高可用TC集群
```yaml
seata:
  registry:
    type: nacos
    nacos:
      server-addr: localhost:8848
      group: SEATA_GROUP
  config:
    type: nacos
    nacos:
      server-addr: localhost:8848
      group: SEATA_GROUP
```

### 存储模式
```yaml
seata:
  server:
    store:
      mode: db  # 使用数据库存储事务日志
      db:
        datasource: druid
        db-type: mysql
        driver-class-name: com.mysql.cj.jdbc.Driver
        url: jdbc:mysql://localhost:3306/seata
        user: root
        password: password
```

## 学习要点

1. CAP理论与BASE理论
2. 两阶段提交(2PC)与三阶段提交(3PC)
3. Seata AT模式的Undo Log机制
4. 分布式事务的隔离级别
5. 事务超时与重试策略

## 参考

- [Seata官方文档](https://seata.io/zh-cn/docs/overview/what-is-seata.html)
- [分布式事务理论基础](https://seata.io/zh-cn/docs/dev/mode/transaction-mode.html)
