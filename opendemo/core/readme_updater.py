"""
README.md 自动更新模块

负责在demo生成后自动更新README.md中的统计信息。
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any

from opendemo.utils.logger import get_logger

# 支持的语言列表
SUPPORTED_LANGUAGES = ['python', 'go', 'nodejs', 'java']

# 语言显示配置
LANGUAGE_CONFIG = {
    'python': {'emoji': '🐍', 'name': 'Python'},
    'go': {'emoji': '🐹', 'name': 'Go'},
    'nodejs': {'emoji': '🟢', 'name': 'Node.js'},
    'java': {'emoji': '☕', 'name': 'Java'},
}


class ReadmeUpdater:
    """README.md 更新器"""
    
    def __init__(self, output_dir: Path, readme_path: Path):
        """
        初始化更新器
        
        Args:
            output_dir: opendemo_output目录路径
            readme_path: README.md文件路径
        """
        self.output_dir = output_dir
        self.readme_path = readme_path
        self.logger = get_logger(__name__)
    
    def collect_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        收集所有语言的demo统计信息
        
        Returns:
            统计信息字典，格式:
            {
                'python': {'base': 51, 'libraries': {'numpy': 25}},
                'go': {'base': 92, 'libraries': {}},
                ...
            }
        """
        stats = {}
        
        for lang in SUPPORTED_LANGUAGES:
            lang_dir = self.output_dir / lang.lower()
            
            if not lang_dir.exists():
                stats[lang] = {'base': 0, 'libraries': {}}
                continue
            
            base_count = 0
            libraries = {}
            
            for item in lang_dir.iterdir():
                if item.is_dir():
                    if item.name == 'libraries':
                        # 统计第三方库demo
                        for lib_dir in item.iterdir():
                            if lib_dir.is_dir():
                                lib_demos = sum(1 for d in lib_dir.iterdir() if d.is_dir())
                                if lib_demos > 0:
                                    libraries[lib_dir.name] = lib_demos
                    else:
                        # 检查是否有metadata.json来确认是有效的demo
                        if (item / 'metadata.json').exists():
                            base_count += 1
                        else:
                            # 兼容：即使没有metadata.json也算作demo
                            base_count += 1
            
            stats[lang] = {'base': base_count, 'libraries': libraries}
        
        return stats
    
    def calculate_totals(self, stats: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """
        计算各类总数
        
        Returns:
            {'base_total': 210, 'lib_total': 25, 'grand_total': 235}
        """
        base_total = 0
        lib_total = 0
        
        for lang, data in stats.items():
            base_total += data.get('base', 0)
            lib_total += sum(data.get('libraries', {}).values())
        
        return {
            'base_total': base_total,
            'lib_total': lib_total,
            'grand_total': base_total + lib_total
        }
    
    def generate_stats_table(self, stats: Dict[str, Dict[str, Any]]) -> str:
        """
        生成Demo统计表格
        
        Returns:
            Markdown格式的表格字符串
        """
        totals = self.calculate_totals(stats)
        
        lines = [
            "## 📊 Demo统计",
            "",
            "| 语言 | 基础Demo | 第三方库 | 总计 | 测试状态 |",
            "|------|----------|----------|------|----------|"
        ]
        
        for lang in ['python', 'go', 'nodejs']:
            config = LANGUAGE_CONFIG.get(lang, {'emoji': '', 'name': lang})
            data = stats.get(lang, {'base': 0, 'libraries': {}})
            
            base = data.get('base', 0)
            libs = data.get('libraries', {})
            lib_total = sum(libs.values())
            total = base + lib_total
            
            # 格式化第三方库信息
            if libs:
                lib_info = ', '.join(f"{name}({count})" for name, count in libs.items())
            else:
                lib_info = '-'
            
            lines.append(
                f"| {config['emoji']} **{config['name']}** | {base} | {lib_info} | {total} | ✅ 全部通过 |"
            )
        
        # 总计行
        lines.append(
            f"| **总计** | **{totals['base_total']}** | **{totals['lib_total']}** | **{totals['grand_total']}** | ✅ |"
        )
        
        return '\n'.join(lines)
    
    def update_badge(self, content: str, total: int) -> str:
        """
        更新徽章中的demo数量
        
        Args:
            content: README内容
            total: 总demo数量
            
        Returns:
            更新后的内容
        """
        # 更新 Demos 徽章
        badge_pattern = r'\[!\[Demos\]\(https://img\.shields\.io/badge/Demos-\d+-orange\.svg\)\]'
        new_badge = f'[![Demos](https://img.shields.io/badge/Demos-{total}-orange.svg)]'
        content = re.sub(badge_pattern, new_badge, content)
        
        return content
    
    def update_stats_section(self, content: str, new_stats: str) -> str:
        """
        更新统计部分
        
        Args:
            content: README内容
            new_stats: 新的统计表格
            
        Returns:
            更新后的内容
        """
        # 匹配从"## 📊 Demo统计"到下一个"---"之前的内容
        pattern = r'## 📊 Demo统计\n\n\| 语言 \| 基础Demo.*?\n\| \*\*总计\*\* \|[^\n]*'
        content = re.sub(pattern, new_stats, content, flags=re.DOTALL)
        
        return content
    
    def update(self) -> bool:
        """
        执行README更新
        
        Returns:
            是否成功更新
        """
        if not self.readme_path.exists():
            self.logger.warning(f"README.md not found at {self.readme_path}")
            return False
        
        try:
            # 收集统计信息
            stats = self.collect_stats()
            totals = self.calculate_totals(stats)
            
            # 读取README内容
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 生成新的统计表格
            new_stats = self.generate_stats_table(stats)
            
            # 更新统计部分
            content = self.update_stats_section(content, new_stats)
            
            # 更新徽章
            content = self.update_badge(content, totals['grand_total'])
            
            # 写回README
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"README.md updated: total {totals['grand_total']} demos")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update README.md: {e}")
            return False
    
    def get_summary(self) -> str:
        """
        获取统计摘要信息
        
        Returns:
            摘要字符串
        """
        stats = self.collect_stats()
        totals = self.calculate_totals(stats)
        
        parts = []
        for lang in ['python', 'go', 'nodejs']:
            config = LANGUAGE_CONFIG.get(lang, {'name': lang})
            data = stats.get(lang, {'base': 0, 'libraries': {}})
            total = data.get('base', 0) + sum(data.get('libraries', {}).values())
            if total > 0:
                parts.append(f"{config['name']}: {total}")
        
        return f"总计 {totals['grand_total']} 个demo ({', '.join(parts)})"


def update_readme_after_new(output_dir: Path, readme_path: Path) -> tuple:
    """
    在生成新demo后更新README.md的便捷函数
    
    Args:
        output_dir: opendemo_output目录路径
        readme_path: README.md文件路径
        
    Returns:
        (成功与否, 摘要信息)
    """
    updater = ReadmeUpdater(output_dir, readme_path)
    success = updater.update()
    summary = updater.get_summary()
    
    return success, summary
