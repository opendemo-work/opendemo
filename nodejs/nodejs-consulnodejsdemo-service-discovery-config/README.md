# Consul服务发现与配置中心Node.js集成Demo

## 简介
本示例演示了如何在Node.js应用中使用Consul进行服务注册、服务发现以及动态配置拉取。通过三个独立脚本，分别展示：
- 服务注册到Consul
- 从Consul发现其他服务
- 监听并获取远程配置变更

## 学习目标
- 掌握Consul在微服务架构中的核心作用
- 学会使用Node.js客户端与Consul交互
- 实现服务自动注册与健康检查
- 动态加载和监听配置变化

## 环境要求
- Node.js >= 16.0.0
- npm >= 8.0.0
- Consul（本地或远程运行）

> 可通过 `node -v` 和 `npm -v` 验证版本

## 安装依赖的详细步骤

1. 克隆项目或创建新目录：
```bash
mkdir consul-demo && cd consul-demo
```

2. 初始化npm项目：
```bash
npm init -y
```

3. 安装依赖库：
```bash
npm install consul dotenv
```

4. 创建代码文件 `register-service.js`, `discover-service.js`, `watch-config.js`

5. 启动Consul代理（开发模式）：
```bash
consul agent -dev -ui
```
> 若未安装Consul，请访问 https://www.consul.io/downloads 下载对应平台版本

## 文件说明
- `register-service.js`: 将当前服务注册到Consul，并附带HTTP健康检查
- `discover-service.js`: 查询已注册的服务实例列表
- `watch-config.js`: 监听Consul中指定键的配置变更

## 逐步实操指南

### 步骤1：启动Consul代理
```bash
consul agent -dev -ui
```
**预期输出**：
```
==> Starting Consul agent in development mode...
==> Consul agent running!
    UI: http://localhost:8500/ui/
    HTTP: http://localhost:8500
```

### 步骤2：运行服务注册脚本
```bash
node register-service.js
```
**预期输出**：
```
✅ 服务 'demo-service' 已成功注册到Consul
→ 每10秒发送一次健康检查心跳
```

### 步骤3：运行服务发现脚本
```bash
node discover-service.js
```
**预期输出**：
```
🔍 发现服务 demo-service 的实例：
[ { ServiceAddress: '127.0.0.1', ServicePort: 3000 } ]
```

### 步骤4：设置并监听配置
在另一个终端设置KV配置：
```bash
curl -X PUT -d '{"logLevel":"debug","port":3001}' http://localhost:8500/v1/kv/config/demo-service
```

然后运行监听脚本：
```bash
node watch-config.js
```
**预期输出**：
```
📝 初始配置加载： { logLevel: 'debug', port: 3001 }
⏳ 正在监听配置变化... 修改KV可触发更新
```

修改配置后再次执行curl命令，观察控制台输出配置更新。

## 代码解析

### register-service.js
- 使用 `consul.agent.service.register` 注册服务
- 包含 `check` 字段定义HTTP健康检查路径
- 模拟周期性健康上报以维持服务存活

### discover-service.js
- 调用 `consul.health.service` 获取特定服务的所有健康实例
- 提取IP和端口用于后续调用

### watch-config.js
- 使用 `consul.watch` 创建长期轮询，监听KV存储中 `/config/demo-service` 路径
- 首次读取后持续监听变更，实现热更新

## 预期输出示例
```
# register-service.js
✅ 服务 'demo-service' 已成功注册到Consul
→ 每10秒发送一次健康检查心跳

# discover-service.js
🔍 发现服务 demo-service 的实例：
[ { ServiceAddress: '127.0.0.1', ServicePort: 3000 } ]

# watch-config.js
📝 初始配置加载： { logLevel: 'debug', port: 3001 }
⏳ 正在监听配置变化... 修改KV可触发更新
```

## 常见问题解答

**Q: 运行时报错 `Cannot connect to Consul`？**
A: 确保Consul代理正在运行，默认地址为 `http://localhost:8500`。可通过浏览器访问UI界面确认。

**Q: 服务注册后显示不健康？**
A: 检查健康检查路径是否可达。本例中 `/health` 应返回200状态码。

**Q: 配置监听无反应？**
A: 确保写入的KV路径为 `config/demo-service`，且内容为合法JSON格式。

## 扩展学习建议
- 结合Express/Koa构建真实Web服务并注册
- 使用Consul ACL增强安全性
- 集成到Docker容器中实现自动化部署
- 替代方案对比：etcd vs ZooKeeper vs Nacos