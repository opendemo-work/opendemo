# Makefile for Go project automation

# 定义二进制文件输出路径
BINARY=bin/app

# 默认目标
all: build

# 构建应用：先格式化再编译
build: fmt
	go build -o $(BINARY) main.go

# 运行测试
test:
	go test ./...

# 格式化所有Go源码
fmt:
	go fmt ./...

# 构建并运行程序
run: build
	./$(BINARY)

# 清理生成的文件
clean:
	rm -f $(BINARY)

# 显示帮助信息
help:
	@echo "Go项目构建帮助菜单："
	@echo "  build        编译应用程序"
	@echo "  test         运行单元测试"
	@echo "  fmt          格式化代码"
	@echo "  clean        清理编译生成的文件"
	@echo "  run          构建并运行程序"
	@echo "  help         显示此帮助信息"

# 声明伪目标，避免与同名文件冲突
.PHONY: all build test fmt run clean help
