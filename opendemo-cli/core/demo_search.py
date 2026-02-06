"""
Demo搜索引擎模块

提供统一的Demo搜索、匹配、排序能力，支持普通Demo和库Demo搜索。
整合了原 search_engine 和 library_manager 的搜索逻辑。
"""

# 修复导入路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any, Optional, Tuple
from core.demo_repository import Demo
from utils.logger import get_logger

logger = get_logger(__name__)


# 匹配权重配置
MATCH_WEIGHTS = {
    "exact_name": 10.0,  # 精确匹配名称
    "prefix_name": 8.0,  # 前缀匹配
    "contain_name": 6.0,  # 包含匹配
    "keyword_match": 5.0,  # 关键字匹配
    "title_match": 4.0,  # 标题匹配
    "description_match": 3.0,  # 描述匹配
}


class DemoSearch:
    """Demo搜索引擎类

    提供统一的搜索能力，支持普通Demo和库功能搜索
    """

    def __init__(self, demo_repository):
        """
        初始化搜索引擎

        Args:
            demo_repository: Demo仓库实例
        """
        self.repository = demo_repository

    # ==================== 普通Demo搜索 ====================

    def search_demos(
        self,
        language: str = None,
        keywords: List[str] = None,
        difficulty: str = None,
        library: str = "all",
    ) -> List[Demo]:
        """
        搜索普通demo

        Args:
            language: 编程语言过滤
            keywords: 关键字列表
            difficulty: 难度级别过滤
            library: 'builtin', 'user' 或 'all'

        Returns:
            匹配的Demo列表
        """
        # 加载所有demo
        all_demos = self.repository.load_all_demos(library, language)

        if not all_demos:
            return []

        # 如果没有任何过滤条件,返回所有demo
        if not keywords and not difficulty:
            return self._sort_demos(all_demos)

        # 过滤demo
        matched_demos = []
        for demo in all_demos:
            score = self._calculate_demo_match_score(demo, keywords, difficulty)
            if score > 0:
                matched_demos.append((demo, score))

        # 按分数排序
        matched_demos.sort(key=lambda x: x[1], reverse=True)

        return [demo for demo, score in matched_demos]

    def find_exact(self, name: str, language: str = None) -> Optional[Demo]:
        """
        精确查找demo

        Args:
            name: demo名称
            language: 语言过滤

        Returns:
            找到的Demo对象,未找到返回None
        """
        all_demos = self.repository.load_all_demos("all", language)

        for demo in all_demos:
            if demo.name.lower() == name.lower():
                return demo

        return None

    def get_all_languages(self) -> List[str]:
        """
        获取所有支持的语言

        Returns:
            语言列表
        """
        all_demos = self.repository.load_all_demos()
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
        all_demos = self.repository.load_all_demos(language=language)
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
        all_demos = self.repository.load_all_demos(language=language)

        stats = {
            "total": len(all_demos),
            "by_language": {},
            "by_difficulty": {"beginner": 0, "intermediate": 0, "advanced": 0},
            "verified": 0,
        }

        for demo in all_demos:
            # 按语言统计
            lang = demo.language.lower()
            stats["by_language"][lang] = stats["by_language"].get(lang, 0) + 1

            # 按难度统计
            difficulty = demo.difficulty.lower()
            if difficulty in stats["by_difficulty"]:
                stats["by_difficulty"][difficulty] += 1

            # 验证统计
            if demo.verified:
                stats["verified"] += 1

        return stats

    # ==================== 库功能搜索 ====================

    def search_library_features(
        self, language: str, library: str, keyword: str
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        搜索库中的功能

        Args:
            language: 编程语言
            library: 库名称
            keyword: 搜索关键字

        Returns:
            匹配的功能列表，每项包含 (feature_dict, score)
        """
        all_features = self.repository.list_library_features(language, library)

        if not all_features:
            return []

        keyword_lower = keyword.lower()
        scored_features = []

        for feature in all_features:
            score = self._calculate_feature_match_score(feature, keyword_lower)
            if score > 0:
                scored_features.append((feature, score))

        # 按分数降序、难度升序、名称升序排序
        scored_features.sort(
            key=lambda x: (
                -x[1],  # 分数降序
                self._difficulty_rank(x[0].get("difficulty", "beginner")),  # 难度升序
                x[0]["name"],  # 名称升序
            )
        )

        return scored_features

    # ==================== 内部辅助方法 ====================

    def _calculate_demo_match_score(
        self, demo: Demo, keywords: List[str] = None, difficulty: str = None
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

    def _calculate_feature_match_score(self, feature: Dict[str, Any], keyword: str) -> float:
        """
        计算功能模块的匹配分数

        Args:
            feature: 功能模块字典
            keyword: 搜索关键字（小写）

        Returns:
            匹配分数
        """
        score = 0.0
        feature_name = feature["name"].lower()

        # 精确匹配：功能名完全等于关键字
        if feature_name == keyword:
            score += MATCH_WEIGHTS["exact_name"]
        # 前缀匹配：功能名以关键字开头
        elif feature_name.startswith(keyword):
            score += MATCH_WEIGHTS["prefix_name"]
        # 包含匹配：功能名包含关键字
        elif keyword in feature_name:
            score += MATCH_WEIGHTS["contain_name"]

        # 关键字匹配：metadata.keywords 中包含关键字
        keywords = feature.get("keywords", [])
        for kw in keywords:
            if keyword in kw.lower():
                score += MATCH_WEIGHTS["keyword_match"]
                break

        # 标题匹配：title 中包含关键字
        title = feature.get("title", "").lower()
        if keyword in title:
            score += MATCH_WEIGHTS["title_match"]

        # 描述匹配：description 中包含关键字
        description = feature.get("description", "").lower()
        if keyword in description:
            score += MATCH_WEIGHTS["description_match"]

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
            " ".join(demo.keywords),
        ]
        return " ".join(parts)

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

    def _difficulty_rank(self, difficulty: str) -> int:
        """
        难度级别排序

        Args:
            difficulty: 难度级别

        Returns:
            排序权重（越小越优先）
        """
        difficulty_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
        return difficulty_map.get(difficulty.lower(), 999)


# 向后兼容的别名
SearchEngine = DemoSearch
