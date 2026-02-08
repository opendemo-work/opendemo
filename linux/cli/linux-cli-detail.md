# Linux CLI命令详解

本文档详细解释Linux系统管理常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. ps (进程状态查看)

### 用途
`ps` 用于显示当前系统中运行的进程信息，是Linux系统管理和故障排查的基础工具。

### 输出示例
```bash
# 查看所有进程详细信息
$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1 168488 11232 ?        Ss   Nov01   0:05 /sbin/init
mysql      12345  0.1  2.3 1847292 189456 ?      Sl   Nov01  12:45 /usr/sbin/mysqld
www-data   12346  0.0  0.8 123456 65432 ?        S    Nov01   2:34 nginx: worker process
user       23456  0.0  0.1  12345  8765 pts/0    Ss   14:30   0:00 -bash
```

### 内容解析
- **PID**: 进程ID
- **%CPU**: CPU使用率
- **%MEM**: 内存使用率
- **VSZ**: 虚拟内存大小
- **RSS**: 常驻内存大小
- **STAT**: 进程状态
- **COMMAND**: 启动命令

### 常用参数
- `aux`: 显示所有进程详细信息
- `-u username`: 显示指定用户进程
- `-p pid`: 显示指定PID进程

### 注意事项
- 监控高资源使用进程
- 及时清理僵尸进程
- 操作前确认进程重要性

### 安全风险
- 终止关键进程可能导致服务中断
- 进程信息可能暴露系统结构

## 2. top (实时系统监控)

### 用途
`top` 提供实时系统性能监控，显示CPU、内存使用和进程活动。

### 输出示例
```bash
$ top
top - 14:45:23 up 12 days,  5:32,  2 users,  load average: 0.75, 0.82, 0.78
MiB Mem :   7962.8 total,    845.2 free,   4234.1 used,   2883.5 buff/cache
    PID USER      %CPU  %MEM     TIME+ COMMAND
  12345 mysql     15.2   2.3  12:45.34 mysqld
  12346 www-data   2.1   0.8   2:34.56 nginx
```

### 常用参数
- `-o field`: 按字段排序
- `-u username`: 显示指定用户进程
- `-b -n 1`: 批处理模式单次输出

## 3. df (磁盘空间使用)

### 用途
`df` 显示文件系统磁盘空间使用情况。

### 输出示例
```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   25G   23G  52% /
/dev/sda2       100G   45G   50G  48% /home
/dev/sdb1       500G  320G  180G  65% /data

$ df -i
Filesystem       Inodes   IUsed    IFree IUse% Mounted on
/dev/sda1      13107200  456789 12650411    4% /
```

### 常用参数
- `-h`: 人类可读格式
- `-i`: 显示inode使用情况
- `-t type`: 显示指定类型文件系统

## 4. du (目录空间使用)

### 用途
`du` 显示目录和文件的磁盘使用情况。

### 输出示例
```bash
$ du -h --max-depth=1
4.0K    ./.ssh
8.0K    ./Documents
24K     ./Projects
2.3G    ./Videos
3.8G    .

$ du -sh /var/log/*
1.2G    /var/log/nginx
890M    /var/log/mysql
```

### 常用参数
- `-h`: 人类可读格式
- `-s`: 只显示总计
- `--max-depth=N`: 限制目录深度

## 5. netstat (网络连接状态)

### 用途
`netstat` 显示网络连接、路由表、接口统计等网络信息。

### 输出示例
```bash
$ netstat -tlnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      5678/mysqld
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      9012/nginx
```

### 常用参数
- `-t`: TCP连接
- `-u`: UDP连接
- `-l`: 监听状态
- `-n`: 数字格式
- `-p`: 显示进程信息

## 6. ss (套接字统计)

### 用途
`ss` 是现代网络诊断工具，比netstat更快更强大。

### 输出示例
```bash
$ ss -tlnp
State      Recv-Q Send-Q     Local Address:Port                      Peer Address:Port
LISTEN     0      128            0.0.0.0:22                            0.0.0.0:*                 users:(("sshd",pid=1234,fd=3))
LISTEN     0      128          127.0.0.1:3306                          0.0.0.0:*                 users:(("mysqld",pid=5678,fd=21))
```

## 7. iptables (防火墙规则)

### 用途
`iptables` 配置网络包过滤规则，实现防火墙功能。

### 输出示例
```bash
$ sudo iptables -L -n -v
Chain INPUT (policy ACCEPT 12345 packets, 6789012 bytes)
 pkts bytes target     prot opt in     out     source               destination
  123   45678 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0
  456  78901 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22
   56   7890 DROP       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:23
```

### 常用操作
```bash
# 允许SSH连接
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 拒绝特定IP
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# 保存规则
sudo iptables-save > /etc/iptables/rules.v4
```

## 8. systemctl (服务管理)

### 用途
`systemctl` 管理systemd服务。

### 输出示例
```bash
$ systemctl status nginx.service
● nginx.service - A high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service)
     Active: active (running) since Thu 2023-12-07 15:30:15 CST
   Main PID: 1236 (nginx)
      Tasks: 5
     Memory: 12.3M
     CGroup: /system.slice/nginx.service
```

### 常用命令
```bash
# 查看服务状态
systemctl status nginx.service

# 启动/停止/重启服务
sudo systemctl start mysql.service
sudo systemctl stop nginx.service
sudo systemctl restart apache2.service

# 启用/禁用开机自启
sudo systemctl enable redis-server.service
sudo systemctl disable bluetooth.service
```

## 9. journalctl (系统日志)

### 用途
`journalctl` 查看systemd日志。

### 输出示例
```bash
$ journalctl -u nginx.service
-- Logs begin at Tue 2023-12-05 09:15:23 CST
Dec 07 15:30:15 server systemd[1]: Starting nginx...
Dec 07 15:30:15 server nginx[1234]: syntax is ok
Dec 07 15:30:15 server systemd[1]: Started nginx.
Dec 07 16:23:45 server nginx[1236]: "GET / HTTP/1.1" 200 612

$ journalctl -f
-- Logs begin at Tue 2023-12-05 09:15:23 CST
Dec 07 17:46:25 server sshd[23456]: Accepted publickey
```

### 常用参数
- `-u service`: 查看特定服务日志
- `-f`: 实时跟踪日志
- `-n number`: 显示最近n条日志
- `--since/--until`: 指定时间范围

## 10. find (文件查找)

### 用途
`find` 在文件系统中查找文件。

### 输出示例
```bash
# 按名称查找
$ find /var/log -name "*.log" -type f
/var/log/nginx/access.log
/var/log/nginx/error.log
/var/log/mysql/error.log

# 按时间查找
$ find /home -mtime -7 -type f
/home/user/document.pdf
/home/user/photo.jpg

# 按大小查找
$ find /tmp -size +100M -type f
/tmp/large_file.tar.gz
```

### 常用参数
- `-name pattern`: 按名称匹配
- `-type f/d`: 查找文件/目录
- `-mtime days`: 按修改时间
- `-size [+/-]size`: 按文件大小

## 11. grep (文本搜索)

### 用途
`grep` 在文件中搜索文本模式。

### 输出示例
```bash
# 基本搜索
$ grep "error" /var/log/nginx/error.log
2023/12/07 14:30:15 [error] 1234#1234: *5678 open() failed

# 忽略大小写
$ grep -i "mysql" /var/log/syslog
Dec 07 15:20:10 server mysql: Starting MySQL

# 显示行号
$ grep -n "timeout" config.txt
23:connection_timeout = 30
45:read_timeout = 60
```

### 常用参数
- `-i`: 忽略大小写
- `-n`: 显示行号
- `-r`: 递归搜索目录
- `-v`: 反向匹配（排除）

## 12. tar (文件打包压缩)

### 用途
`tar` 打包和压缩文件。

### 输出示例
```bash
# 创建压缩包
$ tar -czf backup.tar.gz /home/user/documents
$ tar -cjf backup.tar.bz2 /var/www

# 解压文件
$ tar -xzf backup.tar.gz
$ tar -xjf backup.tar.bz2 -C /tmp

# 查看压缩包内容
$ tar -tzf backup.tar.gz
home/user/documents/
home/user/documents/file1.txt
home/user/documents/file2.pdf
```

### 常用参数
- `-c`: 创建新档案
- `-x`: 解压档案
- `-z`: 使用gzip压缩
- `-j`: 使用bzip2压缩
- `-f`: 指定文件名

## 13. rsync (文件同步)

### 用途
`rsync` 同步文件和目录，支持增量传输。

### 输出示例
```bash
# 本地文件同步
$ rsync -av /home/user/documents/ /backup/documents/
sending incremental file list
document1.pdf
document2.docx

sent 2,345,678 bytes  received 456 bytes  4,692,268.00 bytes/sec

# 远程同步
$ rsync -avz /var/www/ user@remote:/backup/www/
building file list ... done
index.html
css/style.css
```

### 常用参数
- `-a`: 归档模式（保持属性）
- `-v`: 详细输出
- `-z`: 压缩传输
- `-n`: 试运行（不实际执行）

## 14. chmod/chown (权限管理)

### 用途
管理文件和目录的权限和所有权。

### 输出示例
```bash
# 修改文件权限
$ chmod 644 config.txt
$ chmod +x script.sh
$ chmod -R 755 /var/www/html

# 修改文件所有者
$ chown user:group file.txt
$ chown -R www-data:www-data /var/www
$ chown user: /home/user/documents

# 查看权限
$ ls -l
-rw-r--r-- 1 user group 1234 Dec 07 15:30 file.txt
-rwxr-xr-x 1 user group 5678 Dec 07 15:31 script.sh
```

### 权限说明
- 数字模式：755 = rwxr-xr-x
- 字母模式：u+rwx,g+rx,o+rx

## 15. lsof (列出打开的文件)

### 用途
`lsof` 列出进程打开的文件、网络连接等。

### 输出示例
```bash
# 查看进程打开的文件
$ lsof -p 12345
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
mysqld  12345 mysql  cwd    DIR  253,0     4096  524288 /var/lib/mysql
mysqld  12345 mysql  txt    REG  253,0  2345678  654321 /usr/sbin/mysqld

# 查看端口占用
$ lsof -i :80
COMMAND   PID      USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx    1236      root    6u  IPv4  12345      0t0  TCP *:http (LISTEN)
nginx    1237 www-data    6u  IPv4  12345      0t0  TCP *:http (LISTEN)

# 查看用户打开的文件
$ lsof -u user
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
bash     2345 user  cwd    DIR  253,0     4096  789012 /home/user
bash     2345 user  txt    REG  253,0  1234567  345678 /bin/bash
```

### 常用参数
- `-p pid`: 查看指定进程
- `-i port`: 查看端口占用
- `-u user`: 查看用户文件
- `-c command`: 查看命令相关文件

---

**总结**: 以上是Linux系统管理常用的CLI工具详解。在生产环境中使用这些工具时，务必注意权限管理、系统安全和操作规范，确保系统的稳定运行和数据安全。