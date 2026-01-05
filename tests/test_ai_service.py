"""
AIService 单元测试
"""

import pytest
import json
import time
import requests
from unittest.mock import Mock, patch, MagicMock
from opendemo.services.ai_service import AIService


class TestAIServiceInit:
    """AIService 初始化测试"""

    def test_init(self, mock_config):
        """测试初始化"""
        ai_service = AIService(mock_config)
        assert ai_service.config == mock_config
        assert ai_service._api_key is None
        assert ai_service._api_endpoint is None
        assert ai_service._model is None

    def test_load_config(self, mock_config):
        """测试加载配置"""
        ai_service = AIService(mock_config)
        ai_service._load_config()
        
        assert ai_service._api_key == "test-key"
        assert ai_service._api_endpoint == "https://api.openai.com/v1/chat/completions"
        assert ai_service._model == "gpt-4"


class TestAIServicePrompt:
    """Prompt构建测试"""

    def test_build_prompt_python(self, mock_config):
        """测试构建Python prompt"""
        ai_service = AIService(mock_config)
        prompt = ai_service._build_prompt("python", "logging", "beginner")
        
        assert "python" in prompt.lower()
        assert "logging" in prompt.lower()
        assert "beginner" in prompt.lower()
        assert "PEP 8" in prompt

    def test_build_prompt_java(self, mock_config):
        """测试构建Java prompt"""
        ai_service = AIService(mock_config)
        prompt = ai_service._build_prompt("java", "OOP", "intermediate")
        
        assert "java" in prompt.lower()
        assert "OOP" in prompt
        assert "Google Java Style Guide" in prompt

    def test_build_prompt_other_language(self, mock_config):
        """测试其他语言"""
        ai_service = AIService(mock_config)
        prompt = ai_service._build_prompt("go", "channels", "advanced")
        
        assert "go" in prompt.lower()
        assert "channels" in prompt
        assert "industry best practices" in prompt


class TestAIServiceAPI:
    """API调用测试"""

    def test_call_api_success(self, mock_config, mock_ai_response):
        """测试API调用成功"""
        ai_service = AIService(mock_config)
        ai_service._load_config()
        
        with patch("requests.post") as mock_post:
            mock_post.return_value = Mock(
                status_code=200,
                json=lambda: mock_ai_response
            )
            
            result = ai_service._call_api("test prompt")
            
            assert result is not None
            mock_post.assert_called_once()

    def test_call_api_timeout(self, mock_config):
        """测试API超时"""
        ai_service = AIService(mock_config)
        ai_service._load_config()
        
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.Timeout("Request timeout")
            
            with pytest.raises(requests.Timeout):
                ai_service._call_api("test prompt")

    def test_call_api_http_error(self, mock_config):
        """测试HTTP错误"""
        ai_service = AIService(mock_config)
        ai_service._load_config()
        
        with patch("requests.post") as mock_post:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("404")
            mock_post.return_value = mock_response
            
            with pytest.raises(requests.HTTPError):
                ai_service._call_api("test prompt")


class TestAIServiceParsing:
    """响应解析测试"""

    def test_parse_response_valid_json(self, mock_config):
        """测试解析有效JSON"""
        ai_service = AIService(mock_config)
        
        response = json.dumps({
            "metadata": {
                "name": "test-demo",
                "folder_name": "test-demo",
                "language": "python",
                "keywords": ["test"],
                "description": "Test demo",
                "difficulty": "beginner",
                "dependencies": {}
            },
            "files": [
                {"path": "README.md", "content": "# Test"}
            ]
        })
        
        result = ai_service._parse_response(response, "python", "test")
        
        assert result is not None
        assert "metadata" in result
        assert "files" in result

    def test_parse_response_json_with_markdown(self, mock_config):
        """测试解析带markdown的JSON"""
        ai_service = AIService(mock_config)
        
        response = """```json
        {
            "metadata": {"name": "test", "folder_name": "test", "language": "python", "keywords": [], "description": "", "difficulty": "beginner", "dependencies": {}},
            "files": []
        }
        ```"""
        
        result = ai_service._parse_response(response, "python", "test")
        
        assert result is not None

    def test_parse_response_invalid_json(self, mock_config):
        """测试解析无效JSON"""
        ai_service = AIService(mock_config)
        
        result = ai_service._parse_response("invalid json{", "python", "test")
        
        assert result is None

    def test_parse_response_missing_fields(self, mock_config):
        """测试缺少必需字段"""
        ai_service = AIService(mock_config)
        
        response = json.dumps({"metadata": {}})  # 缺少files
        
        result = ai_service._parse_response(response, "python", "test")
        
        assert result is None


class TestAIServiceGenerate:
    """Demo生成测试"""

    def test_generate_demo_success(self, mock_config, mock_ai_response):
        """测试生成demo成功"""
        ai_service = AIService(mock_config)
        
        with patch.object(ai_service, "_call_api") as mock_call:
            mock_call.return_value = json.dumps({
                "metadata": {
                    "name": "test-demo",
                    "folder_name": "test-demo",
                    "language": "python",
                    "keywords": ["test"],
                    "description": "Test",
                    "difficulty": "beginner",
                    "dependencies": {}
                },
                "files": [{"path": "README.md", "content": "# Test"}]
            })
            
            result = ai_service.generate_demo("python", "test", "beginner")
            
            assert result is not None
            assert "metadata" in result

    def test_generate_demo_no_api_key(self, mock_config):
        """测试没有API密钥"""
        mock_config.get.side_effect = lambda key, default=None: {
            "ai.api_key": None
        }.get(key, default)
        
        ai_service = AIService(mock_config)
        result = ai_service.generate_demo("python", "test", "beginner")
        
        assert result is None

    def test_generate_demo_retry_success(self, mock_config):
        """测试重试成功"""
        ai_service = AIService(mock_config)
        
        call_count = [0]
        def mock_call_api_with_retry(prompt):
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("API Error")
            return json.dumps({
                "metadata": {
                    "name": "test",
                    "folder_name": "test",
                    "language": "python",
                    "keywords": [],
                    "description": "",
                    "difficulty": "beginner",
                    "dependencies": {}
                },
                "files": []
            })
        
        with patch.object(ai_service, "_call_api", side_effect=mock_call_api_with_retry):
            with patch("time.sleep"):  # Mock sleep加速测试
                result = ai_service.generate_demo("python", "test", "beginner")
                
                assert result is not None
                assert call_count[0] == 3

    def test_generate_demo_all_retries_fail(self, mock_config):
        """测试所有重试都失败"""
        ai_service = AIService(mock_config)
        
        with patch.object(ai_service, "_call_api", side_effect=Exception("API Error")):
            with patch("time.sleep"):
                result = ai_service.generate_demo("python", "test", "beginner")
                
                assert result is None


class TestAIServiceLibraryDetection:
    """库检测功能测试"""

    def test_classify_keyword_as_library(self, mock_config):
        """测试识别为库"""
        ai_service = AIService(mock_config)
        
        with patch.object(ai_service, "_call_api") as mock_call:
            mock_call.return_value = json.dumps({
                "is_library": True,
                "library_name": "numpy",
                "confidence": 0.95
            })
            
            result = ai_service.classify_keyword("python", "numpy")
            
            assert result["is_library"] is True
            assert result["library_name"] == "numpy"
            assert result["confidence"] >= 0.5

    def test_classify_keyword_as_topic(self, mock_config):
        """测试识别为主题"""
        ai_service = AIService(mock_config)
        
        # Mock requests.post返回响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "is_library": False,
                        "confidence": 0.9,
                        "library_name": None,
                        "description": "Standard library module"
                    })
                }
            }]
        }
        
        with patch("requests.post", return_value=mock_response):
            result = ai_service.classify_keyword("python", "logging")
            
            assert result["is_library"] is False
            assert result["confidence"] > 0

    def test_classify_keyword_api_failure(self, mock_config):
        """测试API调用失败，使用启发式判断"""
        ai_service = AIService(mock_config)
        
        with patch.object(ai_service, "_call_api", return_value=None):
            # 失败时会调用_heuristic_classify
            with patch.object(ai_service, "_heuristic_classify") as mock_heuristic:
                mock_heuristic.return_value = {
                    "is_library": False,
                    "confidence": 0.0,
                    "library_name": None,
                    "description": "Heuristic result"
                }
                
                result = ai_service.classify_keyword("python", "test")
                
                # 失败时返回启发式结果
                assert result["is_library"] is False


class TestAIServiceEdgeCases:
    """边界条件测试"""

    def test_generate_with_empty_topic(self, mock_config):
        """测试空主题"""
        ai_service = AIService(mock_config)
        
        with patch.object(ai_service, "_call_api") as mock_call:
            mock_call.return_value = json.dumps({
                "metadata": {
                    "name": "demo",
                    "folder_name": "demo",
                    "language": "python",
                    "keywords": [],
                    "description": "",
                    "difficulty": "beginner",
                    "dependencies": {}
                },
                "files": []
            })
            
            result = ai_service.generate_demo("python", "", "beginner")
            
            # 应该仍能生成
            assert result is not None

    def test_parse_response_with_extra_text(self, mock_config):
        """测试带额外文本的响应"""
        ai_service = AIService(mock_config)
        
        response = """Here is the demo:
        ```json
        {"metadata": {"name": "t", "folder_name": "t", "language": "p", "keywords": [], "description": "", "difficulty": "b", "dependencies": {}}, "files": []}
        ```
        Hope this helps!"""
        
        result = ai_service._parse_response(response, "python", "test")
        
        assert result is not None

    def test_call_api_with_custom_endpoint(self, mock_config):
        """测试自定义API端点"""
        mock_config.get.side_effect = lambda key, default=None: {
            "ai.api_key": "test-key",
            "ai.api_endpoint": "https://custom.api.com/v1/chat",
            "ai.model": "custom-model",
            "ai.temperature": 0.5,
            "ai.max_tokens": 2000,
            "ai.timeout": 30
        }.get(key, default)
        
        ai_service = AIService(mock_config)
        ai_service._load_config()
        
        assert ai_service._api_endpoint == "https://custom.api.com/v1/chat"
        assert ai_service._model == "custom-model"
        assert ai_service._model == "custom-model"

    def test_call_api_with_custom_endpoint(self, mock_config):
        """测试自定义API端点"""
        mock_config.get.side_effect = lambda key, default=None: {
            "ai.api_key": "test-key",
            "ai.api_endpoint": "https://custom.api.com/v1/chat",
            "ai.model": "custom-model",
            "ai.temperature": 0.5,
            "ai.max_tokens": 2000,
            "ai.timeout": 30
        }.get(key, default)
        
        ai_service = AIService(mock_config)
        ai_service._load_config()
        
        assert ai_service._api_endpoint == "https://custom.api.com/v1/chat"
        assert ai_service._model == "custom-model"
        assert ai_service._model == "custom-model"
        assert ai_service._model == "custom-model"
        assert ai_service._model == "custom-model"
