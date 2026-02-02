#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Linux命令演示项目验证脚本
用于验证所有演示案例的完整性和正确性
"""

import os
import json
import subprocess
from pathlib import Path

class LinuxDemoValidator:
    """Linux演示项目验证器"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.linux_root = self.project_root / "linux"
        self.required_files = ["README.md", "metadata.json"]
        self.validation_results = []
        
    def validate_project_structure(self):
        """验证项目目录结构"""
        print("🔍 验证项目目录结构...")
        
        if not self.linux_root.exists():
            self.validation_results.append(("ERROR", "Linux主目录不存在"))
            return False
            
        # 检查主目录文件
        for required_file in self.required_files:
            file_path = self.linux_root / required_file
            if not file_path.exists():
                self.validation_results.append(("ERROR", f"缺少必需文件: {required_file}"))
            else:
                self.validation_results.append(("SUCCESS", f"找到文件: {required_file}"))
                
        # 检查演示案例目录
        demo_dirs = [
            "linux-netstat-network-monitoring-demo",
            "linux-tsar-system-monitoring-demo", 
            "linux-top-process-monitoring-demo",
            "linux-common-monitoring-commands-demo"
        ]
        
        for demo_dir in demo_dirs:
            demo_path = self.linux_root / demo_dir
            if not demo_path.exists():
                self.validation_results.append(("ERROR", f"演示目录不存在: {demo_dir}"))
                continue
                
            self.validation_results.append(("SUCCESS", f"找到演示目录: {demo_dir}"))
            
            # 验证每个演示案例的必需文件
            for required_file in self.required_files:
                file_path = demo_path / required_file
                if not file_path.exists():
                    self.validation_results.append(("ERROR", f"演示案例缺少文件: {demo_dir}/{required_file}"))
                else:
                    self.validation_results.append(("SUCCESS", f"演示案例文件完整: {demo_dir}/{required_file}"))
                    
        return True
        
    def validate_metadata_format(self):
        """验证元数据格式"""
        print("🔍 验证元数据格式...")
        
        # 验证主元数据
        main_metadata = self.linux_root / "metadata.json"
        if main_metadata.exists():
            try:
                with open(main_metadata, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                required_fields = ["name", "language", "description", "demos"]
                for field in required_fields:
                    if field not in data:
                        self.validation_results.append(("ERROR", f"主元数据缺少字段: {field}"))
                    else:
                        self.validation_results.append(("SUCCESS", f"主元数据包含必需字段: {field}"))
                        
            except json.JSONDecodeError as e:
                self.validation_results.append(("ERROR", f"主元数据JSON格式错误: {str(e)}"))
                
        # 验证演示案例元数据
        demo_dirs = self.linux_root.glob("linux-*-demo")
        for demo_dir in demo_dirs:
            metadata_file = demo_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    required_fields = ["name", "language", "description", "difficulty"]
                    for field in required_fields:
                        if field not in data:
                            self.validation_results.append(("WARNING", f"{demo_dir.name}元数据缺少字段: {field}"))
                        else:
                            self.validation_results.append(("SUCCESS", f"{demo_dir.name}元数据字段完整: {field}"))
                            
                except json.JSONDecodeError as e:
                    self.validation_results.append(("ERROR", f"{demo_dir.name}元数据JSON格式错误: {str(e)}"))
                    
    def validate_script_files(self):
        """验证脚本文件"""
        print("🔍 验证脚本文件...")
        
        script_dirs = self.linux_root.glob("linux-*-demo/scripts")
        for script_dir in script_dirs:
            if script_dir.exists():
                scripts = list(script_dir.glob("*.sh"))
                if scripts:
                    self.validation_results.append(("SUCCESS", f"找到脚本文件: {script_dir.parent.name} ({len(scripts)}个)"))
                    
                    # 检查脚本权限
                    for script in scripts:
                        if os.access(script, os.X_OK):
                            self.validation_results.append(("SUCCESS", f"脚本可执行: {script.name}"))
                        else:
                            self.validation_results.append(("WARNING", f"脚本不可执行(建议chmod +x): {script.name}"))
                else:
                    self.validation_results.append(("INFO", f"无脚本文件: {script_dir.parent.name}"))
                    
    def validate_documentation(self):
        """验证文档完整性"""
        print("🔍 验证文档完整性...")
        
        # 检查README文件内容
        readme_files = self.linux_root.glob("**/README.md")
        for readme_file in readme_files:
            try:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 检查必需的内容元素
                required_elements = ["学习目标", "环境准备", "快速开始"]
                missing_elements = []
                
                for element in required_elements:
                    if element not in content:
                        missing_elements.append(element)
                        
                if missing_elements:
                    self.validation_results.append(("WARNING", f"{readme_file.parent.name} README缺少元素: {', '.join(missing_elements)}"))
                else:
                    self.validation_results.append(("SUCCESS", f"{readme_file.parent.name} README内容完整"))
                    
            except Exception as e:
                self.validation_results.append(("ERROR", f"读取README文件失败: {str(e)}"))
                
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "="*50)
        print("📊 Linux命令演示项目验证报告")
        print("="*50)
        
        success_count = sum(1 for result in self.validation_results if result[0] == "SUCCESS")
        warning_count = sum(1 for result in self.validation_results if result[0] == "WARNING")
        error_count = sum(1 for result in self.validation_results if result[0] == "ERROR")
        
        print(f"✅ 成功: {success_count}")
        print(f"⚠️  警告: {warning_count}")
        print(f"❌ 错误: {error_count}")
        print("-"*50)
        
        # 分类显示结果
        print("\n📋 详细验证结果:")
        
        successes = [r for r in self.validation_results if r[0] == "SUCCESS"]
        warnings = [r for r in self.validation_results if r[0] == "WARNING"]
        errors = [r for r in self.validation_results if r[0] == "ERROR"]
        infos = [r for r in self.validation_results if r[0] == "INFO"]
        
        if errors:
            print("\n🔴 错误项:")
            for _, msg in errors:
                print(f"  • {msg}")
                
        if warnings:
            print("\n🟡 警告项:")
            for _, msg in warnings:
                print(f"  • {msg}")
                
        if infos:
            print("\n🔵 信息项:")
            for _, msg in infos:
                print(f"  • {msg}")
                
        if successes:
            print("\n🟢 成功项:")
            for _, msg in successes[:10]:  # 只显示前10个成功项避免过长
                print(f"  • {msg}")
            if len(successes) > 10:
                print(f"  • ... 还有 {len(successes) - 10} 个成功项")
                
        # 总体评价
        print("\n" + "="*50)
        if error_count == 0:
            print("🎉 项目验证通过！所有演示案例结构完整，可以正常使用。")
            if warning_count > 0:
                print(f"⚠️  建议处理 {warning_count} 个警告项以进一步完善项目。")
        else:
            print(f"❌ 项目验证失败！存在 {error_count} 个错误需要修复。")
            
        print("="*50)
        
        return error_count == 0

def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    validator = LinuxDemoValidator(project_root)
    
    print("🚀 开始Linux命令演示项目验证...")
    print(f"项目根目录: {project_root}")
    
    # 执行各项验证
    validator.validate_project_structure()
    validator.validate_metadata_format()
    validator.validate_script_files()
    validator.validate_documentation()
    
    # 生成报告
    is_valid = validator.generate_report()
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    exit(main())