# 🚀 Nginx 命令行速查表 (CLI Cheatsheet)

> 生产环境必备的 Nginx 命令行参考手册，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [基础管理命令](#基础管理命令)
- [配置管理](#配置管理)
- [性能监控](#性能监控)
- [日志分析](#日志分析)
- [安全加固](#安全加固)
- [SSL/TLS 管理](#ssltls-管理)
- [负载均衡](#负载均衡)
- [缓存优化](#缓存优化)
- [故障排查](#故障排查)
- [性能调优](#性能调优)
- [模块管理](#模块管理)
- [实用技巧](#实用技巧)

---

## 基础管理命令

### 服务管理
```bash
# 启动 Nginx
sudo systemctl start nginx
sudo service nginx start

# 停止 Nginx
sudo systemctl stop nginx
sudo service nginx stop

# 重启 Nginx
sudo systemctl restart nginx
sudo service nginx restart

# 重新加载配置（不中断服务）
sudo systemctl reload nginx
sudo service nginx reload

# 查看 Nginx 状态
sudo systemctl status nginx
sudo service nginx status

# 设置开机自启
sudo systemctl enable nginx
sudo systemctl disable nginx
```

### 进程管理
```bash
# 查看 Nginx 主进程
ps aux | grep nginx

# 查看 Nginx 工作进程
ps -ef | grep nginx

# 查看 Nginx 进程树
pstree -p | grep nginx

# 杀死所有 Nginx 进程
sudo pkill nginx

# 平滑停止 Nginx
sudo nginx -s quit

# 立即停止 Nginx
sudo nginx -s stop

# 重新打开日志文件
sudo nginx -s reopen
```

### 版本和编译信息
```bash
# 查看 Nginx 版本
nginx -v

# 查看详细版本信息
nginx -V

# 查看编译参数
nginx -V 2>&1 | tr ' ' '\n'

# 查看支持的模块
nginx -V 2>&1 | grep -o 'with-[a-zA-Z0-9_]*'
```

---

## 配置管理

### 配置文件操作
```bash
# 测试配置文件语法
sudo nginx -t

# 测试配置并显示详细信息
sudo nginx -T

# 指定配置文件启动
sudo nginx -c /path/to/nginx.conf

# 查看当前使用的配置文件
sudo nginx -T | head -20

# 备份配置文件
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d)

# 恢复配置文件
sudo cp /etc/nginx/nginx.conf.backup.20231201 /etc/nginx/nginx.conf
```

### 配置文件结构
```bash
# 查看主配置文件
cat /etc/nginx/nginx.conf

# 查看站点配置
ls /etc/nginx/sites-available/
ls /etc/nginx/sites-enabled/

# 查看模块配置
ls /etc/nginx/modules-available/
ls /etc/nginx/modules-enabled/

# 查看 MIME 类型配置
cat /etc/nginx/mime.types

# 查看 fastcgi 配置
cat /etc/nginx/fastcgi_params
```

### 配置编辑技巧
```bash
# 使用 vim 编辑配置
sudo vim /etc/nginx/nginx.conf

# 使用 nano 编辑配置
sudo nano /etc/nginx/sites-available/default

# 批量替换配置内容
sudo sed -i 's/old_value/new_value/g' /etc/nginx/nginx.conf

# 查找配置中的特定项
grep -r "server_name" /etc/nginx/

# 递归查找配置文件
find /etc/nginx -name "*.conf" -type f
```

---

## 性能监控

### 实时监控
```bash
# 查看 Nginx 连接状态
ss -tuln | grep :80
netstat -tuln | grep :80

# 查看活跃连接数
netstat -an | grep :80 | grep ESTABLISHED | wc -l

# 查看连接状态统计
netstat -an | grep :80 | awk '{print $6}' | sort | uniq -c | sort -nr

# 实时监控连接数
watch -n 1 'netstat -an | grep :80 | wc -l'
```

### 性能指标
```bash
# 查看 Nginx worker 进程 CPU 使用率
top -p $(pgrep nginx | tr '\n' ',' | sed 's/,$//')

# 查看内存使用情况
ps aux | grep nginx | awk '{sum+=$6} END {print "Memory:", sum/1024 "MB"}'

# 查看文件描述符使用情况
lsof -p $(pgrep nginx) | wc -l

# 查看最大文件描述符限制
cat /proc/$(pgrep nginx | head -1)/limits | grep "Max open files"
```

### 请求统计
```bash
# 查看每秒请求数
curl -s http://localhost/nginx_status | grep "requests" | awk '{print $3}'

# 查看并发连接数
curl -s http://localhost/nginx_status | grep "active" | awk '{print $3}'

# 查看处理中的连接数
curl -s http://localhost/nginx_status | grep "reading" | awk '{print $2}'
```

---

## 日志分析

### 访问日志分析
```bash
# 查看实时访问日志
tail -f /var/log/nginx/access.log

# 查看错误日志
tail -f /var/log/nginx/error.log

# 统计独立访客IP
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -20

# 统计最常访问的页面
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -20

# 统计HTTP状态码分布
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# 统计流量消耗
awk '{sum+=$10} END {print "Total bytes:", sum, "Bytes:", sum/1024/1024 "MB"}' /var/log/nginx/access.log

# 查找404错误请求
grep " 404 " /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -nr

# 查找5xx错误请求
grep " 5[0-9][0-9] " /var/log/nginx/access.log
```

### 错误日志分析
```bash
# 查看最近的错误
tail -n 100 /var/log/nginx/error.log

# 统计错误类型
grep -o "] .*" /var/log/nginx/error.log | sort | uniq -c | sort -nr

# 查找特定时间段的错误
grep "$(date '+%Y/%m/%d')" /var/log/nginx/error.log

# 实时监控错误日志
tail -f /var/log/nginx/error.log | grep --color=auto "error\|warn"
```

### 日志轮转管理
```bash
# 手动轮转日志
sudo logrotate -f /etc/logrotate.d/nginx

# 查看日志轮转配置
cat /etc/logrotate.d/nginx

# 测试日志轮转配置
sudo logrotate -d /etc/logrotate.d/nginx
```

---

## 安全加固

### 访问控制
```bash
# 生成 htpasswd 文件
sudo htpasswd -c /etc/nginx/.htpasswd username

# 添加用户到 htpasswd
sudo htpasswd /etc/nginx/.htpasswd newuser

# 查看 htpasswd 用户
cat /etc/nginx/.htpasswd

# 删除 htpasswd 用户
sudo htpasswd -D /etc/nginx/.htpasswd username
```

### 安全头配置
```bash
# 检查安全头设置
curl -I http://your-domain.com

# 测试安全配置
nmap --script http-security-headers -p 80 your-domain.com

# SSL 配置检查
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

### 防护措施
```bash
# 限制请求频率
# 在配置中添加:
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

# 限制并发连接数
limit_conn_zone $binary_remote_addr zone=addr:10m;

# 防止恶意 User-Agent
if ($http_user_agent ~* (sqlmap|nikto|nessus)) {
    return 403;
}
```

---

## SSL/TLS 管理

### 证书管理
```bash
# 生成自签名证书
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt

# 查看证书信息
openssl x509 -in /etc/nginx/ssl/nginx.crt -text -noout

# 检查证书有效期
openssl x509 -in /etc/nginx/ssl/nginx.crt -noout -dates

# 验证证书链
openssl verify -CAfile /etc/nginx/ssl/ca.crt /etc/nginx/ssl/nginx.crt

# 生成 Diffie-Hellman 参数
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```

### Let's Encrypt 管理
```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 续期证书
sudo certbot renew

# 测试续期过程
sudo certbot renew --dry-run

# 自动续期（添加到 crontab）
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

### SSL 配置测试
```bash
# 测试 SSL 配置
sudo nginx -t

# 检查 SSL 协议支持
openssl s_client -connect your-domain.com:443 -servername your-domain.com -tls1_2

# SSL Labs 评级测试
curl -s https://www.ssllabs.com/ssltest/analyze.html?d=your-domain.com
```

---

## 负载均衡

### 负载均衡配置检查
```bash
# 查看 upstream 配置
grep -r "upstream" /etc/nginx/

# 测试负载均衡
for i in {1..10}; do curl -s http://your-loadbalancer/ | grep "Server IP"; done

# 查看后端服务器状态
curl -s http://your-domain/nginx_status

# 监控后端健康检查
tail -f /var/log/nginx/error.log | grep "upstream"
```

### 会话保持测试
```bash
# 测试 sticky session
for i in {1..5}; do curl -s --cookie-jar cookie.txt --cookie cookie.txt http://your-domain/; done

# 查看粘性会话效果
curl -s --cookie-jar cookie.txt --cookie cookie.txt http://your-domain/ | grep "Server"
```

---

## 缓存优化

### 缓存配置检查
```bash
# 查看 proxy_cache 配置
grep -r "proxy_cache" /etc/nginx/

# 测试缓存命中
curl -I http://your-domain/static-file.js

# 清除特定缓存
curl -X PURGE http://your-domain/cached-resource

# 查看缓存统计
sudo nginx -T | grep -A 10 "proxy_cache_path"
```

### 缓存性能监控
```bash
# 监控缓存命中率
tail -f /var/log/nginx/access.log | grep "HIT\|MISS"

# 统计缓存效果
awk '/HIT/ {hit++} /MISS/ {miss++} END {print "Hit:", hit, "Miss:", miss, "Rate:", hit/(hit+miss)*100 "%"}' /var/log/nginx/access.log
```

---

## 故障排查

### 常见问题诊断
```bash
# 检查配置语法错误
sudo nginx -t

# 查看详细的错误信息
sudo nginx -T 2>&1 | grep -A 5 -B 5 "error"

# 检查端口占用
sudo netstat -tulnp | grep :80
sudo ss -tulnp | grep :80

# 检查防火墙设置
sudo iptables -L -n | grep 80
sudo ufw status | grep 80

# 检查 SELinux 状态
sestatus
sudo setsebool -P httpd_can_network_connect 1
```

### 权限问题排查
```bash
# 检查 Nginx 用户权限
ps aux | grep nginx

# 检查配置文件权限
ls -la /etc/nginx/

# 检查网站目录权限
ls -la /var/www/html/

# 修复权限问题
sudo chown -R www-data:www-data /var/www/html/
sudo chmod -R 755 /var/www/html/
```

### 性能问题排查
```bash
# 检查系统资源使用
top
htop

# 检查磁盘IO
iostat -x 1

# 检查网络连接
netstat -an | grep :80

# 检查内存使用
free -h

# 检查进程限制
ulimit -a
```

---

## 性能调优

### 工作进程优化
```bash
# 查看 CPU 核心数
nproc
lscpu | grep "^CPU(s):"

# 设置合适的 worker_processes
# 在 nginx.conf 中:
worker_processes auto;

# 设置 worker_connections
worker_connections 1024;

# 设置 worker_rlimit_nofile
worker_rlimit_nofile 65535;
```

### 内存优化
```bash
# 调整 TCP 缓冲区大小
echo 'net.core.rmem_max = 16777216' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 16777216' >> /etc/sysctl.conf
sudo sysctl -p

# 启用 TCP 窗口缩放
echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf
```

### 缓存优化配置
```bash
# 启用 sendfile
sendfile on;

# 启用 tcp_nopush
tcp_nopush on;

# 启用 tcp_nodelay
tcp_nodelay on;

# 设置 keepalive_timeout
keepalive_timeout 65;
```

---

## 模块管理

### 动态模块管理
```bash
# 查看已安装的模块
nginx -V 2>&1 | grep -o 'with-[a-zA-Z0-9_]*'

# 查看可用的动态模块
ls /usr/lib/nginx/modules/

# 加载动态模块
load_module modules/ngx_http_geoip_module.so;

# 查看第三方模块
nginx -V 2>&1 | grep -o 'add-module=[^ ]*'
```

### 模块编译
```bash
# 下载 Nginx 源码
wget http://nginx.org/download/nginx-1.24.0.tar.gz
tar -zxvf nginx-1.24.0.tar.gz

# 配置编译选项
cd nginx-1.24.0
./configure --with-http_ssl_module --with-http_v2_module --add-module=/path/to/module

# 编译安装
make && sudo make install
```

---

## 实用技巧

### 批量操作
```bash
# 批量测试多个站点配置
for conf in /etc/nginx/sites-enabled/*; do sudo nginx -t -c "$conf"; done

# 批量重启站点
for site in /etc/nginx/sites-enabled/*; do sudo ln -sf "$site" /etc/nginx/sites-available/; done
sudo systemctl reload nginx

# 批量查找配置文件中的关键字
grep -r "proxy_pass" /etc/nginx/sites-enabled/

# 批量备份配置
sudo tar -czf nginx-config-backup-$(date +%Y%m%d).tar.gz /etc/nginx/
```

### 快捷别名设置
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias ngxreload='sudo systemctl reload nginx'
alias ngxtest='sudo nginx -t'
alias ngxstatus='sudo systemctl status nginx'
alias ngxlogs='sudo tail -f /var/log/nginx/access.log'
alias ngxerrors='sudo tail -f /var/log/nginx/error.log'
alias ngxconf='sudo vim /etc/nginx/nginx.conf'

# 更多实用别名
alias ngxbackup='sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d)'
alias ngxrestore='sudo cp /etc/nginx/nginx.conf.backup.* /etc/nginx/nginx.conf'
```

### 自动化脚本
```bash
# 创建 Nginx 状态检查脚本
cat > /usr/local/bin/nginx-status.sh << 'EOF'
#!/bin/bash
echo "=== Nginx Status Check ==="
echo "Processes: $(pgrep nginx | wc -l)"
echo "Active connections: $(curl -s http://localhost/nginx_status 2>/dev/null | grep active | awk '{print $3}')"
echo "Memory usage: $(ps aux | grep nginx | awk '{sum+=$6} END {print sum/1024 "MB"}')"
EOF
sudo chmod +x /usr/local/bin/nginx-status.sh

# 创建日志清理脚本
cat > /usr/local/bin/clean-nginx-logs.sh << 'EOF'
#!/bin/bash
# 清理 30 天前的日志
find /var/log/nginx -name "*.log.*" -mtime +30 -delete
EOF
sudo chmod +x /usr/local/bin/clean-nginx-logs.sh
```

---

> **📌 注意事项**：
> - 生产环境中执行重启操作前务必测试配置
> - 重要配置变更建议先在测试环境验证
> - 定期备份配置文件和SSL证书
> - 监控日志文件大小，及时轮转
> - 遵循最小权限原则配置访问控制
> - 定期更新 Nginx 版本以获得安全补丁