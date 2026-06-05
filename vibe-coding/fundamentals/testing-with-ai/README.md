# 让 AI 写测试

## 核心理念：测试是 AI 最擅长的领域之一

AI 非常适合写测试，因为：
- 测试模式高度结构化（arrange → act → assert）
- 不需要创造性，需要覆盖率
- 可以从实现代码反向推导测试用例

## 四种 AI 写测试的方法

### 方法一：从实现生成测试

```
为以下函数生成测试用例，覆盖：
- 正常路径
- 边界条件（空输入、最大值、零值）
- 错误路径

代码：
func (s *UserService) Create(ctx context.Context, req CreateUserRequest) (*User, error) {
    if req.Name == "" {
        return nil, ErrNameRequired
    }
    if len(req.Name) > 100 {
        return nil, ErrNameTooLong
    }
    user := &User{
        ID:   uuid.New().String(),
        Name: req.Name,
    }
    if err := s.repo.Save(ctx, user); err != nil {
        return nil, fmt.Errorf("save user: %w", err)
    }
    return user, nil
}

使用 table-driven test 风格。
```

### 方法二：先写测试再写实现（TDD）

```
我要实现一个 RateLimiter，先写测试：

功能：
- 每秒最多允许 N 个请求
- 超过限制的请求返回 false
- 每秒自动重置计数器
- 支持按 key 独立计数

请先写测试用例（Go testing 包），包括：
1. 限制内请求通过
2. 超限请求被拒绝
3. 窗口重置后恢复
4. 不同 key 独立计数
5. 并发安全
```

### 方法三：从 Bug 回归测试

```
修复了一个 bug：当用户名为空字符串时，CreateUser 返回了 nil 而不是错误。

请写一个回归测试确保这个 bug 不会再出现：

修复前的代码：
[paste]

修复后的代码：
[paste]
```

### 方法四：增加覆盖率

```
当前测试覆盖率是 65%，目标是 80%。

运行 go test -coverprofile=cover.out && go tool cover -func=cover.out 的结果：
[paste]

请为覆盖率 0% 的函数补充测试。
```

## 不同语言的测试 Prompt 模板

### Go（table-driven）
```
用 Go table-driven test 风格写测试，格式参考：

func TestXxx(t *testing.T) {
    tests := []struct {
        name    string
        input   Input
        want    Output
        wantErr bool
    }{
        {name: "正常情况", ...},
        {name: "边界条件", ...},
        {name: "错误路径", ...},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            ...
        })
    }
}
```

### Python（pytest）
```
用 pytest 风格写测试：
- 使用 fixture 创建测试数据
- 参数化测试用例用 @pytest.mark.parametrize
- 异步函数用 @pytest.mark.asyncio
- 需要 mock 的地方用 unittest.mock.patch
```

### Node.js（Jest）
```
用 Jest 写测试：
- describe/it 结构
- 每个测试独立，用 beforeEach 清理状态
- 异步用 async/await
- mock 外部依赖用 jest.mock()
```

## AI 写测试的坑

### 1. AI 会写"假"测试
```
// AI 生成的"假"测试——永远是 true
assert(true, "should work")
```
**解决**：明确要求"测试必须验证具体的返回值和副作用"。

### 2. AI 不测试边界
只测 happy path。**解决**：明确列出要测试的边界条件。

### 3. AI 测试依赖外部服务
```
// AI 可能生成需要真实数据库的测试
const result = await db.query("SELECT * FROM users");
```
**解决**：明确要求 mock 外部依赖。

## 实战练习

- [Go Cobra CLI](../../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md) — 给 CLI 命令写测试
- [Python OOP](../../practices/python/oop-classes/CHALLENGE.md) — 给类和方法写测试
- [FastAPI](../../practices/python/fastapi-complete-tutorial/CHALLENGE.md) — 给 API 接口写测试
