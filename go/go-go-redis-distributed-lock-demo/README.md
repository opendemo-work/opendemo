# Go-Redis分布式锁演示

## 简介
本项目演示如何在Go语言中使用Redis实现分布式锁，确保在分布式系统中对共享资源的安全访问。通过`redsync`库封装Redis的原子操作，实现跨多个服务实例的互斥控制。

## 学习目标
- 理解分布式锁的核心概念与应用场景
- 掌握使用Redsync库实现Redis分布式锁的方法
- 学会处理锁获取失败、超时和自动释放等边界情况
- 了解分布式锁的最佳实践与潜在陷阱

## 环境要求
- Go 1.19 或更高版本
- Redis 6.0+（本地或远程运行）
- 支持 `go mod` 的构建环境

## 安装依赖的详细步骤

1. 克隆项目（如适用）：
```bash
go mod init redis-dlock-demo
go mod tidy
```

2. 安装所需依赖库：
```bash
go get github.com/go-redis/redis/v8
go get github.com/go-redsync/redsync/v4
```

## 文件说明
- `main.go`: 主程序，演示单节点锁的获取与释放
- `cluster.go`: 演示基于Redis集群的分布式锁（可选高级场景）
- `go.mod`: 依赖声明文件

## 逐步实操指南

### 步骤1：启动Redis服务
确保Redis正在运行。若使用Docker：
```bash
docker run --rm -p 6379:6379 redis:7
```

### 步骤2：运行主程序
```bash
go run main.go
```

**预期输出**：
```
尝试获取锁...
成功获取锁！
正在执行临界区操作...
操作完成，释放锁。
```

### 步骤3（可选）：运行集群模式
```bash
go run cluster.go
```

> 注意：若未配置Redis集群，该程序将报错退出。

## 代码解析

### main.go 关键段解释
```go
mut := redsync.New(pool).NewMutex("resource_id")
```
创建一个名为 `resource_id` 的互斥锁，底层基于Redis的SET命令实现原子性。

```go
if err := mut.Lock(); err != nil {
    log.Fatalf("无法获取锁: %v", err)
}
```
尝试获取锁，支持自动重试机制，失败时返回错误。

```go
defer func() {
    if ok, _ := mut.Unlock(); !ok {
        log.Println("警告：锁释放失败或已被超时")
    }
}()
```
使用 defer 延迟释放锁，确保即使发生 panic 也能尽量释放。

## 预期输出示例
```
尝试获取锁...
成功获取锁！
正在执行临界区操作...
操作完成，释放锁。
```

## 常见问题解答

**Q: 锁无法获取？**
A: 检查Redis是否运行，网络是否可达，或是否有其他进程长时间持有锁未释放。

**Q: 如何设置锁超时时间？**
A: 使用 `mut.SetExpiry(10 * time.Second)` 在获取前设定过期时间。

**Q: 是否支持重入？**
A: 不支持。Redsync不提供可重入语义，避免死锁风险。

**Q: 多个实例下是否安全？**
A: 是的，只要所有实例连接同一Redis或集群，即可保证互斥。

## 扩展学习建议
- 学习Redlock算法原理（https://redis.io/docs/reference/patterns/distributed-locks/）
- 探索etcd或ZooKeeper实现的分布式锁
- 实现带租约续期的长任务锁机制
- 结合context实现抢占式锁取消
