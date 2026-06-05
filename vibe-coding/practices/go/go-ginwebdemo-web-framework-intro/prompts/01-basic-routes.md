# Prompt 01: 基本路由

用 Go Gin 框架创建一个 REST API。目前只需要：
1. GET / 返回 {"message": "Hello from Gin!"}
2. GET /user/:id 返回路径参数 id 和查询参数 name（默认 Guest）

使用 gin.Default() 和 gin.H 快捷方式。

---
## 背景
- 工具：GitHub Copilot Chat
- 阶段：第 1 轮
- 结果：正确，c.Param 和 c.DefaultQuery 用法正确
