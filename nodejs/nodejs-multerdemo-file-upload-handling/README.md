# Multer文件上传处理Demo

## 简介
本项目是一个基于Node.js和Express框架的简单Web应用，演示了如何使用Multer中间件实现单文件、多文件以及带过滤器的文件上传功能。适合学习后端文件处理的最佳实践。

## 学习目标
- 理解Multer在Express中的作用
- 掌握单文件与多文件上传的实现方式
- 学会设置文件存储路径与重命名策略
- 了解文件类型验证和大小限制的方法

## 环境要求
- Node.js v16 或更高版本
- npm（随Node.js自动安装）
- 操作系统：Windows / macOS / Linux（跨平台兼容）

## 安装依赖的详细步骤

1. 打开终端或命令行工具
2. 进入项目根目录：
   ```bash
   cd multer-upload-demo
   ```
3. 安装所需依赖包：
   ```bash
   npm install
   ```

## 文件说明
- `app.js`：主服务器入口，包含路由和Multer配置
- `upload.js`：封装的文件上传中间件逻辑
- `package.json`：项目依赖声明文件（由npm init生成）

## 逐步实操指南

### 步骤1：启动服务器
运行以下命令启动本地服务：
```bash
node app.js
```

**预期输出**：
```bash
服务器运行在 http://localhost:3000
上传页面可通过 http://localhost:3000 访问
```

### 步骤2：访问上传页面
打开浏览器并访问：
```text
http://localhost:3000
```

你将看到一个包含单文件、多文件上传表单的HTML页面。

### 步骤3：测试文件上传
选择一个图片或其他文件，点击“上传”按钮。

**预期结果**：
- 文件被保存到 `uploads/` 目录
- 浏览器显示上传成功消息及文件信息

## 代码解析

### `app.js` 关键段解释
```js
const upload = multer({ dest: 'uploads/' });
```
> 配置Multer将上传的文件暂存至 `uploads/` 目录，不保留原始文件名。

```js
app.post('/upload', upload.single('file'), (req, res) => { ... });
```
> 使用 `.single('file')` 表示只接受一个名为 'file' 的字段上传。

### `upload.js` 中的自定义存储
> 使用 `DiskStorage` 自定义文件名，防止冲突，并支持扩展名保留。

## 预期输出示例
上传成功后浏览器响应：
```json
{
  "message": "文件上传成功",
  "filename": "abc123.jpg",
  "size": 12345
}
```

控制台日志：
```bash
收到文件: abc123.jpg, 大小: 12345 字节
```

## 常见问题解答

**Q: 上传失败，提示 EACCES 权限错误？**
A: 请确保 `uploads/` 目录存在且当前用户有写权限。可手动创建：
```bash
mkdir uploads
```

**Q: 如何限制上传文件类型？**
A: 在 `upload.js` 中修改 `fileFilter` 函数，检查 `mimetype`。

**Q: 能否上传超过10MB的文件？**
A: 默认限制为10MB。可在Multer配置中通过 `limits` 修改：
```js
limits: { fileSize: 50 * 1024 * 1024 } // 50MB
```

## 扩展学习建议
- 将上传文件保存到云存储（如AWS S3、阿里云OSS）
- 添加图像压缩处理（使用sharp库）
- 实现上传进度条（前端配合AJAX）
- 结合数据库记录文件元数据
- 使用UUID生成唯一文件名避免冲突