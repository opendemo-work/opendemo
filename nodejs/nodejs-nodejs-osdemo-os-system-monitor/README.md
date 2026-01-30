# Node.js OS模块系统信息监控Demo

## 简介
本示例演示如何使用Node.js内置的`os`模块获取操作系统级别的系统信息，包括CPU、内存、网络接口和系统运行时间等。适用于构建轻量级系统监控工具。

## 学习目标
- 掌握Node.js中`os`模块的核心API用法
- 学会获取系统硬件与网络信息
- 实践命令行脚本开发与格式化输出

## 环境要求
- Node.js 14.x 或更高版本（推荐 LTS 版本，如 18.x 或 20.x）
- 支持 Windows、Linux 和 macOS 跨平台运行
- 无需额外安装Python/Java

## 安装依赖
本项目仅使用Node.js内置模块，无需第三方依赖。

1. 检查Node.js版本：
   ```bash
   node --version
   ```
   预期输出（版本号可能不同）：
   ```
   v18.17.0
   ```

2. 确保已安装Node.js，若未安装请前往 [https://nodejs.org](https://nodejs.org) 下载LTS版本。

## 文件说明
- `system-info.js`：显示系统基本信息（主机名、架构、平台、CPU、内存）
- `network-info.js`：列出所有网络接口及其IP地址
- `system-uptime.js`：显示系统启动时间和运行时长

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir os-monitor-demo && cd os-monitor-demo
```

### 步骤2：创建代码文件
将以下三个文件保存到项目目录中：

创建 `system-info.js`：
```bash
node system-info.js
```
预期输出示例：
```
系统信息监控 - 基本信息
========================
主机名: my-computer
操作系统: linux
系统架构: x64
CPU型号: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz\nCPU核心数: 12
总内存: 16.00 GB
可用内存: 3.45 GB (21.56%)
```

运行网络信息脚本：
```bash
node network-info.js
```
预期输出示例：
```
网络接口信息
==============
en0 (IPv4): 192.168.1.100
lo0 (IPv4): 127.0.0.1
lo0 (IPv6): ::1
```

运行系统运行时间脚本：
```bash
node system-uptime.js
```
预期输出示例：
```
系统运行时间
============
已运行: 3天 5小时 23分钟
上次重启时间: 2023-10-01T08:45:12.000Z
```

## 代码解析

### system-info.js
- 使用 `os.hostname()` 获取主机名
- `os.type()` 和 `os.platform()` 区分系统类型
- `os.cpus()[0]` 获取第一个CPU信息，包括型号和频率
- `os.totalmem()` 和 `os.freemem()` 返回字节数，需转换为GB并保留两位小数

### network-info.js
- `os.networkInterfaces()` 返回对象，键为接口名（如eth0、Wi-Fi）
- 遍历每个接口及其地址数组，过滤出IPv4和IPv6有效地址

### system-uptime.js
- `os.uptime()` 返回秒数，转换为天/小时/分钟
- 使用 `new Date(Date.now() - uptime * 1000)` 计算启动时间戳

## 预期输出示例
见各步骤中的“预期输出”部分。

## 常见问题解答

**Q: 运行时报错 `Error: Cannot find module 'os'`？**
A: `os` 是Node.js内置模块，此错误通常因Node.js未正确安装。请重新安装Node.js。

**Q: 输出的内存单位是字节吗？**
A: 是的，`os.totalmem()` 和 `os.freemem()` 返回字节数，代码中已转换为GB。

**Q: 如何让监控每隔5秒刷新一次？**
A: 可在任一脚本中包裹 `setInterval(() => { /* 逻辑 */ }, 5000)` 实现轮询。

## 扩展学习建议
- 将监控数据写入日志文件或发送到HTTP服务器
- 结合 `fs` 模块读取磁盘使用情况
- 使用 `child_process` 调用系统命令增强监控能力
- 探索第三方库如 `systeminformation` 获取更详细的硬件数据