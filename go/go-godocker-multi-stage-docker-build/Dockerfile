# 第一阶段：构建阶段
# 使用官方Golang Alpine镜像作为构建环境
# Alpine版本更小，适合CI/CD
FROM golang:1.21-alpine AS builder

# 设置工作目录
WORKDIR /app

# 为Go模块设置环境变量
# 启用模块下载代理加速
ENV GOPROXY=https://proxy.golang.org,direct

# 关键设置：禁用CGO以生成静态二进制文件
# 这样可以在无glibc的最小镜像（如Alpine）中运行
ENV CGO_ENABLED=0

# 只复制go.mod和go.sum（如果存在）
# 利用Docker构建缓存：只有当这些文件改变时才重新下载依赖
COPY go.mod .*

# 下载依赖到模块缓存
# 使用--mod=readonly确保不意外修改模块文件
RUN go mod download

# 复制整个源代码
COPY . .

# 构建应用为静态二进制文件
# -o 指定输出路径
# ./... 表示构建所有包
RUN go build -o main .


# 第二阶段：运行阶段
# 使用极小的Alpine Linux作为运行时基础
# 最终镜像只包含运行所需内容
FROM alpine:latest AS final

# 创建非root用户以提升安全性
# 避免容器以root权限运行的安全风险
RUN adduser -D -s /bin/sh appuser

# 设置工作目录
WORKDIR /app

# 从构建阶段复制编译好的二进制文件
# --from=builder 指定来源阶段
COPY --from=builder /app/main .

# 更改文件所有权给非root用户
RUN chown appuser:appuser main

# 使用非root用户运行应用
USER appuser

# 声明容器运行时监听的端口
# 这只是文档说明，实际需在运行时用-p映射
EXPOSE 8080

# 定义容器启动命令
# 使用exec格式避免shell注入，更安全
CMD ["./main"]