# Python Design Patterns

Python设计模式实践。

## 常用设计模式

### 1. 单例模式
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 使用
s1 = Singleton()
s2 = Singleton()
assert s1 is s2  # True
```

### 2. 装饰器模式
```python
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
```

### 3. 工厂模式
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError(f"Unknown animal type: {animal_type}")
```

### 4. 上下文管理器
```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = create_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# 使用
with DatabaseConnection() as conn:
    conn.execute("SELECT * FROM users")
```

## Python惯用法

```python
# 列表推导式
squares = [x**2 for x in range(10)]

# 生成器表达式
sum_of_squares = sum(x**2 for x in range(1000000))

# 字典合并
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3}
merged = {**dict1, **dict2}

# 装饰器链
@cache
@timing
def expensive_function():
    pass
```

## 学习要点

1. Pythonic设计模式
2. 鸭子类型
3. 装饰器应用
4. 上下文管理器
5. 元类编程
