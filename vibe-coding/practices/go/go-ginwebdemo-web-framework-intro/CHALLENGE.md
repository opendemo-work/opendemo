# 挑战：Go Gin Web 框架入门

## 难度：intermediate | 预计用时：25 分钟 | 推荐工具：Cursor / Copilot

## 目标

使用 Gin 框架构建一个 REST API 服务器，包含：

1. `GET /` — 返回 `{"message": "Hello from Gin!"}`
2. `GET /user/:id` — 获取用户信息，支持 `?name=` 查询参数（默认 "Guest"）
3. `POST /user` — 接收 JSON 格式的用户数据（name + age），验证后返回确认

## 约束

- 使用 Go 1.19+ 和 Gin v1.9.1
- User 结构体：`Name string`（必填）+ `Age int`（范围 0-150）
- POST 请求体验证失败返回 400 + 错误信息
- 服务监听 `:8080`
- 代码注释使用中文

## 验证

```bash
# 启动服务
go run main.go
# 应输出：[GIN-debug] Listening and serving HTTP on :8080

# 测试 GET /
curl http://localhost:8080/
# {"message":"Hello from Gin!"}

# 测试 GET /user/:id
curl http://localhost:8080/user/123?name=Tom
# {"id":"123","name":"Tom"}

curl http://localhost:8080/user/456
# {"id":"456","name":"Guest"}

# 测试 POST /user（正常）
curl -X POST http://localhost:8080/user \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 25}'
# {"status":"success","received":{"name":"Alice","age":25}}

# 测试 POST /user（验证失败）
curl -X POST http://localhost:8080/user \
  -H "Content-Type: application/json" \
  -d '{"age": 200}'
# {"error":"..."}（400 状态码）
```

## 提示（卡住时再看）

<details>
<summary>提示 1：路径参数 vs 查询参数</summary>

路径参数用 `c.Param("id")`，查询参数用 `c.DefaultQuery("name", "Guest")`。

</details>

<details>
<summary>提示 2：JSON 绑定</summary>

用 `c.ShouldBindJSON(&user)` 解析请求体，它会根据 struct tag 自动验证。

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 Go Gin 框架创建一个 REST API，包含三个路由：GET / 返回欢迎消息，GET /user/:id 支持路径参数和查询参数，POST /user 接收 JSON body 并验证。User 结构体 Name 必填、Age 范围 0-150，用 binding tag 做验证。"

</details>

## 对应原 Demo

完成后对比参考实现：`go/go-ginwebdemo-web-framework-intro/`
