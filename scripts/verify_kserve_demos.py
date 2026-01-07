"""
KServe Demo 批量验证脚本

验证所有 KServe Demo 的静态和 Dry-run 完整性
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from opendemo.services.config_service import ConfigService
from opendemo.core.demo_verifier import DemoVerifier
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


def get_kserve_demos(kubeflow_path: Path) -> List[Path]:
    """
    获取所有 KServe Demo 路径
    
    Args:
        kubeflow_path: kubeflow 目录路径
        
    Returns:
        KServe Demo 路径列表
    """
    kserve_demos = []
    
    if not kubeflow_path.exists():
        logger.error(f"Kubeflow directory not found: {kubeflow_path}")
        return kserve_demos
    
    for demo_dir in kubeflow_path.iterdir():
        if demo_dir.is_dir() and demo_dir.name.startswith("kserve-"):
            kserve_demos.append(demo_dir)
    
    logger.info(f"Found {len(kserve_demos)} KServe demos")
    return sorted(kserve_demos)


def verify_demo(verifier: DemoVerifier, demo_path: Path) -> Dict[str, Any]:
    """
    验证单个 Demo
    
    Args:
        verifier: 验证器实例
        demo_path: Demo 路径
        
    Returns:
        验证结果字典
    """
    logger.info(f"Verifying demo: {demo_path.name}")
    
    result = verifier.verify(demo_path, "kubernetes")
    
    # 添加Demo信息
    result["demo_name"] = demo_path.name
    result["demo_path"] = str(demo_path)
    
    # 检查文件结构
    has_metadata = (demo_path / "metadata.json").exists()
    has_readme = (demo_path / "README.md").exists()
    yaml_files = list(demo_path.rglob("*.yaml")) + list(demo_path.rglob("*.yml"))
    has_yaml = len(yaml_files) > 0
    
    result["file_structure"] = {
        "metadata": has_metadata,
        "readme": has_readme,
        "yaml_files": len(yaml_files),
        "has_yaml": has_yaml,
    }
    
    return result


def generate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成验证摘要
    
    Args:
        results: 所有验证结果
        
    Returns:
        摘要信息字典
    """
    total = len(results)
    verified = sum(1 for r in results if r.get("verified", False))
    partial = sum(1 for r in results if r.get("partial", False))
    failed = total - verified - partial
    
    # 文件结构统计
    with_metadata = sum(1 for r in results if r.get("file_structure", {}).get("metadata", False))
    with_readme = sum(1 for r in results if r.get("file_structure", {}).get("readme", False))
    with_yaml = sum(1 for r in results if r.get("file_structure", {}).get("has_yaml", False))
    
    # 错误和警告统计
    total_errors = sum(len(r.get("errors", [])) for r in results)
    total_warnings = sum(len(r.get("warnings", [])) for r in results)
    
    return {
        "total_demos": total,
        "verified": verified,
        "partial_verified": partial,
        "failed": failed,
        "pass_rate": f"{(verified / max(total, 1)) * 100:.1f}%",
        "file_structure": {
            "with_metadata": with_metadata,
            "with_readme": with_readme,
            "with_yaml": with_yaml,
        },
        "issues": {
            "total_errors": total_errors,
            "total_warnings": total_warnings,
        },
    }


def save_results(results: List[Dict[str, Any]], summary: Dict[str, Any], output_dir: Path):
    """
    保存验证结果
    
    Args:
        results: 验证结果列表
        summary: 摘要信息
        output_dir: 输出目录
    """
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存JSON格式结果
    json_file = output_dir / f"kserve_verification_{timestamp}.json"
    full_report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "results": results,
    }
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Verification results saved to: {json_file}")
    
    # 保存Markdown格式报告
    md_file = output_dir / f"kserve_verification_{timestamp}.md"
    md_content = generate_markdown_report(summary, results)
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    logger.info(f"Markdown report saved to: {md_file}")


def generate_markdown_report(summary: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
    """
    生成 Markdown 格式报告
    
    Args:
        summary: 摘要信息
        results: 验证结果列表
        
    Returns:
        Markdown 格式的报告内容
    """
    lines = [
        "# KServe Demo 验证报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 验证摘要",
        "",
        f"- **总计**: {summary['total_demos']} 个 Demo",
        f"- **完全验证**: {summary['verified']} 个",
        f"- **部分验证**: {summary['partial_verified']} 个",
        f"- **失败**: {summary['failed']} 个",
        f"- **通过率**: {summary['pass_rate']}",
        "",
        "### 文件结构统计",
        "",
        f"- **包含 metadata.json**: {summary['file_structure']['with_metadata']} 个",
        f"- **包含 README.md**: {summary['file_structure']['with_readme']} 个",
        f"- **包含 YAML 文件**: {summary['file_structure']['with_yaml']} 个",
        "",
        "### 问题统计",
        "",
        f"- **错误总数**: {summary['issues']['total_errors']}",
        f"- **警告总数**: {summary['issues']['total_warnings']}",
        "",
        "## 详细结果",
        "",
        "| Demo 名称 | 状态 | Metadata | README | YAML | 错误 | 警告 |",
        "|----------|------|----------|--------|------|------|------|",
    ]
    
    for result in results:
        demo_name = result.get("demo_name", "unknown")
        verified = result.get("verified", False)
        partial = result.get("partial", False)
        
        if verified and not partial:
            status = "✅ 通过"
        elif partial:
            status = "⚠️ 部分"
        else:
            status = "❌ 失败"
        
        fs = result.get("file_structure", {})
        metadata_icon = "✅" if fs.get("metadata") else "❌"
        readme_icon = "✅" if fs.get("readme") else "❌"
        yaml_count = fs.get("yaml_files", 0)
        yaml_info = f"{yaml_count}个" if yaml_count > 0 else "❌"
        
        error_count = len(result.get("errors", []))
        warning_count = len(result.get("warnings", []))
        
        lines.append(
            f"| {demo_name} | {status} | {metadata_icon} | {readme_icon} | {yaml_info} | {error_count} | {warning_count} |"
        )
    
    lines.extend([
        "",
        "## 失败案例详情",
        "",
    ])
    
    failed_demos = [r for r in results if not r.get("verified", False) or r.get("errors")]
    
    if failed_demos:
        for result in failed_demos:
            demo_name = result.get("demo_name", "unknown")
            lines.append(f"### {demo_name}")
            lines.append("")
            
            errors = result.get("errors", [])
            if errors:
                lines.append("**错误**:")
                for error in errors:
                    lines.append(f"- {error}")
                lines.append("")
            
            warnings = result.get("warnings", [])
            if warnings:
                lines.append("**警告**:")
                for warning in warnings:
                    lines.append(f"- {warning}")
                lines.append("")
    else:
        lines.append("无失败案例 ✅")
        lines.append("")
    
    return "\n".join(lines)


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("KServe Demo 批量验证工具")
    logger.info("="*60)
    
    # 初始化服务
    config_service = ConfigService()
    verifier = DemoVerifier(config_service)
    
    # 获取KServe Demo路径
    kubeflow_path = project_root / "opendemo_output" / "kubernetes" / "kubeflow"
    kserve_demos = get_kserve_demos(kubeflow_path)
    
    if not kserve_demos:
        logger.error("No KServe demos found")
        sys.exit(1)
    
    logger.info(f"Starting verification of {len(kserve_demos)} demos...")
    logger.info("")
    
    # 验证所有Demo
    results = []
    for idx, demo_path in enumerate(kserve_demos, 1):
        logger.info(f"[{idx}/{len(kserve_demos)}] Verifying: {demo_path.name}")
        
        result = verify_demo(verifier, demo_path)
        results.append(result)
        
        status = "✅ 通过" if result.get("verified") else "❌ 失败"
        logger.info(f"  Result: {status}")
        
        if result.get("errors"):
            for error in result["errors"]:
                logger.error(f"    Error: {error}")
        
        if result.get("warnings"):
            for warning in result["warnings"][:3]:  # 只显示前3个警告
                logger.warning(f"    Warning: {warning}")
        
        logger.info("")
    
    # 生成摘要
    summary = generate_summary(results)
    
    logger.info("="*60)
    logger.info("验证摘要")
    logger.info("="*60)
    logger.info(f"总计: {summary['total_demos']} 个Demo")
    logger.info(f"完全验证: {summary['verified']} 个")
    logger.info(f"部分验证: {summary['partial_verified']} 个")
    logger.info(f"失败: {summary['failed']} 个")
    logger.info(f"通过率: {summary['pass_rate']}")
    logger.info("")
    
    # 保存结果
    output_dir = project_root / "check"
    save_results(results, summary, output_dir)
    
    logger.info("="*60)
    logger.info("验证完成")
    logger.info("="*60)
    
    # 根据结果设置退出码
    sys.exit(0 if summary['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
"""
KServe Demo 批量验证脚本

验证所有 KServe Demo 的静态和 Dry-run 完整性
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from opendemo.services.config_service import ConfigService
from opendemo.core.demo_verifier import DemoVerifier
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


def get_kserve_demos(kubeflow_path: Path) -> List[Path]:
    """
    获取所有 KServe Demo 路径
    
    Args:
        kubeflow_path: kubeflow 目录路径
        
    Returns:
        KServe Demo 路径列表
    """
    kserve_demos = []
    
    if not kubeflow_path.exists():
        logger.error(f"Kubeflow directory not found: {kubeflow_path}")
        return kserve_demos
    
    for demo_dir in kubeflow_path.iterdir():
        if demo_dir.is_dir() and demo_dir.name.startswith("kserve-"):
            kserve_demos.append(demo_dir)
    
    logger.info(f"Found {len(kserve_demos)} KServe demos")
    return sorted(kserve_demos)


def verify_demo(verifier: DemoVerifier, demo_path: Path) -> Dict[str, Any]:
    """
    验证单个 Demo
    
    Args:
        verifier: 验证器实例
        demo_path: Demo 路径
        
    Returns:
        验证结果字典
    """
    logger.info(f"Verifying demo: {demo_path.name}")
    
    result = verifier.verify(demo_path, "kubernetes")
    
    # 添加Demo信息
    result["demo_name"] = demo_path.name
    result["demo_path"] = str(demo_path)
    
    # 检查文件结构
    has_metadata = (demo_path / "metadata.json").exists()
    has_readme = (demo_path / "README.md").exists()
    yaml_files = list(demo_path.rglob("*.yaml")) + list(demo_path.rglob("*.yml"))
    has_yaml = len(yaml_files) > 0
    
    result["file_structure"] = {
        "metadata": has_metadata,
        "readme": has_readme,
        "yaml_files": len(yaml_files),
        "has_yaml": has_yaml,
    }
    
    return result


def generate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成验证摘要
    
    Args:
        results: 所有验证结果
        
    Returns:
        摘要信息字典
    """
    total = len(results)
    verified = sum(1 for r in results if r.get("verified", False))
    partial = sum(1 for r in results if r.get("partial", False))
    failed = total - verified - partial
    
    # 文件结构统计
    with_metadata = sum(1 for r in results if r.get("file_structure", {}).get("metadata", False))
    with_readme = sum(1 for r in results if r.get("file_structure", {}).get("readme", False))
    with_yaml = sum(1 for r in results if r.get("file_structure", {}).get("has_yaml", False))
    
    # 错误和警告统计
    total_errors = sum(len(r.get("errors", [])) for r in results)
    total_warnings = sum(len(r.get("warnings", [])) for r in results)
    
    return {
        "total_demos": total,
        "verified": verified,
        "partial_verified": partial,
        "failed": failed,
        "pass_rate": f"{(verified / max(total, 1)) * 100:.1f}%",
        "file_structure": {
            "with_metadata": with_metadata,
            "with_readme": with_readme,
            "with_yaml": with_yaml,
        },
        "issues": {
            "total_errors": total_errors,
            "total_warnings": total_warnings,
        },
    }


def save_results(results: List[Dict[str, Any]], summary: Dict[str, Any], output_dir: Path):
    """
    保存验证结果
    
    Args:
        results: 验证结果列表
        summary: 摘要信息
        output_dir: 输出目录
    """
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存JSON格式结果
    json_file = output_dir / f"kserve_verification_{timestamp}.json"
    full_report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "results": results,
    }
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Verification results saved to: {json_file}")
    
    # 保存Markdown格式报告
    md_file = output_dir / f"kserve_verification_{timestamp}.md"
    md_content = generate_markdown_report(summary, results)
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    logger.info(f"Markdown report saved to: {md_file}")


def generate_markdown_report(summary: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
    """
    生成 Markdown 格式报告
    
    Args:
        summary: 摘要信息
        results: 验证结果列表
        
    Returns:
        Markdown 格式的报告内容
    """
    lines = [
        "# KServe Demo 验证报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 验证摘要",
        "",
        f"- **总计**: {summary['total_demos']} 个 Demo",
        f"- **完全验证**: {summary['verified']} 个",
        f"- **部分验证**: {summary['partial_verified']} 个",
        f"- **失败**: {summary['failed']} 个",
        f"- **通过率**: {summary['pass_rate']}",
        "",
        "### 文件结构统计",
        "",
        f"- **包含 metadata.json**: {summary['file_structure']['with_metadata']} 个",
        f"- **包含 README.md**: {summary['file_structure']['with_readme']} 个",
        f"- **包含 YAML 文件**: {summary['file_structure']['with_yaml']} 个",
        "",
        "### 问题统计",
        "",
        f"- **错误总数**: {summary['issues']['total_errors']}",
        f"- **警告总数**: {summary['issues']['total_warnings']}",
        "",
        "## 详细结果",
        "",
        "| Demo 名称 | 状态 | Metadata | README | YAML | 错误 | 警告 |",
        "|----------|------|----------|--------|------|------|------|",
    ]
    
    for result in results:
        demo_name = result.get("demo_name", "unknown")
        verified = result.get("verified", False)
        partial = result.get("partial", False)
        
        if verified and not partial:
            status = "✅ 通过"
        elif partial:
            status = "⚠️ 部分"
        else:
            status = "❌ 失败"
        
        fs = result.get("file_structure", {})
        metadata_icon = "✅" if fs.get("metadata") else "❌"
        readme_icon = "✅" if fs.get("readme") else "❌"
        yaml_count = fs.get("yaml_files", 0)
        yaml_info = f"{yaml_count}个" if yaml_count > 0 else "❌"
        
        error_count = len(result.get("errors", []))
        warning_count = len(result.get("warnings", []))
        
        lines.append(
            f"| {demo_name} | {status} | {metadata_icon} | {readme_icon} | {yaml_info} | {error_count} | {warning_count} |"
        )
    
    lines.extend([
        "",
        "## 失败案例详情",
        "",
    ])
    
    failed_demos = [r for r in results if not r.get("verified", False) or r.get("errors")]
    
    if failed_demos:
        for result in failed_demos:
            demo_name = result.get("demo_name", "unknown")
            lines.append(f"### {demo_name}")
            lines.append("")
            
            errors = result.get("errors", [])
            if errors:
                lines.append("**错误**:")
                for error in errors:
                    lines.append(f"- {error}")
                lines.append("")
            
            warnings = result.get("warnings", [])
            if warnings:
                lines.append("**警告**:")
                for warning in warnings:
                    lines.append(f"- {warning}")
                lines.append("")
    else:
        lines.append("无失败案例 ✅")
        lines.append("")
    
    return "\n".join(lines)


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("KServe Demo 批量验证工具")
    logger.info("="*60)
    
    # 初始化服务
    config_service = ConfigService()
    verifier = DemoVerifier(config_service)
    
    # 获取KServe Demo路径
    kubeflow_path = project_root / "opendemo_output" / "kubernetes" / "kubeflow"
    kserve_demos = get_kserve_demos(kubeflow_path)
    
    if not kserve_demos:
        logger.error("No KServe demos found")
        sys.exit(1)
    
    logger.info(f"Starting verification of {len(kserve_demos)} demos...")
    logger.info("")
    
    # 验证所有Demo
    results = []
    for idx, demo_path in enumerate(kserve_demos, 1):
        logger.info(f"[{idx}/{len(kserve_demos)}] Verifying: {demo_path.name}")
        
        result = verify_demo(verifier, demo_path)
        results.append(result)
        
        status = "✅ 通过" if result.get("verified") else "❌ 失败"
        logger.info(f"  Result: {status}")
        
        if result.get("errors"):
            for error in result["errors"]:
                logger.error(f"    Error: {error}")
        
        if result.get("warnings"):
            for warning in result["warnings"][:3]:  # 只显示前3个警告
                logger.warning(f"    Warning: {warning}")
        
        logger.info("")
    
    # 生成摘要
    summary = generate_summary(results)
    
    logger.info("="*60)
    logger.info("验证摘要")
    logger.info("="*60)
    logger.info(f"总计: {summary['total_demos']} 个Demo")
    logger.info(f"完全验证: {summary['verified']} 个")
    logger.info(f"部分验证: {summary['partial_verified']} 个")
    logger.info(f"失败: {summary['failed']} 个")
    logger.info(f"通过率: {summary['pass_rate']}")
    logger.info("")
    
    # 保存结果
    output_dir = project_root / "check"
    save_results(results, summary, output_dir)
    
    logger.info("="*60)
    logger.info("验证完成")
    logger.info("="*60)
    
    # 根据结果设置退出码
    sys.exit(0 if summary['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
