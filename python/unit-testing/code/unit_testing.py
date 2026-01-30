#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python单元测试演示
展示unittest模块的常用功能
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os


# ========== 被测试的代码 ==========
class Calculator:
    """计算器类"""
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


def fetch_user_data(user_id):
    """模拟获取用户数据(实际会调用API)"""
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()


# ========== 测试类 ==========
class TestCalculatorBasics(unittest.TestCase):
    """计算器基础测试"""
    
    def setUp(self):
        """每个测试方法前执行"""
        self.calc = Calculator()
    
    def tearDown(self):
        """每个测试方法后执行"""
        pass
    
    def test_add(self):
        """测试加法"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 5), -4)
    
    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.333, places=2)
    
    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertIn("除数不能为零", str(context.exception))


class TestAssertions(unittest.TestCase):
    """断言方法演示"""
    
    def test_equality(self):
        """相等性断言"""
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1 + 1, 3)
    
    def test_truthiness(self):
        """真值断言"""
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertIsNone(None)
        self.assertIsNotNone("something")
    
    def test_comparison(self):
        """比较断言"""
        self.assertGreater(5, 3)
        self.assertGreaterEqual(5, 5)
        self.assertLess(3, 5)
        self.assertLessEqual(3, 3)
    
    def test_membership(self):
        """成员断言"""
        self.assertIn(3, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])
    
    def test_type(self):
        """类型断言"""
        self.assertIsInstance("hello", str)
        self.assertIsInstance([], list)
    
    def test_sequence(self):
        """序列断言"""
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        self.assertDictEqual({'a': 1}, {'a': 1})


class TestMocking(unittest.TestCase):
    """Mock测试演示"""
    
    def test_basic_mock(self):
        """基本Mock使用"""
        mock_obj = Mock()
        mock_obj.method.return_value = "mocked result"
        
        result = mock_obj.method()
        
        self.assertEqual(result, "mocked result")
        mock_obj.method.assert_called_once()
    
    def test_mock_with_side_effect(self):
        """Mock副作用"""
        mock_obj = Mock()
        mock_obj.method.side_effect = [1, 2, 3]
        
        self.assertEqual(mock_obj.method(), 1)
        self.assertEqual(mock_obj.method(), 2)
        self.assertEqual(mock_obj.method(), 3)
    
    @patch('os.path.exists')
    def test_patch_decorator(self, mock_exists):
        """使用patch装饰器"""
        mock_exists.return_value = True
        
        result = os.path.exists('/fake/path')
        
        self.assertTrue(result)
        mock_exists.assert_called_with('/fake/path')
    
    def test_patch_context_manager(self):
        """使用patch上下文管理器"""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            
            result = os.path.exists('/fake/path')
            
            self.assertFalse(result)


class TestFixtures(unittest.TestCase):
    """测试夹具演示"""
    
    @classmethod
    def setUpClass(cls):
        """类级别设置(所有测试前执行一次)"""
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.temp_dir, 'test.txt')
        with open(cls.test_file, 'w') as f:
            f.write("test content")
    
    @classmethod
    def tearDownClass(cls):
        """类级别清理(所有测试后执行一次)"""
        import shutil
        shutil.rmtree(cls.temp_dir)
    
    def test_file_exists(self):
        """测试文件存在"""
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_file_content(self):
        """测试文件内容"""
        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, "test content")


class TestSkipAndExpectedFailure(unittest.TestCase):
    """跳过和预期失败"""
    
    @unittest.skip("演示跳过测试")
    def test_skip(self):
        """这个测试会被跳过"""
        self.fail("这不会执行")
    
    @unittest.skipIf(True, "条件为真时跳过")
    def test_skip_if(self):
        """条件跳过"""
        self.fail("这不会执行")
    
    @unittest.expectedFailure
    def test_expected_failure(self):
        """预期失败的测试"""
        self.assertEqual(1, 2)  # 这会失败,但不会报告为错误


class TestSubTest(unittest.TestCase):
    """子测试演示"""
    
    def test_with_subtest(self):
        """使用子测试进行参数化"""
        test_cases = [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5),
        ]
        
        calc = Calculator()
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = calc.add(a, b)
                self.assertEqual(result, expected)


def run_demo():
    """运行演示"""
    print("=" * 50)
    print("Python单元测试演示")
    print("=" * 50)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestAssertions))
    suite.addTests(loader.loadTestsFromTestCase(TestMocking))
    suite.addTests(loader.loadTestsFromTestCase(TestFixtures))
    suite.addTests(loader.loadTestsFromTestCase(TestSkipAndExpectedFailure))
    suite.addTests(loader.loadTestsFromTestCase(TestSubTest))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出统计
    print("\n" + "=" * 50)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    print(f"预期失败: {len(result.expectedFailures)}")
    print("=" * 50)
    
    print("\n[OK] 单元测试演示完成!")


if __name__ == "__main__":
    run_demo()
