<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Go语言性能分析与排查工具实战演示

## 🎯 学习目标

通过本案例你将掌握Go语言应用的性能分析和问题排查技能：

- Go内置pprof性能分析工具的使用
- 内存泄漏检测和分析方法
- Goroutine泄漏和阻塞问题排查
- CPU性能瓶颈定位和优化
- OOM问题诊断和预防
- 生产环境Go应用监控最佳实践

## 🛠️ 环境准备

### 系统要求
- Go 1.16+ 开发环境
- Linux/Unix系统（推荐）
- 至少2GB内存用于分析工具运行
- Go应用开发和部署经验

### 依赖安装
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 验证Go环境
go version
go env GOPATH

# 安装性能分析工具
go install github.com/google/pprof@latest
go install github.com/uber/go-torch@latest  # 火焰图工具

# 安装内存分析工具
go install github.com/pkg/profile@latest

# 验证工具安装
which pprof
go tool pprof --help
```

## 📁 项目结构

```
go-debugging-tools-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── cmd/                               # 示例应用
│   ├── memory-leak-demo/              # 内存泄漏演示程序
│   ├── goroutine-leak-demo/           # Goroutine泄漏演示
│   ├── cpu-intensive-demo/            # CPU密集型演示
│   └── oom-simulation-demo/           # OOM模拟演示
├── scripts/                           # 排查脚本
│   ├── go_pprof_analyzer.sh           # pprof分析脚本
│   ├── memory_profiler.sh             # 内存分析脚本
│   ├── goroutine_inspector.sh         # Goroutine检查脚本
│   ├── oom_detector.sh                # OOM检测脚本
│   └── flame_graph_generator.sh       # 火焰图生成脚本
├── configs/                           # 配置文件
│   ├── pprof_config.go                # pprof配置示例
│   ├── profile_settings.conf          # 性能分析配置
│   └── monitoring_rules.conf          # 监控规则配置
├── examples/                          # 实际案例
│   ├── pprof_output_samples/          # pprof输出样本
│   ├── flame_graphs/                  # 火焰图示例
│   ├── memory_analysis_reports/       # 内存分析报告
│   └── troubleshooting_cases.txt      # 故障排查案例
└── docs/                              # 详细文档
    ├── go_pprof_guide.md              # pprof使用指南
    ├── memory_debugging_manual.md     # 内存调试手册
    ├── goroutine_analysis_guide.md    # Goroutine分析指南
    └── oom_prevention_strategies.md   # OOM预防策略
```

## 🔧 核心排查工具详解

### 1. Go内置pprof工具

```go
// 在Go应用中启用pprof
package main

import (
    "log"
    "net/http"
    _ "net/http/pprof"  // 自动注册pprof处理器
    "runtime"
)

func main() {
    // 设置并发数
    runtime.GOMAXPROCS(runtime.NumCPU())
    
    // 启动HTTP服务
    go func() {
        log.Println("Starting pprof server on :6060")
        log.Fatal(http.ListenAndServe(":6060", nil))
    }()
    
    // 你的应用逻辑
    // ...
}
```

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# pprof基本使用
# 采集CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# 采集内存profile
go tool pprof http://localhost:6060/debug/pprof/heap

# 采集goroutine信息
go tool pprof http://localhost:6060/debug/pprof/goroutine

# 交互式分析命令
(pprof) top                    # 查看最耗资源的函数
(pprof) list functionName      # 查看具体函数代码
(pprof) web                    # 生成Web可视化图表
(pprof) png > profile.png      # 生成PNG图片
(pprof) quit
```

### 2. 内存分析和泄漏检测

```go
// 内存泄漏检测示例
package main

import (
    "fmt"
    "net/http"
    _ "net/http/pprof"
    "runtime"
    "time"
)

func memoryLeakDemo() {
    // 模拟内存泄漏
    leakySlice := make([][]byte, 0)
    
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()
    
    for range ticker.C {
        // 不断分配内存但不释放
        data := make([]byte, 1024*1024) // 1MB
        leakySlice = append(leakySlice, data)
        
        // 打印内存使用情况
        var m runtime.MemStats
        runtime.ReadMemStats(&m)
        fmt.Printf("Alloc = %d KB", bToKb(m.Alloc))
    }
}

func bToKb(b uint64) uint64 {
    return b / 1024
}

func main() {
    go func() {
        log.Println(http.ListenAndServe(":6060", nil))
    }()
    
    memoryLeakDemo()
}
```

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 内存分析脚本
#!/bin/bash
APP_URL="http://localhost:6060"

echo "=== Go内存分析 ==="

# 获取堆内存信息
echo "1. 堆内存概览:"
curl -s $APP_URL/debug/pprof/heap > heap.prof
go tool pprof -text heap.prof | head -20

# 分析内存分配
echo "2. 内存分配分析:"
go tool pprof -alloc_objects $APP_URL/debug/pprof/heap

# 检查GC统计
echo "3. GC统计信息:"
curl -s $APP_URL/debug/pprof/goroutine?debug=2 | grep -A 10 "GC forced"
```

### 3. Goroutine分析和泄漏检测

```go
// Goroutine泄漏检测
package main

import (
    "fmt"
    "net/http"
    _ "net/http/pprof"
    "runtime"
    "sync"
    "time"
)

func goroutineLeakDemo() {
    var wg sync.WaitGroup
    
    // 模拟Goroutine泄漏
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            time.Sleep(time.Hour) // 模拟长时间运行但忘记退出
            fmt.Printf("Goroutine %d finished\n", id)
        }(i)
    }
    
    // 定期检查Goroutine数量
    ticker := time.NewTicker(5 * time.Second)
    go func() {
        for range ticker.C {
            fmt.Printf("Current goroutines: %d\n", runtime.NumGoroutine())
        }
    }()
    
    wg.Wait()
}

func main() {
    go func() {
        log.Fatal(http.ListenAndServe(":6060", nil))
    }()
    
    goroutineLeakDemo()
}
```

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# Goroutine分析脚本
#!/bin/bash
APP_URL="http://localhost:6060"

echo "=== Goroutine分析 ==="

# 获取Goroutine堆栈
echo "1. Goroutine堆栈信息:"
curl -s $APP_URL/debug/pprof/goroutine?debug=2 > goroutine.txt

# 统计Goroutine状态
echo "2. Goroutine状态统计:"
grep "goroutine " goroutine.txt | wc -l
grep "runnable" goroutine.txt | wc -l
grep "waiting" goroutine.txt | wc -l

# 查找可能的泄漏
echo "3. 可疑Goroutine:"
grep -B 5 -A 10 "time.Sleep" goroutine.txt | head -20
```

### 4. OOM问题诊断

```go
// OOM模拟和检测
package main

import (
    "fmt"
    "net/http"
    _ "net/http/pprof"
    "runtime"
    "time"
)

func simulateOOM() {
    fmt.Println("开始OOM模拟...")
    
    var bigSlice [][]byte
    ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()
    
    for range ticker.C {
        // 快速分配大量内存
        chunk := make([]byte, 100*1024*1024) // 100MB
        bigSlice = append(bigSlice, chunk)
        
        // 监控内存使用
        var m runtime.MemStats
        runtime.ReadMemStats(&m)
        fmt.Printf("内存使用: %d MB\n", m.Alloc/1024/1024)
        
        // 当接近限制时记录
        if m.Alloc > 800*1024*1024 { // 800MB
            fmt.Println("内存使用接近上限!")
        }
    }
}

func main() {
    // 设置内存限制
    debug.SetGCPercent(10) // 更频繁的GC
    
    go func() {
        log.Fatal(http.ListenAndServe(":6060", nil))
    }()
    
    simulateOOM()
}
```

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# OOM检测和预防脚本
#!/bin/bash
PID=$1
APP_NAME=${2:-"go-app"}

echo "=== OOM风险检测 ==="

# 1. 监控进程内存使用
MEMORY_USAGE=$(ps -p $PID -o rss= | awk '{print int($1/1024)}')
echo "当前内存使用: ${MEMORY_USAGE}MB"

# 2. 检查系统内存压力
FREE_MEM=$(free -m | awk 'NR==2{printf "%.2f", $7*100/$2}')
echo "系统可用内存: ${FREE_MEM}%"

# 3. 分析Go内存统计
if curl -s http://localhost:6060/debug/pprof/heap >/dev/null 2>&1; then
    echo "获取Go内存统计..."
    curl -s http://localhost:6060/debug/pprof/heap?debug=1 | grep -E "(Alloc|Sys|HeapAlloc)"
fi

# 4. 检查Goroutine数量
GOROUTINE_COUNT=$(curl -s http://localhost:6060/debug/pprof/goroutine?debug=1 | grep -c "^goroutine ")
echo "活跃Goroutine数: $GOROUTINE_COUNT"

# 5. 风险评估
if [ $MEMORY_USAGE -gt 1000 ] || [ $GOROUTINE_COUNT -gt 10000 ]; then
    echo "⚠️  高风险: 可能存在内存泄漏或Goroutine泄漏"
    echo "建议措施:"
    echo "1. 立即采集pprof数据"
    echo "2. 检查是否有goroutine泄漏"
    echo "3. 考虑重启应用"
else
    echo "✅ 内存使用正常"
fi
```

## 🔍 综合诊断实战

### 场景1：CPU使用率过高

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# Go应用CPU高使用率诊断脚本

PID=$1
PORT=${2:-6060}

echo "=== Go CPU性能诊断 ==="

# 1. 采集CPU profile
echo "1. 采集30秒CPU数据..."
go tool pprof -png http://localhost:$PORT/debug/pprof/profile?seconds=30 > cpu_profile.png

# 2. 分析热点函数
echo "2. CPU热点分析:"
go tool pprof -top http://localhost:$PORT/debug/pprof/profile?seconds=10

# 3. 生成火焰图
echo "3. 生成火焰图..."
go-torch -u http://localhost:$PORT -t 30 > flame.svg

# 4. 检查Goroutine状态
echo "4. Goroutine状态检查:"
curl -s http://localhost:$PORT/debug/pprof/goroutine?debug=2 | head -50

echo "诊断完成，查看生成的分析文件"
```

### 场景2：内存泄漏检测

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# Go内存泄漏检测脚本

PORT=${1:-6060}
DURATION=${2:-60}  # 监控持续时间(秒)

echo "=== 内存泄漏检测 (持续${DURATION}秒) ==="

# 1. 初始内存快照
echo "1. 初始内存状态:"
INITIAL_HEAP=$(curl -s http://localhost:$PORT/debug/pprof/heap?debug=1 | grep "Alloc" | awk '{print $2}')
echo "初始堆分配: $INITIAL_HEAP bytes"

# 2. 持续监控内存增长
echo "2. 监控内存变化:"
for i in $(seq 1 $((DURATION/5))); do
    sleep 5
    CURRENT_HEAP=$(curl -s http://localhost:$PORT/debug/pprof/heap?debug=1 | grep "Alloc" | awk '{print $2}')
    GROWTH=$((CURRENT_HEAP - INITIAL_HEAP))
    echo "第$((i*5))秒: 堆分配 ${CURRENT_HEAP} bytes (增长: ${GROWTH} bytes)"
    
    if [ $GROWTH -gt 100000000 ]; then  # 增长超过100MB
        echo "⚠️  内存增长异常，可能存在泄漏"
        break
    fi
done

# 3. 详细内存分析
echo "3. 详细内存分析:"
go tool pprof -alloc_objects http://localhost:$PORT/debug/pprof/heap

# 4. 检查Top内存使用者
echo "4. Top内存使用者:"
go tool pprof -top -alloc_space http://localhost:$PORT/debug/pprof/heap | head -10
```

### 场景3：Goroutine泄漏

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# Goroutine泄漏检测脚本

PORT=${1:-6060}
THRESHOLD=${2:-1000}  # Goroutine数量阈值

echo "=== Goroutine泄漏检测 ==="

# 1. 获取Goroutine统计
GOROUTINE_COUNT=$(curl -s http://localhost:$PORT/debug/pprof/goroutine?debug=1 | grep -c "^goroutine ")

echo "当前Goroutine数量: $GOROUTINE_COUNT"

# 2. 检查是否超过阈值
if [ $GOROUTINE_COUNT -gt $THRESHOLD ]; then
    echo "⚠️  Goroutine数量异常!"
    
    # 3. 分析Goroutine堆栈
    echo "3. 分析Goroutine堆栈:"
    curl -s http://localhost:$PORT/debug/pprof/goroutine?debug=2 > goroutine_stacks.txt
    
    # 4. 统计常见阻塞位置
    echo "4. 常见阻塞位置:"
    grep -E "(chan receive|semacquire|select)" goroutine_stacks.txt | \
        awk '{print $2}' | sort | uniq -c | sort -nr | head -10
    
    # 5. 生成报告
    echo "5. 生成泄漏分析报告..."
    echo "Goroutine泄漏检测报告 - $(date)" > goroutine_leak_report.txt
    echo "Goroutine数量: $GOROUTINE_COUNT" >> goroutine_leak_report.txt
    echo "阈值: $THRESHOLD" >> goroutine_leak_report.txt
    echo "" >> goroutine_leak_report.txt
    echo "Top阻塞位置:" >> goroutine_leak_report.txt
    grep -E "(chan receive|semacquire|select)" goroutine_stacks.txt | \
        awk '{print $2}' | sort | uniq -c | sort -nr | head -10 >> goroutine_leak_report.txt
else
    echo "✅ Goroutine数量正常"
fi
```

## 📊 监控和告警配置

### Prometheus监控集成
```yaml
# prometheus.yml 配置示例
scrape_configs:
  - job_name: 'go-app'
    static_configs:
      - targets: ['localhost:6060']
    metrics_path: '/debug/metrics'
    
# 告警规则
groups:
- name: go_app_alerts
  rules:
  - alert: HighMemoryUsage
    expr: go_memstats_alloc_bytes > 1073741824  # 1GB
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "Go应用内存使用过高"
      
  - alert: HighGoroutineCount
    expr: go_goroutines > 5000
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Goroutine数量异常"
```

### 应用内监控代码
```go
// 内置监控指标
package main

import (
    "expvar"
    "net/http"
    _ "net/http/pprof"
    "runtime"
)

var (
    requestCount = expvar.NewInt("request_count")
    errorCount   = expvar.NewInt("error_count")
    activeGoroutines = expvar.NewInt("active_goroutines")
)

func monitorMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestCount.Add(1)
        activeGoroutines.Set(int64(runtime.NumGoroutine()))
        next.ServeHTTP(w, r)
    })
}

func main() {
    // 注册监控中间件
    http.Handle("/api/", monitorMiddleware(apiHandler))
    
    // 启动服务
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## 🧪 验证测试

### 工具可用性测试
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# Go排查工具验证脚本

echo "=== Go排查工具验证 ==="

# 检查Go环境
if ! command -v go &> /dev/null; then
    echo "❌ Go环境未安装"
    exit 1
fi

GO_VERSION=$(go version)
echo "✅ Go版本: $GO_VERSION"

# 检查pprof工具
if go tool pprof --help >/dev/null 2>&1; then
    echo "✅ pprof工具可用"
else
    echo "❌ pprof工具不可用"
fi

# 检查第三方工具
TOOLS=("go-torch" "profile")
for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool 工具可用"
    else
        echo "⚠️  $tool 工具未安装"
    fi
done

# 编译测试应用
echo "编译测试应用..."
cd cmd/memory-leak-demo
go build -o test-app .
if [ $? -eq 0 ]; then
    echo "✅ 测试应用编译成功"
    ./test-app &
    TEST_PID=$!
    sleep 2
    
    # 测试pprof接口
    if curl -s http://localhost:6060/debug/pprof/ >/dev/null 2>&1; then
        echo "✅ pprof接口正常"
    else
        echo "❌ pprof接口异常"
    fi
    
    kill $TEST_PID
else
    echo "❌ 测试应用编译失败"
fi
```

## ❓ 常见问题处理

### Q1: pprof无法连接到应用？
**解决方案**：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查端口是否开放
netstat -tlnp | grep :6060

# 检查防火墙设置
sudo iptables -L | grep 6060

# 确认pprof已正确导入
import _ "net/http/pprof"

# 检查应用是否正常运行
curl http://localhost:6060/debug/pprof/
```

### Q2: 火焰图生成失败？
**解决方案**：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装Graphviz
sudo apt-get install graphviz  # Ubuntu/Debian
sudo yum install graphviz      # CentOS/RHEL

# 检查go-torch安装
go install github.com/uber/go-torch@latest

# 使用替代方案生成SVG
go tool pprof -svg http://localhost:6060/debug/pprof/profile > profile.svg
```

### Q3: 内存持续增长但找不到泄漏点？
**排查建议**：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 检查全局变量
# 2. 分析finalizer和GC行为
# 3. 检查cgo调用
# 4. 使用更详细的内存分析
go tool pprof -alloc_objects -cumulative http://localhost:6060/debug/pprof/heap
```

## 📚 扩展学习

### 专业工具推荐
- **Delve**: Go调试器
- **Goland**: JetBrains Go IDE内置分析工具
- **Datadog APM**: 分布式追踪
- **Grafana**: 监控面板展示

### 学习进阶路径
1. 掌握Go运行时和调度器原理
2. 深入理解垃圾回收机制
3. 学习并发编程最佳实践
4. 掌握性能优化方法论
5. 学习微服务监控体系

---
> **💡 提示**: Go的pprof工具非常强大，在生产环境中使用时要注意性能影响，建议在低峰期进行深度分析。
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
