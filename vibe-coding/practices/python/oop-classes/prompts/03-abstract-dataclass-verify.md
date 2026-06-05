# Prompt 03: 抽象类 + 数据类 + 验证

添加两个函数：

demo_abstract_class()：Shape(ABC) 抽象类，Rectangle 和 Circle 子类实现 area/perimeter

demo_dataclass()：Product @dataclass，含 name, price, quantity, tags（用 field(default_factory=list)），total_value() 方法

然后运行 python code/oop_classes.py 验证全部 7 个 demo。

---
## 背景
- 工具：Cursor
- 阶段：第 4-5 轮
- 结果：AI 对 tags 用了可变默认值（list），需改为 field(default_factory=list)
