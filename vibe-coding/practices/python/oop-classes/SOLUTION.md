# 解决过程：Python 面向对象编程

## 使用的工具：Cursor（Cmd+K + Cmd+L）

---

### 第 1 轮：类基础

**Prompt：**
> 写一个 demo_class_basics() 函数演示 Python 类基础：
> - Person 类有 name, age 实例属性，species="Human" 类属性
> - introduce() 实例方法返回 "我是{name}, {age}岁"
> - get_species() 类方法（@classmethod）
> - is_adult(age) 静态方法（@staticmethod）
> - 创建两个实例 Alice(25) 和 Bob(17) 测试

**AI 生成：** 正确实现，输出格式和预期一致。

---

### 第 2 轮：继承

**Prompt：**
> 添加 demo_inheritance() 函数：
> - Animal 基类有 name 和 speak()（返回 "Some sound"）
> - Dog(Animal) 添加 breed 属性，重写 speak() 返回 "Woof!"
> - Cat(Animal) 重写 speak() 返回 "Meow!"
> - 演示 isinstance 和 issubclass

**AI 生成：** 正确。`super().__init__(name)` 调用正确。

---

### 第 3 轮：多重继承 + 特殊方法（一次性）

**Prompt：**
> 添加两个函数：
> 1. demo_multiple_inheritance() — 演示 MRO（D 继承 B 和 C，B 和 C 都继承 A）
> 2. demo_special_methods() — Vector 类实现 __repr__, __str__, __add__, __mul__, __eq__, __len__

**AI 生成：** 正确。MRO 输出 `['D', 'B', 'C', 'A', 'object']`。Vector 运算符重载正确。

---

### 第 4 轮：属性装饰器 + 抽象类 + 数据类

**Prompt：**
> 添加三个函数：
> 1. demo_property() — Circle 类，@property radius 做负数验证，@property area 只读
> 2. demo_abstract_class() — Shape(ABC) 抽象类，Rectangle 和 Circle 子类实现 area/perimeter
> 3. demo_dataclass() — Product @dataclass，含 name, price, quantity, tags，total_value() 方法

**AI 生成：** 基本正确。

**问题：** dataclass 的 `tags: list` 用了可变默认值。

**修复：** "把 tags 的默认值改成 `field(default_factory=list)`，避免可变默认值陷阱"。

**学习点：** Python 经典坑——可变默认参数在所有实例间共享。`dataclass` 中必须用 `field(default_factory=list)`。

---

### 第 5 轮：验证

```bash
python code/oop_classes.py
```

**结果：** 全部 7 个 demo 输出正确 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 5 轮 |
| 实际用时 | ~15 分钟 |
| AI 犯错次数 | 1（可变默认值） |
| 人工干预 | 修复 dataclass 默认值 |

### 关键技巧
- **分概念逐步生成** — OOP 概念多但每个简单，可以 2-3 个一批生成
- **注意可变默认值** — Python 的经典坑，AI 也经常踩
- **ABC 的 @abstractmethod** — 忘记装饰器的话子类不会被强制实现

### 常见坑
- `__balance` 双下划线私有属性 — 外部访问返回 `AttributeError`，但实际可以通过 `_ClassName__balance` 访问
- `@dataclass` 的可变默认值 — 必须用 `field(default_factory=...)`
- MRO 顺序 — Python 用 C3 线性化，D(B, C) 的 MRO 是 D→B→C→A→object
