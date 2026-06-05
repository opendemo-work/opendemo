# 用 AI 迁移老代码

## 什么是 AI 辅助的代码迁移

将旧代码迁移到新技术栈——Python 2→3、REST→gRPC、jQuery→React、单体→微服务。AI 非常适合这类"机械但复杂"的工作。

## 迁移策略

### 策略一：逐文件翻译（最安全）

```
将这个 Python 2 文件迁移到 Python 3：
[paste code]

要求：
- print 语句改为函数调用
- dict.keys()/values()/items() 返回视图而非列表
- except Exception, e → except Exception as e
- xrange → range
- 保持完全相同的 API 和行为
```

### 策略二：接口对齐（跨语言）

```
这个 Node.js Express 路由需要迁移到 Go Gin：

[Node.js 代码]

要求：
- 保持相同的 HTTP 方法和路径
- 保持相同的请求/响应 JSON 格式
- 保持相同的错误码和错误消息
- 用 Go 的惯用写法实现
```

### 策略三：渐进式迁移（大型项目）

```
第一步：分析这个项目的依赖关系，输出一个安全的迁移顺序。
先迁移没有内部依赖的模块，最后迁移被依赖最多的模块。

[项目结构]
```

## 迁移中的 AI 验证

### 方法一：行为对比测试

```
这是旧实现的测试输出：
[paste]

这是新实现运行同样测试的输出：
[paste]

找出行为差异并修复新实现。新实现必须完全匹配旧行为。
```

### 方法二：Schema 对比

```
旧 API 返回格式：
{"user_id": 123, "user_name": "Alice"}

新 API 返回格式：
{"id": 123, "name": "Alice"}

修改新 API 使其返回和旧 API 完全相同的字段名。
```

## 迁移的常见坑

1. **编码问题** — Python 2 的 str vs unicode，迁移后出现中文乱码
2. **隐式行为** — 旧代码依赖某个未文档化的行为，迁移后丢失
3. **依赖版本** — 新技术栈的库版本和旧的不兼容
4. **并发模型变化** — 同步代码迁移到异步时，需要全局重写

## 实战练习

- [Python OOP](../../practices/python/oop-classes/CHALLENGE.md) — 把 demo 从面向过程改为面向对象
- [Go gRPC](../../practices/go/go-grpc-protobuf-go-demo/CHALLENGE.md) — 把 REST API 迁移为 gRPC
