#!/usr/bin/env python3
"""
根目录文件整理脚本
将根目录的文档文件按类别整理到相应的文件夹中
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

class RootDirectoryOrganizer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        
        # 定义文件分类规则
        self.file_categories = {
            "docs/reports": [
                "COMPREHENSIVE-GAP-ANALYSIS.md",
                "COMPREHENSIVE-IMPROVEMENT-SUMMARY.md", 
                "COMPREHENSIVE-TODO-EVALUATION.md",
                "JAVA-QUALITY-CHECK-SUMMARY.md",
                "PROJECT-DIRECTORY-AUDIT.md"
            ],
            "docs/guides": [
                "DEVELOPER-GUIDE.md",
                "EXECUTION-PLAN.md",
                "PROFESSIONAL-CLASSIFICATION-SYSTEM.md"
            ],
            "docs/plans": [
                "CROSS-TECH-INTEGRATION-PLAN.md"
            ],
            "reports": [
                "CLEANUP_REPORT.md",
                "DATABASE-DEMO-SUMMARY.md",
                "PROJECT-CLEANUP-REPORT.md"
            ],
            "config": [
                "Makefile",
                "pyproject.toml"
            ],
            "data": [
                "coverage.json",
                "java_validation_report.json"
            ]
        }
        
        # 需要保留的根目录文件
        self.preserve_files = {
            "README.md",
            "LICENSE", 
            ".gitignore",
            ".migration_completed"
        }
        
        self.moved_files = []
        self.preserved_files = []

    def categorize_file(self, filename: str) -> str:
        """根据文件名确定分类目录"""
        for category, files in self.file_categories.items():
            if filename in files:
                return category
        return None

    def organize_files(self, dry_run: bool = True) -> None:
        """执行文件整理"""
        print(f"🚀 开始根目录文件整理 {'(预览模式)' if dry_run else '(执行模式)'}")
        print(f"项目根目录: {self.project_root.absolute()}")
        print()
        
        # 获取根目录所有文件
        root_files = [f for f in self.project_root.iterdir() if f.is_file()]
        
        print("🔍 分析根目录文件...")
        for file_path in root_files:
            filename = file_path.name
            
            # 跳过需要保留的文件
            if filename in self.preserve_files:
                self.preserved_files.append(filename)
                print(f"✅ 保留文件: {filename}")
                continue
            
            # 确定文件分类
            category = self.categorize_file(filename)
            if category:
                target_dir = self.project_root / category
                
                if dry_run:
                    print(f"📁 [预览] {filename} → {category}/")
                else:
                    # 创建目标目录
                    target_dir.mkdir(parents=True, exist_ok=True)
                    
                    # 移动文件
                    target_path = target_dir / filename
                    try:
                        shutil.move(str(file_path), str(target_path))
                        self.moved_files.append((filename, category))
                        print(f"✅ 已移动: {filename} → {category}/")
                    except Exception as e:
                        print(f"❌ 移动失败 {filename}: {e}")
            else:
                print(f"❓ 未分类文件: {filename}")
        
        print()
        self.generate_organization_report()

    def generate_organization_report(self) -> None:
        """生成整理报告"""
        report = []
        report.append("=" * 60)
        report.append("📁 根目录文件整理报告")
        report.append("=" * 60)
        report.append("")
        
        if self.moved_files:
            report.append(f"已移动文件 ({len(self.moved_files)} 个):")
            # 按目录分组显示
            categorized = {}
            for filename, category in self.moved_files:
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(filename)
            
            for category, files in categorized.items():
                report.append(f"  {category}/:")
                for file in files:
                    report.append(f"    - {file}")
            report.append("")
        
        if self.preserved_files:
            report.append(f"保留的根目录文件 ({len(self.preserved_files)} 个):")
            for file in sorted(self.preserved_files):
                report.append(f"  - {file}")
            report.append("")
        
        # 显示整理后的目录结构
        report.append("整理后的根目录结构:")
        report.append("opendemo/")
        report.append("├── README.md")
        report.append("├── LICENSE")
        report.append("├── .gitignore")
        report.append("├── .migration_completed")
        report.append("├── ai/")
        report.append("├── cli/")
        report.append("├── container/")
        report.append("├── data/")
        report.append("├── database/")
        report.append("├── docs/")
        report.append("├── go/")
        report.append("├── java/")
        report.append("├── kubernetes/")
        report.append("├── linux/")
        report.append("├── nodejs/")
        report.append("├── python/")
        report.append("├── scripts/")
        report.append("├── tests/")
        report.append("└── vibe-coding/")
        report.append("")
        
        total_moved = len(self.moved_files)
        report.append(f"总计移动文件: {total_moved} 个")
        report.append(f"保留根文件: {len(self.preserved_files)} 个")
        
        print("\n".join(report))
        
        if not any(flag in str(os.sys.argv) for flag in ['--dry-run', '-n']):
            # 保存报告到文件
            report_file = self.project_root / "ROOT_ORGANIZATION_REPORT.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(report))
            print(f"\n📝 整理报告已保存到: {report_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='整理根目录文件到相应文件夹')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='预览模式，只显示将要移动的文件而不实际移动')
    
    args = parser.parse_args()
    
    organizer = RootDirectoryOrganizer()
    organizer.organize_files(dry_run=args.dry_run)

if __name__ == "__main__":
    main()