#!/usr/bin/env python3
"""
OpenDemo 命令风险自动标注脚本（基于行解析的稳健版本）

为 README.md 中的 bash/sh/shell/powershell/cmd 代码块以及 .sh 脚本添加风险等级徽章和说明。

用法：
    python scripts/security/annotate_command_risks.py [--dry-run] [--stacks STACK [STACK ...]]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
RULES_PATH = PROJECT_ROOT / "configs" / "command-risk-rules.json"

# 需要扫描的代码块语言标识
CODE_BLOCK_LANGS = {"bash", "sh", "shell", "powershell", "cmd", "batch"}

# 忽略目录
IGNORE_DIRS = {
    ".git", ".github", ".venv", "venv", "node_modules", "__pycache__",
    ".kilo", ".claude", ".lingma", ".qoder", "opendemo-wiki", "opendemo-cli",
}


def load_rules(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_patterns(rules: Dict) -> Dict[str, List[re.Pattern]]:
    compiled = {}
    for level, cfg in rules["levels"].items():
        compiled[level] = [re.compile(p, re.IGNORECASE) for p in cfg["patterns"]]
    return compiled


def classify_risk(content: str, compiled: Dict[str, List[re.Pattern]], rules: Dict) -> str:
    """按高 > 中 > 低优先级匹配风险等级。

    低风险规则仅对非注释、非空白的实际命令行生效，避免注释中的 `#`
    或示例输出误触发低风险，从而低估真实风险。
    """
    # 高、中风险直接对全文匹配
    for level in ("high", "medium"):
        for pattern in compiled[level]:
            if pattern.search(content):
                return level

    # 低风险只检查实际命令行
    command_lines = [
        ln for ln in content.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if not command_lines:
        # 块内全是注释或空行，视为低风险说明性内容
        return "low"

    for line in command_lines:
        for pattern in compiled["low"]:
            if pattern.search(line):
                return "low"

    # 存在实际命令但未命中任何规则，保守按中风险处理
    return "medium"


def parse_code_blocks(lines: List[str]) -> List[Dict]:
    """基于行解析提取 fenced code block。

    返回每个块的字典，包含：
    - start_line:  opening fence 所在行号（0-based）
    - end_line:    closing fence 所在行号（0-based）
    - indent:      opening fence 的行首缩进
    - lang:        代码块语言
    - body_lines:  块内内容（原始缩进保留）
    """
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(?P<indent>\s*)(?P<fence>`{3,}|~{3,})\s*(?P<lang>\w+)?\s*$", line)
        if not m:
            i += 1
            continue
        lang = (m.group("lang") or "").lower().strip()
        if lang not in CODE_BLOCK_LANGS:
            i += 1
            continue

        indent = m.group("indent")
        fence = m.group("fence")
        start = i
        body_lines = []
        j = i + 1
        while j < len(lines):
            if re.match(re.escape(indent) + re.escape(fence) + r"\s*$", lines[j]):
                break
            body_lines.append(lines[j])
            j += 1

        if j >= len(lines):
            # 未找到闭合 fence，跳过
            i += 1
            continue

        blocks.append({
            "start_line": start,
            "end_line": j,
            "indent": indent,
            "lang": lang,
            "body_lines": body_lines,
        })
        i = j + 1
    return blocks


def already_annotated(lines: List[str], block_start: int) -> bool:
    """检查代码块前是否已经存在风险徽章。"""
    before = lines[max(0, block_start - 5):block_start]
    for line in before:
        if re.search(r"[🔴🟡🟢]\s*(高风险|中风险|低风险)", line):
            return True
    return False


def make_risk_badge(level: str, rules: Dict) -> str:
    cfg = rules["levels"][level]
    return f"{cfg['badge']}：{cfg['description']}"


def make_warning_block(level: str, rules: Dict) -> str:
    cfg = rules["levels"][level]
    notes = cfg.get("notes", [])
    if not notes:
        return ""
    lines = ["> ⚠️ 生产安全提示："]
    for note in notes:
        lines.append(f"> - {note}")
    return "\n".join(lines)


def detect_newline(text: str) -> str:
    """检测原始文本使用的换行符，优先返回 CRLF 如果存在。"""
    return "\r\n" if "\r\n" in text else "\n"


def annotate_readme(readme_path: Path, compiled: Dict[str, List[re.Pattern]], rules: Dict, dry_run: bool) -> Tuple[int, Dict[str, int]]:
    """标注单个 README，返回 (修改块数, 各级别统计)."""
    # 使用 newline="" 保留原始换行符（CRLF/LF）
    with open(readme_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        text = f.read()
    newline = detect_newline(text)
    lines = text.splitlines()
    blocks = parse_code_blocks(lines)

    stats = defaultdict(int)
    modified = 0

    # 从后往前插入，避免行号偏移
    for block in reversed(blocks):
        if already_annotated(lines, block["start_line"]):
            continue

        body = "\n".join(block["body_lines"])
        if not body.strip():
            continue

        level = classify_risk(body, compiled, rules)
        stats[level] += 1

        indent = block["indent"]
        badge = make_risk_badge(level, rules)
        warning = make_warning_block(level, rules)

        if level == "low":
            insert_lines = [f"{indent}{badge}"]
        else:
            if warning:
                indented_warning = [f"{indent}{ln}" for ln in warning.splitlines()]
                insert_lines = [f"{indent}{badge}"] + indented_warning
            else:
                insert_lines = [f"{indent}{badge}"]

        # 插入到 opening fence 之前
        pos = block["start_line"]
        for ln in reversed(insert_lines):
            lines.insert(pos, ln)
        modified += 1

    if modified and not dry_run:
        new_text = newline.join(lines)
        if text.endswith(newline):
            new_text += newline
        with open(readme_path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)

    return modified, dict(stats)


def annotate_script(script_path: Path, compiled: Dict[str, List[re.Pattern]], rules: Dict, dry_run: bool) -> bool:
    """为 .sh 脚本添加安全头，返回是否修改。"""
    # 使用 newline="" 保留原始换行符（CRLF/LF）
    with open(script_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        text = f.read()
    newline = detect_newline(text)
    lines = text.splitlines()
    if not lines:
        return False

    # 检查是否已有安全头
    if "风险等级" in text[:500] or "生产安全提示" in text[:500]:
        return False

    shebang = lines[0] if lines[0].startswith("#!") else "#!/bin/bash"
    body_start = 1 if lines[0].startswith("#!") else 0

    level = classify_risk(text, compiled, rules)
    cfg = rules["levels"][level]
    notes = cfg.get("notes", [])

    header_lines = [shebang]
    header_lines.append(f"# 风险等级：{cfg['badge']}")
    header_lines.append(f"# 说明：{cfg['description']}")
    if notes:
        header_lines.append("# 生产安全提示：")
        for note in notes:
            header_lines.append(f"#   - {note}")
    header_lines.append("")

    new_text = newline.join(header_lines) + newline + newline.join(lines[body_start:])
    if not new_text.endswith(newline):
        new_text += newline

    if not dry_run:
        with open(script_path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)

    return True


def should_ignore(path: Path) -> bool:
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
        if part.startswith(".") and part not in {".github"}:
            if part != ".github":
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description="OpenDemo 命令风险自动标注")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不写入文件")
    parser.add_argument("--stacks", nargs="+", help="只处理指定技术栈")
    parser.add_argument("--report", default="docs/reports/COMMAND-RISK-ASSESSMENT-REPORT.md", help="报告输出路径")
    args = parser.parse_args()

    rules = load_rules(RULES_PATH)
    compiled = compile_patterns(rules)

    # 收集目标
    readmes: List[Path] = []
    scripts: List[Path] = []

    search_roots = [PROJECT_ROOT / s for s in args.stacks] if args.stacks else [PROJECT_ROOT]

    for root in search_roots:
        if not root.exists():
            print(f"⚠️ 目录不存在: {root}")
            continue
        for path in root.rglob("*"):
            if should_ignore(path):
                continue
            if path.is_file():
                if path.name == "README.md":
                    readmes.append(path)
                elif path.suffix == ".sh":
                    scripts.append(path)

    readmes = sorted(set(readmes))
    scripts = sorted(set(scripts))

    print(f"发现 README.md: {len(readmes)} 个")
    print(f"发现 .sh 脚本: {len(scripts)} 个")
    print(f"模式: {'预览 (dry-run)' if args.dry_run else '写入'}")
    print("=" * 50)

    total_block_stats = defaultdict(int)
    readme_modified_count = 0
    readme_block_modified_count = 0

    for readme in readmes:
        modified, stats = annotate_readme(readme, compiled, rules, args.dry_run)
        if modified:
            readme_modified_count += 1
            readme_block_modified_count += modified
            for level, count in stats.items():
                total_block_stats[level] += count

    script_modified_count = 0
    script_level_stats = defaultdict(int)

    for script in scripts:
        if annotate_script(script, compiled, rules, args.dry_run):
            script_modified_count += 1
            level = classify_risk(script.read_text(encoding="utf-8", errors="ignore"), compiled, rules)
            script_level_stats[level] += 1

    print(f"\nREADME 标注：")
    print(f"  涉及文件数: {readme_modified_count}")
    print(f"  涉及代码块数: {readme_block_modified_count}")
    for level in ("high", "medium", "low"):
        print(f"    {rules['levels'][level]['badge']}: {total_block_stats.get(level, 0)}")

    print(f"\n脚本标注：")
    print(f"  涉及脚本数: {script_modified_count}")
    for level in ("high", "medium", "low"):
        print(f"    {rules['levels'][level]['badge']}: {script_level_stats.get(level, 0)}")

    # 生成报告
    report_lines = [
        "# OpenDemo 命令风险评估标注报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**运行模式**: {'预览 (dry-run)' if args.dry_run else '写入'}",
        "",
        "## 汇总",
        "",
        f"- README.md 文件总数: {len(readmes)}",
        f"- 被修改的 README: {readme_modified_count}",
        f"- 被标注的代码块: {readme_block_modified_count}",
        f"- .sh 脚本总数: {len(scripts)}",
        f"- 被修改的脚本: {script_modified_count}",
        "",
        "## 风险等级分布（代码块）",
        "",
        "| 风险等级 | 数量 |",
        "|----------|------|",
    ]
    for level in ("high", "medium", "low"):
        badge = rules["levels"][level]["badge"]
        report_lines.append(f"| {badge} | {total_block_stats.get(level, 0)} |")

    report_lines.extend([
        "",
        "## 风险等级分布（脚本）",
        "",
        "| 风险等级 | 数量 |",
        "|----------|------|",
    ])
    for level in ("high", "medium", "low"):
        badge = rules["levels"][level]["badge"]
        report_lines.append(f"| {badge} | {script_level_stats.get(level, 0)} |")

    report_lines.extend([
        "",
        "## 规则文件",
        "",
        "- `configs/command-risk-rules.json`",
        "",
        "## 说明",
        "",
        "本次标注仅增加安全提示文案，未修改任何命令的实际逻辑。",
        "高风险命令在执行前请务必在隔离测试环境验证，并做好备份与变更通知。",
    ])

    report_path = PROJECT_ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\n📄 报告已保存: {report_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
