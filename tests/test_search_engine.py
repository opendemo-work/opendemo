"""
DemoSearch 单元测试
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from opendemo.core.demo_repository import Demo
from opendemo.core.demo_search import DemoSearch


class TestDemoSearch:
    """DemoSearch 类测试"""
    
    def _create_mock_demo(self, name, language, keywords, description, difficulty='beginner', verified=False):
        """创建模拟 Demo 对象"""
        metadata = {
            'name': name,
            'language': language,
            'keywords': keywords,
            'description': description,
            'difficulty': difficulty,
            'verified': verified
        }
        return Demo(Path(f"/test/{name}"), metadata)
    
    def test_init(self):
        """测试初始化"""
        mock_repository = Mock()
        search = DemoSearch(mock_repository)
        
        assert search.repository == mock_repository
    
    def test_search_no_demos(self):
        """测试搜索空库"""
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = []
        
        search = DemoSearch(mock_repository)
        results = search.search_demos(language='python')
        
        assert results == []
    
    def test_search_all_demos(self):
        """测试搜索所有 demo（无过滤条件）"""
        demo1 = self._create_mock_demo('demo1', 'python', ['test'], 'Test demo 1')
        demo2 = self._create_mock_demo('demo2', 'python', ['test'], 'Test demo 2')
        
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = [demo1, demo2]
        
        search = DemoSearch(mock_repository)
        results = search.search_demos()
        
        assert len(results) == 2
    
    def test_search_by_keywords(self):
        """测试按关键字搜索"""
        demo1 = self._create_mock_demo('python-logging', 'python', ['logging', 'debug'], 'Logging demo')
        demo2 = self._create_mock_demo('python-http', 'python', ['http', 'requests'], 'HTTP demo')
        
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = [demo1, demo2]
        
        search = DemoSearch(mock_repository)
        results = search.search_demos(keywords=['logging'])
        
        # 应只匹配 demo1
        assert len(results) == 1
        assert results[0].name == 'python-logging'
    
    def test_search_by_difficulty(self):
        """测试按难度搜索"""
        demo1 = self._create_mock_demo('easy', 'python', ['test'], 'Easy', 'beginner')
        demo2 = self._create_mock_demo('hard', 'python', ['test'], 'Hard', 'advanced')
        
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = [demo1, demo2]
        
        search = DemoSearch(mock_repository)
        results = search.search_demos(difficulty='beginner')
        
        assert len(results) == 1
        assert results[0].name == 'easy'
    
    def test_calculate_match_score_name_match(self):
        """测试名称匹配得分"""
        demo = self._create_mock_demo('python-logging', 'python', [], 'Test')
        
        mock_repository = Mock()
        search = DemoSearch(mock_repository)
        
        score = search._calculate_demo_match_score(demo, keywords=['logging'])
        assert score > 0
    
    def test_calculate_match_score_keyword_match(self):
        """测试关键字匹配得分"""
        demo = self._create_mock_demo('test', 'python', ['logging', 'debug'], 'Test')
        
        mock_repository = Mock()
        search = DemoSearch(mock_repository)
        
        score = search._calculate_demo_match_score(demo, keywords=['logging'])
        assert score > 0
    
    def test_calculate_match_score_no_match(self):
        """测试无匹配得分"""
        demo = self._create_mock_demo('test', 'python', ['other'], 'Test')
        
        mock_repository = Mock()
        search = DemoSearch(mock_repository)
        
        score = search._calculate_demo_match_score(demo, keywords=['nonexistent'])
        assert score == 0
    
    def test_find_exact(self):
        """测试精确查找"""
        demo1 = self._create_mock_demo('target-demo', 'python', [], '')
        demo2 = self._create_mock_demo('other-demo', 'python', [], '')
        
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = [demo1, demo2]
        
        search = DemoSearch(mock_repository)
        result = search.find_exact('target-demo')
        
        assert result is not None
        assert result.name == 'target-demo'
    
    def test_find_exact_not_found(self):
        """测试精确查找未找到"""
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = []
        
        search = DemoSearch(mock_repository)
        result = search.find_exact('nonexistent')
        
        assert result is None
    
    def test_get_all_languages(self):
        """测试获取所有语言"""
        demo1 = self._create_mock_demo('test1', 'python', [], '')
        demo2 = self._create_mock_demo('test2', 'java', [], '')
        demo3 = self._create_mock_demo('test3', 'python', [], '')
        
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = [demo1, demo2, demo3]
        
        search = DemoSearch(mock_repository)
        languages = search.get_all_languages()
        
        assert sorted(languages) == ['java', 'python']
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        demo1 = self._create_mock_demo('test1', 'python', [], '', 'beginner', True)
        demo2 = self._create_mock_demo('test2', 'java', [], '', 'advanced', False)
        
        mock_repository = Mock()
        mock_repository.load_all_demos.return_value = [demo1, demo2]
        
        search = DemoSearch(mock_repository)
        stats = search.get_statistics()
        
        assert stats['total'] == 2
        assert stats['verified'] == 1
        assert stats['by_language']['python'] == 1
        assert stats['by_language']['java'] == 1
        assert stats['by_difficulty']['beginner'] == 1
        assert stats['by_difficulty']['advanced'] == 1


class TestDemoSearchSorting:
    """测试搜索结果排序"""
    
    def _create_mock_demo(self, name, language='python'):
        """创建模拟 Demo"""
        return Demo(Path(f"/test/{name}"), {'name': name, 'language': language})
    
    def test_sort_demos_by_name(self):
        """测试按名称排序"""
        demo_c = self._create_mock_demo('c-demo')
        demo_a = self._create_mock_demo('a-demo')
        demo_b = self._create_mock_demo('b-demo')
        
        mock_repository = Mock()
        search = DemoSearch(mock_repository)
        
        sorted_demos = search._sort_demos([demo_c, demo_a, demo_b])
        
        names = [d.name for d in sorted_demos]
        assert names == ['a-demo', 'b-demo', 'c-demo']
