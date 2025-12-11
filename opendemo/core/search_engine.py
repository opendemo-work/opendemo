"""
搜索引擎模块

负责在demo库中搜索和匹配。
"""

from typing import List, Dict, Any, Optional
from opendemo.core.demo_manager import Demo
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


class SearchEngine:
    """搜索引擎类"""
    
    def __init__(self, demo_manager):
        """
        初始化搜索引擎
        
        Args:
            demo_manager: Demo管理器实例
        """
        self.demo_manager = demo_manager
    
    def search(
        self,
        language: str = None,
        keywords: List[str] = None,
        difficulty: str = None,
        library: str = 'all'
    ) -> List[Demo]:
        """
        搜索demo
        
        Args:
            language: 编程语言过滤
            keywords: 关键字列表
            difficulty: 难度级别过滤
            library: 'builtin', 'user' 或 'all'
            
        Returns:
            匹配的Demo列表
        """
        # 加载所有demo
        all_demos = self.demo_manager.load_all_demos(library, language)
        
        if not all_demos:
            return []
        
        # 如果没有任何过滤条件,返回所有demo
        if not keywords and not difficulty:
            return self._sort_demos(all_demos)
        
        # 过滤demo
        matched_demos = []
        for demo in all_demos:
            score = self._calculate_match_score(demo, keywords, difficulty)
            if score > 0:
                matched_demos.append((demo, score))
        
        # 按分数排序
        matched_demos.sort(key=lambda x: x[1], reverse=True)
        
        return [demo for demo, score in matched_demos]
    
    def _calculate_match_score(
        self,
        demo: Demo,
        keywords: List[str] = None,
        difficulty: str = None
    ) -> float:
        """
        计算demo的匹配分数
        
        Args:
            demo: Demo对象
            keywords: 关键字列表
            difficulty: 难度级别
            
        Returns:
            匹配分数,0表示不匹配
        """
        score = 0.0
        
        # 难度匹配(精确匹配)
        if difficulty:
            if demo.difficulty.lower() == difficulty.lower():
                score += 10.0
            else:
                return 0.0  # 难度不匹配则不返回
        
        # 关键字匹配
        if keywords:
            demo_text = self._get_demo_text(demo).lower()
            matched_keywords = 0
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # 在名称中匹配(权重最高)
                if keyword_lower in demo.name.lower():
                    score += 10.0
                    matched_keywords += 1
                
                # 在关键字列表中匹配
                elif any(keyword_lower in kw.lower() for kw in demo.keywords):
                    score += 8.0
                    matched_keywords += 1
                
                # 在描述中匹配
                elif keyword_lower in demo.description.lower():
                    score += 5.0
                    matched_keywords += 1
                
                # 在整体文本中匹配
                elif keyword_lower in demo_text:
                    score += 2.0
                    matched_keywords += 1
            
            # 如果没有任何关键字匹配,返回0
            if matched_keywords == 0:
                return 0.0
            
            # 根据匹配关键字的比例调整分数
            match_ratio = matched_keywords / len(keywords)
            score *= match_ratio
        
        return score
    
    def _get_demo_text(self, demo: Demo) -> str:
        """
        获取demo的所有文本内容(用于搜索)
        
        Args:
            demo: Demo对象
            
        Returns:
            合并的文本
        """
        parts = [
            demo.name,
            demo.description,
            ' '.join(demo.keywords),
        ]
        return ' '.join(parts)
    
    def _sort_demos(self, demos: List[Demo]) -> List[Demo]:
        """
        对demo列表排序(默认排序规则)
        
        Args:
            demos: Demo列表
            
        Returns:
            排序后的Demo列表
        """
        # 按名称排序
        return sorted(demos, key=lambda d: d.name)
    
    def find_exact(self, name: str, language: str = None) -> Optional[Demo]:
        """
        精确查找demo
        
        Args:
            name: demo名称
            language: 语言过滤
            
        Returns:
            找到的Demo对象,未找到返回None
        """
        all_demos = self.demo_manager.load_all_demos('all', language)
        
        for demo in all_demos:
            if demo.name.lower() == name.lower():
                return demo
        
        return None
    
    def find_by_keywords(self, keywords: List[str], language: str = None) -> List[Demo]:
        """
        根据关键字查找demo
        
        Args:
            keywords: 关键字列表
            language: 语言过滤
            
        Returns:
            匹配的Demo列表
        """
        return self.search(language=language, keywords=keywords)
    
    def get_all_languages(self) -> List[str]:
        """
        获取所有支持的语言
        
        Returns:
            语言列表
        """
        all_demos = self.demo_manager.load_all_demos()
        languages = set()
        
        for demo in all_demos:
            languages.add(demo.language.lower())
        
        return sorted(list(languages))
    
    def get_all_keywords(self, language: str = None) -> List[str]:
        """
        获取所有关键字
        
        Args:
            language: 语言过滤
            
        Returns:
            关键字列表
        """
        all_demos = self.demo_manager.load_all_demos(language=language)
        keywords = set()
        
        for demo in all_demos:
            keywords.update(demo.keywords)
        
        return sorted(list(keywords))
    
    def get_statistics(self, language: str = None) -> Dict[str, Any]:
        """
        获取demo库统计信息
        
        Args:
            language: 语言过滤
            
        Returns:
            统计信息字典
        """
        all_demos = self.demo_manager.load_all_demos(language=language)
        
        stats = {
            'total': len(all_demos),
            'by_language': {},
            'by_difficulty': {
                'beginner': 0,
                'intermediate': 0,
                'advanced': 0
            },
            'verified': 0
        }
        
        for demo in all_demos:
            # 按语言统计
            lang = demo.language.lower()
            stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
            
            # 按难度统计
            difficulty = demo.difficulty.lower()
            if difficulty in stats['by_difficulty']:
                stats['by_difficulty'][difficulty] += 1
            
            # 验证统计
            if demo.verified:
                stats['verified'] += 1
        
        return stats
