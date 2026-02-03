"""
Kubeflow Demo批量生成脚本

根据设计文档批量生成35个Kubeflow Demo，使用CLI命令行方式
"""

import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


# Kubeflow Demo定义
KUBEFLOW_DEMOS = {
    # 阶段一：核心组件(12个)
    "phase1": [
        # Central Dashboard（2个）
        {
            "name": "Dashboard基础安装与配置",
            "keywords": ["kubeflow", "dashboard", "installation", "setup"],
            "difficulty": "beginner",
        },
        {
            "name": "Dashboard RBAC权限配置",
            "keywords": ["kubeflow", "dashboard", "rbac", "permissions"],
            "difficulty": "intermediate",
        },
        # Kubeflow Notebooks（4个）
        {
            "name": "Notebook服务器创建与配置",
            "keywords": ["kubeflow", "notebooks", "jupyter", "server"],
            "difficulty": "beginner",
        },
        {
            "name": "Notebook自定义镜像使用",
            "keywords": ["kubeflow", "notebooks", "custom", "image"],
            "difficulty": "intermediate",
        },
        {
            "name": "Notebook GPU资源分配",
            "keywords": ["kubeflow", "notebooks", "gpu", "resources"],
            "difficulty": "intermediate",
        },
        {
            "name": "Notebook持久化存储配置",
            "keywords": ["kubeflow", "notebooks", "storage", "persistent"],
            "difficulty": "beginner",
        },
        # Kubeflow Pipelines（6个）
        {
            "name": "Pipeline Python组件开发",
            "keywords": ["kubeflow", "pipelines", "python", "component"],
            "difficulty": "beginner",
        },
        {
            "name": "Pipeline容器组件开发",
            "keywords": ["kubeflow", "pipelines", "container", "component"],
            "difficulty": "intermediate",
        },
        {
            "name": "Pipeline工作流编排",
            "keywords": ["kubeflow", "pipelines", "workflow", "orchestration"],
            "difficulty": "intermediate",
        },
        {
            "name": "Pipeline实验管理",
            "keywords": ["kubeflow", "pipelines", "experiment", "management"],
            "difficulty": "beginner",
        },
        {
            "name": "Pipeline工件追踪",
            "keywords": ["kubeflow", "pipelines", "artifact", "tracking"],
            "difficulty": "intermediate",
        },
        {
            "name": "Pipeline参数化执行",
            "keywords": ["kubeflow", "pipelines", "parameters", "execution"],
            "difficulty": "beginner",
        },
    ],
    # 阶段二：训练和服务(16个)
    "phase2": [
        # Kubeflow Trainer（5个）
        {
            "name": "PyTorchJob单机训练",
            "keywords": ["kubeflow", "trainer", "pytorch", "training"],
            "difficulty": "beginner",
        },
        {
            "name": "PyTorchJob分布式训练",
            "keywords": ["kubeflow", "trainer", "pytorch", "distributed"],
            "difficulty": "advanced",
        },
        {
            "name": "TFJob训练作业",
            "keywords": ["kubeflow", "trainer", "tensorflow", "training"],
            "difficulty": "intermediate",
        },
        {
            "name": "XGBoostJob训练作业",
            "keywords": ["kubeflow", "trainer", "xgboost", "training"],
            "difficulty": "intermediate",
        },
        {
            "name": "训练作业资源配置",
            "keywords": ["kubeflow", "trainer", "resources", "configuration"],
            "difficulty": "intermediate",
        },
        # Kubeflow KServe（6个）
        {
            "name": "KServe模型部署",
            "keywords": ["kubeflow", "kserve", "model", "deployment"],
            "difficulty": "beginner",
        },
        {
            "name": "KServe自定义预测器",
            "keywords": ["kubeflow", "kserve", "custom", "predictor"],
            "difficulty": "advanced",
        },
        {
            "name": "KServe金丝雀发布",
            "keywords": ["kubeflow", "kserve", "canary", "rollout"],
            "difficulty": "advanced",
        },
        {
            "name": "KServe Transformer集成",
            "keywords": ["kubeflow", "kserve", "transformer", "preprocessing"],
            "difficulty": "intermediate",
        },
        {
            "name": "KServe批量推理",
            "keywords": ["kubeflow", "kserve", "batch", "inference"],
            "difficulty": "intermediate",
        },
        {
            "name": "KServe GPU推理优化",
            "keywords": ["kubeflow", "kserve", "gpu", "inference"],
            "difficulty": "advanced",
        },
        # Kubeflow Katib（5个）
        {
            "name": "Katib超参数调优基础",
            "keywords": ["kubeflow", "katib", "hyperparameter", "tuning"],
            "difficulty": "beginner",
        },
        {
            "name": "Katib随机搜索算法",
            "keywords": ["kubeflow", "katib", "random", "search"],
            "difficulty": "beginner",
        },
        {
            "name": "Katib贝叶斯优化",
            "keywords": ["kubeflow", "katib", "bayesian", "optimization"],
            "difficulty": "intermediate",
        },
        {
            "name": "Katib Early Stopping策略",
            "keywords": ["kubeflow", "katib", "early-stopping", "strategy"],
            "difficulty": "intermediate",
        },
        {
            "name": "Katib神经架构搜索",
            "keywords": ["kubeflow", "katib", "nas", "architecture"],
            "difficulty": "advanced",
        },
    ],
    # 阶段三：高级功能(8个)
    "phase3": [
        # Kubeflow Model Registry（4个）
        {
            "name": "模型注册与管理",
            "keywords": ["kubeflow", "model-registry", "registration", "management"],
            "difficulty": "beginner",
        },
        {
            "name": "模型版本管理",
            "keywords": ["kubeflow", "model-registry", "version", "management"],
            "difficulty": "intermediate",
        },
        {
            "name": "模型元数据追踪",
            "keywords": ["kubeflow", "model-registry", "metadata", "tracking"],
            "difficulty": "intermediate",
        },
        {
            "name": "Model Registry Pipeline集成",
            "keywords": ["kubeflow", "model-registry", "pipeline", "integration"],
            "difficulty": "advanced",
        },
        # Kubeflow Spark Operator（4个）
        {
            "name": "Spark Operator基础作业",
            "keywords": ["kubeflow", "spark", "batch", "job"],
            "difficulty": "beginner",
        },
        {
            "name": "Spark Streaming作业",
            "keywords": ["kubeflow", "spark", "streaming", "job"],
            "difficulty": "intermediate",
        },
        {
            "name": "Spark资源优化配置",
            "keywords": ["kubeflow", "spark", "resources", "optimization"],
            "difficulty": "advanced",
        },
        {
            "name": "Spark监控与日志",
            "keywords": ["kubeflow", "spark", "monitoring", "logging"],
            "difficulty": "intermediate",
        },
    ],
}


def generate_single_demo(demo_config: dict, retry: int = 2, delay: int = 5) -> bool:
    """
    生成单个Kubeflow Demo（通过CLI）
    
    Args:
        demo_config: Demo配置
        retry: 重试次数
        delay: 请求间隔（秒）
    
    Returns:
        是否成功
    """
    # 构建CLI命令 - 使用kubeflow作为第一个关键字让系统识别为kubernetes库demo
    keywords = " ".join(demo_config["keywords"])
    cmd = [
        "python",
        "-m",
        "opendemo",
        "new",
        "kubernetes",
        keywords,
        "--difficulty",
        demo_config["difficulty"],
    ]
    
    for attempt in range(retry + 1):
        try:
            logger.info(f"尝试 {attempt + 1}/{retry + 1}")
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=600,  # 10分钟超时
                cwd=project_root
            )
            
            if result.returncode == 0:
                logger.info("✓ 生成成功")
                return True
            else:
                logger.error(f"✗ 生成失败: {result.stderr}")
                
                if attempt < retry:
                    logger.info(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)
                    
        except subprocess.TimeoutExpired:
            logger.error("✗ 超时")
            if attempt < retry:
                logger.info(f"等待 {delay} 秒后重试...")
                time.sleep(delay)
        except Exception as e:
            logger.error(f"✗ 异常: {e}")
            if attempt < retry:
                logger.info(f"等待 {delay} 秒后重试...")
                time.sleep(delay)
    
    return False


def generate_kubeflow_demos(phase: str = "all"):
    """
    生成Kubeflow Demo
    
    Args:
        phase: 生成阶段，可选值：phase1, phase2, phase3, all
    """
    # 确定要生成的阶段
    if phase == "all":
        phases = ["phase1", "phase2", "phase3"]
    else:
        phases = [phase]
    
    total_demos = 0
    success_count = 0
    failed_demos = []
    
    for phase_name in phases:
        if phase_name not in KUBEFLOW_DEMOS:
            logger.warning(f"Unknown phase: {phase_name}")
            continue
            
        demos = KUBEFLOW_DEMOS[phase_name]
        logger.info(f"\n{'='*60}")
        logger.info(f"开始生成 {phase_name.upper()} Demo ({len(demos)}个)")
        logger.info(f"{'='*60}\n")
        
        for idx, demo_config in enumerate(demos, 1):
            total_demos += 1
            demo_name = demo_config["name"]
            
            logger.info(f"[{idx}/{len(demos)}] 生成Demo: {demo_name}")
            logger.info(f"  关键字: {' '.join(demo_config['keywords'])}")
            
            # 生成Demo
            success = generate_single_demo(demo_config)
            
            if success:
                success_count += 1
            else:
                failed_demos.append(demo_name)
            
            logger.info("")
            
            # 请求间隔，避免API限流
            if idx < len(demos):
                delay = 5
                logger.info(f"等待 {delay} 秒后继续...\n")
                time.sleep(delay)
    
    # 输出统计结果
    logger.info(f"\n{'='*60}")
    logger.info("生成统计")
    logger.info(f"{'='*60}")
    logger.info(f"总计: {total_demos} 个Demo")
    logger.info(f"成功: {success_count} 个")
    logger.info(f"失败: {len(failed_demos)} 个")
    
    if failed_demos:
        logger.info(f"\n失败的Demo:")
        for name in failed_demos:
            logger.info(f"  - {name}")
    
    if total_demos > 0:
        logger.info(f"\n完成率: {success_count}/{total_demos} ({success_count/total_demos*100:.1f}%)")
    
    # 保存报告
    save_report(phase, total_demos, success_count, failed_demos)
    
    return success_count, total_demos, failed_demos


def save_report(phase: str, total: int, success: int, failed_list: list):
    """保存生成报告"""
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = log_dir / f"kubeflow_generation_{phase}_{timestamp}.json"
    
    report = {
        "timestamp": timestamp,
        "phase": phase,
        "total": total,
        "success": success,
        "failed": len(failed_list),
        "success_rate": f"{success/max(1,total)*100:.1f}%",
        "failed_demos": failed_list,
    }
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n报告已保存: {report_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="批量生成Kubeflow Demo")
    parser.add_argument(
        "--phase",
        choices=["phase1", "phase2", "phase3", "all"],
        default="phase1",  # 默认从阶段一开始
        help="指定生成阶段（phase1: 核心组件, phase2: 训练和服务, phase3: 高级功能, all: 全部）",
    )
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("Kubeflow Demo批量生成工具")
    logger.info("="*60)
    logger.info(f"生成阶段: {args.phase}")
    
    if args.phase == "phase1":
        logger.info("包含: Dashboard(2) + Notebooks(4) + Pipelines(6) = 12个Demo")
    elif args.phase == "phase2":
        logger.info("包含: Trainer(5) + KServe(6) + Katib(5) = 16个Demo")
    elif args.phase == "phase3":
        logger.info("包含: Model Registry(4) + Spark Operator(4) = 8个Demo")
    elif args.phase == "all":
        logger.info("包含: 全部36个Demo")
    
    logger.info("")
    
    success, total, failed = generate_kubeflow_demos(args.phase)
    
    # 退出码
    sys.exit(0 if len(failed) == 0 else 1)
