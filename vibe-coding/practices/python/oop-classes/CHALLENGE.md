# 挑战：Python 面向对象编程

## 难度：beginner | 预计用时：25 分钟 | 推荐工具：任何 AI 编码工具

## 目标

用 Python 实现一组面向对象编程示例，涵盖以下概念：

1. **类基础** — Person 类（name, age），包含实例方法、类方法、静态方法
2. **继承** — Student 继承 Person，添加 student_id 属性
3. **多态** — Animal 基类 + Dog/Cat 子类，不同的 speak() 实现
4. **封装** — BankAccount 类，私有属性 `__balance`，提供 deposit/withdraw/get_balance 方法
5. **属性装饰器** — Circle 类，`@property` 控制 radius 的赋值验证，area 只读
6. **抽象基类** — Shape 抽象类（ABC），Rectangle 和 Circle 子类实现 area/perimeter
7. **数据类** — Product 类使用 `@dataclass`，包含 name、price、quantity 和 total_value() 方法

## 约束

- Python 3.8+，只使用标准库
- 所有代码放在一个文件 `oop_classes.py` 的 `demo_*()` 函数中
- 每个概念一个 `demo_*()` 函数，`main()` 依次调用
- 输出要清晰展示每个概念的效果

## 验证

```bash
python code/oop_classes.py
```

预期输出包含以下关键信息：
```
1. 类基础
p1.introduce(): 我是Alice, 25岁
Person.species = Human
Person.is_adult(25) = True

2. 继承
dog.name: Buddy, breed: Golden Retriever
dog.speak(): Woof!
isinstance(dog, Animal): True

3. 多重继承与MRO
D().method(): B
D的MRO: ['D', 'B', 'C', 'A', 'object']

4. 特殊方法
v1 + v2: (4, 6)
v1 * 2: (6, 8)

5. 属性装饰器 @property
面积: 78.54...

6. 抽象类
Rectangle: 面积=20.00, 周长=18.00
Circle: 面积=28.27, 周长=18.85

7. 数据类 @dataclass
p1: Product(name='Apple', price=1.5, quantity=100, tags=[])
p1.total_value(): 150.0

[OK] 面向对象编程演示完成!
```

## 提示（卡住时再看）

<details>
<summary>提示 1：从最简单的开始</summary>

先让 AI 生成 Person 类，确认能跑通，再逐个添加其他 demo 函数。不要一次生成全部。

</details>

<details>
<summary>提示 2：关键 Prompt</summary>

"用 Python 实现一组 OOP 示例：类基础（Person）、继承（Student extends Person）、多态（Animal→Dog/Cat）、封装（BankAccount 私有属性）、@property（Circle 半径验证）、抽象基类（Shape ABC）、@dataclass（Product）。每个概念一个 demo 函数。"

</details>

## 对应原 Demo

完成后对比参考实现：`python/oop-classes/`
