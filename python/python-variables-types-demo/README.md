# Python变量和数据类型基础

## 🎯 案例概述

这是一个全面展示Python变量声明和内置数据类型的基础示例，涵盖变量赋值、数值类型、序列类型、映射类型、集合类型等Python核心数据结构的使用方法。

## 📚 学习目标

通过本示例你将掌握：
- Python变量赋值和命名规则
- 所有内置数据类型的特性和应用
- 类型转换的方法和注意事项
- 类型检查的技术
- Python内存管理机制

## 🔧 核心知识点

### 1. 变量和赋值
- 动态类型系统特点
- 变量命名约定和规则
- 多重赋值和变量交换
- 对象引用机制

### 2. 数值类型
- **int**: 整数类型（支持任意精度）
- **float**: 浮点数类型
- **complex**: 复数类型
- **bool**: 布尔类型

### 3. 序列类型
- **str**: 字符串类型
- **list**: 列表类型（可变）
- **tuple**: 元组类型（不可变）
- **bytes**: 字节类型
- **bytearray**: 可变字节类型

### 4. 映射类型
- **dict**: 字典类型（键值对存储）

### 5. 集合类型
- **set**: 集合类型（可变，无序，去重）
- **frozenset**: 冰冻集合类型（不可变）

## 🚀 运行示例

```bash
# 运行主程序
python variables_types_demo.py

# 运行测试
python -m pytest test_variables_types.py -v
```

## 📖 代码详解

### 主要功能演示

```python
def demonstrate_variable_assignment()    # 变量赋值演示
def demonstrate_numeric_types()          # 数值类型演示
def demonstrate_sequence_types()         # 序列类型演示
def demonstrate_mapping_types()          # 映射类型演示
def demonstrate_set_types()              # 集合类型演示
def demonstrate_type_conversion()        # 类型转换演示
def demonstrate_type_checking()          # 类型检查演示
def demonstrate_memory_management()      # 内存管理演示
```

### 关键技术点演示

#### 1. 变量赋值和命名
```python
# 基本赋值
name = "张三"
age = 25
is_student = True

# 多重赋值
x = y = z = 10
a, b, c = 1, 2, 3

# 变量交换
a, b = b, a

# 命名约定
snake_case_variable = "推荐命名法"
UPPER_CASE_CONSTANT = "常量命名"
_private_variable = "私有变量"
ClassName = "类名命名"
```

#### 2. 数值类型示例
```python
# 整数
integer = 42
binary = 0b1010    # 二进制: 10
octal = 0o755      # 八进制: 493
hex_num = 0xFF     # 十六进制: 255

# 浮点数
float_num = 3.14159
scientific = 1.23e-4
infinity = float('inf')

# 复数
complex_num = 3 + 4j
print(complex_num.real)  # 3.0
print(complex_num.imag)  # 4.0

# 布尔值
is_true = True   # 实际值为1
is_false = False # 实际值为0
```

#### 3. 序列类型示例
```python
# 字符串
string = "Hello World"
multiline = """多行
字符串"""

# 列表（可变）
list_data = [1, 2, 3, 4, 5]
list_data.append(6)  # 可以修改

# 元组（不可变）
tuple_data = (1, 2, 3)
# tuple_data[0] = 10  # 这会报错

# 字节类型
byte_data = b"Hello"
byte_array = bytearray(b"World")
```

#### 4. 映射和集合类型
```python
# 字典
dict_data = {'name': '张三', 'age': 25}
dict_data['city'] = '北京'  # 动态添加

# 集合（自动去重）
set_data = {1, 2, 3, 3, 4}  # 结果: {1, 2, 3, 4}

# 集合运算
set_a = {1, 2, 3}
set_b = {3, 4, 5}
union = set_a | set_b      # 并集: {1, 2, 3, 4, 5}
intersection = set_a & set_b  # 交集: {3}
```

#### 5. 类型转换示例
```python
# 显式转换
num_str = str(42)           # '42'
num_int = int('123')        # 123
num_float = float('3.14')   # 3.14
bool_val = bool(0)          # False

# 序列转换
char_list = list('hello')   # ['h', 'e', 'l', 'l', 'o']
tuple_from_list = tuple([1, 2, 3])  # (1, 2, 3)
set_from_list = set([1, 2, 2, 3])   # {1, 2, 3}

# 字典转换
dict_from_pairs = dict([('a', 1), ('b', 2)])  # {'a': 1, 'b': 2}
```

#### 6. 类型检查方法
```python
# isinstance检查（推荐）
isinstance(42, int)              # True
isinstance(3.14, (int, float))   # True
isinstance("hello", str)         # True

# type检查
type(42) == int                  # True
type([1, 2, 3]) == list          # True

# 实际类型判断
type(42).__name__                # 'int'
```

## 🧪 测试覆盖

测试文件 `test_variables_types.py` 包含以下测试：

✅ 变量赋值测试  
✅ 数值类型测试  
✅ 序列类型测试  
✅ 映射类型测试  
✅ 集合类型测试  
✅ 类型转换测试  
✅ 类型检查测试  
✅ 内存管理测试  

## 🎯 实际应用场景

### 1. 数据处理场景
```python
# 处理用户数据
user_data = {
    'name': '张三',
    'age': 25,
    'scores': [85, 92, 78, 96],
    'subjects': {'数学', '英语', '物理'}
}

# 类型安全的数据处理
if isinstance(user_data['age'], int) and user_data['age'] > 0:
    print(f"用户年龄: {user_data['age']}岁")

# 数据转换
average_score = sum(user_data['scores']) / len(user_data['scores'])
user_data['average'] = round(average_score, 2)
```

### 2. 配置管理场景
```python
# 应用配置
config = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'name': 'myapp',
        'timeout': 30.5
    },
    'features': {
        'debug': True,
        'cache_enabled': False,
        'allowed_hosts': ['localhost', '127.0.0.1']
    }
}

# 配置验证
def validate_config(config):
    required_keys = ['database', 'features']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"缺少必要配置项: {key}")
    
    if not isinstance(config['database']['port'], int):
        raise TypeError("端口号必须是整数")
```

### 3. 数据清洗场景
```python
# 数据去重和类型统一
raw_data = ['123', '456', '123', '789', '456']
unique_numbers = set(int(x) for x in raw_data if x.isdigit())

# 数据分组
data_by_type = {}
mixed_data = [1, 'hello', 3.14, True, [1, 2], {'key': 'value'}]

for item in mixed_data:
    type_name = type(item).__name__
    if type_name not in data_by_type:
        data_by_type[type_name] = []
    data_by_type[type_name].append(item)
```

## ⚡ 最佳实践建议

### 1. 变量命名
- 使用描述性的变量名
- 遵循PEP 8命名规范
- 常量使用全大写
- 私有变量使用下划线前缀

### 2. 类型使用建议
- 选择合适的数据结构
- 注意可变性对程序的影响
- 合理使用类型提示
- 考虑内存使用效率

### 3. 类型转换原则
- 明确转换意图
- 处理转换异常
- 避免不必要的转换
- 保持数据一致性

## 🔍 常见问题和解决方案

### 1. 可变对象陷阱
```python
# 问题：默认参数的可变对象陷阱
def add_item(item, target_list=[]):  # 危险！
    target_list.append(item)
    return target_list

# 解决：使用None作为默认值
def add_item_safe(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

### 2. 浮点数精度问题
```python
# 问题：浮点数计算精度
result = 0.1 + 0.2
print(result)  # 0.30000000000000004

# 解决：使用decimal模块或适当舍入
from decimal import Decimal
precise_result = Decimal('0.1') + Decimal('0.2')
print(precise_result)  # 0.3
```

### 3. 字符串与字节混淆
```python
# 问题：字符串和字节类型混淆
text = "Hello"
# file.write(text)  # 如果文件是二进制模式会报错

# 解决：正确处理编码
encoded_text = text.encode('utf-8')  # 转为bytes
# file.write(encoded_text)  # 正确
```

## 📚 扩展学习资源

### 官方文档
- [Python内置类型](https://docs.python.org/3/library/stdtypes.html)
- [数据模型](https://docs.python.org/3/reference/datamodel.html)

### 推荐书籍
- 《流畅的Python》
- 《Python Cookbook》
- 《Effective Python》

### 相关主题
- 类型提示和mypy
- collections模块
- dataclasses
- typing模块

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的变量和数据类型演示

---
**注意**: 理解Python的数据类型系统是掌握这门语言的基础，建议通过大量练习来熟悉各种类型的特性和使用场景。