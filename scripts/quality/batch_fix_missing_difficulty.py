#!/usr/bin/env python3
"""
修复所有 metadata.json 中缺少 difficulty 或 description 不足的案例。
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(".")
IGNORE_DIRS = {".git", ".github", ".venv", "venv", "node_modules", "__pycache__", "check"}


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def find_all_metadata(root: Path) -> list:
    files = []
    search_stack = [(root, 0)]
    while search_stack:
        current, depth = search_stack.pop()
        if depth > 6:
            continue
        for item in current.iterdir():
            if not item.is_dir():
                continue
            if item.name in IGNORE_DIRS or item.name.startswith("."):
                continue
            meta = item / "metadata.json"
            if meta.exists():
                files.append(meta)
            search_stack.append((item, depth + 1))
    return files


def fix_metadata(metadata_path: Path) -> bool:
    try:
        data = json.loads(safe_read_text(metadata_path))
    except json.JSONDecodeError:
        return False

    original = json.dumps(data, ensure_ascii=False, sort_keys=True)
    demo_dir = metadata_path.parent

    if not data.get("difficulty"):
        data["difficulty"] = "intermediate"

    if not data.get("description") or len(str(data.get("description"))) < 20:
        data["description"] = f"{data.get('name', demo_dir.name.replace('-', ' ').title())} 的实战演示与配置详解"

    if not data.get("author"):
        data["author"] = "OpenDemo Team"

    new = json.dumps(data, ensure_ascii=False, sort_keys=True)
    if original != new:
        metadata_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return True
    return False


def main():
    files = find_all_metadata(PROJECT_ROOT)
    fixed = 0
    failed = []

    for meta_path in files:
        try:
            if fix_metadata(meta_path):
                fixed += 1
        except Exception as e:
            failed.append((str(meta_path), str(e)))

    print(f"修复 metadata: {fixed}")
    print(f"失败: {len(failed)}")
    for path, err in failed[:10]:
        print(f"  {path}: {err}")


if __name__ == "__main__":
    main()
