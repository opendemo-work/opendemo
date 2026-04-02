"""
check 命令模块

质量检查的命令实现。
"""

import sys

import click
from rich.console import Console
from rich.table import Table
from rich import box

from core.quality_checker import QualityChecker
from utils.formatters import print_info, print_success, print_warning


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="显示详细输出")
def check(verbose):
    """运行质量检查

    执行单元测试和CLI功能测试，生成检查报告。
    报告保存在项目根目录的 check 目录下。

    示例:
        opendemo check           # 运行检查并生成报告
        opendemo check -v        # 显示详细输出
    """
    console = Console()

    print_info("开始质量检查...")

    # 创建检查器并运行
    checker = QualityChecker()

    with console.status("[bold blue]运行单元测试..."):
        results = checker.run_all_checks()

    # 保存报告
    report_path = checker.save_report()

    # 显示结果
    summary = results["summary"]

    if summary["overall_status"] == "PASS":
        print_success("质量检查通过!")
    else:
        print_warning("质量检查发现问题")

    # 显示摘要表格
    table = Table(title="检查结果摘要", box=box.ROUNDED)
    table.add_column("检查项", style="cyan")
    table.add_column("状态", justify="center")
    table.add_column("通过/总计", justify="center")

    unit_status = results["unit_tests"].get("status", "N/A")
    unit_style = "green" if unit_status == "PASS" else "red"
    table.add_row(
        "单元测试",
        f"[{unit_style}]{unit_status}[/{unit_style}]",
        f"{results['unit_tests'].get('passed', 0)}/{results['unit_tests'].get('total', 0)}",
    )

    cli_status = results["cli_tests"].get("status", "N/A")
    cli_style = "green" if cli_status == "PASS" else "red"
    table.add_row(
        "CLI功能测试",
        f"[{cli_style}]{cli_status}[/{cli_style}]",
        f"{results['cli_tests'].get('passed', 0)}/{results['cli_tests'].get('total', 0)}",
    )

    console.print(table)

    # 详细输出
    if verbose:
        console.print("\n[bold]CLI测试详情:[/bold]")
        for test in results["cli_tests"].get("tests", []):
            status_icon = "✅" if test["status"] == "PASS" else "❌"
            console.print(f"  {status_icon} {test['name']}: {test['command']}")

    # 显示报告路径
    console.print(f"\n[bold]报告已保存:[/bold] {report_path}")
    console.print(f"[dim]查看完整报告: cat {report_path.with_suffix('.md')}[/dim]")

    # 如果检查失败，返回非零退出码
    if summary["overall_status"] != "PASS":
        sys.exit(1)
