#!/bin/bash

# 网络连接分析脚本
# 功能：深度分析网络连接状态和潜在问题

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 全局变量
OUTPUT_DIR="/tmp/connection_analysis_$(date +%Y%m%d_%H%M%S)"
REPORT_FILE="$OUTPUT_DIR/report.txt"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$REPORT_FILE"
}

# 检查root权限
check_privileges() {
    if [[ $EUID -ne 0 ]]; then
        log "${YELLOW}警告: 建议以root权限运行以获取完整信息${NC}"
    fi
}

# 基础网络信息收集
collect_network_info() {
    log "收集基础网络信息..."
    
    {
        echo "=== 系统网络信息 ==="
        echo "主机名: $(hostname)"
        echo "系统时间: $(date)"
        echo "内核版本: $(uname -r)"
        echo ""
        
        echo "=== 网络接口信息 ==="
        ip addr show 2>/dev/null || ifconfig 2>/dev/null || echo "无法获取网络接口信息"
        echo ""
        
        echo "=== 路由表信息 ==="
        ip route show 2>/dev/null || route -n 2>/dev/null || echo "无法获取路由信息"
        echo ""
        
        echo "=== DNS配置 ==="
        cat /etc/resolv.conf 2>/dev/null || echo "无法读取DNS配置"
        echo ""
        
    } > "$OUTPUT_DIR/network_info.txt"
    
    log "${GREEN}基础网络信息收集完成${NC}"
}

# 详细连接分析
analyze_connections_detailed() {
    log "进行详细连接分析..."
    
    # 获取完整的netstat输出
    netstat_output=$(netstat -tulnpae 2>/dev/null || netstat -tulnp 2>/dev/null)
    
    {
        echo "=== 完整网络连接信息 ==="
        echo "$netstat_output"
        echo ""
        
        echo "=== TCP连接状态统计 ==="
        echo "$netstat_output" | awk '/^tcp/ {print $6}' | sort | uniq -c | sort -nr
        echo ""
        
        echo "=== UDP监听端口 ==="
        echo "$netstat_output" | grep '^udp' | grep LISTEN
        echo ""
        
        echo "=== 按进程分组的连接数 ==="
        echo "$netstat_output" | grep -v '^Active' | grep -v '^Proto' | awk '{print $7}' | grep -v '^-$' | sort | uniq -c | sort -nr | head -20
        echo ""
        
        echo "=== 按用户分组的连接数 ==="
        if echo "$netstat_output" | grep -q 'User'; then
            echo "$netstat_output" | awk 'NR>2 {print $8}' | sort | uniq -c | sort -nr
        else
            echo "当前netstat版本不支持用户信息显示"
        fi
        echo ""
        
    } > "$OUTPUT_DIR/detailed_analysis.txt"
    
    log "${GREEN}详细连接分析完成${NC}"
}

# 安全审计分析
security_audit() {
    log "执行安全审计分析..."
    
    netstat_output=$(netstat -tulnp 2>/dev/null)
    
    {
        echo "=== 安全审计报告 ==="
        echo "生成时间: $(date)"
        echo ""
        
        # 检测对外开放的服务
        echo "=== 对外开放的服务 ==="
        external_services=$(echo "$netstat_output" | grep LISTEN | grep -v '127.0.0.1' | grep -v '::1')
        if [ -n "$external_services" ]; then
            echo "$external_services"
        else
            echo "未发现对外开放的服务"
        fi
        echo ""
        
        # 检测非常见端口
        echo "=== 监听非常见端口的服务 ==="
        unusual_ports=$(echo "$netstat_output" | grep LISTEN | awk '{print $4}' | cut -d: -f2 | \
            grep -E '^(10[0-9]{3}|[2-9][0-9]{4}|[0-9]{5})$' | sort -n)
        if [ -n "$unusual_ports" ]; then
            echo "发现以下非常见端口:"
            echo "$unusual_ports"
            echo ""
            echo "对应的服务详情:"
            for port in $unusual_ports; do
                echo "$netstat_output" | grep ":$port " | grep LISTEN
            done
        else
            echo "未发现监听非常见端口的服务"
        fi
        echo ""
        
        # 检测大量连接的IP
        echo "=== 连接数异常的IP地址 ==="
        high_conn_ips=$(echo "$netstat_output" | grep ESTABLISHED | awk '{print $5}' | \
            cut -d: -f1 | sort | uniq -c | sort -nr | awk '$1 > 20')
        if [ -n "$high_conn_ips" ]; then
            echo "$high_conn_ips"
        else
            echo "未发现连接数异常的IP地址"
        fi
        echo ""
        
        # 检测未知进程
        echo "=== 未知进程的网络连接 ==="
        unknown_processes=$(echo "$netstat_output" | grep -E '(unknown|rpc\.[0-9]+)')
        if [ -n "$unknown_processes" ]; then
            echo "$unknown_processes"
        else
            echo "未发现未知进程的网络连接"
        fi
        echo ""
        
    } > "$OUTPUT_DIR/security_audit.txt"
    
    log "${GREEN}安全审计分析完成${NC}"
}

# 性能分析
performance_analysis() {
    log "执行性能分析..."
    
    {
        echo "=== 网络性能分析 ==="
        echo "分析时间: $(date)"
        echo ""
        
        # TIME_WAIT连接分析
        echo "=== TIME_WAIT连接分析 ==="
        time_wait_count=$(netstat -an | grep TIME_WAIT | wc -l)
        echo "TIME_WAIT连接数: $time_wait_count"
        
        if [ $time_wait_count -gt 1000 ]; then
            echo "${YELLOW}警告: TIME_WAIT连接过多 ($time_wait_count)，可能影响性能${NC}"
        fi
        echo ""
        
        # SYN连接分析
        echo "=== SYN连接状态分析 ==="
        syn_sent_count=$(netstat -an | grep SYN_SENT | wc -l)
        syn_recv_count=$(netstat -an | grep SYN_RECV | wc -l)
        echo "SYN_SENT连接数: $syn_sent_count"
        echo "SYN_RECV连接数: $syn_recv_count"
        
        if [ $syn_sent_count -gt 100 ] || [ $syn_recv_count -gt 100 ]; then
            echo "${YELLOW}警告: SYN连接状态异常，可能存在连接问题${NC}"
        fi
        echo ""
        
        # 连接速率估算
        echo "=== 连接活跃度分析 ==="
        established_count=$(netstat -an | grep ESTABLISHED | wc -l)
        listening_count=$(netstat -tln | grep LISTEN | wc -l)
        echo "已建立连接数: $established_count"
        echo "监听端口数: $listening_count"
        echo "平均每个端口连接数: $((established_count / (listening_count > 0 ? listening_count : 1)))"
        echo ""
        
    } > "$OUTPUT_DIR/performance_analysis.txt"
    
    log "${GREEN}性能分析完成${NC}"
}

# 生成综合报告
generate_report() {
    log "生成综合分析报告..."
    
    {
        echo "==========================================="
        echo "         网络连接深度分析报告"
        echo "==========================================="
        echo "生成时间: $(date)"
        echo "分析主机: $(hostname)"
        echo "输出目录: $OUTPUT_DIR"
        echo ""
        
        echo "=== 报告概要 ==="
        echo "• 基础网络信息已保存至: network_info.txt"
        echo "• 详细连接分析已保存至: detailed_analysis.txt"
        echo "• 安全审计报告已保存至: security_audit.txt"
        echo "• 性能分析报告已保存至: performance_analysis.txt"
        echo ""
        
        echo "=== 关键发现 ==="
        
        # 统计关键指标
        total_tcp=$(netstat -tan | grep '^tcp' | wc -l)
        established_conn=$(netstat -tan | grep ESTABLISHED | wc -l)
        listening_ports=$(netstat -tln | grep LISTEN | wc -l)
        
        echo "总TCP连接数: $total_tcp"
        echo "已建立连接数: $established_conn"
        echo "监听端口数: $listening_ports"
        echo ""
        
        # 安全风险提示
        external_services=$(netstat -tulnp 2>/dev/null | grep LISTEN | grep -v '127.0.0.1' | grep -v '::1' | wc -l)
        if [ $external_services -gt 0 ]; then
            echo "${YELLOW}发现 $external_services 个对外开放的服务，请检查是否必要${NC}"
        fi
        
        time_wait_count=$(netstat -an | grep TIME_WAIT | wc -l)
        if [ $time_wait_count -gt 1000 ]; then
            echo "${RED}警告: TIME_WAIT连接过多 ($time_wait_count)，建议优化网络配置${NC}"
        fi
        
    } > "$REPORT_FILE"
    
    log "${GREEN}综合报告生成完成${NC}"
    log "报告位置: $REPORT_FILE"
    log "详细分析文件位于: $OUTPUT_DIR"
}

# 主函数
main() {
    echo "${BLUE}=== 网络连接深度分析工具 ===${NC}"
    echo "作者: OpenDemo Team"
    echo "版本: 1.0.0"
    echo ""
    
    log "开始网络连接深度分析..."
    
    check_privileges
    collect_network_info
    analyze_connections_detailed
    security_audit
    performance_analysis
    generate_report
    
    echo ""
    echo "${GREEN}分析完成！${NC}"
    echo "详细报告请查看: $REPORT_FILE"
    echo "所有分析文件保存在: $OUTPUT_DIR"
}

# 执行主函数
main "$@"