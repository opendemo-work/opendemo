# n8n 工作流案例集

本文档提供多个实用的 n8n 工作流案例，包含详细配置和步骤说明，帮助你在不同部署环境中练习和复用工作流。

## 使用前提

- 已经通过 `LOCAL_DEPLOYMENT.md` 或 `README.md` 中的 Kubernetes 部署章节，启动了一个可访问的 n8n 实例（本地或集群均可）。
- 对 n8n 的基础概念已有初步了解，例如：节点（Node）、触发器（Trigger）、执行（Execution）等。

## 如何使用本案例集

1. 从目录中选择一个与当前需求接近的案例（基础、自动化、数据处理或高级）。
2. 在 n8n 界面中新建工作流，按照案例中的“节点配置”和“创建步骤”逐步搭建。
3. 根据实际业务需要调整 API 地址、凭据、字段名称等配置，并在本地或 Kubernetes 环境中多次运行验证。
4. 当案例满足你的需求后，可以将工作流导出 JSON 并纳入自己的版本管理（Git 等）。

## 目录

- [基础案例](#基础案例)
  - [案例 1：Hello World - 定时输出](#案例-1hello-world---定时输出)
  - [案例 2：Webhook 数据接收](#案例-2webhook-数据接收)
  - [案例 3：HTTP 请求与数据处理](#案例-3http-请求与数据处理)
- [自动化案例](#自动化案例)
  - [案例 4：邮件自动化](#案例-4邮件自动化)
  - [案例 5：GitHub 监控与通知](#案例-5github-监控与通知)
  - [案例 6：Slack 机器人](#案例-6slack-机器人)
- [数据处理案例](#数据处理案例)
  - [案例 7：数据转换与格式化](#案例-7数据转换与格式化)
  - [案例 8：批量数据处理](#案例-8批量数据处理)
  - [案例 9：数据库同步](#案例-9数据库同步)
- [高级案例](#高级案例)
  - [案例 10：AI 集成 - ChatGPT](#案例-10ai-集成---chatgpt)
  - [案例 11：文件处理自动化](#案例-11文件处理自动化)
  - [案例 12：多步骤审批流程](#案例-12多步骤审批流程)

---

## 基础案例

### 案例 1：Hello World - 定时输出

**场景描述**：每分钟执行一次，输出当前时间。用于学习 n8n 基础。

**节点配置**：

1. **Schedule Trigger**（定时触发器）
   ```
   触发规则: 每 1 分钟
   ```

2. **Set**（设置数据）
   ```json
   {
     "message": "Hello from n8n!",
     "timestamp": "={{$now.toISO()}}"
   }
   ```

**创建步骤**：

1. 新建工作流
2. 添加 Schedule Trigger 节点
3. 设置触发间隔为 1 分钟
4. 添加 Set 节点
5. 配置输出字段
6. 保存并激活工作流

---

### 案例 2：Webhook 数据接收

**场景描述**：创建一个 Webhook 端点，接收外部 POST 请求数据。

**节点配置**：

1. **Webhook**
   ```
   HTTP 方法: POST
   路径: /receive-data
   响应模式: 工作流结束时响应
   ```

2. **Function**（数据处理）
   ```javascript
   // 处理接收到的数据
   const inputData = items[0].json;
   
   return [{
     json: {
       received: true,
       data: inputData,
       processedAt: new Date().toISOString()
     }
   }];
   ```

**使用方式**：

```bash
# 测试 Webhook
curl -X POST http://localhost:5678/webhook/receive-data \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 123}'
```

---

### 案例 3：HTTP 请求与数据处理

**场景描述**：从公开 API 获取数据并进行处理。

**节点配置**：

1. **Schedule Trigger**
   ```
   触发规则: 每 5 分钟
   ```

2. **HTTP Request**
   ```
   方法: GET
   URL: https://api.github.com/repos/n8n-io/n8n
   ```

3. **Function**（数据提取）
   ```javascript
   const repoData = items[0].json;
   
   return [{
     json: {
       name: repoData.name,
       stars: repoData.stargazers_count,
       forks: repoData.forks_count,
       openIssues: repoData.open_issues_count,
       fetchedAt: new Date().toISOString()
     }
   }];
   ```

---

## 自动化案例

### 案例 4：邮件自动化

**场景描述**：定时检查数据并发送邮件报告。

**节点配置**：

1. **Schedule Trigger**
   ```
   触发规则: 每天 09:00
   ```

2. **HTTP Request**（获取数据）
   ```
   方法: GET
   URL: 您的 API 地址
   ```

3. **Function**（生成报告）
   ```javascript
   const data = items[0].json;
   
   const report = `
   日报 - ${new Date().toLocaleDateString()}
   =====================================
   
   总记录数: ${data.total || 0}
   新增数: ${data.new || 0}
   更新数: ${data.updated || 0}
   
   详情请登录系统查看。
   `;
   
   return [{
     json: {
       subject: `日报 - ${new Date().toLocaleDateString()}`,
       body: report
     }
   }];
   ```

4. **Send Email**
   ```
   发件人: noreply@example.com
   收件人: team@example.com
   主题: ={{$json.subject}}
   内容: ={{$json.body}}
   ```

---

### 案例 5：GitHub 监控与通知

**场景描述**：监控 GitHub 仓库的新 Issue 并发送通知。

**节点配置**：

1. **GitHub Trigger**
   ```
   事件: Issues
   操作: opened
   仓库: 您的仓库
   ```

2. **Function**（格式化消息）
   ```javascript
   const issue = items[0].json;
   
   return [{
     json: {
       title: `新 Issue: ${issue.title}`,
       message: `
       仓库: ${issue.repository.full_name}
       标题: ${issue.title}
       作者: ${issue.user.login}
       链接: ${issue.html_url}
       
       内容:
       ${issue.body || '无描述'}
       `
     }
   }];
   ```

3. **Slack**（或其他通知渠道）
   ```
   频道: #github-notifications
   消息: ={{$json.message}}
   ```

---

### 案例 6：Slack 机器人

**场景描述**：创建一个 Slack 机器人，响应特定命令。

**节点配置**：

1. **Webhook**
   ```
   HTTP 方法: POST
   路径: /slack-bot
   ```

2. **Switch**（命令路由）
   ```
   条件 1: {{$json.text}} 包含 "/help"
   条件 2: {{$json.text}} 包含 "/status"
   条件 3: {{$json.text}} 包含 "/report"
   ```

3. **Function**（各分支处理）

   帮助命令：
   ```javascript
   return [{
     json: {
       response_type: "in_channel",
       text: "可用命令：\n/help - 显示帮助\n/status - 查看状态\n/report - 生成报告"
     }
   }];
   ```

---

## 数据处理案例

### 案例 7：数据转换与格式化

**场景描述**：接收 CSV 数据并转换为 JSON 格式。

**节点配置**：

1. **Webhook**
   ```
   HTTP 方法: POST
   路径: /csv-to-json
   ```

2. **Spreadsheet File**
   ```
   操作: 从二进制数据读取
   文件格式: CSV
   ```

3. **Function**（数据清洗）
   ```javascript
   return items.map(item => ({
     json: {
       ...item.json,
       processedAt: new Date().toISOString(),
       // 自定义数据转换逻辑
       amount: parseFloat(item.json.amount) || 0,
       date: new Date(item.json.date).toISOString()
     }
   }));
   ```

---

### 案例 8：批量数据处理

**场景描述**：批量处理大量数据，支持分页和错误处理。

**节点配置**：

1. **Schedule Trigger**
   ```
   触发规则: 每小时
   ```

2. **HTTP Request**（获取数据列表）
   ```
   方法: GET
   URL: https://api.example.com/items?page={{$json.page}}&limit=100
   ```

3. **SplitInBatches**（分批处理）
   ```
   批次大小: 10
   ```

4. **Function**（处理单条数据）
   ```javascript
   const item = items[0].json;
   
   // 数据处理逻辑
   const processed = {
     id: item.id,
     name: item.name.toUpperCase(),
     processedAt: new Date().toISOString()
   };
   
   return [{ json: processed }];
   ```

5. **HTTP Request**（保存处理结果）

---

### 案例 9：数据库同步

**场景描述**：在两个数据库之间同步数据。

**节点配置**：

1. **Schedule Trigger**
   ```
   触发规则: 每 30 分钟
   ```

2. **MySQL**（源数据库）
   ```
   操作: 执行查询
   查询: SELECT * FROM users WHERE updated_at > NOW() - INTERVAL 30 MINUTE
   ```

3. **Function**（数据转换）
   ```javascript
   return items.map(item => ({
     json: {
       external_id: item.json.id,
       name: item.json.name,
       email: item.json.email,
       synced_at: new Date().toISOString()
     }
   }));
   ```

4. **Postgres**（目标数据库）
   ```
   操作: Upsert
   表名: synced_users
   冲突列: external_id
   ```

---

## 高级案例

### 案例 10：AI 集成 - ChatGPT

**场景描述**：使用 ChatGPT 自动回复用户问题。

**节点配置**：

1. **Webhook**
   ```
   HTTP 方法: POST
   路径: /ask-ai
   ```

2. **OpenAI**
   ```
   操作: 消息模型
   模型: gpt-4
   消息:
     - 角色: system
       内容: 你是一个友好的助手
     - 角色: user
       内容: ={{$json.question}}
   ```

3. **Function**（格式化响应）
   ```javascript
   const response = items[0].json;
   
   return [{
     json: {
       answer: response.message.content,
       model: response.model,
       usage: response.usage
     }
   }];
   ```

---

### 案例 11：文件处理自动化

**场景描述**：监控文件夹，自动处理新上传的文件。

**节点配置**：

1. **Schedule Trigger**
   ```
   触发规则: 每 5 分钟
   ```

2. **FTP** / **S3** / **Google Drive**（监控文件）
   ```
   操作: 列出文件
   路径: /incoming/
   ```

3. **IF**（过滤条件）
   ```
   条件: {{$json.modifiedTime}} > {{$now.minus({minutes: 5}).toISO()}}
   ```

4. **Read Binary File**（读取文件）

5. **Function**（处理文件）
   ```javascript
   const file = items[0];
   
   // 文件处理逻辑
   // ...
   
   return [{ json: { processed: true, filename: file.json.name } }];
   ```

6. **Move File**（移动已处理文件）

---

### 案例 12：多步骤审批流程

**场景描述**：实现多级审批流程，支持邮件通知。

**节点配置**：

1. **Webhook**（提交申请）
   ```
   HTTP 方法: POST
   路径: /submit-request
   ```

2. **Function**（创建审批记录）
   ```javascript
   const request = items[0].json;
   
   return [{
     json: {
       id: Date.now().toString(),
       type: request.type,
       requester: request.requester,
       amount: request.amount,
       status: 'pending',
       approvers: ['manager@example.com', 'director@example.com'],
       currentApprover: 0,
       createdAt: new Date().toISOString()
     }
   }];
   ```

3. **Send Email**（通知审批人）
   ```
   收件人: ={{$json.approvers[$json.currentApprover]}}
   主题: 审批申请 - {{$json.type}}
   内容: |
     申请人: {{$json.requester}}
     类型: {{$json.type}}
     金额: {{$json.amount}}
     
     请点击以下链接进行审批:
     批准: http://localhost:5678/webhook/approve/{{$json.id}}
     拒绝: http://localhost:5678/webhook/reject/{{$json.id}}
   ```

4. **Webhook**（审批响应 - 批准）
   ```
   HTTP 方法: GET
   路径: /approve/:id
   ```

5. **Function**（更新审批状态）
   ```javascript
   // 检查是否所有审批人都已批准
   const request = items[0].json;
   
   if (request.currentApprover >= request.approvers.length - 1) {
     request.status = 'approved';
   } else {
     request.currentApprover++;
     // 继续下一级审批
   }
   
   return [{ json: request }];
   ```

---

## 最佳实践

### 1. 错误处理

始终添加错误处理节点：

```javascript
// Error Trigger 节点中处理错误
const error = items[0].json;

// 记录错误日志
console.error('Workflow error:', error);

// 发送错误通知
return [{
  json: {
    error: error.message,
    workflow: error.workflow,
    timestamp: new Date().toISOString()
  }
}];
```

### 2. 环境变量

使用环境变量管理敏感信息：

```
N8N_ENCRYPTION_KEY=your-key
API_KEY={{$env.API_KEY}}
DATABASE_URL={{$env.DATABASE_URL}}
```

### 3. 工作流版本控制

- 定期导出工作流 JSON
- 使用 Git 管理工作流版本
- 在测试环境验证后再部署到生产

### 4. 性能优化

- 使用 SplitInBatches 处理大量数据
- 合理设置触发频率
- 避免在 Function 节点中进行复杂计算

---

## 相关资源

- [n8n 官方文档](https://docs.n8n.io/)
- [n8n 工作流模板](https://n8n.io/workflows/)
- [n8n 社区论坛](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

---

## 版本信息

- 文档版本：1.0.0
- 更新日期：2026-01-22
- 支持 n8n 版本：1.0+
