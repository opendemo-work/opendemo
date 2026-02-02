#!/bin/bash

# 系统性能监控脚本
# 功能：基于tsar的自动化系统性能监控和分析

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 全局变量
LOG_DIR="/var/log/system_monitor"
REPORT_DIR="/tmp/system_analysis_$(date +%Y%m%d_%H%M%S)"
INTERVAL=5
DURATION=3600  # 默认监控1小时

# 创建必要目录
mkdir -p "$LOG_DIR" "$REPORT_DIR"

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_DIR/monitor.log"
}

# 检查依赖
check_dependencies() {
    log "检查系统依赖..."
    
    if ! command -v tsar &> /dev/null; then
        log "${RED}错误: tsar命令未找到${NC}"
        log "请先安装tsar工具"
        exit 1
    fi
    
    if ! command -v bc &> /dev/null; then
        log "${YELLOW}警告: bc计算器未安装，部分计算功能受限${NC}"
    fi
    
    log "${GREEN}依赖检查完成${NC}"
}

# 系统基本信息收集
collect_system_info() {
    log "收集系统基本信息..."
    
    {
        echo "=== 系统基本信息 ==="
        echo "收集时间: $(date)"
        echo "主机名: $(hostname)"
        echo "内核版本: $(uname -r)"
        echo "操作系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
        echo "CPU信息: $(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
        echo "CPU核心数: $(nproc)"
        echo "总内存: $(free -h | awk '/^Mem:/ {print $2}')"
        echo "总交换空间: $(free -h | awk '/^Swap:/ {print $2}')"
        echo ""
        
        echo "=== 文件系统信息 ==="
        df -h | head -10
        echo ""
        
        echo "=== 网络接口信息 ==="
        ip addr show | grep -E '^[0-9]+:|inet ' | head -15
        
    } > "$REPORT_DIR/system_info.txt"
    
    log "${GREEN}系统信息收集完成${NC}"
}

# 实时性能监控
real_time_monitoring() {
    log "开始实时性能监控..."
    
    local counter=0
    local max_iterations=$((DURATION / INTERVAL))
    
    # 监控的主要模块
    local monitor_modules="--cpu --mem --load --io --traffic --tcp"
    
    # 创建监控数据文件
    local data_file="$REPORT_DIR/monitoring_data.csv"
    echo "timestamp,cpu_util,mem_util,load_avg,io_wait,network_in,network_out,tcp_conn" > "$data_file"
    
    log "监控将持续 $((DURATION/60)) 分钟，间隔 ${INTERVAL} 秒"
    
    trap 'log "监控被中断"; generate_summary_report; exit 0' INT TERM
    
    while [ $counter -lt $max_iterations ]; do
        counter=$((counter + 1))
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        
        # 获取各项性能指标
        local cpu_data=$(tsar --cpu -i 1 2>/dev/null | tail -1 | awk '{print $2}')
        local mem_data=$(tsar --mem -i 1 2>/dev/null | tail -1 | awk '{print $8}')
        local load_data=$(tsar --load -i 1 2>/dev/null | tail -1 | awk '{print $2}')
        local io_data=$(tsar --io -i 1 2>/dev/null | tail -1 | awk '{print $6}')
        local net_data=$(tsar --traffic -i 1 2>/dev/null | tail -1 | awk '{print $2","$3}')
        local tcp_data=$(tsar --tcp -i 1 2>/dev/null | tail -1 | awk '{print $2}')
        
        # 处理空值
        cpu_data=${cpu_data:-0}
        mem_data=${mem_data:-0}
        load_data=${load_data:-0}
        io_data=${io_data:-0}
        net_data=${net_data:-0,0}
        tcp_data=${tcp_data:-0}
        
        # 写入CSV文件
        echo "$timestamp,$cpu_data,$mem_data,$load_data,$io_data,$net_data,$tcp_data" >> "$data_file"
        
        # 每10次迭代输出一次状态
        if [ $((counter % 10)) -eq 0 ]; then
            log "已完成 $counter/$max_iterations 次采样"
        fi
        
        sleep $INTERVAL
    done
    
    log "${GREEN}实时监控完成${NC}"
}

# 性能异常检测
detect_performance_anomalies() {
    log "检测性能异常..."
    
    local data_file="$REPORT_DIR/monitoring_data.csv"
    
    if [ ! -f "$data_file" ]; then
        log "${YELLOW}警告: 监控数据文件不存在${NC}"
        return
    fi
    
    {
        echo "=== 性能异常检测报告 ==="
        echo "分析时间: $(date)"
        echo ""
        
        # CPU使用率异常检测 (>80%)
        local high_cpu_count=$(awk -F',' 'NR>1 && $2>80 {count++} END {print count+0}' "$data_file")
        echo "CPU使用率超过80%的次数: $high_cpu_count"
        
        # 内存使用率异常检测 (>90%)
        local high_mem_count=$(awk -F',' 'NR>1 && $3>90 {count++} END {print count+0}' "$data_file")
        echo "内存使用率超过90%的次数: $high_mem_count"
        
        # 系统负载异常检测 (>CPU核心数)
        local cpu_cores=$(nproc)
        local high_load_count=$(awk -F',' -v cores="$cpu_cores" 'NR>1 && $4>cores {count++} END {print count+0}' "$data_file")
        echo "系统负载超过CPU核心数的次数: $high_load_count"
        
        # IO等待时间异常检测 (>50ms)
        local high_io_count=$(awk -F',' 'NR>1 && $5>50 {count++} END {print count+0}' "$data_file")
        echo "IO等待时间超过50ms的次数: $high_io_count"
        
        echo ""
        echo "=== 性能统计摘要 ==="
        
        # 计算平均值
        awk -F',' 'NR>1 {
            cpu_sum+=$2; mem_sum+=$3; load_sum+=$4; io_sum+=$5; 
            count++
        } END {
            if(count>0) {
                printf "平均CPU使用率: %.2f%%\n", cpu_sum/count
                printf "平均内存使用率: %.2f%%\n", mem_sum/count
                printf "平均系统负载: %.2f\n", load_sum/count
                printf "平均IO等待时间: %.2fms\n", io_sum/count
            }
        }' "$data_file"
        
        echo ""
        echo "=== 性能峰值记录 ==="
        
        # 找出各项指标的最大值
        awk -F',' 'NR>1 {
            if($2>max_cpu) {max_cpu=$2; cpu_time=$1}
            if($3>max_mem) {max_mem=$3; mem_time=$1}
            if($4>max_load) {max_load=$4; load_time=$1}
            if($5>max_io) {max_io=$5; io_time=$1}
        } END {
            printf "最高CPU使用率: %.2f%% (时间: %s)\n", max_cpu, cpu_time
            printf "最高内存使用率: %.2f%% (时间: %s)\n", max_mem, mem_time
            printf "最高系统负载: %.2f (时间: %s)\n", max_load, load_time
            printf "最高IO等待时间: %.2fms (时间: %s)\n", max_io, io_time
        }' "$data_file"
        
    } > "$REPORT_DIR/anomaly_report.txt"
    
    log "${GREEN}异常检测完成${NC}"
}

# 生成监控报告
generate_summary_report() {
    log "生成监控总结报告..."
    
    local report_file="$REPORT_DIR/final_report.txt"
    
    {
        echo "==========================================="
        echo "         系统性能监控总结报告"
        echo "==========================================="
        echo "监控时间: $(date)"
        echo "监控主机: $(hostname)"
        echo "报告目录: $REPORT_DIR"
        echo ""
        
        echo "=== 监控概要 ==="
        echo "• 监控时长: $((DURATION/60)) 分钟"
        echo "• 采样间隔: ${INTERVAL} 秒"
        echo "• 总采样次数: $((DURATION/INTERVAL))"
        echo ""
        
        echo "=== 系统状态评估 ==="
        
        # 基于监控数据给出系统健康评分
        local data_file="$REPORT_DIR/monitoring_data.csv"
        if [ -f "$data_file" ]; then
            local score=100
            
            # CPU评分 (权重30%)
            local cpu_violations=$(awk -F',' 'NR>1 && $2>80 {count++} END {print count+0}' "$data_file")
            local cpu_score=$((30 - cpu_violations * 2))
            [ $cpu_score -lt 0 ] && cpu_score=0
            score=$((score - (30 - cpu_score)))
            
            # 内存评分 (权重25%)
            local mem_violations=$(awk -F',' 'NR>1 && $3>90 {count++} END {print count+0}' "$data_file")
            local mem_score=$((25 - mem_violations * 3))
            [ $mem_score -lt 0 ] && mem_score=0
            score=$((score - (25 - mem_score)))
            
            # 负载评分 (权重25%)
            local cpu_cores=$(nproc)
            local load_violations=$(awk -F',' -v cores="$cpu_cores" 'NR>1 && $4>cores {count++} END {print count+0}' "$data_file")
            local load_score=$((25 - load_violations * 3))
            [ $load_score -lt 0 ] && load_score=0
            score=$((score - (25 - load_score)))
            
            # IO评分 (权重20%)
            local io_violations=$(awk -F',' 'NR>1 && $5>50 {count++} END {print count+0}' "$data_file")
            local io_score=$((20 - io_violations * 4))
            [ $io_score -lt 0 ] && io_score=0
            score=$((score - (20 - io_score)))
            
            echo "系统健康评分: ${score}/100"
            
            if [ $score -ge 80 ]; then
                echo "${GREEN}系统状态良好${NC}"
            elif [ $score -ge 60 ]; then
                echo "${YELLOW}系统状态一般，建议关注${NC}"
            else
                echo "${RED}系统状态较差，需要立即处理${NC}"
            fi
        fi
        
        echo ""
        echo "=== 建议措施 ==="
        
        # 根据异常检测结果提供建议
        local anomaly_file="$REPORT_DIR/anomaly_report.txt"
        if [ -f "$anomaly_file" ]; then
            local high_cpu=$(grep "CPU使用率超过80%" "$anomaly_file" | awk '{print $NF}')
            local high_mem=$(grep "内存使用率超过90%" "$anomaly_file" | awk '{print $NF}')
            local high_load=$(grep "系统负载超过CPU核心数" "$anomaly_file" | awk '{print $NF}')
            
            [ "$high_cpu" != "0" ] && echo "• CPU使用率偏高，建议检查高CPU消耗进程"
            [ "$high_mem" != "0" ] && echo "• 内存使用率偏高，建议检查内存泄漏或增加内存"
            [ "$high_load" != "0" ] && echo "• 系统负载过高，建议优化应用或扩容"
        fi
        
        echo ""
        echo "=== 报告文件列表 ==="
        echo "• 系统基本信息: system_info.txt"
        echo "• 监控原始数据: monitoring_data.csv"
        echo "• 异常检测报告: anomaly_report.txt"
        echo "• 本总结报告: final_report.txt"
        
    } > "$report_file"
    
    log "${GREEN}总结报告生成完成${NC}"
    log "报告位置: $report_file"
}

# 主函数
main() {
    echo "${BLUE}=== 系统性能监控工具 ===${NC}"
    echo "作者: OpenDemo Team"
    echo "版本: 1.0.0"
    echo ""
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --duration=*)
                DURATION="${1#*=}"
                shift
                ;;
            --interval=*)
                INTERVAL="${1#*=}"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [选项]"
                echo "选项:"
                echo "  --duration=N    监控持续时间(秒) (默认: 3600)"
                echo "  --interval=N    采样间隔(秒) (默认: 5)"
                echo "  --help,-h       显示帮助信息"
                exit 0
                ;;
        esac
    done
    
    log "开始系统性能监控..."
    
    check_dependencies
    collect_system_info
    real_time_monitoring
    detect_performance_anomalies
    generate_summary_report
    
    echo ""
    echo "${GREEN}监控完成！${NC}"
    echo "详细报告请查看: $REPORT_DIR"
    echo "日志文件位置: $LOG_DIR/monitor.log"
}

# 执行主函数
main "$@"