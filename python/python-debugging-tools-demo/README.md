# Python性能分析与排查工具实战演示

## 🎯 学习目标

通过本案例你将掌握Python应用的性能分析和问题排查技能：

- Python内置profile和cProfile性能分析
- 内存泄漏检测和分析方法
- 多进程和多线程问题排查
- OOM问题诊断和预防
- 生产环境Python应用监控最佳实践
- 第三方性能分析工具使用

## 🛠️ 环境准备

### 系统要求
- Python 3.7+ 运行环境
- Linux/Unix系统（推荐）
- 至少2GB内存用于分析工具运行
- Python应用开发和部署经验

### 依赖安装
```bash
# 安装性能分析工具
pip install line-profiler memory-profiler psutil objgraph
pip install py-spy  # 采样分析器
pip install guppy3  # 内存分析工具

# 系统级工具
sudo apt-get install valgrind htop  # Ubuntu/Debian
sudo yum install valgrind htop      # CentOS/RHEL

# 验证安装
python -c "import cProfile, pstats, memory_profiler, psutil"
py-spy --version
```

## 📁 项目结构

```
python-debugging-tools-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── examples/                          # 示例应用
│   ├── memory_leak_demo.py            # 内存泄漏演示
│   ├── cpu_intensive_demo.py          # CPU密集型演示
│   ├── threading_deadlock_demo.py     # 线程死锁演示
│   ├── multiprocessing_demo.py        # 多进程演示
│   └── oom_simulation_demo.py         # OOM模拟演示
├── scripts/                           # 排查脚本
│   ├── python_profiler.sh             # Python性能分析脚本
│   ├── memory_analyzer.sh             # 内存分析脚本
│   ├── thread_inspector.sh            # 线程检查脚本
│   ├── oom_detector.sh                # OOM检测脚本
│   └── process_monitor.sh             # 进程监控脚本
├── configs/                           # 配置文件
│   ├── profiling_config.py            # 性能分析配置
│   ├── memory_tracking.conf           # 内存跟踪配置
│   └── monitoring_rules.conf          # 监控规则配置
├── analysis_results/                  # 分析结果
│   ├── profile_outputs/               # profile输出
│   ├── memory_reports/                # 内存分析报告
│   ├── flame_graphs/                  # 火焰图
│   └── troubleshooting_logs/          # 故障排查日志
└── docs/                              # 详细文档
    ├── python_profiling_guide.md      # Python性能分析指南
    ├── memory_debugging_manual.md     # 内存调试手册
    ├── multithreading_analysis.md     # 多线程分析指南
    └── oom_prevention_strategies.md   # OOM预防策略
```

## 🔧 核心排查工具详解

### 1. Python内置性能分析工具

```python
# 使用cProfile进行性能分析
import cProfile
import pstats
from functools import wraps

def profile_function(func):
    """装饰器：为函数添加性能分析"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        # 保存分析结果
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # 显示前10个最耗时的函数
        
        return result
    return wrapper

# 使用示例
@profile_function
def cpu_intensive_task():
    # 模拟CPU密集型任务
    total = 0
    for i in range(1000000):
        total += i * i
    return total

# 命令行使用
# python -m cProfile -s cumulative script.py
# python -m cProfile -o profile_output.prof script.py
```

```bash
# 命令行性能分析
# 基本性能分析
python -m cProfile script.py

# 按累计时间排序
python -m cProfile -s cumulative script.py

# 保存分析结果
python -m cProfile -o profile.dat script.py

# 分析保存的结果
python -c "
import pstats
stats = pstats.Stats('profile.dat')
stats.sort_stats('cumulative')
stats.print_stats(20)
"
```

### 2. 内存分析工具

```python
# memory_profiler使用示例
from memory_profiler import profile
import gc

@profile
def memory_leak_demo():
    """内存泄漏演示"""
    big_list = []
    for i in range(1000):
        # 模拟内存泄漏：不断添加数据但不清理
        data = [0] * 100000  # 约800KB
        big_list.append(data)
        
        if i % 100 == 0:
            print(f"Iteration {i}, current memory: {len(big_list)} items")
            
    return len(big_list)

# 使用objgraph分析对象引用
import objgraph

def analyze_memory_objects():
    """分析内存中的对象"""
    # 显示最常见的对象类型
    objgraph.show_most_common_types(limit=10)
    
    # 查找特定类型的对象
    lists = objgraph.by_type('list')
    print(f"List objects in memory: {len(lists)}")
    
    # 查看对象引用链
    if lists:
        objgraph.show_backrefs([lists[0]], max_depth=3)

# Guppy内存分析
from guppy import hpy

def detailed_memory_analysis():
    """详细内存分析"""
    hp = hpy()
    
    # 获取当前堆信息
    heap = hp.heap()
    print("Heap analysis:")
    print(heap)
    
    # 按类型统计
    print("\nBy type:")
    print(hp.heap().byrcs)
```

```bash
# 命令行内存分析
# 实时监控内存使用
mprof run script.py
mprof plot  # 生成内存使用图表

# 分析特定进程
python -m memory_profiler script.py

# 使用psutil监控进程
python -c "
import psutil
import time

process = psutil.Process()
while True:
    mem_info = process.memory_info()
    print(f'RSS: {mem_info.rss / 1024 / 1024:.2f} MB')
    print(f'VMS: {mem_info.vms / 1024 / 1024:.2f} MB')
    time.sleep(1)
"
```

### 3. 多线程和多进程分析

```python
# 线程分析示例
import threading
import time
import sys

def thread_leak_demo():
    """线程泄漏演示"""
    threads = []
    
    def worker(name):
        time.sleep(30)  # 模拟长时间运行的线程
        print(f"Thread {name} finished")
    
    # 创建大量线程但不正确管理
    for i in range(100):
        t = threading.Thread(target=worker, args=(f"Worker-{i}",))
        t.daemon = False  # 非守护线程，不会自动清理
        t.start()
        threads.append(t)
        
        if i % 20 == 0:
            print(f"Created {i+1} threads")
            print(f"Active threads: {threading.active_count()}")
    
    # 不等待线程结束，可能导致资源累积
    return len(threads)

# 使用py-spy分析运行中的进程
# py-spy top --pid <process_id>
# py-spy record -o profile.svg --pid <process_id>
```

```bash
# 线程和进程监控脚本
#!/bin/bash
PID=$1

echo "=== Python进程分析 ==="

# 1. 进程基本信息
echo "1. 进程信息:"
ps -p $PID -o pid,ppid,cmd,etime,rss,vsz,%cpu,%mem

# 2. 线程分析
echo "2. 线程信息:"
ps -T -p $PID -o pid,tid,state,comm,wchan

# 3. 内存映射
echo "3. 内存映射:"
pmap -x $PID | tail -10

# 4. 文件描述符
echo "4. 文件描述符使用:"
ls -l /proc/$PID/fd | wc -l

# 5. 使用py-spy分析
if command -v py-spy &> /dev/null; then
    echo "5. 实时性能分析:"
    timeout 10 py-spy top --pid $PID
fi
```

### 4. OOM问题诊断

```python
# OOM模拟和检测
import psutil
import gc
import time

class OOMDetector:
    def __init__(self, threshold_mb=800):
        self.threshold = threshold_mb * 1024 * 1024  # 转换为字节
        self.process = psutil.Process()
        
    def check_memory_usage(self):
        """检查内存使用情况"""
        mem_info = self.process.memory_info()
        current_memory = mem_info.rss
        
        print(f"当前内存使用: {current_memory / 1024 / 1024:.2f} MB")
        
        if current_memory > self.threshold:
            print("⚠️  内存使用接近阈值!")
            self.analyze_memory()
            return True
        return False
    
    def analyze_memory(self):
        """分析内存使用"""
        # 强制垃圾回收
        gc.collect()
        
        # 显示对象统计
        import objgraph
        objgraph.show_growth(limit=5)
        
        # 显示内存映射
        print("内存映射信息:")
        for mmap in self.process.memory_maps():
            print(f"  {mmap.path}: {mmap.rss / 1024 / 1024:.2f} MB")

def simulate_oom():
    """模拟OOM场景"""
    detector = OOMDetector(threshold_mb=100)  # 100MB阈值
    big_data = []
    
    try:
        for i in range(1000):
            # 分配大量内存
            chunk = bytearray(1024 * 1024)  # 1MB
            big_data.append(chunk)
            
            if detector.check_memory_usage():
                print("检测到内存风险，停止分配")
                break
                
            time.sleep(0.1)
            
    except MemoryError:
        print("发生内存溢出!")
        detector.analyze_memory()

if __name__ == "__main__":
    simulate_oom()
```

## 🔍 综合诊断实战

### 场景1：CPU性能瓶颈分析

```bash
#!/bin/bash
# Python CPU性能分析脚本

SCRIPT_PATH=$1
OUTPUT_DIR=${2:-"./analysis_results"}

echo "=== Python CPU性能分析 ==="
echo "分析脚本: $SCRIPT_PATH"
echo "输出目录: $OUTPUT_DIR"

mkdir -p $OUTPUT_DIR/profile_outputs

# 1. 使用cProfile进行详细分析
echo "1. 执行cProfile分析..."
python -m cProfile -o $OUTPUT_DIR/profile_outputs/cprofile.dat $SCRIPT_PATH

# 2. 生成可读报告
echo "2. 生成分析报告..."
python -c "
import pstats
import os

stats = pstats.Stats('$OUTPUT_DIR/profile_outputs/cprofile.dat')
stats.sort_stats('cumulative')

# 保存完整报告
with open('$OUTPUT_DIR/profile_outputs/full_report.txt', 'w') as f:
    stats.stream = f
    stats.print_stats()

# 保存Top 20函数
with open('$OUTPUT_DIR/profile_outputs/top20_functions.txt', 'w') as f:
    stats.stream = f
    stats.print_stats(20)

print('分析报告已生成')
"

# 3. 使用py-spy进行采样分析
if command -v py-spy &> /dev/null; then
    echo "3. 执行py-spy采样分析..."
    py-spy record -o $OUTPUT_DIR/flame_graphs/cpu_flame.svg --duration 30 -- python $SCRIPT_PATH
fi

# 4. 生成火焰图报告
echo "4. 生成火焰图分析..."
if [ -f "$OUTPUT_DIR/flame_graphs/cpu_flame.svg" ]; then
    echo "火焰图已生成: $OUTPUT_DIR/flame_graphs/cpu_flame.svg"
fi

echo "CPU分析完成"
```

### 场景2：内存泄漏检测

```bash
#!/bin/bash
# Python内存泄漏检测脚本

PID=$1
DURATION=${2:-60}  # 监控持续时间

echo "=== 内存泄漏检测 ==="
echo "进程ID: $PID"
echo "监控时长: ${DURATION}秒"

# 1. 初始内存快照
INITIAL_RSS=$(ps -p $PID -o rss= | tr -d ' ')
echo "初始RSS内存: $((INITIAL_RSS/1024)) MB"

# 2. 持续监控内存增长
echo "开始监控内存变化..."
for i in $(seq 1 $((DURATION/5))); do
    sleep 5
    CURRENT_RSS=$(ps -p $PID -o rss= | tr -d ' ')
    GROWTH=$((CURRENT_RSS - INITIAL_RSS))
    GROWTH_MB=$((GROWTH/1024))
    
    echo "第$((i*5))秒: RSS内存 ${CURRENT_RSS} KB (增长: ${GROWTH_MB} MB)"
    
    # 如果增长超过100MB，进行详细分析
    if [ $GROWTH_MB -gt 100 ]; then
        echo "⚠️  内存增长异常，执行详细分析..."
        
        # 使用gdb附加到进程分析
        gdb -p $PID -batch -ex "py-bt" -ex "quit" 2>/dev/null || echo "GDB分析失败"
        
        # 生成内存报告
        python -c "
import psutil
import gc
process = psutil.Process($PID)
gc.collect()

print('内存详细分析:')
print(f'Memory info: {process.memory_info()}')
print(f'Num handles: {process.num_handles() if hasattr(process, \"num_handles\") else \"N/A\"}')

# 如果是Python进程，尝试获取内部信息
try:
    import sys
    if sys.version_info >= (3, 7):
        print(f'Open files: {process.open_files()}')
except:
    pass
" > /tmp/memory_analysis_$PID.txt
        
        echo "详细分析报告已生成: /tmp/memory_analysis_$PID.txt"
        break
    fi
done

# 3. 最终内存状态
FINAL_RSS=$(ps -p $PID -o rss= | tr -d ' ')
FINAL_GROWTH=$((FINAL_RSS - INITIAL_RSS))
FINAL_GROWTH_MB=$((FINAL_GROWTH/1024))

echo "最终内存增长: ${FINAL_GROWTH_MB} MB"

if [ $FINAL_GROWTH_MB -gt 50 ]; then
    echo "⚠️  存在潜在内存泄漏风险"
else
    echo "✅ 内存使用相对稳定"
fi
```

### 场景3：多线程死锁检测

```python
# 线程死锁检测脚本
import threading
import time
import traceback
import sys

class ThreadMonitor:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.thread_states = {}
        self.monitor_thread = None
        
    def start_monitoring(self):
        """开始监控线程状态"""
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def _monitor_loop(self):
        """监控循环"""
        while True:
            self._check_thread_states()
            time.sleep(5)
            
    def _check_thread_states(self):
        """检查线程状态"""
        current_threads = threading.enumerate()
        
        for thread in current_threads:
            if thread.ident not in self.thread_states:
                self.thread_states[thread.ident] = {
                    'name': thread.name,
                    'start_time': time.time(),
                    'last_seen': time.time()
                }
            else:
                self.thread_states[thread.ident]['last_seen'] = time.time()
                
        # 检查长时间未活动的线程
        current_time = time.time()
        for thread_id, state in self.thread_states.items():
            inactive_time = current_time - state['last_seen']
            if inactive_time > self.timeout:
                print(f"⚠️  线程 {state['name']} ({thread_id}) 已 inactive {inactive_time:.1f} 秒")
                self._analyze_thread(thread_id)
                
    def _analyze_thread(self, thread_id):
        """分析特定线程"""
        # 获取线程堆栈
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                frame = sys._current_frames().get(thread_id)
                if frame:
                    print(f"线程 {thread.name} 堆栈跟踪:")
                    traceback.print_stack(frame)
                break

# 使用示例
def create_potential_deadlock():
    """创建可能的死锁场景"""
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    
    def worker1():
        with lock1:
            time.sleep(1)
            with lock2:  # 可能导致死锁
                print("Worker1 acquired both locks")
                
    def worker2():
        with lock2:
            time.sleep(1)
            with lock1:  # 可能导致死锁
                print("Worker2 acquired both locks")
    
    # 启动监控
    monitor = ThreadMonitor(timeout=10)
    monitor.start_monitoring()
    
    # 启动可能死锁的线程
    t1 = threading.Thread(target=worker1, name="DeadlockWorker1")
    t2 = threading.Thread(target=worker2, name="DeadlockWorker2")
    
    t1.start()
    t2.start()
    
    t1.join(timeout=15)
    t2.join(timeout=15)
    
    print("死锁演示完成")

if __name__ == "__main__":
    create_potential_deadlock()
```

## 📊 监控和告警配置

### 系统级监控脚本
```bash
#!/bin/bash
# Python应用综合监控脚本

APP_NAME=$1
PID_FILE=${2:-"/var/run/python_app.pid"}

# 获取进程ID
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
else
    PID=$(pgrep -f "$APP_NAME" | head -1)
fi

if [ -z "$PID" ]; then
    echo "❌ 未找到应用进程"
    exit 1
fi

echo "=== Python应用监控报告 ==="
echo "应用名称: $APP_NAME"
echo "进程ID: $PID"
echo "检查时间: $(date)"

# 1. 基本进程信息
echo "1. 进程状态:"
ps -p $PID -o pid,ppid,user,%cpu,%mem,vsz,rss,etime,stat,comm

# 2. 内存使用详情
echo "2. 内存使用:"
cat /proc/$PID/status | grep -E "VmRSS|VmSize|VmData|VmStk"

# 3. 线程和文件描述符
echo "3. 线程数: $(ps -T -p $PID --no-headers | wc -l)"
echo "4. 文件描述符: $(ls /proc/$PID/fd | wc -l)"

# 5. 网络连接
echo "5. 网络连接:"
ss -tulnp | grep $PID | head -5

# 6. 性能警告检查
RSS_KB=$(ps -p $PID -o rss= | tr -d ' ')
RSS_MB=$((RSS_KB/1024))

if [ $RSS_MB -gt 1000 ]; then
    echo "⚠️  高内存使用: ${RSS_MB}MB"
fi

CPU_USAGE=$(ps -p $PID -o %cpu= | tr -d ' ')
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "⚠️  高CPU使用: ${CPU_USAGE}%"
fi

# 7. 生成监控报告
REPORT_FILE="/tmp/python_monitor_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
Python应用监控报告
==================
时间: $(date)
应用: $APP_NAME
PID: $PID
内存使用: ${RSS_MB}MB
CPU使用: ${CPU_USAGE}%
线程数: $(ps -T -p $PID --no-headers | wc -l)
文件描述符: $(ls /proc/$PID/fd | wc -l)
EOF

echo "监控报告已保存: $REPORT_FILE"
```

## 🧪 验证测试

### 工具可用性验证
```bash
#!/bin/bash
# Python排查工具验证脚本

echo "=== Python排查工具验证 ==="

# 检查Python环境
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python环境异常"
    exit 1
fi

# 检查必需的包
REQUIRED_PACKAGES=("cProfile" "pstats" "psutil")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    python -c "import $pkg" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ $pkg 可用"
    else
        echo "❌ $pkg 不可用"
    fi
done

# 检查第三方工具
THIRD_PARTY_TOOLS=("memory_profiler" "objgraph" "py-spy")
for tool in "${THIRD_PARTY_TOOLS[@]}"; do
    python -c "import $tool" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ $tool 可用"
        if [ "$tool" = "py-spy" ]; then
            py-spy --version
        fi
    else
        echo "⚠️  $tool 未安装"
    fi
done

# 测试示例脚本
echo "测试示例脚本..."
cd examples
python memory_leak_demo.py &
TEST_PID=$!
sleep 3

# 测试监控
if ps -p $TEST_PID > /dev/null; then
    echo "✅ 示例应用运行正常"
    
    # 测试内存监控
    ps -p $TEST_PID -o rss=
    
    kill $TEST_PID
else
    echo "❌ 示例应用启动失败"
fi

echo "验证完成"
```

## ❓ 常见问题处理

### Q1: memory_profiler显示内存使用为0？
**解决方案**：
```bash
# 确保正确安装
pip install memory-profiler
pip install psutil

# 使用正确的装饰器
from memory_profiler import profile

@profile
def function_to_profile():
    # 函数代码
    pass

# 命令行使用
python -m memory_profiler script.py
```

### Q2: py-spy无法附加到进程？
**解决方案**：
```bash
# 检查权限
sudo py-spy top --pid <process_id>

# 检查进程状态
ps -p <process_id> -o pid,stat

# 确保Python版本兼容
py-spy --version
python --version
```

### Q3: 多进程应用如何监控？
**监控建议**：
```python
# 父进程监控所有子进程
import psutil
import os

def monitor_child_processes():
    current_process = psutil.Process(os.getpid())
    children = current_process.children(recursive=True)
    
    for child in children:
        print(f"子进程 {child.pid}: 内存={child.memory_info().rss/1024/1024:.2f}MB")
```

## 📚 扩展学习

### 专业工具推荐
- **Scalene**: 高精度CPU和内存分析器
- **Austin**: Python采样分析器
- **SnakeViz**: profile结果可视化工具
- **PyCharm Profiler**: IDE内置分析工具

### 学习进阶路径
1. 掌握Python内存管理和垃圾回收机制
2. 深入理解GIL对多线程性能的影响
3. 学习异步编程和性能优化
4. 掌握大规模应用的监控体系
5. 学习容器化环境下的性能分析

---
> **💡 提示**: Python的性能分析工具丰富多样，建议根据具体场景选择合适的工具组合使用。