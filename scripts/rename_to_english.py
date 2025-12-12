#!/usr/bin/env python
"""
批量将中文文件夹名重命名为英文
生成英文-中文对照表
"""
import os
import re
import json
import shutil
from pathlib import Path

# 中文到英文的映射表
CHINESE_TO_ENGLISH = {
    # Go语言
    "工具开发演示": "cli-tool-demo",
    "容器操作管理": "container-management",
    "框架web开发入门": "web-framework-intro",
    "内存数据库存储": "embedded-db-storage",
    "实战演示": "demo",
    "服务注册与发现": "service-discovery",
    "实践示例": "practice",
    "机制实战演示": "mechanism-demo",
    "日志聚合集成": "log-aggregation",
    "静态资源嵌入": "embed-static-assets",
    "客户端实战演示": "client-demo",
    "处理实战演示": "processing-demo",
    "认证用户登录验证": "auth-login-verify",
    "第三方登录示例": "third-party-login",
    "性能分析实战演示": "profiling-demo",
    "分布式锁演示": "distributed-lock-demo",
    "缓存操作演示": "cache-operations-demo",
    "机制演示": "mechanism-demo",
    "网络编程示例": "network-programming",
    "配置管理与环境变量集成示例": "config-env-integration",
    "增删改查实战演示": "crud-demo",
    "中间件模式http服务器示例": "middleware-http-server",
    "依赖注入设计模式实战": "dependency-injection-demo",
    "信号处理与优雅关闭": "signal-graceful-shutdown",
    "健康检查服务监控": "health-check-monitor",
    "函数编程实战演示": "functional-programming-demo",
    "函数编程实践": "functional-programming-practice",
    "加密安全实践hash与jwt示例": "crypto-hash-jwt-demo",
    "单元测试表驱动测试": "table-driven-testing",
    "反射与元编程实战演示": "reflection-metaprogramming-demo",
    "变量与类型演示": "variables-types-demo",
    "变量类型实战演示": "variable-types-demo",
    "变量类型演示": "var-types-demo",
    "基准测试性能分析": "benchmark-profiling",
    "多阶段docker构建演示": "multi-stage-docker-build",
    "字符串处理实战演示": "string-processing-demo",
    "定时任务调度cron示例": "cron-scheduler-demo",
    "嵌入式编程示例": "embedded-programming-demo",
    "常量枚举iota演示": "const-enum-iota-demo",
    "常量枚举与iota使用示例": "const-enum-iota-usage",
    "常量枚举与iota演示": "constants-enums-iota-demo",
    "并发原语实战演示": "concurrency-primitives-demo",
    "并发控制实战mutex与waitgroup演示": "mutex-waitgroup-control-demo",
    "并发编程中的select机制演示": "select-concurrency-demo",
    "并发编程入门goroutines实战演示": "goroutines-intro-demo",
    "并发编程实战goroutines入门": "goroutines-basics-demo",
    "并发编程实战goroutines入门与应用": "goroutines-basics-application",
    "并发编程实战goroutines应用示例": "goroutines-practical-demo",
    "并发编程实战goroutines详解": "goroutines-detailed-demo",
    "并发编程实战mutex与waitgroup": "mutex-waitgroup-demo",
    "并发编程实战mutex与waitgroup详解": "mutex-waitgroup-detailed",
    "指数退避重试机制": "exponential-backoff-retry",
    "接口实战演示": "interfaces-demo",
    "控制流演示": "control-flow-demo",
    "控制流语句实战演示": "control-flow-statements-demo",
    "数据库sql事务操作演示": "sql-transaction-demo",
    "数据库连接池管理演示": "db-connection-pool-demo",
    "数组与切片实战演示": "arrays-slices-demo",
    "文件操作实战演示": "file-operations-demo",
    "日志轮转文件管理": "log-rotation-demo",
    "时间处理实战演示": "time-handling-demo",
    "模板引擎实战演示": "template-engine-demo",
    "正则表达式文本匹配实战演示": "regex-pattern-matching-demo",
    "结构体实战演示": "struct-demo",
    "结构化日志管理zap实战": "structured-logging-zap-demo",
    "缓存预热与缓存策略演示": "cache-warmup-strategy-demo",
    "语言lru缓存策略实现": "lru-cache-impl-demo",
    "语言结构体实战演示": "struct-practical-demo",
    "负载均衡与反向代理": "load-balancer-reverse-proxy",
    "超时控制与context实践": "timeout-context-demo",
    "配置热更新与文件监听": "config-hot-reload-demo",
    "闭包编程实战演示": "closure-programming-demo",
    "限流与熔断机制实战演示": "rate-limit-circuit-breaker-demo",
    "项目自动化构建与makefile集成演示": "makefile-automation-demo",
    "代理服务网格": "service-mesh-proxy",
    "生产者消费者": "producer-consumer",
    "分布式追踪": "distributed-tracing",
    "实时通信": "realtime-communication",
    
    # Node.js
    "拦截器实战演示": "interceptor-demo",
    "队列异步任务处理": "queue-async-tasks",
    "服务发现与配置中心": "service-discovery-config",
    "容器管理演示": "container-management-demo",
    "异步流控制演示": "async-flow-control-demo",
    "查询语言实战演示": "query-language-demo",
    "安全中间件防护示例": "security-middleware-demo",
    "模拟单元测试": "mock-unit-testing",
    "认证与授权": "auth-authorization",
    "文件上传处理": "file-upload-handling",
    "框架入门": "framework-intro",
    "定时任务调度演示": "cron-scheduler-demo",
    "操作实战演示": "operations-demo",
    "多进程负载均衡示例": "cluster-load-balancing",
    "模块实战演示": "module-demo",
    "模块系统信息监控": "os-system-monitor",
    "监控指标采集": "metrics-collection",
    "元编程实战演示": "metaprogramming-demo",
    "多线程编程实战示例": "multithreading-demo",
    "正则表达式文本匹配验证": "regex-validation-demo",
    "中间件处理链演示": "middleware-chain-demo",
    "事件发射器实战演示": "event-emitter-demo",
    "优雅关闭实践": "graceful-shutdown-demo",
    "健康检查示例": "health-check-demo",
    "函数编程实战演示": "functional-programming-demo",
    "加密安全示例crypto-hash与bcrypt实战": "crypto-bcrypt-demo",
    "单元测试与覆盖率实战": "unit-testing-coverage",
    "变量基础演示": "variables-basics-demo",
    "变量类型演示": "variable-types-demo",
    "回调函数实战演示": "callback-demo",
    "子进程管理实战演示": "child-process-demo",
    "定时任务调度": "cron-scheduling",
    "对象操作实战深拷贝冻结与遍历": "object-operations-demo",
    "展开运算符实战演示": "spread-operator-demo",
    "数组方法实战演示": "array-methods-demo",
    "文件系统操作演示": "filesystem-operations-demo",
    "日志管理": "logging-management",
    "熔断器模式实战演示": "circuit-breaker-demo",
    "环境变量管理": "env-variables-demo",
    "类继承演示": "class-inheritance-demo",
    "解构赋值实战演示": "destructuring-demo",
    "请求重试与指数退避机制实战": "retry-exponential-backoff",
    "负载均衡http代理": "load-balancer-proxy",
    "错误处理实战演示": "error-handling-demo",
    "闭包实战演示": "closure-demo",
    "限流器演示": "rate-limiter-demo",
    "高阶函数实战演示": "higher-order-functions-demo",
    "授权passport集成": "passport-oauth-integration",
    "多进程部署": "multi-process-deployment",
    "数据库操作实战示例": "database-operations-demo",
    "实时聊天室": "realtime-chat-demo",
    "符号与迭代器应用示例": "symbol-iterator-demo",
}


def get_english_name(chinese_name: str) -> str:
    """将包含中文的名称转换为纯英文名称"""
    # 提取语言前缀 (go- 或 nodejs-)
    if chinese_name.startswith("go-"):
        prefix = "go-"
        rest = chinese_name[3:]
    elif chinese_name.startswith("nodejs-"):
        prefix = "nodejs-"
        rest = chinese_name[7:]
    else:
        prefix = ""
        rest = chinese_name
    
    # 如果没有中文，直接返回
    if not re.search(r'[\u4e00-\u9fff]', rest):
        return chinese_name
    
    # 尝试从映射表中匹配
    for cn, en in CHINESE_TO_ENGLISH.items():
        if cn in rest:
            # 保留非中文部分
            rest_cleaned = re.sub(r'[\u4e00-\u9fff]+', '', rest).strip('-')
            if rest_cleaned:
                return f"{prefix}{rest_cleaned}-{en}".replace("--", "-")
            else:
                return f"{prefix}{en}"
    
    # 如果没找到精确匹配，使用通用替换
    # 移除所有中文，保留英文和数字
    english_part = re.sub(r'[\u4e00-\u9fff]+', '', rest)
    english_part = english_part.strip('-').replace('--', '-')
    
    if english_part:
        return f"{prefix}{english_part}-demo"
    else:
        return f"{prefix}demo"


def update_metadata(demo_path: Path, new_folder_name: str, old_folder_name: str):
    """更新metadata.json中的相关信息"""
    metadata_file = demo_path / "metadata.json"
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # 添加原始中文名称作为别名
            if 'aliases' not in metadata:
                metadata['aliases'] = []
            if old_folder_name not in metadata['aliases']:
                metadata['aliases'].append(old_folder_name)
            
            # 保存更新后的metadata
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  警告: 更新metadata失败: {e}")


def rename_demos(output_dir: Path) -> dict:
    """重命名所有中文文件夹，返回映射表"""
    mapping = {"go": [], "nodejs": [], "python": []}
    
    for lang in ["go", "nodejs"]:
        lang_dir = output_dir / lang
        if not lang_dir.exists():
            continue
        
        for demo_dir in lang_dir.iterdir():
            if not demo_dir.is_dir():
                continue
            
            old_name = demo_dir.name
            # 检查是否包含中文
            if not re.search(r'[\u4e00-\u9fff]', old_name):
                # 不包含中文，直接添加到映射
                mapping[lang].append({
                    "folder": old_name,
                    "chinese_name": "",  # 从metadata获取
                    "description": ""
                })
                continue
            
            new_name = get_english_name(old_name)
            
            # 确保新名称唯一
            new_path = lang_dir / new_name
            counter = 1
            while new_path.exists() and new_path != demo_dir:
                new_name = f"{get_english_name(old_name)}-{counter}"
                new_path = lang_dir / new_name
                counter += 1
            
            print(f"重命名: {old_name} -> {new_name}")
            
            # 更新metadata
            update_metadata(demo_dir, new_name, old_name)
            
            # 执行重命名
            try:
                demo_dir.rename(new_path)
                mapping[lang].append({
                    "folder": new_name,
                    "chinese_name": old_name,
                    "description": ""
                })
            except Exception as e:
                print(f"  错误: 重命名失败 - {e}")
                mapping[lang].append({
                    "folder": old_name,
                    "chinese_name": old_name,
                    "description": ""
                })
    
    # 处理Python (通常已经是英文)
    python_dir = output_dir / "python"
    if python_dir.exists():
        for demo_dir in python_dir.iterdir():
            if demo_dir.is_dir():
                mapping["python"].append({
                    "folder": demo_dir.name,
                    "chinese_name": "",
                    "description": ""
                })
    
    return mapping


def get_demo_info(demo_path: Path) -> dict:
    """从metadata.json获取demo信息"""
    metadata_file = demo_path / "metadata.json"
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            return {
                "name": metadata.get("name", ""),
                "description": metadata.get("description", ""),
                "keywords": metadata.get("keywords", [])
            }
        except:
            pass
    return {"name": "", "description": "", "keywords": []}


def generate_mapping_table(output_dir: Path) -> dict:
    """生成完整的映射表"""
    mapping = {"go": [], "nodejs": [], "python": []}
    
    for lang in ["go", "nodejs", "python"]:
        lang_dir = output_dir / lang
        if not lang_dir.exists():
            continue
        
        for demo_dir in sorted(lang_dir.iterdir()):
            if not demo_dir.is_dir():
                continue
            
            info = get_demo_info(demo_dir)
            mapping[lang].append({
                "folder": demo_dir.name,
                "name": info["name"],
                "description": info["description"][:50] + "..." if len(info.get("description", "")) > 50 else info.get("description", "")
            })
    
    return mapping


if __name__ == "__main__":
    workspace = Path(__file__).parent.parent
    output_dir = workspace / "opendemo_output"
    
    print("=" * 60)
    print("批量重命名中文文件夹为英文")
    print("=" * 60)
    
    # 执行重命名
    rename_demos(output_dir)
    
    print("\n" + "=" * 60)
    print("生成映射表...")
    print("=" * 60)
    
    # 生成最终映射表
    mapping = generate_mapping_table(output_dir)
    
    # 保存映射表
    mapping_file = workspace / "data" / "demo_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\n映射表已保存到: {mapping_file}")
    
    # 统计
    print("\n统计:")
    for lang, demos in mapping.items():
        print(f"  {lang}: {len(demos)} 个demo")
