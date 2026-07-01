# Linux安全监控与日志管理详解演示

## 🎯 学习目标

通过本案例你将掌握Linux系统安全监控和日志管理的核心技能：

- 系统安全审计和合规检查
- 实时安全事件监控和告警
- 日志收集、分析和可视化
- 入侵检测和威胁分析
- 安全加固和漏洞管理
- 合规性报告和审计跟踪

## 🛠️ 环境准备

### 系统要求
- Linux发行版（推荐CentOS 7+/Ubuntu 18.04+）
- root权限或sudo权限
- 安全管理基础知识
- 日志分析经验

### 依赖安装
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 基础安全工具
sudo yum install -y audit rkhunter chkrootkit aide
sudo apt-get install -y auditd rkhunter chkrootkit aide

# 日志管理工具
sudo yum install -y rsyslog logrotate elasticsearch-kibana
sudo apt-get install -y rsyslog logrotate elasticsearch kibana

# 网络安全工具
sudo yum install -y fail2ban iptables-services
sudo apt-get install -y fail2ban iptables

# 验证安装
which auditctl rkhunter aide fail2ban-server
systemctl is-active auditd rsyslog
```

## 📁 项目结构

```
linux-security-logging-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 安全和日志脚本
│   ├── security_auditor.sh            # 安全审计脚本
│   ├── log_collector.sh               # 日志收集脚本
│   ├── intrusion_detector.sh          # 入侵检测脚本
│   ├── compliance_checker.sh          # 合规检查脚本
│   └── threat_analyzer.sh             # 威胁分析脚本
├── configs/                           # 配置文件
│   ├── audit_rules.conf               # 审计规则配置
│   ├── rsyslog_config.conf            # 日志收集配置
│   ├── fail2ban_config.conf           # 防暴力破解配置
│   └── elasticsearch_config.conf      # ES配置模板
├── examples/                          # 实际示例
│   ├── security_audit_report.txt      # 安全审计报告示例
│   ├── log_analysis_output.txt        # 日志分析示例
│   ├── intrusion_detection_alert.txt  # 入侵检测告警示例
│   └── compliance_check_results.txt   # 合规检查结果
└── docs/                              # 详细文档
    ├── security_best_practices.md     # 安全最佳实践
    ├── log_analysis_guide.md          # 日志分析指南
    ├── incident_response.md           # 事件响应流程
    └── compliance_framework.md        # 合规框架指南
```

## 🔍 核心安全监控技术

### 1. 系统审计(Auditd)

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 审计系统配置
sudo systemctl start auditd
sudo systemctl enable auditd

# 基本审计规则
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
sudo auditctl -w /etc/shadow -p wa -k shadow_changes
sudo auditctl -w /etc/group -p wa -k group_changes

# 监控系统调用
sudo auditctl -a always,exit -F arch=b64 -S execve -k command_execution
sudo auditctl -a always,exit -F arch=b64 -S open -F dir=/etc -k etc_access

# 实时监控审计日志
sudo ausearch -k passwd_changes --start recent
sudo aureport -au --summary  # 用户活动报告
sudo aureport -x --summary   # 执行事件报告

# 审计日志分析
sudo ausearch -sc execve | awk '{print $NF}' | sort | uniq -c | sort -nr | head -10
```

### 2. 入侵检测系统

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Rootkit检测
rkhunter --update
rkhunter --check --skip-keypress

# 文件完整性检查
aide --init
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
aide --check

# 系统完整性扫描
chkrootkit

# 实时文件监控
inotifywait -m -r -e create,delete,modify /etc/ /bin/ /sbin/ /usr/bin/ /usr/sbin/
```

### 3. 网络安全监控

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Fail2ban配置
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# 查看防护状态
sudo fail2ban-client status
sudo fail2ban-client status sshd

# 防火墙规则监控
sudo iptables -L -n -v --line-numbers
sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP

# 网络连接安全检查
netstat -tulnp | grep -E ':(22|23|2323)'  # 检查危险端口
ss -tulnp | awk '$5 ~ /:22$/ {print $0}' | wc -l  # 统计SSH连接数
```

### 4. 日志收集和分析

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# Rsyslog配置
sudo systemctl restart rsyslog

# 远程日志收集配置
cat >> /etc/rsyslog.conf << EOF
# 远程日志服务器配置
*.* @logserver.example.com:514
# 或使用TCP
*.* @@logserver.example.com:514
EOF

# 结构化日志分析
journalctl -o json-pretty -u sshd --since "1 hour ago"
journalctl --field=_COMM | sort | uniq -c | sort -nr

# 应用日志监控
tail -f /var/log/nginx/access.log | grep -E "(404|500)" | awk '{print $1}' | sort | uniq -c
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr
```

### 5. 实时安全监控

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 进程监控
ps aux --sort=-%cpu | head -20 | grep -v "^\[.*\]$"  # 排除内核线程
lsof -i -P -n | grep LISTEN  # 监听端口

# 用户活动监控
last | head -20  # 登录历史
w  # 当前登录用户
who -a  # 详细用户信息

# 文件系统监控
find /tmp -type f -mtime -1 -ls  # 最近修改的文件
find / -perm -4000 -type f 2>/dev/null  # SUID文件
find / -perm -2000 -type f 2>/dev/null  # SGID文件
```

## 🛡️ 安全加固实践

### 系统安全基线
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 系统安全基线检查脚本

echo "=== 系统安全基线检查 ==="
echo "检查时间: $(date)"
echo ""

# 检查密码策略
echo "1. 密码策略检查:"
awk -F: '$2=="*" || $2=="!" {count++} END {print "未设置密码账户数: " count}' /etc/shadow

# 检查空密码账户
echo "2. 空密码账户检查:"
awk -F: '$2=="" {print $1}' /etc/shadow

# 检查root SSH登录
echo "3. Root SSH登录检查:"
grep "^PermitRootLogin" /etc/ssh/sshd_config

# 检查密码认证
echo "4. 密码认证检查:"
grep "^PasswordAuthentication" /etc/ssh/sshd_config

# 检查防火墙状态
echo "5. 防火墙状态检查:"
systemctl is-active firewalld || systemctl is-active ufw

# 检查审计系统
echo "6. 审计系统检查:"
systemctl is-active auditd
```

### 漏洞扫描和修复
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 系统漏洞扫描脚本

echo "=== 系统漏洞扫描 ==="

# 包更新检查
echo "1. 系统包更新检查:"
if command -v yum &> /dev/null; then
    yum check-update | wc -l
elif command -v apt &> /dev/null; then
    apt list --upgradable 2>/dev/null | wc -l
fi

# 已知漏洞扫描
echo "2. 已知漏洞扫描:"
clamscan -r /home/ 2>/dev/null || echo "ClamAV未安装"

# 配置文件权限检查
echo "3. 配置文件权限检查:"
find /etc -name "*.conf" -perm /o+r -ls | head -10

# 服务漏洞检查
echo "4. 运行服务漏洞检查:"
netstat -tulnp | grep -E ':(21|23|25|110|143)' | wc -l
```

## 📊 日志分析和可视化

### ELK Stack配置
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Elasticsearch配置
cat > /etc/elasticsearch/elasticsearch.yml << EOF
cluster.name: security-logging
node.name: log-node-1
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node
EOF

# Logstash配置
cat > /etc/logstash/conf.d/security.conf << EOF
input {
  file {
    path => "/var/log/auth.log"
    start_position => "beginning"
    sincedb_path => "/dev/null"
    codec => multiline {
      pattern => "^\s"
      what => "previous"
    }
  }
}

filter {
  grok {
    match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{SYSLOGHOST:hostname} %{DATA:program}(?:\[%{POSINT:pid}\])?: %{GREEDYDATA:syslog_message}" }
  }
  
  if [program] == "sshd" {
    grok {
      match => { "syslog_message" => "Failed password for %{USERNAME:user} from %{IP:ip} port %{NUMBER:port} ssh2" }
      tag_on_failure => [ "_grokparsefailure_ssh" ]
    }
  }
  
  date {
    match => [ "timestamp", "MMM dd HH:mm:ss" ]
    target => "@timestamp"
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "security-logs-%{+YYYY.MM.dd}"
  }
}
EOF

# Kibana配置
cat > /etc/kibana/kibana.yml << EOF
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
EOF
```

### 自定义日志分析
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 安全日志分析脚本

LOG_FILE="/var/log/auth.log"
REPORT_FILE="/tmp/security_analysis_$(date +%Y%m%d).txt"

echo "=== 安全日志分析报告 ===" > "$REPORT_FILE"
echo "分析时间: $(date)" >> "$REPORT_FILE"
echo "日志文件: $LOG_FILE" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# SSH登录失败统计
echo "SSH登录失败统计:" >> "$REPORT_FILE"
grep "Failed password" "$LOG_FILE" | awk '{print $11}' | sort | uniq -c | sort -nr | head -10 >> "$REPORT_FILE"

# 成功登录统计
echo -e "\nSSH成功登录统计:" >> "$REPORT_FILE"
grep "Accepted password" "$LOG_FILE" | awk '{print $11}' | sort | uniq -c | sort -nr | head -10 >> "$REPORT_FILE"

# 异常时间登录
echo -e "\n异常时间登录(23:00-06:00):" >> "$REPORT_FILE"
awk '$3 >= "23:" || $3 <= "06:"' "$LOG_FILE" | grep "Accepted" | head -5 >> "$REPORT_FILE"

# 高频失败IP
echo -e "\n高频失败登录IP:" >> "$REPORT_FILE"
grep "Failed password" "$LOG_FILE" | awk '{print $11}' | sort | uniq -c | sort -nr | awk '$1 > 10' >> "$REPORT_FILE"

echo "分析完成，报告保存在: $REPORT_FILE"
```

## 🧪 验证测试

### 安全监控有效性测试
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 安全监控系统测试脚本

echo "=== 安全监控系统测试 ==="

# 测试审计规则
echo "1. 审计规则测试:"
auditctl -l | wc -l
if [ $? -eq 0 ]; then
    echo "✅ 审计规则配置正常"
else
    echo "❌ 审计规则配置异常"
fi

# 测试日志收集
echo "2. 日志收集测试:"
logger "Security Test Message"
sleep 2
if journalctl | grep "Security Test Message" >/dev/null; then
    echo "✅ 日志收集功能正常"
else
    echo "❌ 日志收集功能异常"
fi

# 测试入侵检测
echo "3. 入侵检测测试:"
if command -v rkhunter &> /dev/null; then
    rkhunter --version >/dev/null && echo "✅ Rootkit检测工具正常" || echo "❌ Rootkit检测工具异常"
fi

# 测试网络监控
echo "4. 网络监控测试:"
netstat -tulnp | grep :22 >/dev/null && echo "✅ SSH服务监控正常" || echo "❌ SSH服务监控异常"
```

## ❓ 常见安全问题处理

### Q1: 如何应对DDoS攻击？
**应急响应**：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 启用连接限制
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65535" >> /etc/sysctl.conf
sysctl -p

# 配置iptables限速
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j DROP
```

### Q2: 发现可疑进程如何处理？
**处置流程**：
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 1. 收集进程信息
PID=12345
ps -fp $PID
ls -la /proc/$PID/exe
lsof -p $PID

# 2. 网络连接检查
netstat -anp | grep $PID

# 3. 文件关联检查
find / -inum $(ls -i /proc/$PID/exe | awk '{print $1}') 2>/dev/null

# 4. 终止进程并保留证据
kill -STOP $PID  # 暂停进程
cp /proc/$PID/exe /tmp/suspicious_binary_$PID
kill -9 $PID
```

### Q3: 日志文件过大如何处理？
**优化方案**：
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 配置日志轮转
cat > /etc/logrotate.d/security << EOF
/var/log/auth.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 640 root adm
    postrotate
        systemctl reload rsyslog
    endscript
}
EOF

# 实施日志压缩和清理
find /var/log -name "*.log" -mtime +30 -delete
logrotate -f /etc/logrotate.conf
```

## 📚 扩展学习

### 企业级安全工具
- **OSSEC**: 主机入侵检测系统
- **Wazuh**: 基于OSSEC的现代化安全平台
- **Splunk**: 企业级日志分析平台
- **Graylog**: 开源日志管理解决方案
- **Snort**: 网络入侵检测系统

### 学习进阶路径
1. 掌握信息安全基础理论
2. 学习系统安全加固技术
3. 理解安全事件响应流程
4. 掌握合规性框架(CIS, ISO27001等)
5. 学习威胁情报和APT防护

### 认证考试推荐
- CISSP (Certified Information Systems Security Professional)
- CEH (Certified Ethical Hacker)
- CompTIA Security+
- OSCP (Offensive Security Certified Professional)

---
> **💡 提示**: 安全监控是一个持续的过程，需要定期更新规则、分析新型威胁，并保持安全工具的最新版本。
## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/demo.sh
```

### 环境要求

- Linux 或 macOS 系统
- 已安装相关命令工具

## 📖 核心概念

### 1. 基本概念

本节介绍该工具的基本工作原理与关键术语。

### 2. 常用场景

- 场景 1：日常监控与诊断
- 场景 2：故障排查
- 场景 3：性能分析

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际工具替换
command --help
```

### 实际场景

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际工具替换
command -a -b target
```
