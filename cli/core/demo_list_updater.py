"""
Demo List 自动更新模块

负责在 CLI 操作后自动更新 demo-list.md 文件。
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from opendemo.utils.logger import get_logger

# 支持的语言列表
SUPPORTED_LANGUAGES = ["python", "go", "nodejs", "kubernetes"]

# 语言显示配置
LANGUAGE_CONFIG = {
    "python": {"emoji": "🐍", "name": "Python", "order": 1},
    "go": {"emoji": "🐹", "name": "Go", "order": 2},
    "nodejs": {"emoji": "🟢", "name": "Node.js", "order": 3},
    "kubernetes": {"emoji": "⎈", "name": "Kubernetes", "order": 4},
}


class DemoListUpdater:
    """Demo List 更新器"""

    def __init__(self, output_dir: Path, demo_list_path: Path, mapping_path: Optional[Path] = None):
        """
        初始化更新器

        Args:
            output_dir: opendemo_output目录路径
            demo_list_path: demo-list.md文件路径
            mapping_path: demo_mapping.json文件路径
        """
        self.output_dir = output_dir
        self.demo_list_path = demo_list_path
        data_path = Path(__file__).parent.parent.parent / "data" / "demo_mapping.json"
        self.mapping_path = mapping_path or data_path
        self.logger = get_logger(__name__)

    def load_mapping(self) -> Dict[str, List[Dict[str, Any]]]:
        """加载 demo_mapping.json"""
        if not self.mapping_path.exists():
            return {}

        try:
            with open(self.mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load mapping: {e}")
            return {}

    def scan_demos(self, language: str) -> List[Dict[str, Any]]:
        """
        扫描指定语言的所有 demo

        Args:
            language: 语言名称

        Returns:
            demo 信息列表
        """
        demos = []
        lang_dir = self.output_dir / language.lower()

        if not lang_dir.exists():
            return demos

        # 对 kubernetes 特殊处理
        if language.lower() == "kubernetes":
            for tool_dir in lang_dir.iterdir():
                if tool_dir.is_dir():
                    for demo_dir in tool_dir.iterdir():
                        if demo_dir.is_dir():
                            demo_info = self._extract_demo_info(demo_dir, language, tool_dir.name)
                            if demo_info:
                                demos.append(demo_info)
        else:
            for item in lang_dir.iterdir():
                if item.is_dir():
                    if item.name == "libraries":
                        # 处理第三方库 demo
                        for lib_dir in item.iterdir():
                            if lib_dir.is_dir():
                                for demo_dir in lib_dir.iterdir():
                                    if demo_dir.is_dir():
                                        demo_info = self._extract_demo_info(
                                            demo_dir, language, lib_dir.name
                                        )
                                        if demo_info:
                                            demos.append(demo_info)
                    else:
                        demo_info = self._extract_demo_info(item, language)
                        if demo_info:
                            demos.append(demo_info)

        return demos

    def _extract_demo_info(
        self, demo_dir: Path, language: str, category: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        提取 demo 信息

        Args:
            demo_dir: demo 目录
            language: 语言
            category: 分类（库名或工具名）

        Returns:
            demo 信息字典
        """
        metadata_file = demo_dir / "metadata.json"

        info = {
            "folder": demo_dir.name,
            "name": demo_dir.name,
            "description": "",
            "category": category,
            "language": language,
            "path": str(demo_dir.relative_to(self.output_dir)),
        }

        if metadata_file.exists():
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                info["name"] = metadata.get("name", demo_dir.name)
                info["description"] = metadata.get("description", "")
                info["keywords"] = metadata.get("keywords", [])
                info["difficulty"] = metadata.get("difficulty", "beginner")
            except Exception:
                pass
        return info

    def collect_all_demos(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        收集所有语言的 demo

        Returns:
            结构化的 demo 数据
            {
                'python': {
                    'base': [demo1, demo2, ...],
                    'libraries': {'numpy': [demo1, ...]}
                },
                ...
            }
        """
        all_demos = {}
        for lang in SUPPORTED_LANGUAGES:
            demos = self.scan_demos(lang)

            base_demos = []
            libraries = {}
            for demo in demos:
                category = demo.get("category")
                if category:
                    if category not in libraries:
                        libraries[category] = []
                    libraries[category].append(demo)
                else:
                    base_demos.append(demo)

            # 按名称排序
            base_demos.sort(key=lambda x: x["name"].lower())
            for lib_name in libraries:
                libraries[lib_name].sort(key=lambda x: x["name"].lower())

            all_demos[lang] = {"base": base_demos, "libraries": libraries}
        return all_demos

    def generate_markdown(self) -> str:
        """
        生成 demo-list.md 内容

        Returns:
            Markdown 格式的内容
        """
        all_demos = self.collect_all_demos()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            "# Demo 列表",
            "",
            f"> 自动生成于 {now}",
            "",
            "本文件记录了所有可用的 Demo，由 CLI 操作后自动更新。",
            "",
        ]

        # 统计摘要
        total_count = 0
        summary_lines = [
            "## 📊 统计摘要",
            "",
            "| 语言 | 基础 Demo | 第三方库/工具 | 总计 |",
            "|------|----------|--------------|------|",
        ]

        for lang in SUPPORTED_LANGUAGES:
            config = LANGUAGE_CONFIG.get(lang, {"emoji": "", "name": lang})
            data = all_demos.get(lang, {"base": [], "libraries": {}})

            base_count = len(data["base"])
            lib_count = sum(len(demos) for demos in data["libraries"].values())
            lang_total = base_count + lib_count
            total_count += lang_total

            summary_lines.append(
                f"| {config['emoji']} {config['name']} | {base_count} | {lib_count} | {lang_total} |"
            )

        summary_lines.append(f"| **总计** | - | - | **{total_count}** |")
        lines.extend(summary_lines)
        lines.append("")
        # 目录
        lines.extend(
            [
                "## 📑 目录",
                "",
            ]
        )

        for lang in SUPPORTED_LANGUAGES:
            config = LANGUAGE_CONFIG.get(lang, {"emoji": "", "name": lang})
            data = all_demos.get(lang, {"base": [], "libraries": {}})
            if data["base"] or data["libraries"]:
                lines.append(f"- [{config['emoji']} {config['name']}](#{lang.lower()})")
                if data["libraries"]:
                    for lib_name in sorted(data["libraries"].keys()):
                        lines.append(f"  - [{lib_name}](#{lang.lower()}-{lib_name.lower()})")
        lines.append("")

        # 各语言详细列表
        for lang in SUPPORTED_LANGUAGES:
            config = LANGUAGE_CONFIG.get(lang, {"emoji": "", "name": lang})
            data = all_demos.get(lang, {"base": [], "libraries": {}})

            if not data["base"] and not data["libraries"]:
                continue

            lines.extend(
                [
                    f"## {config['emoji']} {config['name']}",
                    f'<a name="{lang.lower()}"></a>',
                    "",
                ]
            )

            # 基础 Demo
            if data["base"]:
                lines.append("### 基础 Demo")
                lines.append("")
                lines.append("| # | 名称 | 描述 | 目录 |")
                lines.append("|---|------|------|------|")

                for i, demo in enumerate(data["base"], 1):
                    name = demo.get("name", demo["folder"])
                    desc = demo.get("description", "-")
                    if len(desc) > 60:
                        desc = desc[:57] + "..."
                    folder = demo["folder"]
                    lines.append(f"| {i} | {name} | {desc} | `{folder}` |")

                lines.append("")

            # 第三方库/工具 Demo
            if data["libraries"]:
                category_name = "工具" if lang.lower() == "kubernetes" else "第三方库"
                lines.append(f"### {category_name} Demo")
                lines.append("")

                for lib_name in sorted(data["libraries"].keys()):
                    lib_demos = data["libraries"][lib_name]
                    lines.append(f"#### {lib_name}")
                    lines.append(f'<a name="{lang.lower()}-{lib_name.lower()}"></a>')
                    lines.append("")
                    lines.append("| # | 名称 | 描述 | 目录 |")
                    lines.append("|---|------|------|------|")

                    for i, demo in enumerate(lib_demos, 1):
                        name = demo.get("name", demo["folder"])
                        desc = demo.get("description", "-")
                        if len(desc) > 60:
                            desc = desc[:57] + "..."
                        folder = demo["folder"]
                        lines.append(f"| {i} | {name} | {desc} | `{folder}` |")

                    lines.append("")

        # 页脚
        lines.extend(
            [
                "---",
                "",
                f"*本文件由 opendemo CLI 自动生成，最后更新: {now}*",
            ]
        )

        return "\n".join(lines)

    def update(self) -> bool:
        """
        执行 demo-list.md 更新

        Returns:
            是否成功更新
        """
        try:
            content = self.generate_markdown()

            with open(self.demo_list_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.logger.info(f"demo-list.md updated at {self.demo_list_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update demo-list.md: {e}")
            return False

    def get_summary(self) -> str:
        """
        获取统计摘要

        Returns:
            摘要字符串
        """
        all_demos = self.collect_all_demos()

        parts = []
        total = 0
        for lang in SUPPORTED_LANGUAGES:
            config = LANGUAGE_CONFIG.get(lang, {"name": lang})
            data = all_demos.get(lang, {"base": [], "libraries": {}})
            count = len(data["base"]) + sum(len(d) for d in data["libraries"].values())
            if count > 0:
                parts.append(f"{config['name']}: {count}")
            total += count

        return f"总计 {total} 个 demo ({', '.join(parts)})"


def update_demo_list(output_dir: Path, demo_list_path: Path) -> tuple:
    """
    更新 demo-list.md 的便捷函数

    Args:
        output_dir: opendemo_output 目录
        demo_list_path: demo-list.md 路径

    Returns:
        (成功与否, 摘要信息)
    """
    updater = DemoListUpdater(output_dir, demo_list_path)
    success = updater.update()
    summary = updater.get_summary()
    return success, summary
