# Go-ELK日志聚合集成Demo

## 简介
本项目演示如何使用Go语言将应用程序日志通过HTTP发送至ELK（Elasticsearch + Logstash + Kibana）栈，实现集中式日志管理与可视化。包含两个场景：直接写入Logstash、结构化日志输出。

## 学习目标
- 掌握Go中使用`log`和`net/http`发送日志到Logstash
- 理解JSON格式日志在ELK中的重要性
- 学会本地搭建简易ELK环境并验证日志流入

## 环境要求
- Go 1.19 或更高版本
- Docker 20.10 或更高版本（用于运行ELK）
- 操作系统：Windows / Linux / macOS

## 安装依赖步骤
1. 安装Go：访问 https://golang.org/dl/ 下载并安装
2. 安装Docker：访问 https://docs.docker.com/get-docker/ 安装
3. 克隆本项目（假设已存在）

## 文件说明
- `main.go`：主程序，模拟业务日志并发送到Logstash
- `structured_logger.go`：使用结构化日志格式发送更丰富的上下文信息
- `docker-compose.yml`：定义ELK服务栈（简化版）

## 逐步实操指南

### 步骤1：启动ELK服务
```bash
docker-compose up -d
```

> 预期输出：
> Creating network "elk_go_demo_default" with default driver
> Creating elk_go_demo_elasticsearch_1 ... done
> Creating elk_go_demo_logstash_1     ... done
> Creating elk_go_demo_kibana_1       ... done

等待约30秒让服务初始化。

### 步骤2：运行Go日志发送程序
```bash
go run main.go
```

> 预期输出：
> 2025/04/05 10:00:00 发送日志成功: map[message:用户登录成功 level:info user_id:1001]
> 2025/04/05 10:00:01 发送日志成功: map[message:订单创建失败 level:error order_id:ORD-2025 user_id:1002]

### 步骤3：查看Kibana仪表板
打开浏览器访问：http://localhost:5601
1. 进入 **Stack Management > Index Patterns** 创建索引模式 `logstash-*`
2. 进入 **Discover** 查看实时日志

## 代码解析

### main.go 关键段
```go
req, _ := http.NewRequest("POST", logstashURL, bytes.NewBuffer(jsonData))
req.Header.Set("Content-Type", "application/json")
client.Do(req)
```
- 使用标准库发送POST请求到Logstash的HTTP输入插件
- 设置正确Content-Type确保Logstash能解析JSON

### structured_logger.go 特点
- 使用`map[string]interface{}`构建结构化日志
- 包含时间戳、级别、trace_id等字段，便于Kibana过滤和分析

## 预期输出示例（Kibana中可见）
```json
{
  "@timestamp": "2025-04-05T02:00:00.000Z",
  "level": "info",
  "message": "用户登录成功",
  "user_id": 1001,
  "service": "go-auth"
}
```

## 常见问题解答

**Q1: 日志未出现在Kibana？**
A: 检查Logstash容器日志：`docker logs elk_go_demo_logstash_1`，确认是否有解析错误或网络拒绝。

**Q2: 提示连接被拒绝？**
A: 确保ELK服务已完全启动，尤其是Logstash监听端口5044或8080。

**Q3: 如何修改日志字段？**
A: 修改`generateLogEntry`函数中的map字段即可，Kibana会自动识别新字段。

## 扩展学习建议
- 集成zap日志库替代标准log以提升性能
- 添加TLS加密和认证到Logstash通信
- 使用Filebeat替代直接HTTP发送，更适合生产环境
- 在Elasticsearch中配置索引模板和生命周期策略