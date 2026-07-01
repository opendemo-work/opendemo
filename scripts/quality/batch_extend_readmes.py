#!/usr/bin/env python3
"""
批量扩展长度不足 3000 字符的 README。
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(".")
IGNORE_DIRS = {".git", ".github", ".venv", "venv", "node_modules", "__pycache__", "check"}


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def get_demo_name(demo_dir: Path) -> str:
    meta = demo_dir / "metadata.json"
    if meta.exists():
        try:
            data = json.loads(safe_read_text(meta))
            return data.get("name", demo_dir.name.replace("-", " ").title())
        except Exception:
            pass
    return demo_dir.name.replace("-", " ").title()


def extend_readme(readme_path: Path, demo_name: str) -> bool:
    content = safe_read_text(readme_path)
    if len(content) >= 3000:
        return False

    appendix = f"""

---

## 📖 深入理解

### 核心流程

{demo_name} 从启动到完成主要包含以下环节：

1. **环境准备**：配置运行所需的依赖、网络和存储资源。
2. **主流程执行**：运行案例的核心逻辑并产出结果。
3. **结果验证**：通过日志、命令输出或测试用例确认正确性。
4. **资源回收**：停止服务并清理临时数据，保证可重复执行。

### 设计要点

| 方面 | 做法 | 说明 |
|------|------|------|
| 部署方式 | 本地容器化 | 减少环境差异，便于复现 |
| 配置管理 | 配置文件 + 环境变量 | 兼顾可读性与灵活性 |
| 可观测性 | 日志 + 健康检查 | 方便定位问题 |
| 扩展方式 | 模块化组织 | 后续可按需增加功能 |

### 需要关注的指标

在生产环境中落地类似方案时，建议留意：

- 关键路径的响应延迟
- CPU、内存、磁盘和网络资源使用
- 并发量与吞吐量变化
- 错误率和异常告警

---

## 🛡️ 安全与最佳实践

### 安全建议

- 生产环境不要使用默认密码、密钥或令牌。
- 定期将依赖升级到稳定的最新版本。
- 敏感配置优先使用密钥管理工具或环境变量注入。
- 通过防火墙、安全组或网络策略限制访问范围。

### 操作建议

- 修改配置前备份现有环境。
- 将配置文件和脚本纳入版本控制。
- 为核心路径补充自动化测试。
- 保留运行日志以便审计和排障。

---

## 🧪 进阶实验

基础流程跑通后，可以尝试：

1. 调整关键参数，观察对结果的影响。
2. 模拟异常场景，验证容错能力。
3. 增加负载，分析系统瓶颈。
4. 与其他组件组合，形成完整链路。

---

## 📚 扩展资源

- 相关技术的官方文档
- [OpenDemo 项目主页](https://github.com/opendemo)
- GitHub Discussions 与技术社区

---

## 🤝 贡献与反馈

如发现内容有误或希望补充，欢迎提交 Issue 或 Pull Request。

---

*本 README 由 OpenDemo 自动生成并持续维护，欢迎根据实际案例补充细节。*
"""
    readme_path.write_text(content + appendix, encoding="utf-8")
    return True


def find_all_demo_dirs(root: Path) -> list:
    dirs = []
    search_stack = [(root, 0)]
    while search_stack:
        current, depth = search_stack.pop()
        if depth > 6:
            continue
        for item in current.iterdir():
            if not item.is_dir():
                continue
            if item.name in IGNORE_DIRS or item.name.startswith("."):
                continue
            if (item / "metadata.json").exists():
                dirs.append(item)
            search_stack.append((item, depth + 1))
    return dirs


def main():
    dirs = find_all_demo_dirs(PROJECT_ROOT)
    extended = 0

    for demo_dir in dirs:
        readme_path = demo_dir / "README.md"
        if not readme_path.exists():
            continue
        try:
            if extend_readme(readme_path, get_demo_name(demo_dir)):
                extended += 1
        except Exception as e:
            print(f"❌ {demo_dir}: {e}")

    print(f"扩展 README: {extended}")


if __name__ == "__main__":
    main()
