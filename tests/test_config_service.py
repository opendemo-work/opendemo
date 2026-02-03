"""
ConfigService 单元测试
"""

import pytest
from pathlib import Path
from opendemo.services.config_service import ConfigService


class TestConfigService:
    """ConfigService 测试类"""

    def test_init(self):
        """测试初始化"""
        config = ConfigService()
        assert config.global_config_path is not None
        assert config.project_config_path == Path(".opendemo.yaml")

    def test_default_config(self):
        """测试默认配置"""
        config = ConfigService()

        # 验证默认值存在
        assert "output_directory" in ConfigService.DEFAULT_CONFIG
        assert "ai" in ConfigService.DEFAULT_CONFIG
        assert "enable_verification" in ConfigService.DEFAULT_CONFIG

    def test_get_default_value(self):
        """测试获取默认值"""
        config = ConfigService()

        # 测试简单键 - 默认值或配置文件中的值
        output_dir = config.get("output_directory")
        assert output_dir is not None

        # 测试嵌套键 - 确保能正确获取（可能被用户配置覆盖）
        model = config.get("ai.model")
        assert model is not None  # 用户配置可能覆盖默认值

    def test_get_nonexistent_key(self):
        """测试获取不存在的键"""
        config = ConfigService()

        # 不存在的键应返回 None
        value = config.get("nonexistent_key")
        assert value is None

        # 带默认值
        value = config.get("nonexistent_key", "default")
        assert value == "default"

    def test_get_nested_key(self):
        """测试获取嵌套键"""
        config = ConfigService()

        # 测试多层嵌套
        temperature = config.get("ai.temperature")
        assert temperature == 0.7

        # 测试不存在的嵌套键
        value = config.get("ai.nonexistent")
        assert value is None

    def test_load_returns_dict(self):
        """测试 load 返回字典"""
        config = ConfigService()
        loaded = config.load()

        assert isinstance(loaded, dict)
        assert "output_directory" in loaded
        assert "ai" in loaded

    def test_get_all(self):
        """测试获取所有配置"""
        config = ConfigService()
        all_config = config.get_all()

        assert isinstance(all_config, dict)
        # 确保是副本，不是原始对象
        all_config["test"] = "value"
        assert "test" not in config.load()

    def test_validate(self):
        """测试配置验证"""
        config = ConfigService()
        valid, errors = config.validate()

        assert isinstance(valid, bool)
        assert isinstance(errors, list)


class TestConfigServiceMerge:
    """测试配置合并功能"""

    def test_merge_simple(self):
        """测试简单配置合并"""
        config = ConfigService()

        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}

        result = config._merge_config(base, override)

        assert result["a"] == 1
        assert result["b"] == 3
        assert result["c"] == 4

    def test_merge_nested(self):
        """测试嵌套配置合并"""
        config = ConfigService()

        base = {"level1": {"a": 1, "b": 2}}
        override = {"level1": {"b": 3}}

        result = config._merge_config(base, override)

        assert result["level1"]["a"] == 1
        assert result["level1"]["b"] == 3
