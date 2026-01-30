# 逻辑函数编程实战演示

## 简介
本项目通过三个实用场景，帮助初学者深入理解Python中的逻辑函数（如 `and`, `or`, `not`）和自定义逻辑判断函数的应用。涵盖数据验证、权限控制和复杂条件判断等常见用途。

## 学习目标
- 掌握Python基本逻辑运算符的用法
- 学会构建复合逻辑表达式
- 理解布尔值在程序流程控制中的作用
- 能够编写可复用的逻辑判断函数

## 环境要求
- Python 3.7 或更高版本
- 操作系统：Windows / Linux / macOS（均支持）

## 安装依赖
1. 确保已安装Python：
   ```bash
   python --version
   # 应输出 Python 3.x.x
   ```

2. 安装所需依赖包（本项目无外部依赖，仅需标准库）：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`：用户登录权限验证逻辑
- `code/example2.py`：学生成绩等级与奖学金资格判断
- `code/example3.py`：电商平台订单发货可行性分析

## 逐步实操指南

### 步骤1：运行用户权限验证示例
```bash
python code/example1.py
```
**预期输出**：
```
用户 'alice' 权限检查结果: True
用户 'bob' 权限检查结果: False
```

### 步骤2：运行成绩与奖学金判断示例
```bash
python code/example2.py
```
**预期输出**：
```
学生Alice (成绩: 85, 出勤率: 0.92) 是否有奖学金资格: True
学生Bob (成绩: 70, 出勤率: 0.85) 是否有奖学金资格: False
```

### 步骤3：运行订单发货判断示例
```bash
python code/example3.py
```
**预期输出**：
```
订单1（金额: 300, VIP: True, 地区: 国内）是否可发货: True
订单2（金额: 100, VIP: False, 地区: 国外）是否可发货: False
```

## 代码解析

### example1.py 关键代码解析
```python
def has_access(username, is_active, role):
    return is_active and (role == "admin" or username == "alice")
```
- 使用 `and` 确保用户必须处于激活状态
- 使用 `or` 实现“管理员角色或特定用户名”任一满足即可
- 括号明确优先级，避免逻辑错误

### example2.py 关键代码解析
```python
return score >= 80 and attendance_rate >= 0.9
```
- 双重条件同时满足才返回True
- 展示数值比较与布尔逻辑结合使用

### example3.py 关键代码解析
```python
return (order_amount > 200 or is_vip) and shipping_region in ["国内", "international"]
```
- 复合逻辑：高消费或VIP身份 + 有效配送区域
- 演示 `in` 运算符与逻辑运算结合

## 预期输出示例
完整运行三个脚本后应看到类似以下输出：
```
=== 示例1：权限验证 ===
用户 'alice' 权限检查结果: True
用户 'bob' 权限检查结果: False

=== 示例2：奖学金资格 ===
学生Alice (成绩: 85, 出勤率: 0.92) 是否有奖学金资格: True
学生Bob (成绩: 70, 出勤率: 0.85) 是否有奖学金资格: False

=== 示例3：订单发货 ===
订单1（金额: 300, VIP: True, 地区: 国内）是否可发货: True
订单2（金额: 100, VIP: False, 地区: 国外）是否可发货: False
```

## 常见问题解答

**Q1：为什么我的输出是False，但我觉得应该是True？**
A：请检查括号是否正确使用，逻辑运算符优先级为 `not` > `and` > `or`，建议用括号显式分组。

**Q2：如何调试复杂的逻辑表达式？**
A：可以将子表达式拆分为变量，例如：
```python
is_high_value = order_amount > 200
is_eligible_region = shipping_region in ["国内", "international"]
return is_high_value or (is_vip and is_eligible_region)
```

**Q3：能否用数字代替True/False？**
A：Python中非零数字被视为True，但建议始终使用布尔值以提高代码可读性。

## 扩展学习建议
- 尝试将每个逻辑函数改写为 `if-else` 形式进行对比
- 学习 `any()` 和 `all()` 内置函数处理多个条件
- 阅读 [Python官方文档 - 布尔运算](https://docs.python.org/3/library/stdtypes.html#boolean-operations)
- 练习使用德摩根定律简化逻辑表达式
- 探索 `operator` 模块中的逻辑函数