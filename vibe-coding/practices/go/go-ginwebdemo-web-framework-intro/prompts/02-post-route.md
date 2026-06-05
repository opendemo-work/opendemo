# Prompt 02: 添加 POST 路由

添加 POST /user 路由：
- 定义 User 结构体：Name string (json:"name" binding:"required"), Age int (json:"age" binding:"gte=0,lte=150")
- 用 c.ShouldBindJSON 解析请求体
- 验证失败返回 400 + {"error": err.Error()}
- 成功返回 200 + {"status": "success", "received": user}

---
## 背景
- 工具：Copilot Chat
- 阶段：第 2 轮
- 结果：AI 额外添加了 gorm.Model 嵌入（不需要），修复后正确
