# 🐹 Go 命令行速查表 (go-cli.md)

> Go语言开发必备的命令行参考手册，涵盖Go工具链、包管理、测试、构建等核心功能，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [Go基础命令](#go基础命令)
- [包管理](#包管理)
- [构建和编译](#构建和编译)
- [测试工具](#测试工具)
- [代码质量](#代码质量)
- [调试工具](#调试工具)
- [性能分析](#性能分析)
- [文档生成](#文档生成)
- [依赖管理](#依赖管理)
- [模块操作](#模块操作)
- [跨平台编译](#跨平台编译)
- [最佳实践](#最佳实践)

---

## Go基础命令

### 环境管理
```bash
# 查看Go环境信息
go env
go env GOPATH
go env GOROOT

# 设置环境变量
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GO111MODULE=on

# 查看版本信息
go version
go version -m binary_file

# 清理缓存
go clean -cache
go clean -modcache
```

### 项目初始化
```bash
# 初始化Go模块
go mod init github.com/username/project

# 下载依赖
go mod download

# 整理依赖
go mod tidy

# 查看依赖图
go mod graph
```

---

## 包管理

### 包操作
```bash
# 安装包
go get github.com/gin-gonic/gin
go get github.com/gin-gonic/gin@v1.9.1

# 更新包
go get -u github.com/gin-gonic/gin

# 删除未使用的依赖
go mod tidy

# 查看可用版本
go list -m -versions github.com/gin-gonic/gin
```

### 私有包管理
```bash
# 配置私有模块
go env -w GOPRIVATE=github.com/company/*

# SSH认证
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
```

---

## 构建和编译

### 基础编译
```bash
# 编译当前包
go build
go build -o myapp

# 编译指定包
go build ./cmd/server

# 编译并安装到GOPATH/bin
go install

# 编译参数优化
go build -ldflags="-s -w"  # 去除符号表和调试信息
go build -ldflags="-X main.Version=v1.0.0"  # 设置变量
```

### 跨平台编译
```bash
# Windows
GOOS=windows GOARCH=amd64 go build

# Linux
GOOS=linux GOARCH=amd64 go build

# macOS
GOOS=darwin GOARCH=amd64 go build

# ARM架构
GOOS=linux GOARCH=arm64 go build
```

---

## 测试工具

### 单元测试
```bash
# 运行测试
go test
go test -v  # 详细输出

# 运行特定测试
go test -run TestFunctionName

# 测试覆盖率
go test -cover
go test -coverprofile=coverage.out
go tool cover -html=coverage.out

# 基准测试
go test -bench=.
go test -bench=BenchmarkFunction
```

### 测试工具
```bash
# 压力测试
go test -bench=. -benchmem

# 竞态检测
go test -race

# 性能分析
go test -cpuprofile=cpu.prof
go test -memprofile=mem.prof
```

---

## 代码质量

### 代码格式化
```bash
# 格式化代码
go fmt ./...

# 格式化并覆盖原文件
gofmt -w *.go

# 代码检查
go vet ./...
```

### 静态分析
```bash
# 安装静态分析工具
go install golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow@latest

# 运行分析
go vet -vettool=$(which shadow) ./...

# 第三方工具
golangci-lint run
revive ./...
```

---

## 调试工具

### Delve调试器
```bash
# 安装Delve
go install github.com/go-delve/delve/cmd/dlv@latest

# 调试程序
dlv debug main.go
dlv exec ./myapp

# 调试命令
(dlv) break main.main
(dlv) continue
(dlv) print variable_name
(dlv) goroutines
```

### 运行时调试
```bash
# 启用pprof
go tool pprof http://localhost:6060/debug/pprof/profile

# 堆栈跟踪
kill -USR1 <pid>

# 内存转储
go tool pprof -png heap_profile
```

---

## 性能分析

### CPU性能分析
```bash
# 生成CPU profile
go test -cpuprofile=cpu.prof

# 分析profile
go tool pprof cpu.prof
(pprof) top
(pprof) web  # 生成SVG图
```

### 内存分析
```bash
# 生成内存profile
go test -memprofile=mem.prof

# 分析内存使用
go tool pprof mem.prof
(pprof) top
(pprof) list function_name
```

### 并发分析
```bash
# goroutine分析
go tool pprof http://localhost:6060/debug/pprof/goroutine

# 阻塞分析
go tool pprof http://localhost:6060/debug/pprof/block
```

---

## 文档生成

### godoc工具
```bash
# 启动文档服务器
godoc -http=:6060

# 生成文档
go doc package_name
go doc package_name.function_name

# 在线文档
# https://pkg.go.dev/
```

### 注释规范
```go
// Package main implements a simple HTTP server.
package main

// User represents a user entity.
type User struct {
    // ID is the unique identifier.
    ID int `json:"id"`
    // Name is the user's name.
    Name string `json:"name"`
}

// GetUserByID returns a user by ID.
func GetUserByID(id int) (*User, error) {
    // Implementation here
}
```

---

## 依赖管理

### Go Modules
```bash
# 初始化模块
go mod init myproject

# 添加依赖
go get github.com/gin-gonic/gin

# 更新依赖
go get -u github.com/gin-gonic/gin

# 清理未使用依赖
go mod tidy

# 查看依赖树
go mod graph

# 验证依赖
go mod verify
```

### 版本管理
```bash
# 语义化版本
go get github.com/gin-gonic/gin@v1.9.1
go get github.com/gin-gonic/gin@latest

# 兼容性检查
go mod why github.com/gin-gonic/gin

# 替换依赖
go mod edit -replace github.com/gin-gonic/gin=../local/gin
```

---

## 模块操作

### 工作区模式
```bash
# 初始化工作区
go work init ./module1 ./module2

# 添加模块到工作区
go work use ./new-module

# 查看工作区状态
go work sync
```

### 私有模块
```bash
# 配置私有代理
go env -w GOPRIVATE=*.company.com,github.com/company/*

# GOSUMDB配置
go env -w GOSUMDB=sum.golang.org
```

---

## 跨平台编译

### 编译选项
```bash
# 基本跨平台编译
GOOS=linux GOARCH=amd64 go build
GOOS=windows GOARCH=amd64 go build
GOOS=darwin GOARCH=arm64 go build

# 编译标志
go build -ldflags "-s -w -X main.version=1.0.0"

# CGO跨平台编译
CGO_ENABLED=0 GOOS=linux go build
```

### 构建脚本示例
```bash
#!/bin/bash
# build.sh

PLATFORMS=(
    "darwin/amd64"
    "darwin/arm64" 
    "linux/amd64"
    "linux/arm64"
    "windows/amd64"
)

for platform in "${PLATFORMS[@]}"; do
    os=$(echo $platform | cut -d'/' -f1)
    arch=$(echo $platform | cut -d'/' -f2)
    
    echo "Building for $os/$arch"
    GOOS=$os GOARCH=$arch go build -o bin/myapp-$os-$arch
done
```

---

## 最佳实践

### 项目结构
```
project/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/
│   └── utils/
├── api/
├── configs/
├── docs/
├── test/
├── go.mod
├── go.sum
└── README.md
```

### 代码规范
```bash
# 代码检查工具
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
golangci-lint run

# 格式化配置
# .golangci.yml
linters:
  enable:
    - gofmt
    - golint
    - govet
```

### 性能优化
```go
// 避免内存分配
func efficientConcat(strs []string) string {
    var sb strings.Builder
    for _, s := range strs {
        sb.WriteString(s)
    }
    return sb.String()
}

// 使用池化
var bufferPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}
```

---