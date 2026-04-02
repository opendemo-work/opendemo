"""
AI 服务测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from services.ai_service import AIService
from services.config_service import ConfigService


class TestAIService:
    """AI服务测试类"""

    def setup_method(self):
        """设置测试环境"""
        self.config = Mock(spec=ConfigService)
        self.config.get.side_effect = lambda key, default=None: {
            'ai.api_key': 'test-api-key',
            'ai.model': 'gpt-3.5-turbo',
            'ai.temperature': 0.7,
            'ai.max_tokens': 2000,
            'ai.timeout': 30,
            'ai.retry_times': 3,
            'ai.retry_interval': 2
        }.get(key, default)
        self.ai_service = AIService(self.config)

    def test_init(self):
        """测试初始化"""
        assert self.ai_service.config == self.config
        assert self.ai_service.api_key == 'test-api-key'
        assert self.ai_service.model == 'gpt-3.5-turbo'

    def test_generate_demo_success(self):
        """测试成功生成demo"""
        mock_response = {
            'demo': {
                'name': 'test-demo',
                'language': 'python',
                'keywords': ['test'],
                'description': 'Test demo',
                'code': 'print("Hello World")',
                'readme': '# Test Demo',
                'metadata': {'verified': False}
            }
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response

            result = self.ai_service.generate_demo('python', 'test demo', 'beginner')
            assert result == mock_response['demo']

    def test_generate_demo_no_api_key(self):
        """测试无API密钥"""
        self.config.get.return_value = None
        ai_service = AIService(self.config)
        result = ai_service.generate_demo('python', 'test demo', 'beginner')
        assert result is None

    def test_build_prompt(self):
        """测试构建提示词"""
        prompt = self.ai_service._build_prompt('python', 'test demo', 'beginner')
        assert 'python' in prompt
        assert 'test demo' in prompt
        assert 'beginner' in prompt

    def test_call_api_success(self):
        """测试API调用成功"""
        mock_response = {'demo': {'name': 'test'}}

        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response

            result = self.ai_service._call_api('test prompt')
            assert result == mock_response

    def test_call_api_failure(self):
        """测试API调用失败"""
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 500

            result = self.ai_service._call_api('test prompt')
            assert result is None

    def test_parse_response(self):
        """测试解析响应"""
        mock_response = {
            'demo': {
                'name': 'test-demo',
                'language': 'python',
                'keywords': ['test'],
                'description': 'Test demo',
                'code': 'print("Hello")',
                'readme': '# Test',
                'metadata': {'verified': False}
            }
        }

        result = self.ai_service._parse_response(mock_response)
        assert result == mock_response['demo']

    def test_validate_api_key(self):
        """测试验证API密钥"""
        # 有效的API密钥
        assert self.ai_service._validate_api_key('sk-1234567890abcdef') is True
        # 无效的API密钥
        assert self.ai_service._validate_api_key('') is False
        assert self.ai_service._validate_api_key(None) is False

    def test_classify_keyword(self):
        """测试关键词分类"""
        # 测试已知库
        assert self.ai_service._classify_keyword('numpy') == 'numpy'
        # 测试未知库
        assert self.ai_service._classify_keyword('unknownlib') is None

    def test_heuristic_classify(self):
        """测试启发式分类"""
        # 测试明确的库名
        result = self.ai_service._heuristic_classify(['numpy', 'array'])
        assert result == 'numpy'
        # 测试不明确的输入
        result = self.ai_service._heuristic_classify(['test', 'demo'])
        assert result is None
