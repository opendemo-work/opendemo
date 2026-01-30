# Go语言LRU缓存策略实现Demo

## 简介
本项目演示如何在Go中实现一个高效的LRU（Least Recently Used，最近最少使用）缓存。LRU是一种常见的缓存淘汰策略，广泛应用于数据库、操作系统和Web服务中。

## 学习目标
- 理解LRU缓存的工作原理
- 掌握Go中结构体、指针和哈希表的组合使用
- 学会用双向链表+哈希表实现O(1)时间复杂度的LRU缓存
- 提升对Go内存管理和接口设计的理解

## 环境要求
- Go 1.19 或更高版本
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖步骤
1. 下载并安装Go：https://golang.org/dl/
2. 验证安装：
   ```bash
   go version
   # 预期输出：go version go1.19.x os/arch
   ```
3. 创建项目目录并进入：
   ```bash
   mkdir lru-demo && cd lru-demo
   go mod init lru-demo
   ```

## 文件说明
- `lru_cache.go`：核心LRU缓存实现
- `main.go`：测试和演示程序

## 逐步实操指南

### 步骤1：创建LRU缓存文件
```bash
cat > lru_cache.go << 'EOF'
$(cat lru_cache.go)
EOF
```

### 步骤2：创建主程序文件
```bash
cat > main.go << 'EOF'
$(cat main.go)
EOF
```

### 步骤3：运行程序
```bash
go run main.go
```

**预期输出**：
```
Put: A=1
Put: B=2
Put: C=3
Get B: 2, true
Get A: 1, true
Put D=4 （触发A被移除）
Get A: 0, false
Get B: 2, true
Get C: 3, true
Get D: 4, true
```

## 代码解析

### 双向链表节点
```go
// entry 表示缓存中的键值对，同时作为双向链表的节点
// 包含前后指针，用于维护访问顺序
```

### 核心数据结构
```go
// LRUCache 使用哈希表+双向链表实现
// map实现O(1)查找，双向链表维护访问顺序
// 头部为最新使用，尾部为最久未使用
```

### Get操作
- 命中时将节点移到链表头部（标记为最新使用）
- 未命中返回零值和false

### Put操作
- 已存在则更新值并移至头部
- 不存在时检查容量，满则删除尾部元素
- 新节点插入头部

## 常见问题解答

**Q：为什么使用双向链表而不是单向链表？**
A：因为需要从链表中间删除节点，双向链表可以O(1)找到前驱节点。

**Q：为什么哈希表存储的是指针而不是值？**
A：为了在O(1)时间内定位到链表节点并移动它，避免遍历链表。

**Q：这个实现是线程安全的吗？**
A：不是。如需并发使用，需额外添加互斥锁（sync.Mutex）。

## 扩展学习建议
1. 添加并发支持（使用sync.RWMutex）
2. 实现TTL（Time-To-Live）过期机制
3. 将缓存持久化到磁盘
4. 实现LFU（最不经常使用）缓存策略
5. 使用Go的pprof分析内存性能