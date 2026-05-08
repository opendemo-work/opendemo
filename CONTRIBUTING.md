# 贡献指南

感谢您对 OpenDemo 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 提交新的技术案例 (Demo)
- 改进现有案例的文档和代码
- 报告 Bug 或提出功能建议
- 修复错误或优化代码
- 分享您的使用经验

## 如何贡献

### 1. 准备工作

```bash
# Fork 本仓库
git clone https://github.com/opendemo/opendemo.git
cd opendemo

# 安装开发依赖
cd opendemo-cli && pip install -e .
```

### 2. 创建案例

#### 案例目录结构

```
<tech-stack>/
└── <demo-name>/
    ├── README.md          # 必须：完整文档（≥3000字符）
    ├── metadata.json     # 必须：元数据
    ├── main.ext          # 主代码文件
    ├── code/             # 代码目录（可选）
    ├── tests/            # 测试目录（可选）
    └── config/           # 配置目录（可选）
```

#### metadata.json 格式

```json
{
  "name": "demo-name",
  "language": "python",
  "keywords": ["keyword1", "keyword2"],
  "description": "简短描述",
  "difficulty": "beginner|intermediate|advanced",
  "dependencies": {}
}
```

### 3. 质量标准

所有案例必须满足以下标准：

| 标准 | 要求 |
|------|------|
| README.md | ≥3000 字符，包含完整实操指南 |
| metadata.json | 必须包含所有必需字段 |
| 代码可运行 | 代码可直接执行，无明显错误 |
| 中文注释 | 代码包含中文注释，解释关键逻辑 |

### 4. 提交 Pull Request

```bash
# 创建分支
git checkout -b feature/<demo-name>

# 提交更改
git add .
git commit -m "Add <demo-name> for <tech-stack>"

# 推送到 GitHub
git push origin feature/<demo-name>
```

### 5. Code Review

提交后，维护者将进行 Code Review。请保持耐心，我们会在 2-3 个工作日内回复。

## 技术栈分类

项目按技术栈组织案例目录：

| 目录 | 技术栈 |
|------|--------|
| go/ | Go 语言 |
| java/ | Java 技术 |
| nodejs/ | Node.js/JavaScript |
| python/ | Python 技术 |
| kubernetes/ | Kubernetes 生态 |
| database/ | 数据库技术 |
| security/ | 安全技术 |
| networking/ | 网络技术 |
| ai-ml/ | AI/机器学习 |

## 案例命名规范

- 使用英文小写
- 单词间用连字符 `-` 分隔
- 格式：`<技术栈>-<主题>-demo`
- 示例：`python-async-await-demo`, `go-gin-web-demo`

## 联系方式

- GitHub Issues: [报告问题](https://github.com/opendemo/opendemo/issues)
- GitHub Discussions: [技术讨论](https://github.com/opendemo/opendemo/discussions)

---

感谢每一位贡献者！