# Go配置热更新与文件监听Demo

## 简介
本示例演示如何使用Go语言结合`fsnotify`库实现配置文件的热更新。当配置文件被修改时，程序能自动检测变更并重新加载配置，无需重启服务。

## 学习目标
- 掌握使用 `fsnotify` 监听文件系统变化
- 实现配置热更新机制
- 理解非阻塞式事件监听模型
- 提升Go中并发与I/O处理能力

## 环境要求
- Go 1.19 或更高版本（跨平台支持：Windows/Linux/macOS）

## 安装依赖的详细步骤
1. 确保已安装Go环境：
   ```bash
   go version
   # 预期输出：go version go1.19+ ...
   ```

2. 初始化Go模块并添加依赖：
   ```bash
   go mod init config-watcher-demo
   go get github.com/fsnotify/fsnotify@v1.6.0
   ```

## 文件说明
- `main.go`：主程序，启动文件监听器并处理配置变更
- `config.json`：模拟的配置文件，程序会监听其变化

## 逐步实操指南

### 步骤1：创建配置文件
```bash
echo '{"port": 8080, "debug": true}' > config.json
```

### 步骤2：运行程序
```bash
go run main.go
```

### 步骤3：修改配置文件触发热更新
在另一个终端中执行：
```bash
echo '{"port": 8081, "debug": false}' > config.json
```

观察原程序输出，应打印出“检测到配置文件变更，正在重载...”

### 步骤4：停止程序
按 `Ctrl+C` 结束程序，会看到优雅退出日志。

## 代码解析

### `main.go` 关键逻辑
- 使用 `fsnotify.NewWatcher()` 创建监听器
- 启动 goroutine 异步监听文件事件（Write/Rename等）
- 捕获 `os.Interrupt` 信号实现优雅关闭
- 模拟重载配置：实际项目中可替换为结构体解析或回调函数

### 事件过滤
仅对 `Write` 和 `Create` 事件响应，避免重复触发。使用 `time.After` 可做防抖优化（本例未展开）。

## 预期输出示例
```bash
监听 config.json 中...
检测到配置文件变更，正在重载...
检测到配置文件变更，正在重载...
收到中断信号，正在退出...
```

## 常见问题解答

**Q: 修改文件后没有反应？**
A: 确保编辑器保存的是同一个文件路径，某些编辑器会先写临时文件再移动，建议用命令行 `echo` 测试。

**Q: 如何监听整个目录？**
A: 将 `watcher.Add("config.json")` 改为 `watcher.Add("./configs/")` 即可。

**Q: 能否支持YAML/TOML格式？**
A: 可以！只需在重载时用对应解析库（如`go-yaml/yaml`）读取内容即可，监听机制不变。

## 扩展学习建议
- 添加配置解析结构体和验证逻辑
- 引入 `viper` 库实现更强大的热更新功能
- 结合 HTTP 服务，在配置变更时通知其他模块
- 实现去重与防抖机制防止高频触发
- 使用 `fsnotify` + `embed` 实现静态资源热加载（开发模式）