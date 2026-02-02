#!/bin/bash

# 网络连接监控脚本
# 功能：实时监控网络连接状态和变化

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 全局变量
LOG_FILE="/tmp/network_monitor.log"
INTERVAL=5
MAX_LOG_LINES=1000

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# 检查依赖
check_dependencies() {
    log "检查系统依赖..."
    
    if ! command -v netstat &> /dev/null; then
        log "${RED}错误: netstat命令未找到${NC}"
        log "请安装net-tools包:"
        log "Ubuntu/Debian: sudo apt-get install net-tools"
        log "CentOS/RHEL: sudo yum install net-tools"
        exit 1
    fi
    
    if ! command -v awk &> /dev/null; then
        log "${RED}错误: awk命令未找到${NC}"
        exit 1
    fi
    
    log "${GREEN}依赖检查完成${NC}"
}

# 获取当前连接快照
get_connection_snapshot() {
    netstat -tulnp 2>/dev/null | tail -n +3
}

# 分析连接状态统计
analyze_connections() {
    local snapshot="$1"
    
    echo "=== 当前连接状态统计 ==="
    echo "$snapshot" | awk '/^tcp/ {print $6}' | sort | uniq -c | sort -nr
    
    echo ""
    echo "=== 监听端口统计 ==="
    echo "$snapshot" | grep LISTEN | awk '{print $4}' | cut -d: -f2 | sort -n | uniq -c
    
    echo ""
    echo "=== 连接数最多的远程IP ==="
    echo "$snapshot" | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -10
}

# 检测异常连接
detect_anomalies() {
    local snapshot="$1"
    
    echo "=== 异常连接检测 ==="
    
    # 检测非本地监听的服务
    local external_listeners=$(echo "$snapshot" | grep LISTEN | grep -v '127.0.0.1' | grep -v '::1')
    if [ -n "$external_listeners" ]; then
        echo "${YELLOW}发现对外监听的服务:${NC}"
        echo "$external_listeners"
    fi
    
    # 检测大量连接的IP
    local high_conn_ips=$(echo "$snapshot" | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | awk '$1 > 50')
    if [ -n "$high_conn_ips" ]; then
        echo "${YELLOW}发现连接数超过50的IP:${NC}"
        echo "$high_conn_ips"
    fi
    
    # 检测不常见的端口
    local unusual_ports=$(echo "$snapshot" | grep LISTEN | awk '{print $4}' | cut -d: -f2 | grep -E '^(10[0-9]{3}|[2-9][0-9]{4})$')
    if [ -n "$unusual_ports" ]; then
        echo "${YELLOW}发现监听不常见端口的服务:${NC}"
        echo "$unusual_ports"
    fi
}

# 实时监控循环
real_time_monitor() {
    local prev_snapshot=""
    local counter=0
    
    log "开始实时网络监控，按Ctrl+C退出"
    
    trap 'log "监控结束"; exit 0' INT TERM
    
    while true; do
        counter=$((counter + 1))
        log "第 $counter 次监控"
        
        local current_snapshot=$(get_connection_snapshot)
        
        # 首次运行只显示基线
        if [ -z "$prev_snapshot" ]; then
            echo ""
            analyze_connections "$current_snapshot"
            echo ""
            detect_anomalies "$current_snapshot"
            prev_snapshot="$current_snapshot"
            sleep $INTERVAL
            continue
        fi
        
        # 比较连接变化
        local diff_output=$(diff <(echo "$prev_snapshot") <(echo "$current_snapshot") 2>/dev/null || true)
        
        if [ -n "$diff_output" ]; then
            log "${YELLOW}检测到连接状态变化${NC}"
            echo "=== 连接变化详情 ==="
            echo "$diff_output"
            echo ""
            
            # 重新分析当前状态
            analyze_connections "$current_snapshot"
            echo ""
            detect_anomalies "$current_snapshot"
        else
            log "连接状态无变化"
        fi
        
        prev_snapshot="$current_snapshot"
        
        # 控制日志文件大小
        if [ $(wc -l < "$LOG_FILE") -gt $MAX_LOG_LINES ]; then
            tail -n $((MAX_LOG_LINES/2)) "$LOG_FILE" > "${LOG_FILE}.tmp"
            mv "${LOG_FILE}.tmp" "$LOG_FILE"
            log "日志文件已清理"
        fi
        
        sleep $INTERVAL
    done
}

# 主函数
main() {
    echo "${BLUE}=== Linux网络连接监控工具 ===${NC}"
    echo "作者: OpenDemo Team"
    echo "版本: 1.0.0"
    echo ""
    
    # 解析命令行参数
    case "${1:-}" in
        --interval=*)
            INTERVAL="${1#*=}"
            shift
            ;;
        --log-file=*)
            LOG_FILE="${1#*=}"
            shift
            ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  --interval=N    设置监控间隔秒数 (默认: 5)"
            echo "  --log-file=PATH 设置日志文件路径 (默认: /tmp/network_monitor.log)"
            echo "  --help,-h       显示帮助信息"
            exit 0
            ;;
    esac
    
    check_dependencies
    real_time_monitor
}

# 执行主函数
main "$@"