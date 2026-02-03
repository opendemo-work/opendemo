# Linux生产环境运维命令详解演示

## 🎯 学习目标

通过本案例你将掌握Linux生产环境中的核心运维命令和最佳实践：

- 系统服务管理和服务监控
- 日志分析和故障排查
- 性能调优和资源优化
- 安全加固和访问控制
- 自动化运维和批量操作
- 灾难恢复和备份策略

## 🛠️ 环境准备

### 系统要求
- Linux发行版（CentOS 7+/Ubuntu 18.04+/RHEL 7+）
- root或sudo权限
- 生产环境运维经验基础
- 系统安全和合规性知识

### 依赖安装
```bash
# CentOS/RHEL系统
sudo yum install -y systemd systemd-tools logrotate rsyslog audit
sudo yum install -y firewalld selinux-policy selinux-policy-targeted

# Ubuntu/Debian系统
sudo apt-get update
sudo apt-get install -y systemd systemd-sysv logrotate rsyslog auditd
sudo apt-get install -y ufw apparmor

# 验证关键组件
systemctl --version
journalctl --version
auditctl -v
```

## 📁 项目结构

```
linux-production-ops-commands-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 生产环境脚本
│   ├── service_manager.sh             # 服务管理脚本
│   ├── log_analyzer.sh                # 日志分析脚本
│   ├── security_checker.sh            # 安全检查脚本
│   ├── backup_manager.sh              # 备份管理脚本
│   └── performance_tuner.sh           # 性能调优脚本
├── configs/                           # 配置文件模板
│   ├── systemd_service_template.conf  # systemd服务模板
│   ├── logrotate_config.conf          # 日志轮转配置
│   ├── audit_rules.conf               # 审计规则配置
│   └── firewall_rules.conf            # 防火墙规则模板
├── examples/                          # 实际应用示例
│   ├── service_management.txt         # 服务管理示例
│   ├── log_analysis_output.txt        # 日志分析示例
│   ├── security_audit_report.txt      # 安全审计示例
│   └── performance_tuning.txt         # 性能调优示例
└── docs/                              # 详细文档
    ├── production_best_practices.md   # 生产环境最佳实践
    ├── disaster_recovery_guide.md     # 灾难恢复指南
    ├── compliance_checklist.md        # 合规性检查清单
    └── automation_playbooks.md        # 自动化操作手册
```

## 🚀 核心运维命令详解

### 1. 系统服务管理

```bash
# systemd服务管理
systemctl status nginx                    # 查看服务状态
systemctl start|stop|restart nginx        # 服务启停操作
systemctl enable|disable nginx            # 设置开机自启
systemctl list-units --type=service       # 列出所有服务
systemctl daemon-reload                   # 重新加载服务配置

# 服务依赖关系查看
systemctl list-dependencies nginx

# 服务日志查看
journalctl -u nginx -f                    # 实时查看服务日志
journalctl -u nginx --since "1 hour ago"  # 查看最近1小时日志
journalctl -p err -f                      # 实时查看错误日志

# 服务资源配置
systemctl set-property nginx.service CPUQuota=50% MemoryMax=1G
```

### 2. 日志管理与分析

```bash
# 系统日志管理
tail -f /var/log/messages                 # 实时查看系统日志
grep "error" /var/log/syslog              # 搜索错误信息
awk '/CRITICAL/ {print $0}' /var/log/application.log

# 日志轮转配置
logrotate -d /etc/logrotate.conf         # 调试日志轮转配置
logrotate -f /etc/logrotate.d/nginx      # 强制执行日志轮转

# 结构化日志分析
journalctl --since today --priority=err --output=json
journalctl --field=SYSLOG_IDENTIFIER     # 查看所有日志标识符

# 应用日志监控
multitail /var/log/nginx/access.log /var/log/nginx/error.log
```

### 3. 性能监控与调优

```bash
# 系统性能基线
uptime                                   # 系统负载情况
vmstat 1 5                               # 虚拟内存统计
iostat -x 1 5                            # IO性能统计
mpstat -P ALL 1 5                        # CPU使用情况

# 进程性能分析
pidstat -u -p $(pgrep nginx) 1 5         # 监控特定进程
perf top                                 # 实时性能分析
perf record -g -p $(pgrep mysql)         # 性能数据采集

# 内存优化
echo 1 > /proc/sys/vm/drop_caches        # 清理页面缓存
echo 3 > /proc/sys/vm/drop_caches        # 清理所有缓存
slabtop                                  # 内存slab信息

# 网络性能调优
ss -tulnp                                # 网络连接统计
tcptraceroute google.com                 # TCP路径跟踪
nethogs                                  # 按进程分组的网络流量
```

### 4. 安全加固与审计

```bash
# 系统安全检查
auditctl -l                              # 查看审计规则
ausearch -sc execve --start recent       # 搜索执行事件
aureport -au                             # 用户活动报告

# 访问控制管理
faillock --user username --reset         # 重置用户锁定
last                                     # 查看登录历史
lastb                                    # 查看失败登录尝试

# 文件系统安全
find / -perm -4000 -type f 2>/dev/null   # 查找SUID文件
find / -perm -2000 -type f 2>/dev/null   # 查找SGID文件
rpm -Va                                  # 验证已安装包完整性

# 防火墙配置
firewall-cmd --list-all                  # 查看防火墙规则
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --reload
```

### 5. 自动化运维

```bash
# 批量操作工具
ansible all -m ping                      # Ansible连通性测试
salt '*' test.ping                       # SaltStack连通性测试
pssh -h hosts.txt -i "uptime"            # 并行SSH执行

# 配置管理
etckeeper commit "Configuration backup"  # 配置文件版本管理
rsync -avz /etc/ backup_server:/etc_backup/  # 配置同步

# 系统更新管理
yum update --assumeno                    # 预览更新内容
apt-get upgrade -s                       # 模拟升级过程
needrestart                              # 检查需要重启的服务
```

### 6. 备份与恢复

```bash
# 系统备份策略
tar -czf /backup/system_$(date +%Y%m%d).tar.gz \
    --exclude=/proc --exclude=/sys --exclude=/dev \
    --exclude=/backup /

# 数据库备份
mysqldump -u root -p --all-databases > /backup/mysql_full.sql
pg_dumpall -U postgres > /backup/postgresql_full.sql

# 增量备份
rsnapshot daily                         # 执行每日增量备份
restic backup /home --tag user-data     # 使用restic备份

# 灾难恢复测试
systemctl rescue                        # 进入救援模式
chroot /mnt                             # 挂载根文件系统进行修复
```

## 🔍 生产环境最佳实践

### 服务管理规范
```bash
# 服务启动前检查清单
#!/bin/bash
# 服务健康检查脚本
SERVICE_NAME="nginx"
CHECK_URL="http://localhost:80"

# 检查服务状态
if ! systemctl is-active --quiet $SERVICE_NAME; then
    echo "服务 $SERVICE_NAME 未运行"
    exit 1
fi

# 检查端口监听
if ! ss -tulnp | grep -q ":80 "; then
    echo "服务端口未监听"
    exit 1
fi

# 检查HTTP响应
if ! curl -sf $CHECK_URL >/dev/null; then
    echo "HTTP服务无响应"
    exit 1
fi

echo "服务 $SERVICE_NAME 健康检查通过"
```

### 日志管理策略
```bash
# 集中式日志收集配置
cat > /etc/rsyslog.d/remote.conf << EOF
*.* @@logserver.example.com:514
EOF

# 应用日志轮转配置
cat > /etc/logrotate.d/application << EOF
/var/log/application/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 appuser appgroup
    postrotate
        systemctl reload application
    endscript
}
EOF
```

### 安全加固措施
```bash
# SSH安全配置
cat >> /etc/ssh/sshd_config << EOF
PermitRootLogin no
PasswordAuthentication no
AllowUsers admin ops
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

# 系统安全基线
# 禁用不必要的服务
systemctl disable cups postfix bluetooth

# 内核参数优化
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_syncookies = 1
net.ipv4.ip_forward = 0
kernel.randomize_va_space = 2
EOF
```

## 🧪 验证测试

### 服务可靠性测试
```bash
#!/bin/bash
# 服务可靠性验证脚本

TEST_DURATION=300  # 测试持续时间(秒)
SERVICE_NAME="nginx"
START_TIME=$(date +%s)

echo "开始服务可靠性测试..."

while [ $(($(date +%s) - START_TIME)) -lt $TEST_DURATION ]; do
    # 检查服务状态
    if ! systemctl is-active --quiet $SERVICE_NAME; then
        echo "$(date): 服务异常停止"
        systemctl start $SERVICE_NAME
        sleep 5
    fi
    
    # 检查响应时间
    RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}\n" http://localhost:80 2>/dev/null)
    if (( $(echo "$RESPONSE_TIME > 5" | bc -l) )); then
        echo "$(date): 响应时间过长: ${RESPONSE_TIME}s"
    fi
    
    sleep 10
done

echo "服务可靠性测试完成"
```

### 安全合规检查
```bash
#!/bin/bash
# 安全合规性检查脚本

echo "=== 系统安全合规检查报告 ==="
echo "检查时间: $(date)"
echo ""

# 检查密码策略
echo "1. 密码策略检查:"
awk -F: '$2!="*" && $2!="!" {print $1}' /etc/shadow | wc -l
echo "未设置密码的账户数: $?"

# 检查SSH配置
echo "2. SSH安全配置:"
grep "^PermitRootLogin" /etc/ssh/sshd_config
grep "^PasswordAuthentication" /etc/ssh/sshd_config

# 检查防火墙状态
echo "3. 防火墙状态:"
systemctl is-active firewalld

# 检查审计日志
echo "4. 审计系统状态:"
systemctl is-active auditd
```

## ❓ 常见问题处理

### Q1: 服务启动失败如何排查？
**解决方案**：
```bash
# 详细故障排查步骤
systemctl status service_name --no-pager
journalctl -u service_name --no-pager
systemctl cat service_name
# 检查依赖服务
systemctl list-dependencies service_name
# 检查配置文件语法
servicename --configtest
```

### Q2: 系统性能突然下降怎么办？
**应急处理**：
```bash
# 快速性能诊断
top -b -n 1 | head -20
iostat -x 1 3
free -h
df -h
# 查找高资源消耗进程
ps aux --sort=-%cpu | head -10
# 检查系统负载
uptime
```

### Q3: 安全事件应急响应流程？
**标准流程**：
1. 立即隔离受影响系统
2. 收集证据和日志
3. 分析攻击路径和影响范围
4. 修复漏洞和清除恶意软件
5. 恢复系统和服务
6. 总结经验和改进防护

## 📚 扩展学习

### 企业级工具链
- **监控系统**: Prometheus + Grafana + Alertmanager
- **日志管理**: ELK Stack (Elasticsearch + Logstash + Kibana)
- **配置管理**: Ansible + Terraform + Consul
- **容器编排**: Kubernetes + Helm + Istio
- **CI/CD**: Jenkins + GitLab CI + ArgoCD

### 学习进阶路径
1. 掌握云原生运维理念
2. 学习微服务架构运维
3. 理解DevSecOps实践
4. 掌握混沌工程方法论
5. 学习SRE站点可靠性工程

### 认证考试推荐
- RHCE (Red Hat Certified Engineer)
- LPIC (Linux Professional Institute Certification)
- AWS Certified SysOps Administrator
- Google Professional Cloud DevOps Engineer

---
> **💡 提示**: 生产环境运维需要严格遵循变更管理流程，任何操作都应该经过充分测试和审批，确保系统的稳定性和安全性。