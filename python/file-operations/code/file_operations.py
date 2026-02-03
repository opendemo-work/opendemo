#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python文件操作演示
展示文件读写、路径处理、目录操作等
"""
import os
import shutil
import tempfile
from pathlib import Path


def demo_file_read_write():
    """文件读写基础"""
    print("=" * 50)
    print("1. 文件读写基础")
    print("=" * 50)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test.txt")
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("第一行\n")
        f.write("第二行\n")
        f.writelines(["第三行\n", "第四行\n"])
    print(f"写入文件: {file_path}")
    
    # 读取整个文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"读取全部内容:\n{content}")
    
    # 按行读取
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"readlines(): {lines}")
    
    # 逐行迭代(推荐大文件)
    print("逐行迭代:")
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            print(f"  第{i}行: {line.strip()}")
    
    # 清理
    shutil.rmtree(temp_dir)


def demo_file_modes():
    """文件打开模式"""
    print("\n" + "=" * 50)
    print("2. 文件打开模式")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "modes.txt")
    
    # 写模式 'w' - 覆盖
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("初始内容\n")
    
    # 追加模式 'a'
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write("追加内容\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        print(f"追加后内容:\n{f.read()}")
    
    # 读写模式 'r+'
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0)  # 回到开头
        f.write("新内容\n" + content)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        print(f"r+模式修改后:\n{f.read()}")
    
    # 二进制模式
    binary_path = os.path.join(temp_dir, "binary.bin")
    with open(binary_path, 'wb') as f:
        f.write(b'\x00\x01\x02\x03\x04')
    
    with open(binary_path, 'rb') as f:
        data = f.read()
    print(f"二进制读取: {data}, 类型: {type(data)}")
    
    print("\n常用模式说明:")
    modes = [
        ("'r'", "只读(默认)"),
        ("'w'", "写入(覆盖)"),
        ("'a'", "追加"),
        ("'r+'", "读写"),
        ("'rb'", "二进制读"),
        ("'wb'", "二进制写"),
    ]
    for mode, desc in modes:
        print(f"  {mode}: {desc}")
    
    shutil.rmtree(temp_dir)


def demo_pathlib():
    """pathlib路径操作"""
    print("\n" + "=" * 50)
    print("3. pathlib路径操作")
    print("=" * 50)
    
    # 创建Path对象
    p = Path("./example/subdir/file.txt")
    print(f"Path对象: {p}")
    print(f"父目录: {p.parent}")
    print(f"文件名: {p.name}")
    print(f"后缀: {p.suffix}")
    print(f"不带后缀的名称: {p.stem}")
    print(f"各部分: {p.parts}")
    
    # 路径拼接
    base = Path("/home/user")
    full_path = base / "documents" / "file.txt"
    print(f"\n路径拼接: {full_path}")
    
    # 当前目录和用户目录
    print(f"当前目录: {Path.cwd()}")
    print(f"用户目录: {Path.home()}")
    
    # 临时目录操作示例
    temp_dir = Path(tempfile.mkdtemp())
    test_file = temp_dir / "test.txt"
    
    # 写入和读取
    test_file.write_text("Hello, pathlib!", encoding='utf-8')
    content = test_file.read_text(encoding='utf-8')
    print(f"\n写入并读取: {content}")
    
    # 文件信息
    print(f"文件存在: {test_file.exists()}")
    print(f"是文件: {test_file.is_file()}")
    print(f"是目录: {test_file.is_dir()}")
    print(f"绝对路径: {test_file.absolute()}")
    
    shutil.rmtree(temp_dir)


def demo_directory_operations():
    """目录操作"""
    print("\n" + "=" * 50)
    print("4. 目录操作")
    print("=" * 50)
    
    temp_dir = Path(tempfile.mkdtemp())
    
    # 创建目录
    new_dir = temp_dir / "level1" / "level2" / "level3"
    new_dir.mkdir(parents=True, exist_ok=True)
    print(f"创建多级目录: {new_dir}")
    
    # 创建测试文件
    (temp_dir / "file1.txt").write_text("test1")
    (temp_dir / "file2.py").write_text("test2")
    (temp_dir / "level1" / "file3.txt").write_text("test3")
    
    # 列出目录内容
    print(f"\n目录内容 (iterdir):")
    for item in temp_dir.iterdir():
        item_type = "目录" if item.is_dir() else "文件"
        print(f"  {item.name} ({item_type})")
    
    # glob模式匹配
    print(f"\n匹配 *.txt:")
    for f in temp_dir.glob("*.txt"):
        print(f"  {f.name}")
    
    print(f"\n递归匹配 **/*.txt:")
    for f in temp_dir.rglob("*.txt"):
        print(f"  {f}")
    
    shutil.rmtree(temp_dir)


def demo_file_operations():
    """文件操作(复制、移动、删除)"""
    print("\n" + "=" * 50)
    print("5. 文件操作(复制、移动、删除)")
    print("=" * 50)
    
    temp_dir = Path(tempfile.mkdtemp())
    
    # 创建测试文件
    source = temp_dir / "source.txt"
    source.write_text("原始内容")
    
    # 复制文件
    dest = temp_dir / "dest.txt"
    shutil.copy(source, dest)
    print(f"复制文件: {source.name} -> {dest.name}")
    print(f"  dest内容: {dest.read_text()}")
    
    # 移动/重命名
    new_name = temp_dir / "renamed.txt"
    dest.rename(new_name)
    print(f"重命名: dest.txt -> renamed.txt")
    print(f"  renamed.txt存在: {new_name.exists()}")
    print(f"  dest.txt存在: {dest.exists()}")
    
    # 删除文件
    new_name.unlink()
    print(f"删除文件: renamed.txt")
    print(f"  文件存在: {new_name.exists()}")
    
    # 复制目录
    src_dir = temp_dir / "src_folder"
    src_dir.mkdir()
    (src_dir / "file.txt").write_text("test")
    
    dst_dir = temp_dir / "dst_folder"
    shutil.copytree(src_dir, dst_dir)
    print(f"\n复制目录: src_folder -> dst_folder")
    print(f"  dst_folder内容: {list(dst_dir.iterdir())}")
    
    shutil.rmtree(temp_dir)


def demo_file_info():
    """获取文件信息"""
    print("\n" + "=" * 50)
    print("6. 获取文件信息")
    print("=" * 50)
    
    temp_dir = Path(tempfile.mkdtemp())
    test_file = temp_dir / "info_test.txt"
    test_file.write_text("测试内容" * 100)
    
    # 文件大小
    size = test_file.stat().st_size
    print(f"文件大小: {size} 字节")
    
    # 时间信息
    import time
    stat = test_file.stat()
    mtime = time.ctime(stat.st_mtime)
    print(f"修改时间: {mtime}")
    
    # 使用os.path
    print(f"\nos.path方法:")
    print(f"  exists: {os.path.exists(test_file)}")
    print(f"  isfile: {os.path.isfile(test_file)}")
    print(f"  isdir: {os.path.isdir(test_file)}")
    print(f"  getsize: {os.path.getsize(test_file)} 字节")
    print(f"  basename: {os.path.basename(test_file)}")
    print(f"  dirname: {os.path.dirname(test_file)}")
    print(f"  splitext: {os.path.splitext(test_file)}")
    
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    demo_file_read_write()
    demo_file_modes()
    demo_pathlib()
    demo_directory_operations()
    demo_file_operations()
    demo_file_info()
    print("\n[OK] 文件操作演示完成!")
