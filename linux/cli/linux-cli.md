# 🐧 Linux 命令行速查表 (linux-cli.md)

> 生产环境必备的 Linux 命令行参考手册，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [系统信息查看](#系统信息查看)
- [进程管理](#进程管理)
- [网络诊断](#网络诊断)
- [文件系统操作](#文件系统操作)
- [系统监控](#系统监控)
- [性能分析](#性能分析)
- [安全审计](#安全审计)
- [日志分析](#日志分析)
- [磁盘管理](#磁盘管理)
- [用户权限管理](#用户权限管理)
- [服务管理](#服务管理)
- [备份恢复](#备份恢复)
- [故障排查](#故障排查)
- [自动化脚本](#自动化脚本)
- [最佳实践](#最佳实践)

---

## 系统信息查看

### 基础系统信息
```bash
# 查看系统版本信息
cat /etc/os-release
uname -a
lsb_release -a

# 查看内核版本
uname -r
cat /proc/version

# 查看主机名
hostname
hostnamectl

# 查看系统架构
uname -m
arch

# 查看启动时间
uptime
who -b
```

### 硬件信息
```bash
# 查看CPU信息
lscpu
cat /proc/cpuinfo

# 查看内存信息
free -h
cat /proc/meminfo

# 查看磁盘信息
lsblk
fdisk -l
df -h

# 查看网卡信息
ip addr show
ifconfig
lspci | grep -i ethernet
```

### 系统负载
```bash
# 查看系统负载
w
top
htop

# 查看平均负载
cat /proc/loadavg

# 查看登录用户
who
users
last
```

---

## 进程管理

### 进程查看
```bash
# 查看所有进程
ps aux
ps -ef

# 查看树状进程结构
pstree
pstree -p

# 实时监控进程
top
htop

# 按用户查看进程
ps -u username
```

### 进程控制
```bash
# 杀死进程
kill PID
kill -9 PID

# 按名称杀死进程
killall process_name
pkill process_name

# 后台运行程序
nohup command &
disown

# 查看进程树
ps -ejH
```

### 进程调试
```bash
# 查看进程打开的文件
lsof -p PID
lsof -c process_name

# 查看进程网络连接
lsof -i -p PID

# 查看进程内存映射
pmap PID
cat /proc/PID/maps

# 跟踪系统调用
strace command
strace -p PID
```

---

## 网络诊断

### 网络连接查看
```bash
# 查看网络连接
netstat -tuln
ss -tuln

# 查看TCP连接状态
netstat -an | grep ESTABLISHED
ss -s

# 查看监听端口
netstat -tlnp
ss -tlnp

# 查看UDP连接
netstat -ulnp
ss -ulnp
```

### 网络连通性测试
```bash
# 测试网络连通性
ping hostname
ping -c 4 hostname

# 端口连通性测试
nc -zv hostname port
telnet hostname port

# DNS解析测试
nslookup domain
dig domain
host domain

# 路径追踪
traceroute hostname
mtr hostname
```

### 网络接口管理
```bash
# 查看网络接口
ip addr show
ifconfig

# 配置网络接口
ip addr add ip/netmask dev interface
ifconfig interface ip netmask netmask

# 启用/禁用接口
ip link set interface up/down
ifconfig interface up/down

# 查看路由表
ip route show
route -n
```

---

## 文件系统操作

### 文件查找
```bash
# 按名称查找文件
find /path -name "filename"

# 按类型查找
find /path -type f  # 文件
find /path -type d  # 目录

# 按大小查找
find /path -size +100M

# 按时间查找
find /path -mtime -7  # 7天内修改的文件
```

### 文件权限管理
```bash
# 查看文件权限
ls -l filename
stat filename

# 修改文件权限
chmod 755 filename
chmod u+x filename

# 修改文件所有者
chown user:group filename
chgrp group filename

# 递归修改权限
chmod -R 755 directory/
```

### 文件操作
```bash
# 查看文件内容
cat filename
less filename
more filename

# 实时查看文件变化
tail -f filename
tail -n 100 filename

# 搜索文件内容
grep "pattern" filename
grep -r "pattern" /path/

# 文件同步
rsync -av source/ destination/
rsync -avz source/ user@host:/destination/
```

---

## 系统监控

### CPU监控
```bash
# 实时CPU使用率
top
htop

# 查看CPU详细信息
vmstat 1
sar -u 1

# 查看每个核心使用率
mpstat -P ALL 1

# 查看进程CPU使用
ps aux --sort=-%cpu | head -10
```

### 内存监控
```bash
# 实时内存使用
free -h
watch -n 1 free -h

# 查看内存详细使用
vmstat 1
sar -r 1

# 查看进程内存使用
ps aux --sort=-%mem | head -10

# 查看内存占用大户
smem -s rss
```

### 磁盘IO监控
```bash
# 实时IO监控
iostat -x 1
iotop

# 查看磁盘使用率
df -h
du -sh /path/*

# 查看目录大小
du -h --max-depth=1 /path
ncdu /path
```

---

## 性能分析

### 系统性能概览
```bash
# 系统性能快照
dstat
glances

# 全面性能监控
sar -A

# 系统活动报告
sar -u -r -b 1 10

# 实时系统监控
nmon
```

### 应用性能分析
```bash
# 进程性能分析
pidstat -u -r -p PID 1

# 网络性能分析
iftop
nethogs

# 磁盘性能分析
iostat -x 1
iotop

# 内存性能分析
vmstat 1
```

### 压力测试
```bash
# CPU压力测试
stress --cpu 4 --timeout 60s

# 内存压力测试
stress --vm 2 --vm-bytes 1G --timeout 60s

# IO压力测试
stress --io 4 --timeout 60s

# 综合压力测试
stress-ng --cpu 4 --io 4 --vm 2 --vm-bytes 1G --timeout 60s
```

---

## 安全审计

### 用户和权限审计
```bash
# 查看当前登录用户
who
w
users

# 查看登录历史
last
lastlog

# 查看sudo权限
sudo -l
cat /etc/sudoers

# 查看用户组
groups username
cat /etc/group
```

### 系统安全检查
```bash
# 查看开放端口
netstat -tuln
ss -tuln

# 查看防火墙规则
iptables -L -n -v
firewall-cmd --list-all

# 查看SELinux状态
sestatus
getenforce

# 检查系统漏洞
yum update --security  # RHEL/CentOS
apt list --upgradable  # Ubuntu/Debian
```

### 日志安全审计
```bash
# 查看系统日志
journalctl -f
tail -f /var/log/syslog

# 查看认证日志
tail -f /var/log/auth.log
journalctl -u ssh

# 查看安全事件
ausearch -m avc
sealert -a /var/log/audit/audit.log
```

---

## 日志分析

### 系统日志查看
```bash
# 实时查看系统日志
journalctl -f
tail -f /var/log/messages

# 查看特定时间段日志
journalctl --since "2024-01-01" --until "2024-01-02"
tail -f /var/log/syslog | grep "Jan 1"

# 查看特定服务日志
journalctl -u service_name
tail -f /var/log/service_name.log
```

### 日志搜索和过滤
```bash
# 搜索错误日志
grep -i "error" /var/log/messages
journalctl -p err

# 按关键字过滤
grep "keyword" /var/log/*.log
awk '/keyword/ {print}' /var/log/file.log

# 统计日志条目
wc -l /var/log/messages
grep "error" /var/log/*.log | wc -l
```

### 日志分析工具
```bash
# 日志轮转配置
logrotate -d /etc/logrotate.conf

# 查看日志轮转状态
logrotate -s /var/lib/logrotate/status

# 集中式日志分析
# (需要安装ELK/EFK stack)
```

---

## 磁盘管理

### 磁盘空间管理
```bash
# 查看磁盘使用情况
df -h
du -sh /*

# 查找大文件
find / -type f -size +100M -exec ls -lh {} \;

# 清理临时文件
rm -rf /tmp/*
find /tmp -type f -atime +7 -delete

# 清理日志文件
logrotate -f /etc/logrotate.conf
```

### 文件系统操作
```bash
# 查看文件系统类型
df -T
lsblk -f

# 挂载文件系统
mount /dev/sdb1 /mnt/data
umount /mnt/data

# 查看挂载点
mount | grep filesystem
findmnt

# 磁盘配额管理
quota -u username
repquota -a
```

### 存储扩容
```bash
# 扩展LVM逻辑卷
lvextend -L +10G /dev/vg0/lv0
resize2fs /dev/vg0/lv0

# 创建新分区
fdisk /dev/sdb
partprobe

# 格式化文件系统
mkfs.ext4 /dev/sdb1
mkfs.xfs /dev/sdb1
```

---

## 用户权限管理

### 用户管理
```bash
# 添加用户
useradd username
adduser username

# 删除用户
userdel username
userdel -r username

# 修改用户信息
usermod -l newname oldname
passwd username

# 锁定/解锁用户
usermod -L username
usermod -U username
```

### 组管理
```bash
# 添加组
groupadd groupname

# 删除组
groupdel groupname

# 将用户添加到组
usermod -a -G groupname username
gpasswd -a username groupname

# 从组中删除用户
gpasswd -d username groupname
```

### 权限管理
```bash
# 查看用户权限
id username
groups username

# 设置特殊权限
chmod u+s filename  # SUID
chmod g+s filename  # SGID
chmod +t directory  # Sticky bit

# ACL权限管理
setfacl -m u:username:rwx file
getfacl file
```

---

## 服务管理

### Systemd服务管理
```bash
# 查看服务状态
systemctl status service_name
systemctl is-active service_name

# 启动/停止服务
systemctl start service_name
systemctl stop service_name

# 重启服务
systemctl restart service_name
systemctl reload service_name

# 设置开机自启
systemctl enable service_name
systemctl disable service_name
```

### 传统服务管理
```bash
# 查看运行级别
runlevel
who -r

# 服务控制
service service_name start
service service_name stop
service service_name restart

# 查看服务列表
chkconfig --list
ls /etc/init.d/
```

### 服务监控
```bash
# 查看运行中的服务
ps aux | grep service_name
netstat -tulnp | grep :port

# 服务性能监控
systemctl status service_name --no-pager
journalctl -u service_name -f
```

---

## 备份恢复

### 文件备份
```bash
# 基本文件备份
tar -czf backup.tar.gz /path/to/backup
tar -cjf backup.tar.bz2 /path/to/backup

# 增量备份
tar -czf backup-$(date +%Y%m%d).tar.gz --listed-incremental=snapshot.file /path

# 排除文件备份
tar -czf backup.tar.gz --exclude='*.log' /path

# 远程备份
rsync -avz /local/path/ user@remote:/remote/path/
scp -r /local/path/ user@remote:/remote/path/
```

### 数据库备份
```bash
# MySQL备份
mysqldump -u username -p database_name > backup.sql
mysqldump -u username -p --all-databases > all_backup.sql

# PostgreSQL备份
pg_dump -U username database_name > backup.sql
pg_dumpall -U username > all_backup.sql

# MongoDB备份
mongodump --db database_name --out /backup/path
```

### 系统备份
```bash
# 系统镜像备份
dd if=/dev/sda of=/backup/system.img bs=4M
dd if=/dev/sda1 of=/backup/boot.img bs=4M

# LVM快照备份
lvcreate -L 10G -s -n snapshot_name /dev/vg0/lv0
dd if=/dev/vg0/snapshot_name of=/backup/lv0_snapshot.img

# 恢复系统
dd if=/backup/system.img of=/dev/sda bs=4M
```

---

## 故障排查

### 系统启动问题
```bash
# 查看启动日志
journalctl -b
dmesg | tail -50

# 检查文件系统
fsck /dev/sda1
fsck -f /dev/sda1

# 查看启动服务
systemctl list-units --type=service --state=failed
```

### 网络问题排查
```bash
# 检查网络配置
ip addr show
ip route show

# 测试DNS解析
nslookup google.com
dig google.com

# 检查防火墙
iptables -L -n -v
firewall-cmd --list-all

# 网络抓包
tcpdump -i eth0 port 80
tcpdump -i any host 192.168.1.1
```

### 性能问题排查
```bash
# 查看系统瓶颈
vmstat 1
iostat -x 1
sar -u 1

# 查看高负载进程
top
htop

# 分析内存泄漏
pmap PID
cat /proc/PID/status

# 检查磁盘IO
iotop
iostat -x 1
```

---

## 自动化脚本

### 系统监控脚本
```bash
#!/bin/bash
# system_monitor.sh - 系统监控脚本

# CPU使用率监控
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
echo "CPU Usage: ${cpu_usage}%"

# 内存使用率监控
mem_info=$(free | grep Mem)
mem_total=$(echo $mem_info | awk '{print $2}')
mem_used=$(echo $mem_info | awk '{print $3}')
mem_percent=$((mem_used * 100 / mem_total))
echo "Memory Usage: ${mem_percent}%"

# 磁盘使用率监控
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
echo "Disk Usage: ${disk_usage}%"

# 发送告警邮件
if [ $cpu_usage -gt 80 ] || [ $mem_percent -gt 80 ] || [ $disk_usage -gt 80 ]; then
    echo "System alert: High resource usage detected" | mail -s "System Alert" admin@example.com
fi
```

### 日志分析脚本
```bash
#!/bin/bash
# log_analyzer.sh - 日志分析脚本

LOG_FILE="/var/log/application.log"
ERROR_COUNT=$(grep -c "ERROR" $LOG_FILE)
WARNING_COUNT=$(grep -c "WARNING" $LOG_FILE)

echo "=== Log Analysis Report ==="
echo "Error count: $ERROR_COUNT"
echo "Warning count: $WARNING_COUNT"
echo ""
echo "Top 10 error messages:"
grep "ERROR" $LOG_FILE | head -10

# 生成报告文件
REPORT_FILE="/tmp/log_report_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
Log Analysis Report - $(date)
================================
Error count: $ERROR_COUNT
Warning count: $WARNING_COUNT

Top 10 error messages:
$(grep "ERROR" $LOG_FILE | head -10)
EOF
```

### 自动化部署脚本
```bash
#!/bin/bash
# deploy.sh - 自动化部署脚本

APP_NAME="myapp"
DEPLOY_PATH="/opt/$APP_NAME"
BACKUP_PATH="/opt/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 创建备份
if [ -d "$DEPLOY_PATH" ]; then
    tar -czf "${BACKUP_PATH}/${APP_NAME}_backup_${TIMESTAMP}.tar.gz" $DEPLOY_PATH
fi

# 停止服务
systemctl stop $APP_NAME

# 部署新版本
rm -rf $DEPLOY_PATH
mkdir -p $DEPLOY_PATH
cp -r /tmp/new_version/* $DEPLOY_PATH

# 设置权限
chown -R appuser:appgroup $DEPLOY_PATH
chmod -R 755 $DEPLOY_PATH

# 启动服务
systemctl start $APP_NAME

# 验证部署
sleep 5
if systemctl is-active $APP_NAME; then
    echo "Deployment successful"
else
    echo "Deployment failed, rolling back..."
    tar -xzf "${BACKUP_PATH}/${APP_NAME}_backup_${TIMESTAMP}.tar.gz" -C /
    systemctl start $APP_NAME
fi
```

---

## 最佳实践

### 安全最佳实践
```bash
# 定期更新系统
yum update -y  # RHEL/CentOS
apt update && apt upgrade -y  # Ubuntu/Debian

# 配置SSH安全
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
AllowUsers admin

# 配置防火墙
ufw enable
ufw allow ssh
ufw allow http
ufw allow https

# 定期安全扫描
lynis audit system
```

### 性能优化建议
```bash
# 内核参数优化
# /etc/sysctl.conf
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
vm.swappiness = 1

# 文件系统优化
noatime,nodiratime  # 挂载选项
deadline  # IO调度器

# 服务优化
# 调整服务资源配置
# 设置适当的ulimit值
```

### 监控告警设置
```bash
# 配置系统告警
# /etc/crontab
*/5 * * * * /usr/local/bin/system_monitor.sh

# 配置日志轮转
# /etc/logrotate.d/application
/var/log/application.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}

# 配置监控工具
# Prometheus + Grafana
# Zabbix
# Nagios
```

---