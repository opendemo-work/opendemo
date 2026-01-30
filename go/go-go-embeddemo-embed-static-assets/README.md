# Go Embed静态资源嵌入Demo

## 简介
本项目演示了如何使用Go语言中的`embed`包将静态资源（如HTML模板、配置文件、图片等）直接嵌入到编译后的二进制文件中，实现零外部依赖部署。

## 学习目标
- 掌握Go `embed`包的基本用法
- 理解`//go:embed`指令的工作机制
- 学会在项目中嵌入单个文件和多个文件/目录
- 实践读取嵌入资源并输出内容

## 环境要求
- Go 1.16 或更高版本（`embed`包自Go 1.16引入）

## 安装依赖的详细步骤
本示例不依赖第三方库，仅使用Go标准库。只需安装Go即可：

1. 访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应操作系统的Go安装包
2. 按照官方指南完成安装
3. 验证安装：
   ```bash
   go version
   # 预期输出：go version go1.16+ ...
   ```

## 文件说明
- `main.go`：主程序，展示嵌入单个文件（version.txt）
- `assets.go`：专门处理嵌入静态资源（templates/ 和 config/ 目录）
- `version.txt`：被嵌入的版本信息文件
- `templates/index.html`：HTML模板文件，用于演示目录嵌入
- `config/app.json`：JSON配置文件，演示多类型文件嵌入

## 逐步实操指南

### 步骤1：创建项目目录结构
```bash
mkdir go-embed-demo && cd go-embed-demo
mkdir templates config
```

### 步骤2：初始化Go模块
```bash
go mod init embed-demo
```

### 步骤3：创建并运行代码
将以下文件保存到对应路径，然后执行：

```bash
# 运行程序
go run .
```

**预期输出**：
```
--- 嵌入的版本信息 ---
1.0.0-beta

--- 嵌入的HTML模板 ---
<!DOCTYPE html>
<html><body><h1>Hello, {{.Name}}!</h1></body></html>

--- 嵌入的JSON配置 ---
{
	"port": 8080,
	"env": "development"
}
```

## 代码解析

### main.go
- 使用 `//go:embed version.txt` 将版本文件嵌入变量 `versionContent`
- 直接打印内容，无需文件IO

### assets.go
- 使用 `embed.FS` 类型嵌入整个目录
- `templateFS` 嵌入 `templates/` 目录下的所有文件
- `configFS` 嵌入 `config/` 目录
- 通过 `fs.ReadFile` 从虚拟文件系统读取内容

### 关键点
- `//go:embed` 是编译指令，不是注释，前面不能有空格
- 变量必须是 `string`, `[]byte`, 或 `embed.FS` 类型
- 路径为相对路径，相对于当前Go文件

## 预期输出示例
```
--- 嵌入的版本信息 ---
1.0.0-beta

--- 嵌入的HTML模板 ---
<!DOCTYPE html>
<html><body><h1>Hello, {{.Name}}!</h1></body></html>

--- 嵌入的JSON配置 ---
{
	"port": 8080,
	"env": "development"
}
```

## 常见问题解答

**Q: 报错 `could not import embed`？**
A: 请确认Go版本 >= 1.16

**Q: `//go:embed` 不生效？**
A: 确保指令前无空格，且目标文件存在；检查文件路径是否正确

**Q: 如何嵌入多个不同目录？**
A: 使用多个 `embed.FS` 变量分别声明，如示例中的 `templateFS` 和 `configFS`

**Q: 编译后的二进制文件包含资源吗？**
A: 是的，所有嵌入资源已编译进二进制，无需外部文件即可运行

## 扩展学习建议
- 尝试嵌入图片、CSS、JS等前端资源，构建完整Web应用
- 结合 `html/template` 包动态渲染嵌入的HTML模板
- 使用 `embed` 实现配置热加载替代方案
- 探索 `statik` 等第三方工具与 `embed` 的对比