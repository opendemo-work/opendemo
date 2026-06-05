# 解决过程：Go Gin Web 框架

## 使用的工具：GitHub Copilot Chat

---

### 第 1 轮：基本路由

**Prompt：**
> 用 Go Gin 框架创建一个 REST API。目前只需要：
> 1. GET / 返回 {"message": "Hello from Gin!"}
> 2. GET /user/:id 返回路径参数 id 和查询参数 name（默认 Guest）
>
> 使用 gin.Default() 和 gin.H 快捷方式。

**AI 生成：** main.go，两个路由正确。`c.Param("id")` 和 `c.DefaultQuery("name", "Guest")` 用法正确。

---

### 第 2 轮：添加 POST 路由

**Prompt：**
> 添加 POST /user 路由：
> - 定义 User 结构体：Name string (json:"name" binding:"required"), Age int (json:"age" binding:"gte=0,lte=150")
> - 用 c.ShouldBindJSON 解析请求体
> - 验证失败返回 400 + {"error": err.Error()}
> - 成功返回 200 + {"status": "success", "received": user}

**AI 生成：** 正确实现。binding tag 写法准确。

**问题：** AI 在 User 结构体上方加了 `gorm.Model` 嵌入。这里不需要数据库。

**修复：** "去掉 gorm.Model 嵌入，这是一个纯 API demo 不需要 ORM"。

---

### 第 3 轮：验证

```bash
go run main.go &
curl http://localhost:8080/
curl http://localhost:8080/user/123?name=Tom
curl -X POST http://localhost:8080/user -H "Content-Type: application/json" -d '{"name":"Alice","age":25}'
```

**结果：** 全部正确 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 3 轮 |
| 实际用时 | ~10 分钟 |
| AI 犯错次数 | 1（不必要的 gorm 依赖） |
| 人工干预 | 移除多余依赖 |

### 关键技巧
- **Gin 的 binding tag 很强大** — `required`、`gte=0`、`lte=150` 自动验证，不需要手写验证逻辑
- **gin.H 是 map[string]any 的别名** — 简化 JSON 响应构造
- **ShouldBind vs MustBind** — Should 不会自动返回 400，给你自定义错误响应的机会

### 常见坑
- `c.Param()` 返回的是字符串，需要自己转 int
- `c.DefaultQuery()` 的默认值只在参数缺失时生效，空字符串不算缺失
- Gin 默认是 debug 模式，生产环境设 `GIN_MODE=release`
