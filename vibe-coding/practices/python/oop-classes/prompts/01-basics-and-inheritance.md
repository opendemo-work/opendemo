# Prompt 01: 类基础 + 继承

用 Python 实现两组 OOP demo 函数：

demo_class_basics()：
- Person 类有 name, age 实例属性，species="Human" 类属性
- introduce() 实例方法返回 "我是{name}, {age}岁"
- get_species() 类方法（@classmethod）
- is_adult(age) 静态方法（@staticmethod）
- 创建两个实例 Alice(25) 和 Bob(17)

demo_inheritance()：
- Animal 基类有 name 和 speak()
- Dog(Animal) 添加 breed，重写 speak() → "Woof!"
- Cat(Animal) 重写 speak() → "Meow!"
- 演示 isinstance 和 issubclass

---
## 背景
- 工具：Cursor
- 阶段：第 1-2 轮
- 结果：一次正确
