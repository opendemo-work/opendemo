# Go Viper配置管理与环境变量集成示例

本项目演示了如何使用 [Viper](https://github.com/spf13/viper) 库在Go应用程序中优雅地管理配置，支持从环境变量、配置文件等多种来源读取配置。

## 学习目标

- 理解 Viper 在 Go 中的作用：统一管理多种配置源
- 掌握如何通过 Viper 读取环境变量
- 学会使用 Viper 加载 YAML 配置文件并合并环境变量
- 实践 Go 中配置初始化的最佳方式

## 环境要求

- Go 1.20 或更高版本
- 支持 Windows、Linux、macOS

## 安装依赖的详细步骤

1. 打开终端（或命令提示符）
2. 进入项目目录
   ```bash
   mkdir go-viper-demo && cd go-viper-demo
   ```
3. 初始化 Go 模块
   ```bash
   go mod init go-viper-demo
   ```
4. 添加 Viper 依赖
   ```bash
   go get github.com/spf13/viper@v1.16.0
   ```

## 文件说明

- `main.go`：主程序，展示基础配置加载与环境变量绑定
- `config.yaml`：YAML 格式的默认配置文件
- `advanced.go`：高级用法，展示多环境配置与动态重载（不启用重载）

## 逐步实操指南

### 步骤 1：创建 main.go

```bash
cat > main.go <<EOF
// +build ignore

[内容见代码文件]
EOF
```

### 步骤 2：创建 config.yaml

```bash
cat > config.yaml <<EOF
server:
  host: localhost
  port: 8080
database:
  url: postgres://localhost:5432/mydb
EOF
```

### 步骤 3：运行主程序

```bash
go run main.go
```

**预期输出**：
```
服务器将在 localhost:8080 启动
数据库连接: postgres://localhost:5432/mydb
```

### 步骤 4：使用环境变量覆盖配置

```bash
export SERVER_HOST=0.0.0.0
export SERVER_PORT=9000
go run main.go
```

**预期输出**：
```
服务器将在 0.0.0.0:9000 启动
数据库连接: postgres://localhost:5432/mydb
```

## 代码解析

### main.go 关键段解释

```go
viper.AutomaticEnv()                    // 自动绑定环境变量
viper.SetEnvPrefix("SERVER")           // 设置前缀，匹配 SERVER_HOST
viper.BindEnv("host", "SERVER_HOST")  // 显式绑定
```

Viper 会自动将配置键映射到同名大写环境变量，也可通过 `SetEnvPrefix` 和 `BindEnv` 精确控制。

### config.yaml 结构

YAML 层级结构会自动映射为 `viper.Get("server.host")` 形式访问。

## 预期输出示例

```
服务器将在 0.0.0.0:9000 启动
数据库连接: postgres://localhost:5432/mydb
```

## 常见问题解答

**Q: 为什么修改环境变量后没有生效？**
A: 确保调用了 `viper.AutomaticEnv()` 并且变量名匹配（如 `SERVER_HOST` 对应 `server.host`）。

**Q: 如何支持 .env 文件？**
A: 使用 `viper.SetConfigFile(".env")` 并调用 `viper.ReadInConfig()`，但需注意格式支持（建议用 `godotenv` 配合）。

**Q: Viper 支持哪些配置格式？**
A: JSON, TOML, YAML, HCL, envfile 及 Java properties 等。

## 扩展学习建议

- 尝试集成 `cobra` 构建 CLI 工具，与 Viper 联动
- 使用 `fsnotify` 实现配置热重载（生产注意并发安全）
- 多环境配置：开发/测试/生产使用不同 config 文件（如 config-dev.yaml）