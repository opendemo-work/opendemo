# Python TDD with pytest

Python测试驱动开发实践。

## pytest基础

```python
# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    @pytest.fixture
    def calc(self):
        return Calculator()
    
    def test_add(self, calc):
        # Arrange
        a, b = 2, 3
        
        # Act
        result = calc.add(a, b)
        
        # Assert
        assert result == 5
    
    def test_divide_by_zero(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ])
    def test_add_parametrized(self, calc, a, b, expected):
        assert calc.add(a, b) == expected

# 被测试代码
class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest test_calculator.py

# 运行特定测试
pytest test_calculator.py::TestCalculator::test_add

# 生成覆盖率报告
pytest --cov=calculator --cov-report=html
```

## Mock测试

```python
from unittest.mock import Mock, patch

def test_api_call():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'status': 'ok'}
        
        result = fetch_data()
        
        assert result['status'] == 'ok'
        mock_get.assert_called_once()
```

## 学习要点

1. pytest fixtures
2. 参数化测试
3. Mock对象
4. 覆盖率检查
5. TDD循环
