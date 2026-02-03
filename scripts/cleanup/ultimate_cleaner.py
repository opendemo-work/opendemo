#!/usr/bin/env python3
"""
根目录极致精简脚本
将除README.md外的所有文件移动到合适的位置
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

class UltimateRootCleaner:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.moved_files: List[Tuple[str, str]] = []
        
        # 定义文件迁移规则
        self.migration_rules = {
            ".gitignore": "config/.gitignore",
            ".migration_completed": "meta/.migration_completed",
            "LICENSE": "legal/LICENSE",
            "ROOT_ORGANIZATION_REPORT.md": "docs/reports/ROOT_ORGANIZATION_REPORT.md"
        }
        
        # 需要保留的核心文件
        self.core_files = {"README.md"}

    def prepare_directories(self) -> None:
        """预先创建必要的目录"""
        directories = ["config", "meta", "legal", "docs/reports"]
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 创建目录: {dir_name}/")

    def migrate_files(self, dry_run: bool = True) -> None:
        """执行文件迁移"""
        print(f"🚀 开始根目录极致精简 {'(预览模式)' if dry_run else '(执行模式)'}")
        print(f"项目根目录: {self.project_root.absolute()}")
        print()
        
        # 预先创建目录
        if not dry_run:
            self.prepare_directories()
        
        # 获取根目录所有文件
        root_files = [f for f in self.project_root.iterdir() if f.is_file()]
        
        print("🔍 分析根目录文件...")
        for file_path in root_files:
            filename = file_path.name
            
            # 跳过核心文件
            if filename in self.core_files:
                print(f"✅ 保留核心文件: {filename}")
                continue
            
            # 确定迁移目标
            if filename in self.migration_rules:
                target_path = self.project_root / self.migration_rules[filename]
                
                if dry_run:
                    print(f"📁 [预览] {filename} → {self.migration_rules[filename]}")
                else:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        self.moved_files.append((filename, str(target_path.relative_to(self.project_root))))
                        print(f"✅ 已移动: {filename} → {target_path.relative_to(self.project_root)}")
                    except Exception as e:
                        print(f"❌ 移动失败 {filename}: {e}")
            else:
                # 未定义规则的文件给出建议
                suggestion = self.suggest_location(filename)
                print(f"❓ 未定义规则: {filename} (建议位置: {suggestion})")

    def suggest_location(self, filename: str) -> str:
        """为未定义规则的文件建议位置"""
        if filename.endswith(('.md', '.rst', '.txt')):
            return "docs/misc/"
        elif filename.startswith('.'):
            return "config/"
        elif filename.upper() == filename:
            return "legal/"
        else:
            return "temp/"

    def generate_final_report(self) -> None:
        """生成最终精简报告"""
        report = []
        report.append("=" * 60)
        report.append("🎯 根目录极致精简报告")
        report.append("=" * 60)
        report.append("")
        
        if self.moved_files:
            report.append(f"已迁移文件 ({len(self.moved_files)} 个):")
            for filename, target in self.moved_files:
                report.append(f"  - {filename} → {target}")
            report.append("")
        
        # 显示最终根目录状态
        report.append("精简后的根目录结构:")
        report.append("opendemo/")
        report.append("└── README.md")
        report.append("")
        
        # 显示完整的项目结构概览
        report.append("项目整体结构概览:")
        report.append("opendemo/")
        report.append("├── README.md              # 项目入口文档")
        report.append("├── config/                # 配置文件")
        report.append("│   └── .gitignore         # Git忽略规则")
        report.append("├── meta/                  # 元数据文件")
        report.append("│   └── .migration_completed # 迁移完成标记")
        report.append("├── legal/                 # 法律文件")
        report.append("│   └── LICENSE            # 开源许可证")
        report.append("├── docs/                  # 文档中心")
        report.append("│   └── reports/           # 项目报告")
        report.append("│       └── ROOT_ORGANIZATION_REPORT.md")
        report.append("├── scripts/               # 维护脚本")
        report.append("└── 各技术栈目录...         # 核心功能模块")
        report.append("")
        
        total_moved = len(self.moved_files)
        report.append(f"总计迁移文件: {total_moved} 个")
        report.append(f"根目录保留文件: 1 个 (README.md)")
        
        print("\n".join(report))
        
        if not any(flag in str(os.sys.argv) for flag in ['--dry-run', '-n']):
            # 保存报告到文件
            report_file = self.project_root / "FINAL_CLEANUP_REPORT.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(report))
            print(f"\n📝 精简报告已保存到: {report_file}")

    def update_readme_references(self) -> None:
        """更新README中对迁移文件的引用"""
        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            return
            
        print("🔄 更新README中的文件引用...")
        
        # 需要更新的引用映射
        reference_updates = {
            "ROOT_ORGANIZATION_REPORT.md": "docs/reports/ROOT_ORGANIZATION_REPORT.md",
            "LICENSE": "legal/LICENSE"
        }
        
        try:
            content = readme_path.read_text(encoding='utf-8')
            original_content = content
            
            for old_ref, new_ref in reference_updates.items():
                content = content.replace(old_ref, new_ref)
            
            if content != original_content:
                readme_path.write_text(content, encoding='utf-8')
                print("✅ README文件引用已更新")
            else:
                print("ℹ️  README文件无需更新")
                
        except Exception as e:
            print(f"❌ 更新README失败: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='极致精简根目录，只保留README.md')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='预览模式，只显示将要移动的文件而不实际移动')
    parser.add_argument('--update-readme', action='store_true',
                       help='同时更新README中的文件引用')
    
    args = parser.parse_args()
    
    cleaner = UltimateRootCleaner()
    cleaner.migrate_files(dry_run=args.dry_run)
    
    if not args.dry_run and args.update_readme:
        cleaner.update_readme_references()
    
    cleaner.generate_final_report()

if __name__ == "__main__":
    main()