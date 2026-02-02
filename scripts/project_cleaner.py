#!/usr/bin/env python3
"""
项目文件清理脚本
自动识别和清理无用文件，保持项目整洁
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Set

class ProjectCleaner:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.cleaned_files: List[Path] = []
        self.cleaned_dirs: List[Path] = []
        
        # 定义需要清理的文件模式
        self.unwanted_patterns = {
            # 临时文件
            '.tmp', '.temp', '.bak', '.old', '.orig',
            '.swp', '.swo', '~', '.DS_Store', 'Thumbs.db',
            '.log', '.cache', '.coverage',
            
            # 编译产物
            '.pyc', '.pyo', '__pycache__',
            '.class', '.jar', '.war', '.ear',
            '.o', '.obj', '.exe', '.dll', '.so',
            
            # IDE和编辑器文件
            '.vscode', '.idea', '.settings',
            '*.iml', '*.iws', '*.ipr',
            
            # 构建产物
            'node_modules', 'dist', 'build', 'target',
            '.next', '.nuxt', 'out',
            
            # 版本控制
            '.git', '.svn', '.hg',
            
            # 包管理
            '.npm', '.yarn', 'yarn-error.log',
            
            # 其他无用文件
            'TODO*', 'WIP*', '*draft*', '*backup*',
            'COPYING*', 'LICENSE.md'
        }
        
        # 定义需要保留的重要文件
        self.essential_files = {
            'README.md', 'metadata.json', '.gitignore',
            'LICENSE', 'requirements.txt', 'package.json',
            'Dockerfile', 'docker-compose.yml'
        }

    def is_unwanted_file(self, file_path: Path) -> bool:
        """判断是否为无用文件"""
        filename = file_path.name
        
        # 检查文件扩展名
        for pattern in self.unwanted_patterns:
            if pattern.startswith('*') and pattern.endswith('*'):
                if pattern[1:-1] in filename:
                    return True
            elif pattern.startswith('*'):
                if filename.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('*'):
                if filename.startswith(pattern[:-1]):
                    return True
            else:
                if filename == pattern:
                    return True
                    
        return False

    def is_empty_directory(self, dir_path: Path) -> bool:
        """判断是否为空目录"""
        try:
            return not any(dir_path.iterdir())
        except PermissionError:
            return False

    def clean_files(self, dry_run: bool = True) -> None:
        """清理无用文件"""
        print("🔍 开始扫描无用文件...")
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # 跳过隐藏目录和版本控制目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['.git', 'node_modules']]
            
            # 检查文件
            for file in files:
                file_path = root_path / file
                
                # 跳过重要文件
                if file in self.essential_files:
                    continue
                    
                if self.is_unwanted_file(file_path):
                    if dry_run:
                        print(f"📄 [预览] 将删除: {file_path.relative_to(self.project_root)}")
                    else:
                        try:
                            file_path.unlink()
                            self.cleaned_files.append(file_path)
                            print(f"✅ 已删除: {file_path.relative_to(self.project_root)}")
                        except Exception as e:
                            print(f"❌ 删除失败 {file_path}: {e}")

    def clean_empty_dirs(self, dry_run: bool = True) -> None:
        """清理空目录"""
        print("📁 开始扫描空目录...")
        
        # 从最深层开始向上清理
        for root, dirs, files in os.walk(self.project_root, topdown=False):
            root_path = Path(root)
            
            # 跳过项目根目录和重要目录
            if root_path == self.project_root:
                continue
                
            if '.git' in root_path.parts:
                continue
                
            if self.is_empty_directory(root_path):
                if dry_run:
                    print(f"📂 [预览] 将删除空目录: {root_path.relative_to(self.project_root)}")
                else:
                    try:
                        root_path.rmdir()
                        self.cleaned_dirs.append(root_path)
                        print(f"✅ 已删除空目录: {root_path.relative_to(self.project_root)}")
                    except Exception as e:
                        print(f"❌ 删除目录失败 {root_path}: {e}")

    def generate_cleanup_report(self) -> str:
        """生成清理报告"""
        report = []
        report.append("=" * 50)
        report.append("🗑️  项目清理报告")
        report.append("=" * 50)
        report.append("")
        
        if self.cleaned_files:
            report.append(f"已清理文件 ({len(self.cleaned_files)} 个):")
            for file_path in self.cleaned_files:
                report.append(f"  - {file_path.relative_to(self.project_root)}")
            report.append("")
            
        if self.cleaned_dirs:
            report.append(f"已清理空目录 ({len(self.cleaned_dirs)} 个):")
            for dir_path in self.cleaned_dirs:
                report.append(f"  - {dir_path.relative_to(self.project_root)}")
            report.append("")
            
        total_cleaned = len(self.cleaned_files) + len(self.cleaned_dirs)
        report.append(f"总计清理: {total_cleaned} 项")
        
        return "\n".join(report)

    def run_cleanup(self, dry_run: bool = True) -> None:
        """执行清理"""
        print(f"🚀 开始项目清理 {'(预览模式)' if dry_run else '(执行模式)'}")
        print(f"项目根目录: {self.project_root.absolute()}")
        print()
        
        # 清理文件
        self.clean_files(dry_run)
        print()
        
        # 清理空目录
        self.clean_empty_dirs(dry_run)
        print()
        
        # 生成报告
        if not dry_run:
            report = self.generate_cleanup_report()
            print(report)
            
            # 保存报告到文件
            report_file = self.project_root / "CLEANUP_REPORT.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📝 清理报告已保存到: {report_file}")

def main():
    parser = argparse.ArgumentParser(description='清理项目中的无用文件')
    parser.add_argument('--dry-run', action='store_true', 
                       help='预览模式，只显示将要清理的文件而不实际删除')
    parser.add_argument('--path', default='.', 
                       help='项目根目录路径')
    
    args = parser.parse_args()
    
    cleaner = ProjectCleaner(args.path)
    cleaner.run_cleanup(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
