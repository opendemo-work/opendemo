#!/usr/bin/env python3
"""
Java案例质量检查和验证工具

用于批量检查和验证Java技术栈案例的质量和可执行性。
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 修改导入路径
sys.path.insert(0, str(project_root / "cli"))

from services.java_verifier import JavaVerifier
from services.java_quality_checker import JavaQualityChecker
from core.demo_verifier import DemoVerifier
from utils.logger import get_logger

logger = get_logger(__name__)


class JavaDemoValidator:
    """Java案例验证器"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or project_root
        self.java_root = self.project_root / "java"
        
        # 模拟配置服务
        self.config = {
            "enable_verification": True,
            "verification_method": "direct",
            "verification_timeout": 300,
            "minimum_readme_length": 500
        }

    def validate_all_java_demos(self) -> Dict[str, Any]:
        """验证所有Java案例"""
        results = {
            "summary": {
                "total_demos": 0,
                "verified_demos": 0,
                "quality_passed": 0,
                "overall_pass_rate": 0
            },
            "demos": {}
        }
        
        if not self.java_root.exists():
            logger.error("Java目录不存在")
            return results
            
        # 查找所有Java案例目录
        java_demos = [d for d in self.java_root.iterdir() 
                     if d.is_dir() and not d.name.startswith('.')]
        
        results["summary"]["total_demos"] = len(java_demos)
        
        for demo_dir in java_demos:
            demo_name = demo_dir.name
            logger.info(f"正在验证案例: {demo_name}")
            
            demo_result = self.validate_single_demo(demo_dir)
            results["demos"][demo_name] = demo_result
            
            if demo_result["verification"]["verified"]:
                results["summary"]["verified_demos"] += 1
                
            if demo_result["quality"]["passed"]:
                results["summary"]["quality_passed"] += 1
        
        # 计算总体通过率
        if results["summary"]["total_demos"] > 0:
            results["summary"]["overall_pass_rate"] = (
                results["summary"]["verified_demos"] / results["summary"]["total_demos"]
            ) * 100
            
        return results

    def validate_single_demo(self, demo_path: Path) -> Dict[str, Any]:
        """验证单个Java案例"""
        result = {
            "path": str(demo_path),
            "verification": {},
            "quality": {},
            "timestamp": ""
        }
        
        try:
            # 执行验证
            verifier = JavaVerifier(self.config)
            result["verification"] = verifier.verify(demo_path)
            
            # 执行质量检查
            quality_checker = JavaQualityChecker(self.config)
            result["quality"] = quality_checker.check_quality(demo_path)
            
            result["timestamp"] = "2026-01-31"  # 固定时间戳用于演示
            
        except Exception as e:
            logger.error(f"验证案例 {demo_path.name} 时出错: {e}")
            result["verification"] = {
                "verified": False,
                "errors": [f"验证异常: {str(e)}"]
            }
            result["quality"] = {
                "passed": False,
                "issues": [f"质量检查异常: {str(e)}"]
            }
            
        return result

    def generate_report(self, results: Dict[str, Any], output_file: Path = None):
        """生成验证报告"""
        report = {
            "report_title": "Java案例质量验证报告",
            "generated_at": "2026-01-31",
            "summary": results["summary"],
            "detailed_results": {}
        }
        
        # 整理详细结果
        for demo_name, demo_result in results["demos"].items():
            report["detailed_results"][demo_name] = {
                "verification_status": "通过" if demo_result["verification"]["verified"] else "失败",
                "quality_status": "通过" if demo_result["quality"]["passed"] else "失败",
                "quality_score": demo_result["quality"]["score"],
                "verification_steps": demo_result["verification"].get("steps", []),
                "verification_errors": demo_result["verification"].get("errors", []),
                "quality_issues": demo_result["quality"].get("issues", []),
                "recommendations": demo_result["quality"].get("recommendations", [])
            }
        
        # 输出到文件或控制台
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            logger.info(f"报告已保存到: {output_file}")
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))

    def fix_common_issues(self, demo_path: Path) -> List[str]:
        """修复常见问题"""
        fixed_issues = []
        
        try:
            # 1. 检查并创建标准目录结构
            src_main_java = demo_path / "src" / "main" / "java"
            if not src_main_java.exists():
                src_main_java.mkdir(parents=True, exist_ok=True)
                fixed_issues.append("创建标准目录结构: src/main/java")
            
            # 2. 检查README文件
            readme_path = demo_path / "README.md"
            if not readme_path.exists():
                # 创建基础README模板
                basic_readme = f"""# {demo_path.name}

## 学习目标

## 环境准备

## 项目结构

## 快速开始

## 代码详解

## 验证测试

## 常见问题
"""
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(basic_readme)
                fixed_issues.append("创建基础README.md模板")
            
            # 3. 检查metadata.json
            metadata_path = demo_path / "metadata.json"
            if not metadata_path.exists():
                basic_metadata = {
                    "name": demo_path.name,
                    "language": "java",
                    "keywords": ["java", "demo"],
                    "description": f"{demo_path.name} Java演示案例",
                    "difficulty": "beginner",
                    "author": "OpenDemo Team",
                    "created_at": "2026-01-31",
                    "updated_at": "2026-01-31",
                    "version": "1.0.0"
                }
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(basic_metadata, f, ensure_ascii=False, indent=2)
                fixed_issues.append("创建基础metadata.json")
                
        except Exception as e:
            fixed_issues.append(f"修复过程中出现错误: {str(e)}")
            
        return fixed_issues


def main():
    parser = argparse.ArgumentParser(description="Java案例质量验证工具")
    parser.add_argument("--validate-all", action="store_true", 
                       help="验证所有Java案例")
    parser.add_argument("--validate-demo", type=str, 
                       help="验证指定的Java案例目录")
    parser.add_argument("--fix-issues", type=str,
                       help="修复指定案例的常见问题")
    parser.add_argument("--report", type=str,
                       help="生成报告文件路径")
    parser.add_argument("--verbose", action="store_true",
                       help="显示详细输出")
    
    args = parser.parse_args()
    
    validator = JavaDemoValidator()
    
    if args.validate_all:
        logger.info("开始验证所有Java案例...")
        results = validator.validate_all_java_demos()
        
        if args.report:
            validator.generate_report(results, Path(args.report))
        else:
            validator.generate_report(results)
            
    elif args.validate_demo:
        demo_path = Path(args.validate_demo)
        if not demo_path.exists():
            logger.error(f"案例目录不存在: {args.validate_demo}")
            return 1
            
        logger.info(f"验证案例: {demo_path.name}")
        result = validator.validate_single_demo(demo_path)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.fix_issues:
        demo_path = Path(args.fix_issues)
        if not demo_path.exists():
            logger.error(f"案例目录不存在: {args.fix_issues}")
            return 1
            
        logger.info(f"修复案例问题: {demo_path.name}")
        fixed_issues = validator.fix_common_issues(demo_path)
        
        if fixed_issues:
            print("已修复的问题:")
            for issue in fixed_issues:
                print(f"  - {issue}")
        else:
            print("未发现需要修复的问题")
            
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())