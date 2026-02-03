#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 路径操作 (pathlib & os) 完整示例
演示现代路径处理和系统操作
"""

from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
import os
import shutil
import tempfile
import glob


# ============ 1. pathlib 基础 ============
print("=" * 50)
print("1. pathlib 基础")
print("=" * 50)

# 创建 Path 对象
current = Path(".")
home = Path.home()
cwd = Path.cwd()

print(f"当前目录: {current.absolute()}")
print(f"用户主目录: {home}")
print(f"工作目录: {cwd}")

# 路径拼接
data_dir = Path("data")
file_path = data_dir / "users" / "config.json"
print(f"路径拼接: {file_path}")


# ============ 2. 路径属性 ============
print("\n" + "=" * 50)
print("2. 路径属性")
print("=" * 50)

p = Path("/home/user/documents/report.pdf")

print(f"完整路径: {p}")
print(f"父目录: {p.parent}")
print(f"所有父目录: {list(p.parents)}")
print(f"文件名: {p.name}")
print(f"文件名(无后缀): {p.stem}")
print(f"后缀: {p.suffix}")
print(f"所有后缀: {Path('file.tar.gz').suffixes}")
print(f"各部分: {p.parts}")
print(f"是绝对路径: {p.is_absolute()}")


# ============ 3. 路径操作 ============
print("\n" + "=" * 50)
print("3. 路径操作")
print("=" * 50)

# 修改路径
p = Path("documents/old_report.txt")
print(f"原路径: {p}")
print(f"改后缀: {p.with_suffix('.pdf')}")
print(f"改文件名: {p.with_name('new_report.txt')}")
print(f"改stem: {p.with_stem('updated_report')}")

# 解析路径
raw = Path("./data/../config/./settings.json")
print(f"原始: {raw}")
print(f"解析后: {raw.resolve()}")


# ============ 4. 文件系统检查 ============
print("\n" + "=" * 50)
print("4. 文件系统检查")
print("=" * 50)

script_path = Path(__file__)
print(f"当前脚本: {script_path}")
print(f"存在: {script_path.exists()}")
print(f"是文件: {script_path.is_file()}")
print(f"是目录: {script_path.is_dir()}")
print(f"是符号链接: {script_path.is_symlink()}")

# 获取文件信息
stat = script_path.stat()
print(f"文件大小: {stat.st_size} bytes")
print(f"修改时间: {stat.st_mtime}")


# ============ 5. 目录操作 ============
print("\n" + "=" * 50)
print("5. 目录操作")
print("=" * 50)

# 使用临时目录演示
with tempfile.TemporaryDirectory() as tmpdir:
    base = Path(tmpdir)
    
    # 创建目录
    new_dir = base / "level1" / "level2" / "level3"
    new_dir.mkdir(parents=True, exist_ok=True)
    print(f"创建目录: {new_dir}")
    
    # 创建文件
    (new_dir / "test.txt").write_text("Hello, World!")
    (new_dir.parent / "config.json").write_text('{"key": "value"}')
    
    # 列出目录内容
    print(f"目录内容: {list(base.glob('**/*'))}")
    
    # 遍历目录
    print("递归遍历:")
    for item in base.rglob("*"):
        prefix = "  文件" if item.is_file() else "  目录"
        print(f"{prefix}: {item.relative_to(base)}")


# ============ 6. 文件读写 ============
print("\n" + "=" * 50)
print("6. 文件读写")
print("=" * 50)

with tempfile.TemporaryDirectory() as tmpdir:
    file = Path(tmpdir) / "sample.txt"
    
    # 写入文本
    file.write_text("Hello\nWorld\n中文内容", encoding="utf-8")
    print(f"写入完成: {file}")
    
    # 读取文本
    content = file.read_text(encoding="utf-8")
    print(f"读取内容:\n{content}")
    
    # 二进制读写
    binary_file = Path(tmpdir) / "data.bin"
    binary_file.write_bytes(b"\x00\x01\x02\x03")
    print(f"二进制内容: {binary_file.read_bytes()}")
    
    # 追加内容
    with file.open("a", encoding="utf-8") as f:
        f.write("追加内容\n")
    print(f"追加后:\n{file.read_text(encoding='utf-8')}")


# ============ 7. 文件匹配 ============
print("\n" + "=" * 50)
print("7. 文件匹配 (glob)")
print("=" * 50)

with tempfile.TemporaryDirectory() as tmpdir:
    base = Path(tmpdir)
    
    # 创建测试文件
    (base / "file1.py").touch()
    (base / "file2.py").touch()
    (base / "file3.txt").touch()
    (base / "sub").mkdir()
    (base / "sub" / "module.py").touch()
    
    # glob 匹配
    print("*.py 匹配:")
    for f in base.glob("*.py"):
        print(f"  {f.name}")
    
    print("**/*.py 递归匹配:")
    for f in base.glob("**/*.py"):
        print(f"  {f.relative_to(base)}")
    
    # match 方法
    p = Path("data/users/config.json")
    print(f"\n路径匹配:")
    print(f"  {p} 匹配 'data/*/*.json': {p.match('data/*/*.json')}")
    print(f"  {p} 匹配 '*.json': {p.match('*.json')}")


# ============ 8. os 模块路径操作 ============
print("\n" + "=" * 50)
print("8. os 模块路径操作")
print("=" * 50)

# 环境变量
print(f"PATH: {os.environ.get('PATH', '')[:50]}...")
print(f"HOME: {os.environ.get('HOME') or os.environ.get('USERPROFILE')}")

# 路径操作
print(f"\nos.path 操作:")
path = "/home/user/documents/file.txt"
print(f"  dirname: {os.path.dirname(path)}")
print(f"  basename: {os.path.basename(path)}")
print(f"  split: {os.path.split(path)}")
print(f"  splitext: {os.path.splitext(path)}")
print(f"  join: {os.path.join('a', 'b', 'c.txt')}")

# 路径规范化
print(f"\n路径规范化:")
print(f"  normpath: {os.path.normpath('a/b/../c/./d')}")
print(f"  abspath: {os.path.abspath('.')}")
print(f"  expanduser: {os.path.expanduser('~')}")


# ============ 9. shutil 高级操作 ============
print("\n" + "=" * 50)
print("9. shutil 高级操作")
print("=" * 50)

with tempfile.TemporaryDirectory() as tmpdir:
    base = Path(tmpdir)
    
    # 创建源目录和文件
    src = base / "source"
    src.mkdir()
    (src / "file1.txt").write_text("content1")
    (src / "file2.txt").write_text("content2")
    (src / "subdir").mkdir()
    (src / "subdir" / "file3.txt").write_text("content3")
    
    # 复制文件
    dst_file = base / "copied.txt"
    shutil.copy(src / "file1.txt", dst_file)
    print(f"复制文件: {dst_file.exists()}")
    
    # 复制目录
    dst_dir = base / "backup"
    shutil.copytree(src, dst_dir)
    print(f"复制目录: {list(dst_dir.rglob('*'))}")
    
    # 移动文件
    moved = base / "moved.txt"
    shutil.move(dst_file, moved)
    print(f"移动文件: {moved.exists()}, 原文件: {dst_file.exists()}")
    
    # 磁盘使用
    usage = shutil.disk_usage(base)
    print(f"磁盘使用: 总计={usage.total/1e9:.1f}GB, 已用={usage.used/1e9:.1f}GB, 可用={usage.free/1e9:.1f}GB")


# ============ 10. 跨平台路径 ============
print("\n" + "=" * 50)
print("10. 跨平台路径处理")
print("=" * 50)

# PurePath 不访问文件系统
posix_path = PurePosixPath("/home/user/file.txt")
windows_path = PureWindowsPath(r"C:\Users\user\file.txt")

print(f"POSIX 路径: {posix_path}")
print(f"Windows 路径: {windows_path}")
print(f"POSIX 各部分: {posix_path.parts}")
print(f"Windows 各部分: {windows_path.parts}")

# 自动选择当前系统路径类型
current_path = PurePath("data/file.txt")
print(f"当前系统路径: {current_path} (类型: {type(current_path).__name__})")


# ============ 11. 实用函数 ============
print("\n" + "=" * 50)
print("11. 实用函数")
print("=" * 50)

def ensure_dir(path: Path) -> Path:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_filename(name: str) -> str:
    """安全的文件名"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

def find_files(directory: Path, pattern: str, recursive: bool = True) -> list:
    """查找文件"""
    if recursive:
        return list(directory.rglob(pattern))
    return list(directory.glob(pattern))

def get_unique_path(path: Path) -> Path:
    """获取唯一路径(如果存在则添加序号)"""
    if not path.exists():
        return path
    
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    
    counter = 1
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

print(f"安全文件名: {safe_filename('file<>:name?.txt')}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("路径操作总结")
print("=" * 50)
print("""
pathlib vs os.path:
- pathlib: 面向对象, 现代, 推荐
- os.path: 函数式, 兼容老代码

常用操作:
- Path.cwd(): 当前目录
- Path.home(): 用户目录
- path / "sub": 路径拼接
- path.glob("*.py"): 文件匹配
- path.read_text(): 读取文件
- path.write_text(): 写入文件

文件系统:
- shutil.copy(): 复制文件
- shutil.copytree(): 复制目录
- shutil.move(): 移动/重命名
- shutil.rmtree(): 删除目录树

最佳实践:
1. 优先使用 pathlib
2. 使用 with 管理文件
3. 处理跨平台路径
4. 检查路径存在性
""")
