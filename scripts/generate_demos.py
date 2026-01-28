#!/usr/bin/env python
"""
批量生成 Demo 脚本

用于批量生成 Go 和 Node.js 的核心概念 Demo
"""

import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

# Go 语言核心概念清单
GO_DEMOS = [
    # 批次1：基础语法类
    {"topic": "variables types", "difficulty": "beginner", "desc": "变量声明、基本类型、类型推断"},
    {"topic": "constants enums iota", "difficulty": "beginner", "desc": "常量定义、iota 枚举"},
    {"topic": "control-flow if-switch-for", "difficulty": "beginner", "desc": "条件语句、循环结构"},
    {"topic": "arrays slices", "difficulty": "beginner", "desc": "数组、切片操作和内存模型"},
    {"topic": "maps", "difficulty": "beginner", "desc": "map 的创建、操作、遍历"},
    {"topic": "strings", "difficulty": "beginner", "desc": "字符串操作、格式化"},
    # 批次2：并发编程类
    {"topic": "goroutines", "difficulty": "intermediate", "desc": "协程创建和使用"},
    {"topic": "channels", "difficulty": "intermediate", "desc": "通道的创建、发送、接收"},
    {"topic": "select", "difficulty": "intermediate", "desc": "select 多路复用"},
    {"topic": "sync mutex waitgroup", "difficulty": "intermediate", "desc": "sync 包的使用"},
    {"topic": "context", "difficulty": "intermediate", "desc": "上下文控制和取消"},
    # 批次3：函数与方法类
    {"topic": "functions", "difficulty": "beginner", "desc": "函数定义、多返回值、参数传递"},
    {"topic": "methods receivers", "difficulty": "intermediate", "desc": "值接收者、指针接收者"},
    {"topic": "closures", "difficulty": "intermediate", "desc": "闭包概念和应用"},
    {"topic": "defer", "difficulty": "beginner", "desc": "defer 语句的使用和执行顺序"},
    # 批次4：接口与类型系统类
    {"topic": "structs", "difficulty": "beginner", "desc": "结构体定义、嵌套、标签"},
    {"topic": "interfaces", "difficulty": "intermediate", "desc": "接口定义、实现、类型断言"},
    {"topic": "empty-interface", "difficulty": "intermediate", "desc": "interface{} 和泛型使用"},
    {"topic": "embedding", "difficulty": "intermediate", "desc": "结构体嵌入、方法提升"},
    # 批次5：错误处理类
    {"topic": "error-handling", "difficulty": "beginner", "desc": "error 接口、错误返回"},
    {"topic": "panic recover", "difficulty": "intermediate", "desc": "异常处理机制"},
    # 批次6：标准库类
    {"topic": "file-io", "difficulty": "beginner", "desc": "文件读写、os 包"},
    {"topic": "json", "difficulty": "beginner", "desc": "JSON 序列化和反序列化"},
    {"topic": "http-client", "difficulty": "intermediate", "desc": "net/http 客户端"},
    {"topic": "time", "difficulty": "beginner", "desc": "time 包的使用"},
]

# Node.js 核心概念清单
NODEJS_DEMOS = [
    # 批次1：基础语法类
    {"topic": "variables types", "difficulty": "beginner", "desc": "var/let/const、基本类型"},
    {"topic": "destructuring", "difficulty": "beginner", "desc": "对象和数组解构"},
    {"topic": "template-strings", "difficulty": "beginner", "desc": "模板字面量"},
    {"topic": "arrow-functions", "difficulty": "beginner", "desc": "箭头函数语法和 this 绑定"},
    {"topic": "spread-operator", "difficulty": "beginner", "desc": "展开语法和剩余参数"},
    {"topic": "array-methods", "difficulty": "beginner", "desc": "数组常用方法"},
    # 批次2：异步编程类
    {"topic": "callbacks", "difficulty": "beginner", "desc": "回调模式和回调地狱"},
    {"topic": "promises", "difficulty": "intermediate", "desc": "Promise 链式调用"},
    {"topic": "async-await", "difficulty": "intermediate", "desc": "异步函数语法"},
    {"topic": "event-emitter", "difficulty": "intermediate", "desc": "事件发射器模式"},
    # 批次3：函数类
    {"topic": "functions", "difficulty": "beginner", "desc": "函数声明、表达式、回调"},
    {
        "topic": "higher-order-functions",
        "difficulty": "intermediate",
        "desc": "map、filter、reduce",
    },
    {"topic": "closures", "difficulty": "intermediate", "desc": "闭包和作用域"},
    # 批次4：核心模块类
    {"topic": "fs file-system", "difficulty": "beginner", "desc": "fs 模块文件操作"},
    {"topic": "path", "difficulty": "beginner", "desc": "path 模块"},
    {"topic": "buffer", "difficulty": "intermediate", "desc": "Buffer 缓冲区操作"},
    {"topic": "streams", "difficulty": "intermediate", "desc": "流处理：Readable/Writable"},
    {"topic": "http-module", "difficulty": "intermediate", "desc": "原生 HTTP 服务器"},
    # 批次5：模块系统类
    {"topic": "commonjs require", "difficulty": "beginner", "desc": "require/module.exports"},
    {"topic": "es-modules import", "difficulty": "beginner", "desc": "import/export 语法"},
    # 批次6：现代特性类
    {"topic": "classes inheritance", "difficulty": "intermediate", "desc": "ES6 类语法"},
    {"topic": "map-set", "difficulty": "beginner", "desc": "Map、Set 数据结构"},
    {"topic": "json", "difficulty": "beginner", "desc": "JSON.parse/stringify"},
    {"topic": "error-handling", "difficulty": "intermediate", "desc": "try/catch、自定义错误"},
]


class DemoGenerator:
    """批量 Demo 生成器"""

    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.results = {
            "go": {"success": [], "failed": []},
            "nodejs": {"success": [], "failed": []},
        }

    def generate_demo(self, language, topic, difficulty, retry=2, delay=3):
        """
        生成单个 Demo

        Args:
            language: 语言
            topic: 主题
            difficulty: 难度
            retry: 重试次数
            delay: 请求间隔(秒)

        Returns:
            bool: 是否成功
        """
        cmd = ["python", "-m", "opendemo", "new", language, topic, "--difficulty", difficulty]

        for attempt in range(retry + 1):
            try:
                print(f"\n{'='*60}")
                print(f"正在生成: {language} - {topic} (难度: {difficulty})")
                print(f"尝试: {attempt + 1}/{retry + 1}")
                print(f"{'='*60}")

                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=600  # 10分钟超时
                )

                if result.returncode == 0:
                    print(f"✓ 成功生成: {language} - {topic}")
                    return True
                else:
                    print(f"✗ 生成失败: {language} - {topic}")
                    print(f"错误输出: {result.stderr}")

                    if attempt < retry:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)

            except subprocess.TimeoutExpired:
                print(f"✗ 超时: {language} - {topic}")
                if attempt < retry:
                    print(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)
            except Exception as e:
                print(f"✗ 异常: {language} - {topic} - {str(e)}")
                if attempt < retry:
                    print(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)

        return False

    def generate_batch(self, language, demos, batch_name=""):
        """
        批量生成 Demo

        Args:
            language: 语言
            demos: Demo 列表
            batch_name: 批次名称
        """
        print(f"\n{'#'*60}")
        print(f"开始生成 {batch_name} - {language}")
        print(f"总数: {len(demos)}")
        print(f"{'#'*60}\n")

        for i, demo in enumerate(demos, 1):
            print(f"\n进度: {i}/{len(demos)}")

            success = self.generate_demo(
                language=language, topic=demo["topic"], difficulty=demo["difficulty"]
            )

            if success:
                self.results[language]["success"].append(demo)
            else:
                self.results[language]["failed"].append(demo)

            # 请求间隔，避免 API 限流
            if i < len(demos):
                delay = 3
                print(f"\n等待 {delay} 秒后继续...")
                time.sleep(delay)

    def save_report(self):
        """保存生成报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.log_dir / f"generation_report_{timestamp}.json"

        report = {
            "timestamp": timestamp,
            "results": self.results,
            "summary": {
                "go": {
                    "total": len(self.results["go"]["success"]) + len(self.results["go"]["failed"]),
                    "success": len(self.results["go"]["success"]),
                    "failed": len(self.results["go"]["failed"]),
                    "success_rate": f"{len(self.results['go']['success']) / max(1, len(self.results['go']['success']) + len(self.results['go']['failed'])) * 100:.1f}%",
                },
                "nodejs": {
                    "total": len(self.results["nodejs"]["success"])
                    + len(self.results["nodejs"]["failed"]),
                    "success": len(self.results["nodejs"]["success"]),
                    "failed": len(self.results["nodejs"]["failed"]),
                    "success_rate": f"{len(self.results['nodejs']['success']) / max(1, len(self.results['nodejs']['success']) + len(self.results['nodejs']['failed'])) * 100:.1f}%",
                },
            },
        }

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n报告已保存至: {report_file}")
        return report

    def print_summary(self):
        """打印汇总信息"""
        print(f"\n{'='*60}")
        print("生成汇总")
        print(f"{'='*60}")

        for language in ["go", "nodejs"]:
            total = len(self.results[language]["success"]) + len(self.results[language]["failed"])
            success = len(self.results[language]["success"])
            failed = len(self.results[language]["failed"])
            rate = success / max(1, total) * 100

            print(f"\n{language.upper()}:")
            print(f"  总数: {total}")
            print(f"  成功: {success}")
            print(f"  失败: {failed}")
            print(f"  成功率: {rate:.1f}%")

            if failed > 0:
                print(f"\n  失败的 Demo:")
                for demo in self.results[language]["failed"]:
                    print(f"    - {demo['topic']} ({demo['difficulty']})")


def main():
    """主函数"""
    generator = DemoGenerator()

    print("=" * 60)
    print("批量生成 Go 和 Node.js Demo")
    print("=" * 60)

    # 生成 Go Demo - 批次1：基础语法
    generator.generate_batch("go", GO_DEMOS[:6], "批次1：基础语法")

    # 生成 Go Demo - 批次2：并发编程
    generator.generate_batch("go", GO_DEMOS[6:11], "批次2：并发编程")

    # 生成 Go Demo - 批次3-6：其他概念
    generator.generate_batch("go", GO_DEMOS[11:], "批次3-6：其他核心概念")

    # 生成 Node.js Demo - 批次1：基础语法
    generator.generate_batch("nodejs", NODEJS_DEMOS[:6], "批次1：基础语法")

    # 生成 Node.js Demo - 批次2：异步编程
    generator.generate_batch("nodejs", NODEJS_DEMOS[6:10], "批次2：异步编程")

    # 生成 Node.js Demo - 批次3-6：其他概念
    generator.generate_batch("nodejs", NODEJS_DEMOS[10:], "批次3-6：其他核心概念")

    # 保存报告并打印汇总
    generator.save_report()
    generator.print_summary()

    print(f"\n{'='*60}")
    print("批量生成完成！")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
