# Encryption Performance Benchmark

磁盘加密性能基准测试演示。

## 测试环境要求

```
性能测试环境:
┌─────────────────────────────────────────────────────────┐
│                    测试目标系统                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  CPU: 支持AES-NI (Intel/AMD)                     │   │
│  │  RAM: 16GB+                                      │   │
│  │  Storage: NVMe SSD / SATA SSD / HDD              │   │
│  │  OS: Linux (推荐) / Windows / macOS              │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    测试工具                              │
│  • fio (Flexible I/O Tester)                           │
│  • crypsetup benchmark                                  │
│  • hdparm / dd (基础测试)                               │
│  • bonnie++ (综合文件系统测试)                           │
└─────────────────────────────────────────────────────────┘
```

## 加密算法性能对比

### cryptsetup benchmark
```bash
# 测试系统加密性能
cryptsetup benchmark

# 典型输出:
# Algorithm       | Key      | Encryption | Decryption
# ----------------|----------|------------|------------
# aes-xts        | 256b     | 3200.0 MiB/s | 3200.0 MiB/s
# aes-cbc-essiv  | 256b     | 2800.0 MiB/s | 2800.0 MiB/s
# serpent-xts    | 256b     |  450.0 MiB/s |  450.0 MiB/s
# twofish-xts    | 256b     |  380.0 MiB/s |  380.0 MiB/s
```

## fio性能测试脚本

```bash
#!/bin/bash
# 加密磁盘性能测试脚本

TEST_DEVICE="/dev/mapper/encrypted"
RESULTS_DIR="./benchmark_results"
mkdir -p $RESULTS_DIR

# 测试参数
BLOCK_SIZES=("4k" "8k" "64k" "128k" "1m")
IO_PATTERNS=("randread" "randwrite" "read" "write")
RUNTIME=60

run_fio_test() {
    local pattern=$1
    local bs=$2
    local output_file="$RESULTS_DIR/${pattern}_${bs}.json"
    
    echo "Running: pattern=$pattern, blocksize=$bs"
    
    fio --name=encryption_test \
        --filename=$TEST_DEVICE \
        --rw=$pattern \
        --bs=$bs \
        --size=4G \
        --runtime=$RUNTIME \
        --numjobs=4 \
        --ioengine=libaio \
        --direct=1 \
        --group_reporting \
        --output-format=json \
        --output=$output_file
}

# 运行所有测试组合
for pattern in "${IO_PATTERNS[@]}"; do
    for bs in "${BLOCK_SIZES[@]}"; do
        run_fio_test $pattern $bs
    done
done

echo "Benchmark complete. Results in $RESULTS_DIR"
```

## 性能分析Python脚本

```python
#!/usr/bin/env python3
"""
磁盘加密性能分析工具
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

class EncryptionBenchmarkAnalyzer:
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)
        self.data = []
    
    def parse_fio_results(self, json_file):
        """解析fio JSON输出"""
        with open(json_file) as f:
            data = json.load(f)
        
        job = data['jobs'][0]
        
        return {
            'pattern': job['jobname'].split('_')[0],
            'block_size': job['jobname'].split('_')[1],
            'iops': job['read']['iops'] if 'read' in job else job['write']['iops'],
            'bandwidth_mib': job['read']['bw'] / 1024 if 'read' in job else job['write']['bw'] / 1024,
            'latency_us': job['read']['lat_ns']['mean'] / 1000 if 'read' in job else job['write']['lat_ns']['mean'] / 1000
        }
    
    def load_all_results(self):
        """加载所有测试结果"""
        for json_file in self.results_dir.glob('*.json'):
            try:
                result = self.parse_fio_results(json_file)
                self.data.append(result)
            except Exception as e:
                print(f"Error parsing {json_file}: {e}")
        
        return pd.DataFrame(self.data)
    
    def generate_comparison_chart(self, df, metric='bandwidth_mib'):
        """生成性能对比图表"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        patterns = df['pattern'].unique()
        block_sizes = sorted(df['block_size'].unique(), 
                           key=lambda x: int(x[:-1]))
        
        x = range(len(block_sizes))
        width = 0.2
        
        for i, pattern in enumerate(patterns):
            pattern_data = df[df['pattern'] == pattern]
            values = [pattern_data[pattern_data['block_size'] == bs][metric].values[0] 
                     for bs in block_sizes]
            ax.bar([xi + i*width for xi in x], values, width, label=pattern)
        
        ax.set_xlabel('Block Size')
        ax.set_ylabel('Bandwidth (MiB/s)' if metric == 'bandwidth_mib' else 'IOPS')
        ax.set_title('Encryption Performance by Pattern and Block Size')
        ax.set_xticks([xi + width*1.5 for xi in x])
        ax.set_xticklabels(block_sizes)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'performance_comparison.png')
        print(f"Chart saved to {self.results_dir / 'performance_comparison.png'}")
    
    def generate_report(self):
        """生成性能报告"""
        df = self.load_all_results()
        
        if df.empty:
            print("No data to analyze")
            return
        
        # 生成统计摘要
        summary = df.groupby('pattern').agg({
            'iops': ['mean', 'max'],
            'bandwidth_mib': ['mean', 'max'],
            'latency_us': ['mean', 'min']
        }).round(2)
        
        print("\n=== Encryption Performance Summary ===\n")
        print(summary)
        
        # 生成图表
        self.generate_comparison_chart(df, 'bandwidth_mib')
        self.generate_comparison_chart(df, 'iops')
        
        # 保存CSV报告
        csv_file = self.results_dir / 'performance_report.csv'
        df.to_csv(csv_file, index=False)
        print(f"\nCSV report saved to {csv_file}")
        
        return summary

# 使用
if __name__ == "__main__":
    analyzer = EncryptionBenchmarkAnalyzer('./benchmark_results')
    analyzer.generate_report()
```

## 典型性能数据

### 加密vs未加密性能对比

| 存储类型 | 未加密读 | 加密读 | 性能损失 | 未加密写 | 加密写 | 性能损失 |
|---------|---------|--------|---------|---------|--------|---------|
| NVMe SSD | 3500 MB/s | 3200 MB/s | 8.5% | 3000 MB/s | 2800 MB/s | 6.7% |
| SATA SSD | 550 MB/s | 520 MB/s | 5.5% | 520 MB/s | 480 MB/s | 7.7% |
| HDD 7200 | 180 MB/s | 175 MB/s | 2.8% | 170 MB/s | 165 MB/s | 2.9% |

### CPU使用率对比

| 工作负载 | 未加密CPU | 加密CPU | 增加 |
|---------|----------|--------|------|
| 顺序读写 | 5% | 15% | +10% |
| 随机读写 | 10% | 25% | +15% |
| 大文件传输 | 3% | 12% | +9% |

## 优化建议

### 1. 硬件加速
```bash
# 检查AES-NI支持
grep -o aes /proc/cpuinfo | head -1

# 确保使用AES-NI优化的算法
cryptsetup luksFormat --cipher aes-xts-plain64 /dev/sda2
```

### 2. I/O调度器选择
```bash
# NVMe推荐none调度器
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler

# SSD推荐mq-deadline
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
```

### 3. 加密参数调优
```bash
# 启用TRIM (SSD必需)
cryptsetup --allow-discards luksOpen /dev/sda2 secure

# 调整加密队列深度
cryptsetup luksOpen --perf-no_read_workqueue --perf-no_write_workqueue /dev/sda2 secure
```

## 学习要点

1. 性能测试方法论
2. 加密算法选择
3. 硬件加速利用
4. 性能优化技巧
5. 实际场景性能预期
