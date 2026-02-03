# Node.js Swagger OpenAPI 演示项目

## 简介
本项目演示如何在Node.js中使用Swagger（OpenAPI）来自动生成美观、交互式的API文档。通过集成`swagger-ui-express`和YAML格式的OpenAPI定义，开发者可以轻松为RESTful API提供实时文档。

## 学习目标
- 掌握在Express应用中集成Swagger UI的方法
- 学会使用YAML编写OpenAPI规范
- 理解API文档自动化的重要性与最佳实践
- 能够运行并访问本地API文档界面

## 环境要求
- Node.js 16.x 或更高版本
- npm（随Node.js自动安装）
- 任意现代浏览器（Chrome/Firefox/Safari/Edge）

## 安装依赖的详细步骤

1. 打开终端或命令行工具
2. 进入项目根目录：
   ```bash
   cd path/to/your/project
   ```
3. 安装所需依赖包：
   ```bash
   npm install
   ```

## 文件说明
- `app.js`：主服务器文件，启动Express并挂载Swagger UI
- `api-docs.yaml`：使用YAML编写的OpenAPI 3.0规范，定义API结构和文档
- `package.json`：项目依赖声明文件

## 逐步实操指南

### 第一步：启动服务器
```bash
node app.js
```

**预期输出：**
```
Server is running on http://localhost:3000
Swagger UI available at http://localhost:3000/api-docs
```

### 第二步：打开浏览器访问文档
在浏览器中访问：
```
http://localhost:3000/api-docs
```

### 第三步：查看和测试API
- 在Swagger UI界面中，展开 `/users` 接口
- 点击“Try it out”按钮测试GET请求
- 查看模拟返回结果

## 代码解析

### app.js 关键代码段
```javascript
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const swaggerDocument = YAML.load('./api-docs.yaml');
```
- 引入Swagger UI中间件和YAML解析器
- 加载本地YAML格式的OpenAPI文档

```javascript
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
```
- 将Swagger UI挂载到 `/api-docs` 路由
- 提供可视化交互式API文档页面

### api-docs.yaml 说明
- 使用OpenAPI 3.0标准定义接口
- 包含路径、参数、响应码、示例等元数据
- 支持复杂对象模型和嵌套结构

## 预期输出示例
成功启动后，访问 `http://localhost:3000/api-docs` 应看到Swagger UI界面，包含以下内容：
- 标题："My API"
- 版本："1.0.0"
- `/users` 接口描述及测试按钮
- 右侧可发送请求并查看JSON响应

## 常见问题解答

**Q1: 访问 http://localhost:3000/api-docs 显示空白？**
A: 确保 `api-docs.yaml` 文件存在且路径正确，检查控制台是否有文件读取错误。

**Q2: 如何更新API文档？**
A: 修改 `api-docs.yaml` 文件中的OpenAPI定义，重启服务即可生效。

**Q3: 是否支持JSON格式的OpenAPI定义？**
A: 是的，可将YAML替换为JSON，使用 `require('./api-docs.json')` 直接加载。

## 扩展学习建议
- 尝试添加POST、PUT等其他HTTP方法到OpenAPI文档
- 集成JSDoc + Swagger自动生成工具如`swagger-jsdoc`
- 将Swagger文档部署到生产环境并设置权限保护
- 学习使用Swagger Editor进行可视化编辑