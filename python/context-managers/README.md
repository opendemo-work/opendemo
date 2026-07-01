# Python 上下文管理器 - 资源安全处理

> 学习 Python 上下文管理器（with 语句），理解 __enter__ 和 __exit__，实现自定义资源管理。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 with 语句的工作原理
- ✅ 使用 contextlib 快速创建上下文管理器
- ✅ 自定义类实现 __enter__ 和 __exit__
- ✅ 使用上下文管理器处理文件、锁、数据库连接

---

## 📐 架构图

```
with Resource() as r:
    执行操作

__enter__ ──▶ 业务逻辑 ──▶ __exit__
```

---

## 🚀 快速开始

```bash
cd python/context-managers
python code/context_manager_demo.py
```

---

## 📖 核心概念

### 1. with 语句

自动管理资源生命周期：

```python
with open('file.txt', 'r') as f:
    content = f.read()
# 文件自动关闭
```

### 2. 自定义上下文管理器

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = create_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
```

### 3. contextlib

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)
```

---

## 🧪 验证测试

```bash
python code/context_manager_demo.py
pytest tests/
```

---

## 📚 扩展学习

- [Python 异步编程](../async-programming/)
- [Python 缓存](../caching/)
- [Python 官方文档](https://docs.python.org/3/reference/datamodel.html#context-managers)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

Context Managers Demo 从启动到完成主要包含以下环节：

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


---

## 🔄 多个上下文管理器

```python
with open('a.txt') as f1, open('b.txt') as f2:
    content = f1.read() + f2.read()
```

---

## 🛡️ suppress 忽略异常

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove('temp.txt')
```


---

## 🌐 网络资源管理

```python
from urllib.request import urlopen

with urlopen('https://api.example.com') as response:
    data = response.read()
```

上下文管理器确保网络连接及时释放。


---

## 🧪 上下文管理器练习

实现一个用于计时的上下文管理器：

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")

with timer():
    time.sleep(1)
```
