# 跨栈项目

## 什么是跨栈项目

单一技术栈无法完成的真实项目——前端 + 后端 + 数据库 + 部署。Vibe Coding 的终极挑战。

## AI 如何处理跨栈

AI 对单语言代码非常擅长，但跨栈需要你做"胶水"：
- 定义清晰的接口边界
- 用 AI 分栈实现，手动保证接口一致
- 用 AI 生成集成测试

## 典型跨栈项目结构

```
project/
├── frontend/        # React/Vue/HTML — AI 实现
├── backend/         # Go/Python/Node — AI 实现
├── infra/           # Docker/K8s YAML — AI 生成
└── api-contract/    # OpenAPI/Protobuf — 手动定义后让 AI 实现
```

## Prompt 策略

### 第一步：定义 API 契约

```
设计一个任务管理系统的 API：

POST   /api/tasks       — 创建任务
GET    /api/tasks       — 获取任务列表
GET    /api/tasks/:id   — 获取单个任务
PUT    /api/tasks/:id   — 更新任务
DELETE /api/tasks/:id   — 删除任务

Task 模型：
- id: string (UUID)
- title: string (1-200 chars)
- description: string (optional)
- status: "todo" | "in_progress" | "done"
- created_at: ISO 8601 datetime
- updated_at: ISO 8601 datetime

请输出 OpenAPI 3.0 规范。
```

### 第二步：按栈实现

```
基于上面的 OpenAPI 规范，用 Go + Gin 实现后端。
数据库用 SQLite（不需要外部数据库服务）。
```

```
基于上面的 OpenAPI 规范，用 HTML + vanilla JS 实现前端。
直接 fetch 调用后端 API。
```

### 第三步：集成

```
创建 docker-compose.yml：
- backend 服务：Go 应用，暴露 8080
- frontend 服务：nginx 提供 HTML，代理 /api 到 backend
```

## 跨栈的常见坑

1. **CORS** — 前端和后端不同端口时必须处理跨域
2. **数据格式不一致** — 前端发 JSON，后端期望 form-data
3. **时间格式** — Go 默认 RFC3339，JS 默认 ISO 8601（大部分情况兼容）
4. **错误格式** — 统一 `{ "error": "...", "code": 400 }` 格式

## 实战练习

结合以下 OpenDemo 案例：
- 后端：[Go Gin Web](../../practices/go/go-ginwebdemo-web-framework-intro/CHALLENGE.md)
- 后端：[Python FastAPI](../../practices/python/fastapi-complete-tutorial/CHALLENGE.md)
- 部署：[K8s n8n](../../practices/kubernetes/n8n/CHALLENGE.md)
