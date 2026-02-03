# Go模板引擎实战演示

## 简介
本示例演示了Go语言中`text/template`和`html/template`包的核心功能，包括数据渲染、条件判断、循环遍历以及安全的HTML输出。通过两个具体场景帮助开发者掌握Go模板系统的使用。

## 学习目标
- 理解Go模板的基本语法和执行流程
- 掌握`text/template`与`html/template`的区别
- 学会使用模板函数（如条件、循环）
- 了解自动转义机制在HTML模板中的作用

## 环境要求
- Go 1.19 或更高版本（稳定版）
- 支持终端操作的系统（Windows / Linux / macOS）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库，无需额外安装依赖。

## 文件说明
- `main.go`: 主程序，演示文本模板的动态内容生成
- `web_template.go`: 演示HTML模板的安全渲染和结构化数据输出

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir go-template-demo && cd go-template-demo
```

### 步骤2: 创建并复制代码文件
创建 `main.go` 并粘贴对应内容：
```bash
touch main.go
# 将 main.go 的内容复制进去
```

创建 `web_template.go`：
```bash
touch web_template.go
# 将 web_template.go 的内容复制进去
```

### 步骤3: 运行文本模板示例
```bash
go run main.go
```

**预期输出**：
```
姓名: 张三
年龄: 30
兴趣: 编程, 阅读, 跑步
是否已婚: 是
```

### 步骤4: 运行HTML模板示例
```bash
go run web_template.go
```

**预期输出**：
```html
<html><body>
<h1>用户资料 - 张三</h1>
<p>年龄: 30</p>
<ul>
<li>编程</li>
<li>阅读</li>
<li>跑步</li>
</ul>
<p>状态: 已婚</p>
</body></html>
```

## 代码解析

### main.go 关键点
- 使用 `text/template` 包处理纯文本模板
- `.Hobbies` 使用 `join` 函数拼接切片
- 条件语句 `{{if .Married}}` 实现逻辑分支

### web_template.go 关键点
- 使用 `html/template` 自动防止XSS攻击
- 模板嵌入在代码中，使用反引号定义多行字符串
- 结构体字段必须导出（大写首字母）才能被模板访问
- `{{range .Hobbies}}` 实现列表循环渲染

## 预期输出示例
见上文各步骤的“预期输出”部分。

## 常见问题解答

**Q: 为什么HTML模板不会转义我想要保留的HTML标签？**
A: `html/template` 默认对所有输出进行HTML转义以防止XSS。若需输出原始HTML，请使用 `template.HTML` 类型包装内容。

**Q: 模板变量为何无法访问结构体字段？**
A: 确保字段名首字母大写（导出），且字段名称与模板中引用的一致。

**Q: 如何从文件加载模板？**
A: 使用 `template.ParseFiles("template.html")` 即可从外部文件加载模板。

## 扩展学习建议
- 尝试将模板分离到独立的`.tmpl`文件中
- 学习自定义模板函数（FuncMap）
- 探索结合Gin或Echo框架使用模板构建Web页面
- 研究嵌套模板（block, define）实现布局复用