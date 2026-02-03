#!/usr/bin/env python
"""
最小化 Demo 生成脚本 - 快速生成满足最低要求的 Demo
每种语言生成 20 个核心 Demo
"""

import subprocess
import time
import sys
from pathlib import Path

# 精选最重要的 20 个概念
GO_DEMOS = [
    ("variables types", "beginner"),
    ("arrays slices", "beginner"),
    ("maps", "beginner"),
    ("functions", "beginner"),
    ("structs", "beginner"),
    ("interfaces", "intermediate"),
    ("goroutines", "intermediate"),
    ("channels", "intermediate"),
    ("error-handling", "beginner"),
    ("json", "beginner"),
    ("file-io", "beginner"),
    ("http-client", "intermediate"),
    ("defer", "beginner"),
    ("closures", "intermediate"),
    ("select", "intermediate"),
    ("sync mutex waitgroup", "intermediate"),
    ("time", "beginner"),
    ("strings", "beginner"),
    ("constants enums iota", "beginner"),
    ("panic recover", "intermediate"),
]

NODEJS_DEMOS = [
    ("variables types", "beginner"),
    ("arrow-functions", "beginner"),
    ("destructuring", "beginner"),
    ("promises", "intermediate"),
    ("async-await", "intermediate"),
    ("callbacks", "beginner"),
    ("functions", "beginner"),
    ("array-methods", "beginner"),
    ("fs file-system", "beginner"),
    ("http-module", "intermediate"),
    ("event-emitter", "intermediate"),
    ("buffer", "intermediate"),
    ("streams", "intermediate"),
    ("path", "beginner"),
    ("json", "beginner"),
    ("error-handling", "intermediate"),
    ("classes inheritance", "intermediate"),
    ("closures", "intermediate"),
    ("map-set", "beginner"),
    ("spread-operator", "beginner"),
]


def generate_demo(language, topic, difficulty):
    """生成单个 Demo"""
    cmd = ["python", "-m", "opendemo", "new", language, topic, "--difficulty", difficulty]

    print(f"\n{'='*60}")
    print(f"[{language.upper()}] 正在生成: {topic}")
    print(f"{'='*60}")

    try:
        process = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        stdout, stderr = process.communicate(input="n\n", timeout=180)

        if process.returncode == 0 and "Demo生成成功!" in stdout:
            print(f"✓ 成功: {topic}")
            return True
        else:
            print(f"✗ 失败: {topic}")
            if stderr:
                print(f"错误: {stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ 超时: {topic}")
        process.kill()
        return False
    except Exception as e:
        print(f"✗ 异常: {topic} - {str(e)}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("快速生成最小化 Demo 集合")
    print("目标: Go 20个, Node.js 20个")
    print("=" * 60 + "\n")

    results = {"go": {"success": 0, "failed": 0}, "nodejs": {"success": 0, "failed": 0}}

    # 生成 Go Demos
    print("\n" + "#" * 60)
    print("阶段 1: 生成 Go 语言 Demo (20个)")
    print("#" * 60)
    for i, (topic, difficulty) in enumerate(GO_DEMOS, 1):
        print(f"\n进度: {i}/20")
        if generate_demo("go", topic, difficulty):
            results["go"]["success"] += 1
        else:
            results["go"]["failed"] += 1

        if i < len(GO_DEMOS):
            time.sleep(3)  # 间隔 3 秒

    # 生成 Node.js Demos
    print("\n" + "#" * 60)
    print("阶段 2: 生成 Node.js Demo (20个)")
    print("#" * 60)
    for i, (topic, difficulty) in enumerate(NODEJS_DEMOS, 1):
        print(f"\n进度: {i}/20")
        if generate_demo("nodejs", topic, difficulty):
            results["nodejs"]["success"] += 1
        else:
            results["nodejs"]["failed"] += 1

        if i < len(NODEJS_DEMOS):
            time.sleep(3)  # 间隔 3 秒

    # 打印汇总
    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)
    print(f"\nGo 语言:")
    print(f"  成功: {results['go']['success']}/20")
    print(f"  失败: {results['go']['failed']}/20")
    print(f"  成功率: {results['go']['success']/20*100:.1f}%")

    print(f"\nNode.js:")
    print(f"  成功: {results['nodejs']['success']}/20")
    print(f"  失败: {results['nodejs']['failed']}/20")
    print(f"  成功率: {results['nodejs']['success']/20*100:.1f}%")

    total_success = results["go"]["success"] + results["nodejs"]["success"]
    print(f"\n总计: {total_success}/40 成功")
    print("=" * 60 + "\n")

    return results


if __name__ == "__main__":
    results = main()
    sys.exit(0 if results["go"]["success"] >= 18 and results["nodejs"]["success"] >= 18 else 1)
