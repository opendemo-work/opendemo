<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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

```bash
# 请根据实际案例替换
./scripts/demo.sh
```


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*


---

## 📖 深入理解

### 工作原理

Go-ELK日志聚合集成Demo 的核心机制可以概括为以下几个步骤：

1. **初始化阶段**：准备运行环境，加载必要的配置和依赖。
2. **执行阶段**：按照预定的流程执行主要逻辑，处理输入并生成输出。
3. **验证阶段**：检查结果是否符合预期，记录关键指标和日志。
4. **清理阶段**：释放资源，确保环境可以重复运行。

### 关键设计决策

| 决策点 | 方案 | 理由 |
|--------|------|------|
| 部署方式 | 本地容器化 | 降低环境依赖，便于复现 |
| 配置管理 | 环境变量 + 配置文件 | 灵活且安全 |
| 可观测性 | 日志 + 指标 | 便于排查和优化 |
| 扩展性 | 模块化设计 | 方便后续添加新功能 |

### 性能考量

在实际生产环境中使用本案例时，建议关注以下性能指标：

- **响应时间**：确保核心操作在可接受范围内完成。
- **资源占用**：监控 CPU、内存、磁盘和网络使用情况。
- **吞吐量**：根据业务需求评估并发处理能力。
- **错误率**：建立告警机制，及时发现异常。

---

## 🛡️ 安全与最佳实践

### 安全建议

- 不要在生产环境中使用默认密码或密钥。
- 定期更新依赖组件到最新稳定版本。
- 对敏感配置使用密钥管理工具（如 Kubernetes Secrets、Vault）。
- 限制网络暴露面，使用防火墙或安全组控制访问。

### 最佳实践

- 在修改配置前备份现有环境。
- 使用版本控制管理所有配置文件和脚本。
- 编写自动化测试覆盖核心路径。
- 记录运行日志，便于审计和故障排查。

---

## 🧪 进阶实验

完成基础演示后，可以尝试以下进阶实验：

1. **参数调优**：修改关键配置参数，观察对结果的影响。
2. **故障注入**：故意制造错误，验证系统的容错能力。
3. **压力测试**：增加负载，评估系统瓶颈。
4. **集成测试**：将本案例与其他组件组合，构建完整链路。

---

## 📚 扩展资源

### 官方文档

- [相关技术官方文档](https://example.com)
- [OpenDemo 项目主页](https://github.com/opendemo)

### 推荐书籍

- 《相关技术权威指南》
- 《云原生架构实践》

### 社区与论坛

- Stack Overflow 相关标签
- GitHub Discussions
- 技术博客与公众号

---

## 🤝 贡献与反馈

如果你发现本案例有任何问题，或希望补充更多内容，欢迎提交 Issue 或 Pull Request。

---

*本 README 为 OpenDemo 五星案例标准模板，请根据实际案例内容持续完善。*
