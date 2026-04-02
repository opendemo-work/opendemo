# Docker Integration Demo
# 多阶段构建示例

# 第一阶段：构建
FROM eclipse-temurin:11-jdk-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制Maven文件
COPY pom.xml .
COPY src ./src

# 构建应用
RUN apk add --no-cache maven && \
    mvn clean package -DskipTests

# 第二阶段：运行
FROM eclipse-temurin:11-jre-alpine

# 设置时区
ENV TZ=Asia/Shanghai
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone

# 创建非root用户
RUN addgroup -S spring && adduser -S spring -G spring

# 设置工作目录
WORKDIR /app

# 从构建阶段复制jar包
COPY --from=builder /app/target/*.jar app.jar

# 更改所有权
RUN chown -R spring:spring /app

# 切换到非root用户
USER spring

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# 启动应用
ENTRYPOINT ["java", "-jar", "app.jar"]
