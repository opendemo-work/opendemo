#!/usr/bin/env python3
"""
OpenDemo 五星案例结构校验脚本

校验每个有效案例是否满足五星标准：
1. metadata.json 存在且符合 schema 1.0
2. README.md 存在且长度 >= 3000 字符
3. 至少包含一个可运行产物（脚本/YAML/docker-compose/代码/测试）
4. README 中引用的本地文件存在
5. 目录非空（不得只有 README + metadata）

用法：
    python scripts/quality/validate_five_star.py [--fix]
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# 技术栈根目录
TECH_STACKS = [
    "go", "java", "nodejs", "python", "kubernetes", "database",
    "networking", "kvm", "virtualization", "container", "sre",
    "security", "linux", "ai-ml", "monitoring", "messaging", "traffic",
    "bigdata"
]

# 可运行产物扩展名
RUNNABLE_PATTERNS = [
    "*.py", "*.go", "*.java", "*.js", "*.sh", "*.yaml", "*.yml",
    "Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "*.sql", "*.md"  # README 不算可运行产物，但 markdown 可包含可执行说明
]

# 忽略的特殊目录
IGNORE_DIRS = {".git", ".github", ".venv", "venv", "node_modules", "__pycache__"}


def load_schema(project_root: Path) -> Dict:
    """加载 metadata schema"""
    schema_path = project_root / "configs" / "metadata-schema-1.0.json"
    if not schema_path.exists():
        print(f"❌ Schema 文件不存在: {schema_path}")
        sys.exit(1)
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_json_schema(metadata: Dict, schema: Dict) -> List[str]:
    """基于 JSON Schema 校验 metadata"""
    errors = []
    required = schema.get("required", [])
    for field in required:
        if field not in metadata:
            errors.append(f"缺少必填字段: {field}")

    props = schema.get("properties", {})
    for field, value in metadata.items():
        if field not in props:
            continue
        prop = props[field]
        expected_type = prop.get("type")
        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"字段 {field} 应为字符串")
        elif expected_type == "array" and not isinstance(value, list):
            errors.append(f"字段 {field} 应为数组")
        elif expected_type == "object" and not isinstance(value, dict):
            errors.append(f"字段 {field} 应为对象")
        elif expected_type == "boolean" and not isinstance(value, bool):
            errors.append(f"字段 {field} 应为布尔值")

        if isinstance(value, str):
            if "minLength" in prop and len(value) < prop["minLength"]:
                errors.append(f"字段 {field} 长度不足 {prop['minLength']} 字符")
            if "enum" in prop and value not in prop["enum"]:
                errors.append(f"字段 {field} 值 '{value}' 不在允许枚举中")
            if "pattern" in prop:
                if not re.match(prop["pattern"], value):
                    errors.append(f"字段 {field} 格式不符合正则: {prop['pattern']}")

        if isinstance(value, list) and "minItems" in prop:
            if len(value) < prop["minItems"]:
                errors.append(f"字段 {field} 元素数量不足 {prop['minItems']} 个")

    return errors


def check_readme(readme_path: Path, safe_read_text) -> Tuple[bool, int, List[str]]:
    """检查 README 质量"""
    issues = []
    if not readme_path.exists():
        return False, 0, ["缺少 README.md"]

    content = safe_read_text(readme_path)
    char_count = len(content)
    if char_count < 3000:
        issues.append(f"README 长度仅 {char_count} 字符，不足 3000")

    # 检查关键章节
    required_sections = ["学习目标", "快速开始", "核心概念", "代码示例"]
    for section in required_sections:
        if section not in content:
            issues.append(f"README 缺少 '{section}' 章节")

    return len(issues) == 0, char_count, issues


def check_runnable_artifacts(demo_dir: Path) -> Tuple[bool, List[str]]:
    """检查是否存在可运行产物"""
    found = []
    for pattern in RUNNABLE_PATTERNS:
        if pattern == "*.md":
            continue
        matches = list(demo_dir.rglob(pattern))
        matches = [m for m in matches if not any(part in IGNORE_DIRS for part in m.parts)]
        found.extend(matches)

    # 过滤掉 README.md 和 metadata.json 自身
    found = [f for f in found if f.name not in ("README.md", "metadata.json")]

    has_runnable = len(found) > 0
    detail = [str(f.relative_to(demo_dir)) for f in found[:5]]
    return has_runnable, detail


def _strip_code_blocks(content: str) -> str:
    """移除 Markdown 代码块，避免代码片段被误解析为文件引用。"""
    # 匹配 ```...``` 代码块（包括语言标识）
    return re.sub(r"```[\s\S]*?```", "", content)


def check_referenced_files(readme_path: Path, demo_dir: Path, safe_read_text) -> Tuple[List[str], List[str]]:
    """检查 README 中引用的本地文件是否存在。

    返回 (issues, warnings)。跨案例链接缺失作为警告，不视为失败。
    """
    if not readme_path.exists():
        return [], []

    content = safe_read_text(readme_path)
    # 只在非代码块区域检查文件引用
    content_without_code = _strip_code_blocks(content)
    issues = []
    warnings = []

    # 匹配 Markdown 链接中的相对路径 [text](path)
    md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content_without_code)
    for text, link in md_links:
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if "://" in link:
            continue
        # 忽略通配符、省略号、表格残留等无效路径
        if "*" in link or link in ("...", "", "."):
            continue
        if "|" in link:
            continue
        # 去掉锚点
        link = link.split("#")[0]
        if not link:
            continue
        target = demo_dir / link
        if not target.exists():
            # 如果是跨案例链接（包含 ../），暂视为警告，不导致失败
            if link.startswith("../") or link.startswith("/"):
                warnings.append(f"README 跨案例链接待验证: {link}")
                continue
            issues.append(f"README 引用文件不存在: {link}")

    # 匹配代码块中引用的文件路径（简单启发式）
    # 使用负向回顾避免匹配 classpath:、h2:file: 等复合词中的 path/file
    file_refs = re.findall(r"(?<!\w)(?:文件|file|path):\s*[`\"']?([^\n`\"']+)[`\"']?", content_without_code, re.IGNORECASE)
    for ref in file_refs:
        if ref.startswith(("http://", "https://")):
            continue
        if "*" in ref or ref in ("...", "", ".") or "|" in ref:
            continue
        target = demo_dir / ref.strip()
        if not target.exists():
            if ref.strip().startswith("../") or ref.strip().startswith("/"):
                warnings.append(f"README 跨案例文件引用待验证: {ref.strip()}")
                continue
            issues.append(f"README 引用文件不存在: {ref.strip()}")

    return issues, warnings


def check_empty_directory(demo_dir: Path) -> Tuple[bool, List[str]]:
    """检查目录是否为空壳"""
    files = [f for f in demo_dir.rglob("*") if f.is_file()]
    files = [f for f in files if f.name not in ("README.md", "metadata.json")]
    if not files:
        return True, ["目录下只有 README.md 和 metadata.json，无其他实质文件"]
    return False, []


def check_demo(demo_dir: Path, schema: Dict) -> Dict:
    """校验单个案例"""
    result = {
        "path": str(demo_dir),
        "name": demo_dir.name,
        "status": "PASS",
        "issues": [],
        "metadata_errors": [],
        "readme_chars": 0,
        "runnable_artifacts": [],
        "is_shell": False,
    }

    metadata_path = demo_dir / "metadata.json"
    readme_path = demo_dir / "README.md"

    def safe_read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                return path.read_text(encoding="gbk")
            except Exception:
                return path.read_text(encoding="utf-8", errors="ignore")

    # 1. 校验 metadata
    if not metadata_path.exists():
        result["metadata_errors"].append("缺少 metadata.json")
    else:
        try:
            metadata = json.loads(safe_read_text(metadata_path))
            result["metadata_errors"] = validate_json_schema(metadata, schema)
            result["name"] = metadata.get("name", demo_dir.name)
        except json.JSONDecodeError as e:
            result["metadata_errors"].append(f"metadata.json JSON 解析失败: {e}")

    # 2. 校验 README
    readme_ok, char_count, readme_issues = check_readme(readme_path, safe_read_text)
    result["readme_chars"] = char_count
    result["issues"].extend(readme_issues)

    # 3. 可运行产物
    has_runnable, artifacts = check_runnable_artifacts(demo_dir)
    result["runnable_artifacts"] = artifacts
    if not has_runnable:
        result["issues"].append("缺少可运行产物（脚本/YAML/代码/测试等）")

    # 4. 引用文件存在性
    ref_issues, ref_warnings = check_referenced_files(readme_path, demo_dir, safe_read_text)
    result["issues"].extend(ref_issues)
    result.setdefault("warnings", []).extend(ref_warnings)

    # 5. 空目录检查
    is_shell, shell_issues = check_empty_directory(demo_dir)
    result["is_shell"] = is_shell
    result["issues"].extend(shell_issues)

    # 汇总状态
    all_errors = result["metadata_errors"] + result["issues"]
    if all_errors:
        result["status"] = "FAIL"

    return result


def find_demos(project_root: Path, stacks: List[str]) -> List[Path]:
    """查找所有候选案例目录。

    策略：
    - 在技术栈根目录下，递归查找包含 metadata.json 的目录。
    - 排除技术栈根目录本身（如 go/、ai-ml/llm/）。
    - 最大深度为 5，避免进入过深的非案例目录。
    - 忽略已知工具目录和空目录。
    """
    demos = []
    stack_names = set(stacks)

    for stack in stacks:
        stack_dir = project_root / stack
        if not stack_dir.exists():
            continue

        search_stack = [(stack_dir, 0)]
        while search_stack:
            current_dir, depth = search_stack.pop()
            if depth > 5:
                continue

            for item in current_dir.iterdir():
                if not item.is_dir():
                    continue
                if item.name in IGNORE_DIRS:
                    continue
                if item.name.startswith("."):
                    continue

                # 排除技术栈根目录本身
                if depth == 0 and item.name in stack_names:
                    search_stack.append((item, depth + 1))
                    continue

                # 候选案例必须包含 metadata.json
                has_metadata = (item / "metadata.json").is_file()
                if has_metadata:
                    demos.append(item)

                # 继续向下搜索
                search_stack.append((item, depth + 1))

    # 去重并按路径排序
    unique_demos = sorted(set(demos), key=lambda p: str(p))
    return unique_demos


def main():
    parser = argparse.ArgumentParser(description="OpenDemo 五星案例结构校验")
    parser.add_argument("--stacks", nargs="+", help="只检查指定技术栈")
    parser.add_argument("--report", default="check/five_star_validation_report.json", help="报告输出路径")
    parser.add_argument("--markdown", default="check/five_star_validation_report.md", help="Markdown 报告路径")
    parser.add_argument("--summary", action="store_true", help="只输出摘要")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent.resolve()
    schema = load_schema(project_root)

    stacks = args.stacks or TECH_STACKS
    demos = find_demos(project_root, stacks)

    results = []
    pass_count = 0
    fail_count = 0

    for demo in demos:
        result = check_demo(demo, schema)
        results.append(result)
        if result["status"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1

    # 按技术栈分组统计
    stack_stats: Dict[str, Dict[str, int]] = {}
    for result in results:
        stack = Path(result["path"]).parent.name
        if stack not in stack_stats:
            stack_stats[stack] = {"total": 0, "pass": 0, "fail": 0}
        stack_stats[stack]["total"] += 1
        if result["status"] == "PASS":
            stack_stats[stack]["pass"] += 1
        else:
            stack_stats[stack]["fail"] += 1

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(results),
            "pass": pass_count,
            "fail": fail_count,
            "pass_rate": round(pass_count / len(results) * 100, 2) if results else 0,
        },
        "stack_stats": stack_stats,
        "results": results,
    }

    # 保存报告
    report_path = project_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 生成 Markdown 报告
    md_lines = [
        "# OpenDemo 五星案例结构校验报告",
        "",
        f"**检查时间**: {report['timestamp']}",
        "",
        "## 汇总",
        "",
        f"- 案例总数: **{len(results)}**",
        f"- 通过: **{pass_count}**",
        f"- 失败: **{fail_count}**",
        f"- 通过率: **{report['summary']['pass_rate']}%**",
        "",
        "## 按技术栈统计",
        "",
        "| 技术栈 | 总数 | 通过 | 失败 | 通过率 |",
        "|--------|------|------|------|--------|",
    ]
    for stack, stats in sorted(stack_stats.items()):
        rate = round(stats["pass"] / stats["total"] * 100, 2) if stats["total"] else 0
        md_lines.append(f"| {stack} | {stats['total']} | {stats['pass']} | {stats['fail']} | {rate}% |")

    md_lines.extend([
        "",
        "## 失败案例详情",
        "",
    ])

    for result in results:
        if result["status"] == "PASS":
            continue
        md_lines.append(f"### {result['name']} (`{result['path']}`)")
        md_lines.append("")
        if result["metadata_errors"]:
            md_lines.append("**Metadata 问题**:")
            for err in result["metadata_errors"]:
                md_lines.append(f"- ❌ {err}")
            md_lines.append("")
        if result["issues"]:
            md_lines.append("**内容/可运行性问题**:")
            for issue in result["issues"]:
                md_lines.append(f"- ⚠️ {issue}")
            md_lines.append("")

    md_path = project_root / args.markdown
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    # 控制台输出
    if not args.summary:
        print(f"\n🔍 检查完成: {len(results)} 个案例")
        print(f"✅ 通过: {pass_count}")
        print(f"❌ 失败: {fail_count}")
        print(f"📊 通过率: {report['summary']['pass_rate']}%")
        print(f"\n报告已保存:")
        print(f"  JSON: {report_path}")
        print(f"  Markdown: {md_path}")
    else:
        print(f"{len(results)},{pass_count},{fail_count},{report['summary']['pass_rate']}")

    # 失败时返回非 0 退出码
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
