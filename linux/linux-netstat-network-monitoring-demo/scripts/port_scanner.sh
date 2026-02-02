#!/bin/bash

# 端口扫描和连接测试脚本
# 功能：扫描常用端口和服务连接状态

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 常用端口和服务映射
declare -A COMMON_PORTS=(
    [21]="FTP"
    [22]="SSH"
    [23]="Telnet"
    [25]="SMTP"
    [53]="DNS"
    [80]="HTTP"
    [110]="POP3"
    [143]="IMAP"
    [443]="HTTPS"
    [993]="IMAPS"
    [995]="POP3S"
    [3306]="MySQL"
    [5432]="PostgreSQL"
    [6379]="Redis"
    [27017]="MongoDB"
    [8080]="HTTP-Alt"
    [8443]="HTTPS-Alt"
)

# 全局变量
TARGET_HOST="localhost"
PORT_RANGE="1-1000"
TIMEOUT=3
OUTPUT_FILE="/tmp/port_scan_results_$(date +%Y%m%d_%H%M%S).txt"

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$OUTPUT_FILE"
}

# 显示帮助信息
show_help() {
    echo "端口扫描工具"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --host HOST     目标主机 (默认: localhost)"
    echo "  -p, --ports RANGE   端口范围 (默认: 1-1000)"
    echo "  -t, --timeout SEC   连接超时秒数 (默认: 3)"
    echo "  -o, --output FILE   输出文件路径"
    echo "  --common-only       仅扫描常用端口"
    echo "  --help              显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --host 192.168.1.1 --ports 1-1000"
    echo "  $0 --common-only --timeout 5"
    echo "  $0 -h example.com -p 80,443,8080"
}

# 解析命令行参数
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--host)
                TARGET_HOST="$2"
                shift 2
                ;;
            -p|--ports)
                PORT_RANGE="$2"
                shift 2
                ;;
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --common-only)
                PORT_RANGE="common"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                echo "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 检查网络工具
check_tools() {
    log "检查必要的网络工具..."
    
    local missing_tools=()
    
    if ! command -v nc &> /dev/null && ! command -v telnet &> /dev/null; then
        missing_tools+=("nc (netcat) 或 telnet")
    fi
    
    if ! command -v timeout &> /dev/null; then
        missing_tools+=("timeout")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log "${RED}缺少必要的工具: ${missing_tools[*]}${NC}"
        log "请安装缺失的工具后再运行此脚本"
        exit 1
    fi
    
    log "${GREEN}工具检查通过${NC}"
}

# 解析端口范围
parse_port_range() {
    local ports=()
    
    if [ "$PORT_RANGE" = "common" ]; then
        # 使用常用端口
        for port in "${!COMMON_PORTS[@]}"; do
            ports+=("$port")
        done
    elif [[ "$PORT_RANGE" =~ ^[0-9]+-[0-9]+$ ]]; then
        # 范围格式: start-end
        local start=$(echo "$PORT_RANGE" | cut -d- -f1)
        local end=$(echo "$PORT_RANGE" | cut -d- -f2)
        for ((port=start; port<=end; port++)); do
            ports+=("$port")
        done
    elif [[ "$PORT_RANGE" =~ ^[0-9,]+$ ]]; then
        # 列表格式: port1,port2,port3
        IFS=',' read -ra port_list <<< "$PORT_RANGE"
        ports=("${port_list[@]}")
    else
        log "${RED}无效的端口范围格式: $PORT_RANGE${NC}"
        exit 1
    fi
    
    echo "${ports[@]}"
}

# 测试单个端口连接
test_port_connection() {
    local host="$1"
    local port="$2"
    local service_name="${COMMON_PORTS[$port]:-Unknown}"
    
    # 使用nc进行连接测试
    if command -v nc &> /dev/null; then
        if timeout "$TIMEOUT" nc -z "$host" "$port" 2>/dev/null; then
            echo "OPEN|$host|$port|$service_name"
            return 0
        fi
    # 备用telnet测试
    elif command -v telnet &> /dev/null; then
        if echo "quit" | timeout "$TIMEOUT" telnet "$host" "$port" 2>&1 | grep -q "Connected"; then
            echo "OPEN|$host|$port|$service_name"
            return 0
        fi
    fi
    
    echo "CLOSED|$host|$port|$service_name"
    return 1
}

# 执行端口扫描
perform_port_scan() {
    local ports=($(parse_port_range))
    local open_ports=()
    local closed_ports=()
    local total_ports=${#ports[@]}
    local current=0
    
    log "开始扫描目标: $TARGET_HOST"
    log "端口范围: $PORT_RANGE"
    log "超时设置: ${TIMEOUT}秒"
    log "总计端口数: $total_ports"
    log ""
    
    # 输出表头
    printf "%-8s %-15s %-8s %-20s %s\n" "状态" "主机" "端口" "服务" "详情" | tee -a "$OUTPUT_FILE"
    printf "%-8s %-15s %-8s %-20s %s\n" "--------" "---------------" "--------" "--------------------" "--------------------" | tee -a "$OUTPUT_FILE"
    
    # 扫描每个端口
    for port in "${ports[@]}"; do
        current=$((current + 1))
        printf "\r进度: %d/%d (%.1f%%)" "$current" "$total_ports" "$(echo "scale=1; $current*100/$total_ports" | bc -l)"
        
        result=$(test_port_connection "$TARGET_HOST" "$port")
        IFS='|' read -ra parts <<< "$result"
        status="${parts[0]}"
        host="${parts[1]}"
        port_num="${parts[2]}"
        service="${parts[3]}"
        
        # 彩色输出
        if [ "$status" = "OPEN" ]; then
            printf "%-8s %-15s %-8s %-20s %s\n" "${GREEN}$status${NC}" "$host" "$port_num" "$service" "端口开放" | tee -a "$OUTPUT_FILE"
            open_ports+=("$port_num")
        else
            printf "%-8s %-15s %-8s %-20s %s\n" "${RED}$status${NC}" "$host" "$port_num" "$service" "端口关闭" | tee -a "$OUTPUT_FILE"
            closed_ports+=("$port_num")
        fi
    done
    
    echo "" | tee -a "$OUTPUT_FILE"
    log "扫描完成!"
    log "开放端口数: ${#open_ports[@]}"
    log "关闭端口数: ${#closed_ports[@]}"
    
    # 显示开放端口摘要
    if [ ${#open_ports[@]} -gt 0 ]; then
        log "${GREEN}开放的端口:${NC} ${open_ports[*]}"
    else
        log "${YELLOW}未发现开放的端口${NC}"
    fi
}

# 生成扫描报告
generate_report() {
    log ""
    log "=== 扫描报告摘要 ==="
    log "目标主机: $TARGET_HOST"
    log "扫描时间: $(date)"
    log "使用工具: ${0##*/}"
    
    # 添加系统信息
    log ""
    log "=== 系统信息 ==="
    log "本地主机: $(hostname)"
    log "本地IP: $(hostname -I 2>/dev/null || echo '无法获取')"
    log "扫描工具版本: 1.0.0"
}

# 主函数
main() {
    echo "${BLUE}=== 端口扫描工具 ===${NC}"
    echo "作者: OpenDemo Team"
    echo "版本: 1.0.0"
    echo ""
    
    parse_arguments "$@"
    check_tools
    perform_port_scan
    generate_report
    
    log ""
    log "${GREEN}扫描结果已保存至: $OUTPUT_FILE${NC}"
    log "您可以使用以下命令查看结果:"
    log "  cat $OUTPUT_FILE"
    log "  grep OPEN $OUTPUT_FILE  # 只查看开放端口"
}

# 执行主函数
main "$@"