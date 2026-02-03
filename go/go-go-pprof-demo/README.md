# Go pprof性能分析实战演示

## 简介
本项目提供两个完整的Go程序示例，演示如何使用内置的`net/http/pprof`包进行CPU和内存性能剖析。这些示例模拟了真实场景中的性能问题，并展示了如何通过pprof定位瓶颈。

## 学习目标
- 掌握在Go服务中集成pprof的方法
- 学会采集CPU和内存性能数据
- 理解pprof输出的含义并定位性能热点
- 使用命令行工具分析性能数据

## 环境要求
- Go 1.20 或更高版本
- 标准终端工具（bash/zsh/cmd）
- graphviz（可选，用于生成调用图）

> 验证Go版本：
> ```bash
> go version
> # 预期输出: go version go1.20.x linux/amd64 (或对应平台)
> ```

## 安装依赖
本项目仅依赖Go标准库，无需额外安装依赖。

如果希望生成可视化调用图，可安装graphviz：

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**Windows (使用Chocolatey):**
```powershell
choco install graphviz
```

## 文件说明
- `main.go`: 主服务程序，暴露HTTP接口并集成pprof，包含CPU密集型操作
- `memory.go`: 内存泄漏模拟代码，用于内存剖析
- `go.mod`: Go模块声明文件

## 逐步实操指南

### 步骤1: 初始化模块
```bash
go mod init pprof-demo
```

### 步骤2: 启动服务
```bash
go run main.go memory.go
```

预期输出：
```text
服务器启动在 :8080
访问 /debug/pprof/ 查看pprof界面
模拟内存增长，请稍等...
```

### 步骤3: 采集CPU性能数据
在另一个终端窗口执行：

```bash
# 采集30秒的CPU使用情况
curl "http://localhost:8080/debug/pprof/profile?seconds=30" -o cpu.prof
```

预期输出：
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 1916k    0 1916k    0     0   573k      0 --:--:--  0:00:05 --:--:--  768k
```

### 步骤4: 分析CPU数据
```bash
go tool pprof cpu.prof
```

在pprof交互界面中尝试以下命令：
```text
(pprof) top
(pprof) web
(pprof) list cpuHeavyFunction
```

### 步骤5: 采集内存数据
```bash
# 采集堆内存快照
curl http://localhost:8080/debug/pprof/heap > mem.prof
```

### 步骤6: 分析内存数据
```bash
go tool pprof mem.prof
```

在交互界面中：
```text
(pprof) top
(pprof) tree
(pprof) web
```

## 代码解析

### main.go 关键部分
```go
import _ "net/http/pprof"
```
导入pprof包的副作用是自动注册`/debug/pprof/*`路由到默认HTTP服务。

```go
r.HandleFunc("/cpu", cpuHandler)
```
该处理器模拟CPU密集型任务，便于pprof捕捉到明显的CPU使用热点。

### memory.go 关键部分
```go
var memoryHog []string

func growMemory() {
    for i := 0; i < 10000; i++ {
        memoryHog = append(memoryHog, strings.Repeat("x", 1000))
    }
}
```
此函数持续追加字符串到全局切片，模拟内存泄漏或不当的内存使用模式。

## 预期输出示例

### CPU分析 top 输出示例
```text
Showing nodes accounting for 2.82s, 98.60% of 2.86s total
Dropped 10 nodes (cum <= 0.01s)
Showing top 10 nodes out of 13
      flat  flat%   sum%        cum   cum%
     2.82s 98.60% 98.60%      2.82s 98.60%  runtime.cpuHeavyFunction
         0     0% 98.60%      2.86s   100%  main.cpuHandler
```

### 内存分析 top 输出示例
```text
Showing nodes accounting for 40.13MB, 100% of 40.13MB total
      flat  flat%   sum%        cum   cum%
   40.13MB   100%   100%    40.13MB   100%  main.growMemory
         0     0%   100%    40.13MB   100%  main.memoryHandler
```

## 常见问题解答

**Q: 为什么访问 /debug/pprof/ 没有响应？**
A: 确保已导入 `_ "net/http/pprof"` 并启动了HTTP服务。

**Q: pprof采集的数据为空？**
A: 在采集CPU profile前确保有足够的CPU负载。本示例中需先访问 `/cpu` 接口触发计算。

**Q: 如何在生产环境安全使用pprof？**
A: 建议将pprof端口绑定到内网地址或通过身份验证中间件保护，避免暴露在公网。

**Q: web命令报错“could not execute dot”？**
A: 需要安装graphviz，请参考安装依赖章节。

## 扩展学习建议
- 阅读官方文档：https://pkg.go.dev/net/http/pprof
- 学习使用`runtime.SetBlockProfileRate`进行阻塞分析
- 尝试`mutex`剖析定位锁竞争问题
- 探索`go-torch`等第三方可视化工具
- 实践在Kubernetes环境中远程调试pod的性能问题