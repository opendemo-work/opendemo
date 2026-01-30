# Go缓存预热与缓存策略演示

## 简介
本Demo展示了在Go语言中如何实现缓存预热和常见的缓存策略（如LRU、TTL过期）。通过两个示例程序，帮助开发者理解如何提升系统性能并避免缓存击穿问题。

## 学习目标
- 理解缓存预热的概念及其作用
- 掌握使用第三方库实现带TTL的内存缓存
- 学会在应用启动时预加载热点数据
- 了解并发安全的缓存访问模式

## 环境要求
- Go 1.19 或更高版本
- 支持git的网络环境（用于拉取依赖）
- Windows / Linux / Mac 均可

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目目录：`cd path/to/demo`
3. 下载依赖包：
   ```bash
   go mod init cache-demo
   go get github.com/patrickmn/go-cache@v2.1.0
   ```

## 文件说明
- `main.go`: 主程序，展示缓存预热流程
- `cache_strategy.go`: 实现不同缓存策略的封装
- `go.mod`: Go模块依赖声明文件

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir cache-demo && cd cache-demo
```

### 步骤2: 初始化Go模块并安装依赖
```bash
go mod init cache-demo
go get github.com/patrickmn/go-cache@v2.1.0
```
**预期输出**:
```
go: creating new go.mod: module cache-demo
... 下载成功 ...
go: downloading github.com/patrickmn/go-cache v2.1.0
```

### 步骤3: 复制代码文件
将 `main.go` 和 `cache_strategy.go` 的内容复制到对应文件中。

### 步骤4: 运行程序
```bash
go run main.go
```

**预期输出**:
```
[初始化] 正在预热缓存...
[缓存预热] 已加载用户: user_1 -> Alice
[缓存预热] 已加载用户: user_2 -> Bob
[查询] 从缓存获取 user_1: Alice, 存在: true
[查询] 从缓存获取 user_3: , 存在: false
[后台] 缓存清理完成，剩余条目数: 1
```

## 代码解析

### `preloadCache()` 函数（main.go）
```go
func preloadCache(c *CacheManager) {
    fmt.Println("[初始化] 正在预热缓存...")
    users := map[string]string{
        "user_1": "Alice",
        "user_2": "Bob",
    }
    for k, v := range users {
        c.Set(k, v)
        fmt.Printf("[缓存预热] 已加载用户: %s -> %s\n", k, v)
    }
}
```
- 在应用启动时模拟从数据库加载热点数据
- 提前填充缓存，避免首次请求时的延迟高峰

### `NewCacheManager()` 构造函数（cache_strategy.go）
```go
func NewCacheManager() *CacheManager {
    return &CacheManager{
        cache: gocache.New(5*time.Minute, 10*time.Minute),
    }
}
```
- 使用 `patrickmn/go-cache` 库创建一个线程安全的内存缓存
- 设置默认过期时间为5分钟，清理间隔为10分钟

## 预期输出示例
```
[初始化] 正在预热缓存...
[缓存预热] 已加载用户: user_1 -> Alice
[缓存预热] 已加载用户: user_2 -> Bob
[查询] 从缓存获取 user_1: Alice, 存在: true
[查询] 从缓存获取 user_3: , 存在: false
[后台] 缓存清理完成，剩余条目数: 1
```

## 常见问题解答

**Q: 为什么需要缓存预热？**
A: 避免系统启动后首次访问数据库造成瞬时高负载，提升响应速度。

**Q: 缓存过期时间设置多久合适？**
A: 根据业务需求调整。高频变动数据建议短TTL（如30秒），静态数据可设为几分钟甚至更长。

**Q: 是否支持分布式缓存？**
A: 当前示例为本地内存缓存。若需分布式，请结合 Redis 并使用 `go-redis` 库。

## 扩展学习建议
- 尝试集成Redis作为远程缓存后端
- 添加HTTP服务接口暴露缓存查询功能
- 实现LRU淘汰策略替代TTL机制
- 使用 `sync.Once` 确保预热只执行一次