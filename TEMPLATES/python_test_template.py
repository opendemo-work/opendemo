#!/usr/bin/env python3
"""
Python 测试模板

使用方法:
1. 将此文件复制到 demo 目录下
2. 重命名为 test_*.py 或 *_test.py
3. 运行测试: pytest -v

测试命名规范:
- 测试文件: test_<module>.py 或 <module>_test.py
- 测试类: Test<ClassName>
- 测试函数: test_<function_name>_<scenario>
"""

import pytest
from typing import Any, List, Tuple, Optional


# ============================================================================
# 测试夹具 (Fixtures)
# ============================================================================

@pytest.fixture
def sample_data():
    """提供测试数据的夹具"""
    return {
        "name": "test",
        "value": 42,
        "items": [1, 2, 3],
    }


@pytest.fixture(scope="module")
def module_setup():
    """模块级别的设置"""
    # 设置代码
    print("\n模块级设置")
    yield
    # 清理代码
    print("模块级清理")


# ============================================================================
# 测试类
# ============================================================================

class TestFeature:
    """
    功能测试类
    
    描述: [描述你要测试的功能]
    """
    
    @classmethod
    def setup_class(cls):
        """类级别的设置"""
        print("\n类级设置")
    
    @classmethod
    def teardown_class(cls):
        """类级别的清理"""
        print("类级清理")
    
    def setup_method(self):
        """方法级别的设置"""
        print("方法级设置")
    
    def teardown_method(self):
        """方法级别的清理"""
        print("方法级清理")
    
    def test_normal_case(self):
        """测试正常情况"""
        # Arrange (准备)
        input_data = "test_input"
        expected = "expected_output"
        
        # Act (执行)
        # result = your_function(input_data)
        result = input_data  # 占位符
        
        # Assert (断言)
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_edge_case_empty_input(self):
        """测试边界情况 - 空输入"""
        # Arrange
        input_data = ""
        expected = ""
        
        # Act
        result = input_data  # 占位符
        
        # Assert
        assert result == expected
    
    def test_error_case_invalid_input(self):
        """测试错误情况 - 无效输入"""
        # Arrange
        input_data = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid input"):
            # your_function(input_data)
            raise ValueError("Invalid input")  # 占位符
    
    @pytest.mark.parametrize("input_val,expected", [
        ("case1", "result1"),
        ("case2", "result2"),
        ("case3", "result3"),
    ])
    def test_multiple_cases(self, input_val, expected):
        """参数化测试多个用例"""
        # Act
        result = input_val  # 占位符
        
        # Assert
        assert result == input_val


# ============================================================================
# 独立测试函数
# ============================================================================

def test_standalone_function():
    """
    独立测试函数示例
    
    适用于简单的功能测试
    """
    # Arrange
    data = [1, 2, 3, 4, 5]
    
    # Act
    result = sum(data)
    
    # Assert
    assert result == 15
    assert isinstance(result, int)


@pytest.mark.slow
def test_slow_operation():
    """标记为慢测试"""
    import time
    time.sleep(0.1)
    assert True


@pytest.mark.skip(reason="功能尚未实现")
def test_unimplemented_feature():
    """跳过未实现的功能测试"""
    pass


@pytest.mark.skipif(True, reason="条件不满足时跳过")
def test_conditional_skip():
    """条件跳过的测试"""
    pass


# ============================================================================
# 集成测试
# ============================================================================

@pytest.mark.integration
def test_integration():
    """
    集成测试示例
    
    运行: pytest -m integration
    """
    # 集成测试代码
    pass


# ============================================================================
# 性能测试
# ============================================================================

def test_performance():
    """性能测试示例"""
    import time
    
    start = time.time()
    
    # 执行操作
    for _ in range(1000):
        pass
    
    end = time.time()
    elapsed = end - start
    
    # 断言执行时间小于阈值
    assert elapsed < 1.0, f"Performance test failed: {elapsed}s"


# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])
