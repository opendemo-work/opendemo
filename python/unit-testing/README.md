# Python Unit Testing Demo

Python单元测试演示项目，全面展示unittest、pytest、mock等测试技术。

## 技术栈

- Python 3.8+
- unittest (标准库)
- pytest
- unittest.mock

## 核心概念

### unittest基础

```python
import unittest

class Calculator:
    """计算器类"""
    
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b

class TestCalculator(unittest.TestCase):
    """计算器测试类"""
    
    def setUp(self):
        """每个测试方法前执行"""
        self.calc = Calculator()
    
    def tearDown(self):
        """每个测试方法后执行"""
        pass
    
    def test_add(self):
        """测试加法"""
        self.assertEqual(self.calc.add(1, 2), 3)
        self.assertEqual(self.calc.add(-1, 1), 0)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(6, 2), 3)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.333, places=3)
    
    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ValueError):
            self.calc.divide(1, 0)

if __name__ == '__main__':
    unittest.main()
```

### pytest基础

```python
# test_pytest_demo.py
import pytest

class TestString:
    """字符串测试"""
    
    def test_upper(self):
        assert 'hello'.upper() == 'HELLO'
    
    def test_isupper(self):
        assert 'HELLO'.isupper()
        assert not 'Hello'.isupper()
    
    @pytest.mark.parametrize("input,expected", [
        ("hello", 5),
        ("world", 5),
        ("pytest", 6)
    ])
    def test_len(self, input, expected):
        assert len(input) == expected

# fixture示例
@pytest.fixture
def sample_data():
    """提供测试数据"""
    return {'name': 'test', 'value': 42}

def test_data(sample_data):
    assert sample_data['name'] == 'test'
    assert sample_data['value'] == 42
```

### Mock测试

```python
from unittest.mock import Mock, patch, MagicMock
import unittest

class TestMock(unittest.TestCase):
    """Mock测试示例"""
    
    def test_mock_object(self):
        """测试Mock对象"""
        mock = Mock()
        mock.return_value = 42
        
        result = mock()
        self.assertEqual(result, 42)
        mock.assert_called_once()
    
    def test_mock_method(self):
        """测试Mock方法"""
        mock = Mock()
        mock.some_method.return_value = 'hello'
        
        result = mock.some_method()
        self.assertEqual(result, 'hello')
    
    @patch('requests.get')
    def test_patch_decorator(self, mock_get):
        """使用patch装饰器"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}
        
        import requests
        response = requests.get('https://api.example.com')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'key': 'value'})
    
    def test_patch_context(self):
        """使用patch上下文管理器"""
        with patch('builtins.open') as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = 'test data'
            
            with open('test.txt') as f:
                content = f.read()
            
            self.assertEqual(content, 'test data')
```

### 测试覆盖率

```bash
# 安装pytest-cov
pip install pytest-cov

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html --cov-report=term
```

### 高级测试技巧

```python
# 跳过测试
@pytest.mark.skip(reason="功能未实现")
def test_feature_not_ready():
    pass

# 条件跳过
@pytest.mark.skipif(sys.platform == 'win32', reason="Windows不支持")
def test_unix_feature():
    pass

# 预期失败
@pytest.mark.xfail(reason="已知bug")
def test_bug():
    assert 1 == 2

# 超时设置
@pytest.mark.timeout(5)
def test_slow_operation():
    pass
```

## 测试目录结构

```
project/
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   └── utils.py
└── tests/
    ├── __init__.py
    ├── test_calculator.py
    ├── test_utils.py
    └── conftest.py
```

## 快速开始

```bash
# 安装依赖
pip install pytest pytest-cov

# 运行unittest
python -m unittest discover -s tests -v

# 运行pytest
pytest -v

# 运行特定测试
pytest test_calculator.py::TestCalculator::test_add -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 学习要点

1. 测试驱动开发(TDD)理念
2. 单元测试vs集成测试
3. Mock和Patch的使用场景
4. 测试覆盖率的重要性
5. 持续集成中的测试自动化

## 参考

- [unittest文档](https://docs.python.org/3/library/unittest.html)
- [pytest文档](https://docs.pytest.org/)
