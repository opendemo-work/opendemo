# Python 异步编程 - asyncio 实战

> 学习 Python asyncio 异步编程模型，理解事件循环、协程、任务和异步 IO，编写高性能并发程序。

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

- ✅ 理解协程与线程的区别
- ✅ 使用 async/await 编写异步代码
- ✅ 使用 asyncio.gather 并发执行任务
- ✅ 使用 aiohttp 进行异步 HTTP 请求

---

## 📐 架构图

```
单线程事件循环 ──▶ 调度多个协程 ──▶ 异步 IO 操作
```

---

## 🚀 快速开始

```bash
cd python/async-programming
pip install -r requirements.txt
python code/async_demo.py
```

---

## 📖 核心概念

### 1. 协程

使用 `async def` 定义的函数：

```python
async def hello():
    await asyncio.sleep(1)
    print("hello")
```

### 2. 事件循环

协调所有协程的执行：

```python
asyncio.run(main())
```

### 3. Task

将协程包装为任务，实现并发：

```python
task1 = asyncio.create_task(fetch_data())
task2 = asyncio.create_task(fetch_data())
await asyncio.gather(task1, task2)
```

---

## 💻 代码示例

### 并发 HTTP 请求

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://api.github.com"] * 10
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls])
        print(f"Fetched {len(results)} pages")

asyncio.run(main())
```

---

## 🧪 验证测试

```bash
python code/async_demo.py
pytest tests/
```

---

## 📚 扩展学习

- [Python 缓存](../caching/)
- [Python 上下文管理器](../context-managers/)
- [asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

Python Async Programming Demo 从启动到完成主要包含以下环节：

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

## ⏳ asyncio.gather vs asyncio.wait

```python
# gather 返回结果列表
results = await asyncio.gather(task1, task2, task3)

# wait 更灵活，可指定返回策略
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
```

---

## 🔒 asyncio.Lock

保护共享资源：

```python
lock = asyncio.Lock()

async def update():
    async with lock:
        shared_value += 1
```
