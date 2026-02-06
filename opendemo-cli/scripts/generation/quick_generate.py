#!/usr/bin/env python
"""
快速生成核心 Demo 脚本 - 生成足够数量的 Demo 用于验证系统
"""

import subprocess
import time
from pathlib import Path

# 精选的核心 Demo 列表
DEMOS = {
    "go": [
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
        ("context", "intermediate"),
        ("defer", "beginner"),
        ("closures", "intermediate"),
        ("select", "intermediate"),
        ("sync mutex waitgroup", "intermediate"),
        ("embedding", "intermediate"),
        ("time", "beginner"),
        ("strings", "beginner"),
        ("constants enums iota", "beginner"),
        ("panic recover", "intermediate"),
    ],
    "nodejs": [
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
        ("template-strings", "beginner"),
        ("higher-order-functions", "intermediate"),
    ],
}


def generate_demo(language, topic, difficulty, output_file):
    """生成单个 Demo 并记录结果"""
    cmd = ["python", "-m", "opendemo", "new", language, topic, "--difficulty", difficulty]

    print(f"\n正在生成: {language} - {topic}")

    try:
        # 创建子进程并自动输入 'n' 来跳过贡献询问
        process = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # 发送 'n' 并等待完成
        stdout, stderr = process.communicate(input="n\n", timeout=120)

        if process.returncode == 0 and "Demo生成成功!" in stdout:
            print(f"✓ 成功: {language} - {topic}")
            output_file.write(f"SUCCESS,{language},{topic},{difficulty}\n")
            return True
        else:
            print(f"✗ 失败: {language} - {topic}")
            output_file.write(f"FAILED,{language},{topic},{difficulty}\n")
            return False

    except Exception as e:
        print(f"✗ 异常: {language} - {topic} - {str(e)}")
        output_file.write(f"ERROR,{language},{topic},{difficulty},{str(e)}\n")
        return False


def main():
    log_file = Path("demo_generation_log.csv")

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("STATUS,LANGUAGE,TOPIC,DIFFICULTY,ERROR\n")

        total = 0
        success = 0

        # 生成 Go Demos
        print("\n" + "=" * 60)
        print("生成 Go 语言 Demo")
        print("=" * 60)
        for topic, difficulty in DEMOS["go"]:
            if generate_demo("go", topic, difficulty, f):
                success += 1
            total += 1
            time.sleep(2)  # 避免 API 限流

        # 生成 Node.js Demos
        print("\n" + "=" * 60)
        print("生成 Node.js Demo")
        print("=" * 60)
        for topic, difficulty in DEMOS["nodejs"]:
            if generate_demo("nodejs", topic, difficulty, f):
                success += 1
            total += 1
            time.sleep(2)  # 避免 API 限流

    print("\n" + "=" * 60)
    print("生成完成！")
    print(f"总数: {total}")
    print(f"成功: {success}")
    print(f"失败: {total - success}")
    print(f"成功率: {success/total*100:.1f}%")
    print(f"日志已保存至: {log_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
