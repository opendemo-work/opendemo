"""
ReadmeUpdater单元测试
"""

from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from opendemo.core.readme_updater import ReadmeUpdater


class TestReadmeUpdater:
    """ReadmeUpdater测试类"""

    def test_init(self):
        """测试初始化"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        assert updater.output_dir == output_dir
        assert updater.readme_path == readme_path

    def test_collect_stats(self):
        """测试收集统计信息"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "iterdir") as mock_iterdir:
                # 模拟demo目录结构
                mock_python_dir = MagicMock(spec=Path)
                mock_python_dir.is_dir.return_value = True
                mock_python_dir.name = "python"
                
                mock_demo1 = MagicMock(spec=Path)
                mock_demo1.is_dir.return_value = True
                mock_demo1.name = "test-demo"
                
                mock_python_dir.iterdir.return_value = [mock_demo1]
                mock_iterdir.return_value = [mock_python_dir]
                
                stats = updater.collect_stats()
                
                assert isinstance(stats, dict)

    def test_calculate_totals(self):
        """测试计算总计"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        stats = {
            "python": {"base": 10, "libraries": {"numpy": 5}},
            "go": {"base": 8, "libraries": {}},
        }
        
        totals = updater.calculate_totals(stats)
        
        assert totals["base_total"] == 18
        assert totals["lib_total"] == 5
        assert totals["grand_total"] == 23

    def test_generate_stats_table(self):
        """测试生成统计表格"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        stats = {
            "python": {"base": 10, "libraries": {"numpy": 5}},
            "go": {"base": 8, "libraries": {}},
        }
        
        table = updater.generate_stats_table(stats)
        
        assert "## 📊 Demo统计" in table
        assert "python" in table.lower()
        assert "10" in table

    def test_update_badge(self):
        """测试更新徽章"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        content = "[![Demos](https://img.shields.io/badge/Demos-100-orange.svg)]"
        updated = updater.update_badge(content, 150)
        
        assert "150" in updated
        assert "100" not in updated

    def test_update_stats_section(self):
        """测试更新统计部分"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        content = """## 📊 Demo统计

| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| **总计** | **100** | **50** | **150** | ✅ |"""
        
        new_stats = "## 📊 Demo统计\n\nNew content"
        updated = updater.update_stats_section(content, new_stats)
        
        assert "New content" in updated

    def test_update_success(self):
        """测试成功更新README"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(Path, "exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="test content")):
                with patch.object(updater, "collect_stats", return_value={}):
                    with patch.object(updater, "generate_stats_table", return_value="table"):
                        result = updater.update()
        
        assert result is True

    def test_update_no_readme(self):
        """测试README不存在"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(Path, "exists", return_value=False):
            result = updater.update()
        
        assert result is False

    def test_get_summary(self):
        """测试获取摘要"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(updater, "collect_stats") as mock_collect:
            mock_collect.return_value = {
                "python": {"base": 10, "libraries": {"numpy": 5}},
                "go": {"base": 8, "libraries": {}},
            }
            
            summary = updater.get_summary()
            
            assert "23" in summary
            assert "demo" in summary.lower()
"""
ReadmeUpdater单元测试
"""

from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from opendemo.core.readme_updater import ReadmeUpdater


class TestReadmeUpdater:
    """ReadmeUpdater测试类"""

    def test_init(self):
        """测试初始化"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        assert updater.output_dir == output_dir
        assert updater.readme_path == readme_path

    def test_collect_stats(self):
        """测试收集统计信息"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "iterdir") as mock_iterdir:
                # 模拟demo目录结构
                mock_python_dir = MagicMock(spec=Path)
                mock_python_dir.is_dir.return_value = True
                mock_python_dir.name = "python"
                
                mock_demo1 = MagicMock(spec=Path)
                mock_demo1.is_dir.return_value = True
                mock_demo1.name = "test-demo"
                
                mock_python_dir.iterdir.return_value = [mock_demo1]
                mock_iterdir.return_value = [mock_python_dir]
                
                stats = updater.collect_stats()
                
                assert isinstance(stats, dict)

    def test_calculate_totals(self):
        """测试计算总计"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        stats = {
            "python": {"base": 10, "libraries": {"numpy": 5}},
            "go": {"base": 8, "libraries": {}},
        }
        
        totals = updater.calculate_totals(stats)
        
        assert totals["base_total"] == 18
        assert totals["lib_total"] == 5
        assert totals["grand_total"] == 23

    def test_generate_stats_table(self):
        """测试生成统计表格"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        stats = {
            "python": {"base": 10, "libraries": {"numpy": 5}},
            "go": {"base": 8, "libraries": {}},
        }
        
        table = updater.generate_stats_table(stats)
        
        assert "## 📊 Demo统计" in table
        assert "python" in table.lower()
        assert "10" in table

    def test_update_badge(self):
        """测试更新徽章"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        content = "[![Demos](https://img.shields.io/badge/Demos-100-orange.svg)]"
        updated = updater.update_badge(content, 150)
        
        assert "150" in updated
        assert "100" not in updated

    def test_update_stats_section(self):
        """测试更新统计部分"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        content = """## 📊 Demo统计

| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| **总计** | **100** | **50** | **150** | ✅ |"""
        
        new_stats = "## 📊 Demo统计\n\nNew content"
        updated = updater.update_stats_section(content, new_stats)
        
        assert "New content" in updated

    def test_update_success(self):
        """测试成功更新README"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(Path, "exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="test content")):
                with patch.object(updater, "collect_stats", return_value={}):
                    with patch.object(updater, "generate_stats_table", return_value="table"):
                        result = updater.update()
        
        assert result is True

    def test_update_no_readme(self):
        """测试README不存在"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(Path, "exists", return_value=False):
            result = updater.update()
        
        assert result is False

    def test_get_summary(self):
        """测试获取摘要"""
        output_dir = Path("/test/output")
        readme_path = Path("/test/README.md")
        
        updater = ReadmeUpdater(output_dir, readme_path)
        
        with patch.object(updater, "collect_stats") as mock_collect:
            mock_collect.return_value = {
                "python": {"base": 10, "libraries": {"numpy": 5}},
                "go": {"base": 8, "libraries": {}},
            }
            
            summary = updater.get_summary()
            
            assert "23" in summary
            assert "demo" in summary.lower()
