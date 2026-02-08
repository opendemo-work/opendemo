# Linux 技术栈命名大全

本文件定义了Linux系统管理中各类命令、脚本、配置文件、服务等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、系统服务命名规范

### 1.1 systemd服务单元文件
```bash
# 系统服务命名
/etc/systemd/system/
├── web-app.service              # 应用名称.service
├── database-server.service      # 服务类型-功能.service
├── backup-scheduler.service     # 功能-类型.service
├── monitoring-agent.service     # 监控-代理.service
└── log-rotator.service          # 日志-轮转.service

# 服务模板文件
/etc/systemd/system/
├── web-app@.service             # 应用名称@.service (模板服务)
└── worker@.service              # 工作进程@.service (实例化服务)
```

### 1.2 服务配置示例
```ini
# /etc/systemd/system/web-app.service
[Unit]
Description=Web Application Service
Documentation=https://company.com/docs/web-app
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service
RequiresMountsFor=/var/www/web-app

[Service]
Type=simple
User=webapp
Group=webapp
WorkingDirectory=/var/www/web-app
Environment=NODE_ENV=production
EnvironmentFile=/etc/web-app/environment
ExecStart=/usr/bin/node /var/www/web-app/server.js
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=web-app
TimeoutStopSec=30

# 资源限制
LimitNOFILE=65536
LimitNPROC=4096
MemoryMax=1G
CPUQuota=50%

# 安全配置
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/www/web-app/uploads /var/log/web-app

[Install]
WantedBy=multi-user.target
```

### 1.3 定时任务服务
```ini
# /etc/systemd/system/daily-backup.timer
[Unit]
Description=Daily Backup Timer
Requires=backup-scheduler.service

[Timer]
OnCalendar=daily
AccuracySec=1h
Persistent=true

[Install]
WantedBy=timers.target

# /etc/systemd/system/daily-backup.service
[Unit]
Description=Daily Backup Service
After=local-fs.target

[Service]
Type=oneshot
User=backup
ExecStart=/usr/local/bin/backup-script.sh
```

## 二、脚本和可执行文件命名

### 2.1 系统管理脚本
```bash
# 系统监控脚本
/usr/local/bin/
├── system-health-check.sh       # 系统-功能-类型.sh
├── disk-space-monitor.sh        # 磁盘-空间-监控.sh
├── network-connectivity-test.sh # 网络-连接性-测试.sh
├── service-status-report.sh     # 服务-状态-报告.sh
└── security-audit.sh            # 安全-审计.sh

# 应用部署脚本
/opt/deploy/
├── deploy-web-app.sh            # 部署-应用名称.sh
├── rollback-web-app.sh          # 回滚-应用名称.sh
├── backup-database.sh           # 备份-数据库.sh
└── restore-database.sh          # 恢复-数据库.sh

# 日常维护脚本
/usr/local/admin/
├── cleanup-temp-files.sh        # 清理-临时文件.sh
├── rotate-logs.sh               # 轮转-日志.sh
├── update-system.sh             # 更新-系统.sh
└── create-user-account.sh       # 创建-用户-账户.sh
```

### 2.2 脚本头部规范
```bash
#!/bin/bash
# system-health-check.sh - 系统健康检查脚本
# 作者: System Administrator
# 版本: 1.2.3
# 创建时间: 2023-01-01
# 最后修改: 2023-12-01
#
# 功能描述:
#   - 检查系统资源使用情况
#   - 监控关键服务状态
#   - 报告系统健康状况
#
# 使用方法:
#   ./system-health-check.sh [--verbose] [--email recipient@example.com]

set -euo pipefail
IFS=$'\n\t'

# 全局变量
SCRIPT_NAME=$(basename "$0")
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"
TEMP_DIR="/tmp/${SCRIPT_NAME%.sh}_$$"
VERBOSE=false
EMAIL_RECIPIENT=""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    local message="$1"
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $message${NC}" | tee -a "$LOG_FILE"
}

log_warn() {
    local message="$1"
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $message${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    local message="$1"
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $message${NC}" | tee -a "$LOG_FILE" >&2
}

# 参数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=true
            shift
            ;;
        --email)
            EMAIL_RECIPIENT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $SCRIPT_NAME [--verbose] [--email recipient]"
            exit 0
            ;;
        *)
            log_error "Unknown parameter: $1"
            exit 1
            ;;
    esac
done
```

## 三、配置文件命名规范

### 3.1 应用配置文件
```bash
# 应用配置目录结构
/etc/
├── web-app/                     # 应用名称目录
│   ├── web-app.conf             # 应用名称.conf
│   ├── database.ini             # 数据库.ini
│   ├── logging.yaml             # 日志.yaml
│   └── ssl/                     # SSL证书目录
│       ├── web-app.crt          # 应用名称.crt
│       └── web-app.key          # 应用名称.key
│
├── nginx/
│   ├── sites-available/         # 站点配置
│   │   ├── web-app.conf         # 应用名称.conf
│   │   └── api-gateway.conf     # API网关.conf
│   └── sites-enabled/
│       └── web-app.conf -> ../sites-available/web-app.conf
│
└── postgresql/
    ├── postgresql.conf          # 数据库主配置
    ├── pg_hba.conf              # 访问控制配置
    └── conf.d/                  # 自定义配置目录
        ├── performance.conf     # 性能优化.conf
        └── security.conf        # 安全配置.conf
```

### 3.2 环境配置文件
```bash
# 环境变量配置
/etc/environment.d/
├── web-app-env.conf             # 应用名称-env.conf
├── database-env.conf            # 数据库-env.conf
└── monitoring-env.conf          # 监控-env.conf

# 应用特定环境文件
/etc/web-app/
├── environment                  # 环境变量文件
├── environment.production       # 环境变量.生产环境
├── environment.staging          # 环境变量.预发布
└── environment.development      # 环境变量.开发环境
```

## 四、日志文件命名规范

### 4.1 系统日志
```bash
# 系统日志目录
/var/log/
├── system/                      # 系统日志目录
│   ├── kernel.log               # 内核.log
│   ├── boot.log                 # 启动.log
│   ├── dmesg.log                # 内核消息.log
│   └── secure.log               # 安全日志.log
│
├── applications/                # 应用日志目录
│   ├── web-app/                 # 应用名称目录
│   │   ├── access.log           # 访问.log
│   │   ├── error.log            # 错误.log
│   │   ├── application.log      # 应用.log
│   │   └── audit.log            # 审计.log
│   │
│   ├── database/                # 数据库日志
│   │   ├── postgresql.log       # 数据库名称.log
│   │   ├── slow-query.log       # 慢查询.log
│   │   └── connection.log       # 连接.log
│   │
│   └── monitoring/              # 监控日志
│       ├── prometheus.log       # 监控工具.log
│       └── alertmanager.log     # 告警管理.log
│
└── security/                    # 安全日志目录
    ├── auth.log                 # 认证.log
    ├── firewall.log             # 防火墙.log
    └── intrusion.log            # 入侵检测.log
```

### 4.2 日志轮转配置
```bash
# /etc/logrotate.d/web-app
/var/log/applications/web-app/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 webapp webapp
    postrotate
        systemctl reload web-app.service > /dev/null 2>&1 || true
    endscript
}

# /etc/logrotate.d/system-logs
/var/log/system/*.log {
    weekly
    missingok
    rotate 12
    compress
    delaycompress
    notifempty
    create 0644 root root
}
```

## 五、网络配置命名规范

### 5.1 网络接口配置
```bash
# 网络配置文件
/etc/sysconfig/network-scripts/
├── ifcfg-eth0                   # 接口类型-编号
├── ifcfg-eth1                   # 接口类型-编号
├── ifcfg-bond0                  # 绑定接口-编号
├── ifcfg-br0                    # 网桥-编号
└── route-eth0                   # 路由-接口

# 网络配置示例
# /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
BOOTPROTO=static
ONBOOT=yes
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4
USERCTL=no
```

### 5.2 防火墙配置
```bash
# iptables规则文件
/etc/iptables/
├── rules.v4                     # IPv4规则
├── rules.v6                     # IPv6规则
├── web-app.rules                # 应用名称.rules
└── database.rules               # 数据库.rules

# firewalld配置
/etc/firewalld/
├── zones/                       # 区域配置
│   ├── public.xml               # 公共区域.xml
│   ├── internal.xml             # 内部区域.xml
│   └── dmz.xml                  # DMZ区域.xml
├── services/                    # 服务配置
│   ├── web-app.xml              # 应用名称.xml
│   └── database.xml             # 数据库.xml
└── ipsets/                      # IP集合
    ├── trusted-ips.xml          # 可信IP.xml
    └── blocked-ips.xml          # 阻止IP.xml
```

## 六、用户和权限命名规范

### 6.1 用户账户命名
```bash
# 系统用户命名规范
# 应用服务用户
webapp:x:1001:1001:Web Application User:/var/www/web-app:/sbin/nologin
database:x:1002:1002:Database Service User:/var/lib/postgresql:/bin/bash
monitoring:x:1003:1003:Monitoring Service User:/opt/monitoring:/sbin/nologin

# 管理员用户
sysadmin:x:1004:1004:System Administrator:/home/sysadmin:/bin/bash
dba:x:1005:1005:Database Administrator:/home/dba:/bin/bash
secadmin:x:1006:1006:Security Administrator:/home/secadmin:/bin/bash

# 临时用户
temp_user_20231201:x:2001:2001:Temporary User:/tmp/temp_user_20231201:/sbin/nologin
```

### 6.2 用户组命名
```bash
# 用户组配置
# 应用相关组
webapp:x:1001:webapp,database,nginx
database:x:1002:database,backup
monitoring:x:1003:monitoring,prometheus,grafana

# 管理员组
sysadmins:x:1004:sysadmin,dba,secadmin
developers:x:1005:dev1,dev2,dev3
operators:x:1006:operator1,operator2

# 功能组
backup:x:2001:backup,webapp,database
logging:x:2002:logging,webapp,database,monitoring
audit:x:2003:secadmin,auditor
```

## 七、监控和告警命名规范

### 7.1 监控脚本
```bash
# 监控脚本目录
/usr/local/monitoring/
├── check-system-health.sh       # 检查-系统-健康.sh
├── check-disk-space.sh          # 检查-磁盘-空间.sh
├── check-network-latency.sh     # 检查-网络-延迟.sh
├── check-service-status.sh      # 检查-服务-状态.sh
└── check-security-events.sh     # 检查-安全-事件.sh

# 自定义监控检查
/usr/local/monitoring/checks/
├── web-app-response-time.sh     # 应用名称-响应时间.sh
├── database-connection-count.sh # 数据库-连接数.sh
├── ssl-certificate-expiry.sh    # SSL证书-过期.sh
└── backup-success-check.sh      # 备份-成功-检查.sh
```

### 7.2 告警配置
```bash
# 告警规则文件
/etc/monitoring/alerts/
├── system-alerts.conf           # 系统-告警.conf
├── application-alerts.conf      # 应用-告警.conf
├── security-alerts.conf         # 安全-告警.conf
└── performance-alerts.conf      # 性能-告警.conf

# 告警脚本
/usr/local/bin/
├── send-email-alert.sh          # 发送-邮件-告警.sh
├── send-sms-alert.sh            # 发送-SMS-告警.sh
├── send-slack-alert.sh          # 发送-Slack-告警.sh
└── send-webhook-alert.sh        # 发送-Webhook-告警.sh
```

## 八、备份和恢复命名规范

### 8.1 备份脚本
```bash
# 备份脚本目录
/usr/local/backup/
├── backup-full-system.sh        # 备份-完整-系统.sh
├── backup-database.sh           # 备份-数据库.sh
├── backup-application.sh        # 备份-应用.sh
├── backup-config-files.sh       # 备份-配置文件.sh
└── backup-logs.sh               # 备份-日志.sh

# 恢复脚本
/usr/local/restore/
├── restore-full-system.sh       # 恢复-完整-系统.sh
├── restore-database.sh          # 恢复-数据库.sh
├── restore-application.sh       # 恢复-应用.sh
└── restore-config-files.sh      # 恢复-配置文件.sh
```

### 8.2 备份文件命名
```bash
# 备份文件命名规范
/backups/
├── system/
│   ├── full-system-20231201-143022.tar.gz    # 完整-系统-日期-时间.tar.gz
│   ├── system-config-20231201.tar.gz         # 系统-配置-日期.tar.gz
│   └── boot-partition-20231201.img           # 启动-分区-日期.img
│
├── databases/
│   ├── postgresql-full-20231201-143022.sql.gz    # 数据库-完整-日期-时间.sql.gz
│   ├── postgresql-incremental-20231201-143022.sql.gz
│   ├── mysql-backup-20231201-143022.sql.gz
│   └── redis-snapshot-20231201-143022.rdb
│
├── applications/
│   ├── web-app-code-20231201-143022.tar.gz   # 应用-代码-日期-时间.tar.gz
│   ├── web-app-data-20231201-143022.tar.gz
│   └── web-app-config-20231201.tar.gz
│
└── logs/
    ├── system-logs-20231201.tar.gz            # 系统-日志-日期.tar.gz
    ├── application-logs-20231201.tar.gz
    └── security-logs-20231201.tar.gz
```

## 九、安全配置命名规范

### 9.1 安全脚本
```bash
# 安全审计脚本
/usr/local/security/
├── security-audit.sh            # 安全-审计.sh
├── vulnerability-scan.sh        # 漏洞-扫描.sh
├── compliance-check.sh          # 合规-检查.sh
├── intrusion-detection.sh       # 入侵-检测.sh
└── log-analysis.sh              # 日志-分析.sh

# 安全加固脚本
/usr/local/hardening/
├── ssh-hardening.sh             # SSH-加固.sh
├── firewall-setup.sh            # 防火墙-设置.sh
├── user-management.sh           # 用户-管理.sh
├── file-permissions.sh          # 文件-权限.sh
└── kernel-hardening.sh          # 内核-加固.sh
```

### 9.2 安全配置文件
```bash
# 安全配置目录
/etc/security/
├── limits.conf                  # 资源限制配置
├── pam.d/                       # PAM配置目录
│   ├── sshd                     # SSH守护进程配置
│   ├── su                       # su命令配置
│   └── sudo                     # sudo配置
├── audit/                       # 审计配置
│   ├── audit.rules              # 审计规则
│   └── auditd.conf              # 审计守护进程配置
└── faillock.conf                # 失败锁定配置

# SELinux配置
/etc/selinux/
├── config                       # SELinux主配置
├── targeted/                    # 目标策略目录
│   └── contexts/
│       ├── files/               # 文件上下文
│       └── users/               # 用户上下文
└── mls/                         # MLS策略目录
```

## 十、最佳实践示例

### 10.1 系统健康检查脚本
```bash
#!/bin/bash
# system-health-check.sh - Comprehensive system health monitoring script

set -euo pipefail
IFS=$'\n\t'

# Configuration
SCRIPT_NAME=$(basename "$0")
LOG_FILE="/var/log/system-health/${SCRIPT_NAME%.sh}_$(date +%Y%m%d).log"
REPORT_FILE="/tmp/system-health-report_$(date +%Y%m%d_%H%M%S).txt"
EMAIL_RECIPIENT="admin@company.com"
THRESHOLDS_FILE="/etc/system-health/thresholds.conf"

# Load thresholds
if [[ -f "$THRESHOLDS_FILE" ]]; then
    source "$THRESHOLDS_FILE"
else
    # Default thresholds
    CPU_THRESHOLD=80
    MEMORY_THRESHOLD=85
    DISK_THRESHOLD=90
    LOAD_THRESHOLD=2.0
fi

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

log_info() { log_message "INFO" "$1"; }
log_warn() { log_message "WARN" "$1"; }
log_error() { log_message "ERROR" "$1"; }

# System information collection
collect_system_info() {
    cat >> "$REPORT_FILE" << EOF
==================== SYSTEM HEALTH REPORT ====================
Report Generated: $(date)
Hostname: $(hostname)
Kernel Version: $(uname -r)
Uptime: $(uptime)
Load Average: $(uptime | awk -F'load average:' '{print $2}')

EOF
}

# CPU monitoring
check_cpu_usage() {
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    local cpu_int=${cpu_usage%.*}
    
    cat >> "$REPORT_FILE" << EOF
-------------------- CPU Usage --------------------
Current CPU Usage: ${cpu_usage}%

EOF
    
    if [[ $cpu_int -gt $CPU_THRESHOLD ]]; then
        log_warn "High CPU usage detected: ${cpu_usage}%"
        echo "⚠️  HIGH CPU USAGE: ${cpu_usage}%" >> "$REPORT_FILE"
    else
        echo "✅ CPU usage normal: ${cpu_usage}%" >> "$REPORT_FILE"
    fi
}

# Memory monitoring
check_memory_usage() {
    local mem_info=$(free -m)
    local total_mem=$(echo "$mem_info" | awk 'NR==2{print $2}')
    local used_mem=$(echo "$mem_info" | awk 'NR==2{print $3}')
    local mem_percent=$((used_mem * 100 / total_mem))
    
    cat >> "$REPORT_FILE" << EOF
-------------------- Memory Usage --------------------
Total Memory: ${total_mem}MB
Used Memory: ${used_mem}MB
Memory Usage: ${mem_percent}%

EOF
    
    if [[ $mem_percent -gt $MEMORY_THRESHOLD ]]; then
        log_warn "High memory usage detected: ${mem_percent}%"
        echo "⚠️  HIGH MEMORY USAGE: ${mem_percent}%" >> "$REPORT_FILE"
    else
        echo "✅ Memory usage normal: ${mem_percent}%" >> "$REPORT_FILE"
    fi
}

# Disk space monitoring
check_disk_usage() {
    cat >> "$REPORT_FILE" << EOF
-------------------- Disk Usage --------------------

EOF
    
    df -h | grep -E '^/dev/' | while read -r line; do
        local filesystem=$(echo "$line" | awk '{print $1}')
        local usage_percent=$(echo "$line" | awk '{print $5}' | tr -d '%')
        local mount_point=$(echo "$line" | awk '{print $6}')
        
        echo "Filesystem: $filesystem ($mount_point) - Usage: ${usage_percent}%" >> "$REPORT_FILE"
        
        if [[ $usage_percent -gt $DISK_THRESHOLD ]]; then
            log_warn "Low disk space on $filesystem: ${usage_percent}%"
            echo "⚠️  LOW DISK SPACE: $filesystem (${usage_percent}%)" >> "$REPORT_FILE"
        else
            echo "✅ Disk space normal: $filesystem (${usage_percent}%)" >> "$REPORT_FILE"
        fi
    done
    echo "" >> "$REPORT_FILE"
}

# Service status checking
check_service_status() {
    local critical_services=("sshd" "nginx" "postgresql" "redis")
    
    cat >> "$REPORT_FILE" << EOF
-------------------- Service Status --------------------

EOF
    
    for service in "${critical_services[@]}"; do
        if systemctl is-active --quiet "$service"; then
            echo "✅ $service: RUNNING" >> "$REPORT_FILE"
        else
            log_error "Service $service is not running"
            echo "❌ $service: STOPPED" >> "$REPORT_FILE"
        fi
    done
    echo "" >> "$REPORT_FILE"
}

# Network connectivity check
check_network_connectivity() {
    local test_hosts=("8.8.8.8" "1.1.1.1" "google.com")
    
    cat >> "$REPORT_FILE" << EOF
-------------------- Network Connectivity --------------------

EOF
    
    for host in "${test_hosts[@]}"; do
        if ping -c 1 -W 3 "$host" >/dev/null 2>&1; then
            echo "✅ Network to $host: CONNECTED" >> "$REPORT_FILE"
        else
            log_warn "Network connectivity issue to $host"
            echo "❌ Network to $host: DISCONNECTED" >> "$REPORT_FILE"
        fi
    done
    echo "" >> "$REPORT_FILE"
}

# Security checks
check_security_status() {
    cat >> "$REPORT_FILE" << EOF
-------------------- Security Status --------------------

EOF
    
    # Failed login attempts
    local failed_logins=$(grep "Failed password" /var/log/auth.log | wc -l)
    echo "Failed login attempts (last 24h): $failed_logins" >> "$REPORT_FILE"
    
    # Firewall status
    if systemctl is-active --quiet firewalld; then
        echo "✅ Firewall: ACTIVE" >> "$REPORT_FILE"
    else
        log_warn "Firewall is not active"
        echo "⚠️  Firewall: INACTIVE" >> "$REPORT_FILE"
    fi
    
    # SELinux status
    if command -v getenforce >/dev/null; then
        local selinux_status=$(getenforce)
        echo "SELinux Status: $selinux_status" >> "$REPORT_FILE"
    fi
    echo "" >> "$REPORT_FILE"
}

# Main execution
main() {
    # Create log directory
    mkdir -p "$(dirname "$LOG_FILE")"
    
    log_info "Starting system health check"
    
    # Collect system information
    collect_system_info
    
    # Perform checks
    check_cpu_usage
    check_memory_usage
    check_disk_usage
    check_service_status
    check_network_connectivity
    check_security_status
    
    # Send report
    if [[ -n "$EMAIL_RECIPIENT" ]]; then
        mail -s "System Health Report - $(hostname)" "$EMAIL_RECIPIENT" < "$REPORT_FILE"
    fi
    
    # Display summary
    echo "System health check completed. Report saved to: $REPORT_FILE"
    echo "Log file: $LOG_FILE"
    
    log_info "System health check completed"
}

# Cleanup function
cleanup() {
    # Remove old reports (older than 7 days)
    find /tmp -name "system-health-report_*" -mtime +7 -delete 2>/dev/null || true
    
    # Remove old logs (older than 30 days)
    find "$(dirname "$LOG_FILE")" -name "*.log" -mtime +30 -delete 2>/dev/null || true
}

# Trap cleanup
trap cleanup EXIT

# Execute main function
main "$@"
```

### 10.2 服务监控和自动恢复脚本
```bash
#!/bin/bash
# service-monitor.sh - Service monitoring and auto-recovery script

set -euo pipefail

SERVICE_NAME="$1"
MAX_RESTARTS=3
RESTART_COUNT_FILE="/tmp/${SERVICE_NAME}_restart_count"
LOCK_FILE="/tmp/${SERVICE_NAME}_monitor.lock"

# Logging function
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "/var/log/service-monitor.log"
}

# Check if another instance is running
if [[ -f "$LOCK_FILE" ]]; then
    log_message "Monitor for $SERVICE_NAME already running"
    exit 1
fi

# Create lock file
echo $$ > "$LOCK_FILE"

# Cleanup function
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

# Get restart count
get_restart_count() {
    if [[ -f "$RESTART_COUNT_FILE" ]]; then
        cat "$RESTART_COUNT_FILE"
    else
        echo "0"
    fi
}

# Increment restart count
increment_restart_count() {
    local count=$(get_restart_count)
    local new_count=$((count + 1))
    echo "$new_count" > "$RESTART_COUNT_FILE"
    echo "$new_count"
}

# Reset restart count
reset_restart_count() {
    echo "0" > "$RESTART_COUNT_FILE"
}

# Check service status
check_service() {
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        reset_restart_count
        return 0
    else
        return 1
    fi
}

# Restart service
restart_service() {
    local restart_count=$(increment_restart_count)
    
    log_message "Attempting to restart $SERVICE_NAME (attempt $restart_count)"
    
    if systemctl restart "$SERVICE_NAME"; then
        log_message "$SERVICE_NAME restarted successfully"
        return 0
    else
        log_message "Failed to restart $SERVICE_NAME"
        return 1
    fi
}

# Main monitoring loop
main() {
    log_message "Starting monitoring for service: $SERVICE_NAME"
    
    while true; do
        if ! check_service; then
            local restart_count=$(get_restart_count)
            
            if [[ $restart_count -lt $MAX_RESTARTS ]]; then
                restart_service
            else
                log_message "Maximum restart attempts reached for $SERVICE_NAME"
                log_message "Sending critical alert for $SERVICE_NAME"
                
                # Send alert (implement your alerting mechanism here)
                echo "CRITICAL: Service $SERVICE_NAME has failed and reached maximum restart attempts" | \
                    mail -s "Service Down Alert" admin@company.com
                
                # Reset count and wait longer before next check
                reset_restart_count
                sleep 300  # Wait 5 minutes
            fi
        fi
        
        sleep 60  # Check every minute
    done
}

# Validate input
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

if ! systemctl list-unit-files | grep -q "^$SERVICE_NAME.service"; then
    log_message "Service $SERVICE_NAME not found"
    exit 1
fi

# Start monitoring
main
```

---

**注意事项：**
1. 所有脚本都应该包含适当的错误处理和日志记录
2. 配置文件应该使用清晰的命名约定和注释
3. 生产环境中必须实施适当的安全措施和访问控制
4. 定期审查和更新命名规范以适应新的需求
5. 文档化所有的自定义脚本和配置变更