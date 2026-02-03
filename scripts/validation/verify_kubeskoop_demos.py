"""
KubeSkoop Demo 批量验证脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from opendemo.services.config_service import ConfigService
from opendemo.core.demo_verifier import DemoVerifier


def verify_all_kubeskoop_demos():
    """验证所有KubeSkoop Demo"""
    # 初始化服务
    config = ConfigService()
    verifier = DemoVerifier(config)

    # KubeSkoop Demo 目录
    kubeskoop_dir = project_root / "opendemo_output" / "kubernetes" / "kubeskoop"

    if not kubeskoop_dir.exists():
        print("❌ KubeSkoop目录不存在")
        return

    # 获取所有Demo目录
    demo_dirs = [d for d in kubeskoop_dir.iterdir() if d.is_dir()]

    print(f"\n{'='*60}")
    print(f"开始验证 {len(demo_dirs)} 个 KubeSkoop Demo")
    print(f"{'='*60}\n")

    results = []

    for demo_dir in sorted(demo_dirs):
        print(f"\n[{len(results)+1}/{len(demo_dirs)}] 验证: {demo_dir.name}")
        print("-" * 60)

        # 执行验证
        result = verifier._verify_kubernetes(demo_dir)

        # 记录结果
        results.append(
            {
                "name": demo_dir.name,
                "verified": result.get("verified", False),
                "partial": result.get("partial", False),
                "steps": len(result.get("steps", [])),
                "errors": len(result.get("errors", [])),
                "warnings": len(result.get("warnings", [])),
                "result": result,
            }
        )

        # 显示结果
        if result.get("verified"):
            if result.get("partial"):
                print("✓ 部分验证通过")
            else:
                print("✓ 完全验证通过")
        else:
            print("✗ 验证失败")

        # 显示步骤
        steps = result.get("steps", [])
        if steps:
            print(f"\n执行步骤 ({len(steps)}):")
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {step}")

        # 显示警告
        warnings = result.get("warnings", [])
        if warnings:
            print(f"\n警告 ({len(warnings)}):")
            for warning in warnings:
                print(f"  ⚠ {warning}")

        # 显示错误
        errors = result.get("errors", [])
        if errors:
            print(f"\n错误 ({len(errors)}):")
            for error in errors:
                print(f"  ✗ {error}")

    # 生成总结报告
    print(f"\n\n{'='*60}")
    print("验证总结报告")
    print(f"{'='*60}\n")

    total = len(results)
    fully_verified = sum(1 for r in results if r["verified"] and not r["partial"])
    partially_verified = sum(1 for r in results if r["verified"] and r["partial"])
    failed = sum(1 for r in results if not r["verified"])

    print(f"总计: {total} 个Demo")
    print(f"完全验证通过: {fully_verified} 个")
    print(f"部分验证通过: {partially_verified} 个")
    print(f"验证失败: {failed} 个")

    pass_rate = ((fully_verified + partially_verified) / total * 100) if total > 0 else 0
    print(f"\n验证通过率: {pass_rate:.1f}%")

    if pass_rate >= 80:
        print("\n✓ 达到设计目标 (≥80% 通过率)")
    else:
        print("\n✗ 未达到设计目标 (需要≥80% 通过率)")

    # 显示详细列表
    print(f"\n\n详细列表:")
    print(f"{'Demo名称':<50} {'状态':<15} {'步骤':<8} {'警告':<8} {'错误':<8}")
    print("-" * 95)

    for r in results:
        status = (
            "✓ 完全通过"
            if (r["verified"] and not r["partial"])
            else "✓ 部分通过" if r["verified"] else "✗ 失败"
        )
        print(f"{r['name']:<50} {status:<15} {r['steps']:<8} {r['warnings']:<8} {r['errors']:<8}")

    print("\n")

    return pass_rate >= 80


if __name__ == "__main__":
    success = verify_all_kubeskoop_demos()
    sys.exit(0 if success else 1)
