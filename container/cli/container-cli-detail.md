# Container CLI命令详解

本文档详细解释容器技术常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. docker (Docker容器平台)

### 用途
`docker` 是容器化平台的核心命令行工具，用于构建、运行、管理Docker容器和镜像。它是现代应用部署和微服务架构的基础工具。

### 输出示例
```bash
# 查看Docker版本和系统信息
$ docker version
Client: Docker Engine - Community
 Version:           24.0.5
 API version:       1.43
 Go version:        go1.20.6
 Git commit:        ced0996
 Built:             Wed Jul 26 16:42:05 2023
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          24.0.5
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.6
  Git commit:       a61e2b4
  Built:            Wed Jul 26 16:42:05 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.21
  GitCommit:        3dce8eb055cbb6872793272b4f20ed16117344f8
 runc:
  Version:          1.1.7
  GitCommit:        v1.1.7-0-g860f061
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0

# 查看Docker系统信息
$ docker info
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
  compose: Docker Compose (Docker Inc.)

Server:
 Containers: 12
  Running: 8
  Paused: 0
  Stopped: 4
 Images: 25
 Server Version: 24.0.5
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Runtimes: runc io.containerd.runc.v2
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 3dce8eb055cbb6872793272b4f20ed16117344f8
 runc version: v1.1.7-0-g860f061
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 5.15.0-76-generic
 Operating System: Ubuntu 22.04.2 LTS
 OSType: linux
 Architecture: x86_64

# 列出本地镜像
$ docker images
REPOSITORY              TAG       IMAGE ID       CREATED        SIZE
nginx                   latest    605c77e624dd   2 weeks ago    141MB
redis                   7.0       761a5b0e709d   3 weeks ago    113MB
python                  3.9       9141382ff9da   4 weeks ago    917MB
ubuntu                  22.04     58db3edaf2be   2 months ago   77.8MB
hello-world             latest    feb5d9fea6a5   14 months ago  13.3kB

# 搜索Docker Hub镜像
$ docker search nginx
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
nginx                             Official build of Nginx.                        18000+    [OK]       
bitnami/nginx                     Bitnami nginx Docker Image                      120+      [OK]       
linuxserver/nginx                 An Nginx container, brought to you by LinuxS…   180+      [OK]       
```

### 内容解析
- **版本信息**: 显示客户端和服务端的版本、构建信息和Git提交
- **系统状态**: 显示容器运行状态统计、存储驱动和安全选项
- **镜像列表**: 显示本地镜像的仓库名、标签、ID、创建时间和大小
- **搜索结果**: 显示Docker Hub上的镜像搜索结果和星级评价

### 常用参数详解
- `version`: 显示Docker版本信息
- `info`: 显示Docker系统详细信息
- `images`: 列出本地镜像
- `search <term>`: 搜索Docker Hub镜像
- `pull <image>`: 拉取镜像到本地
- `push <image>`: 推送镜像到仓库

### 注意事项
- 确保Docker服务正常运行
- 定期清理无用镜像和容器
- 注意镜像的安全性和来源可信度

### 安全风险
- ⚠️ 运行不受信任的镜像可能带来安全威胁
- ⚠️ 容器逃逸可能导致主机系统受损
- ⚠️ 端口映射可能暴露内部服务

## 2. docker run (运行容器)

### 用途
`docker run` 用于创建并启动新的容器实例，是Docker最核心的操作命令。支持各种运行时配置选项。

### 输出示例
```bash
# 基本容器运行
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete 
Digest: sha256:37a0b92b08d4919615c3ee023f7ddb068d12b8387475d64c622ac30f45c29c51
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

# 后台运行容器
$ docker run -d --name web-server -p 8080:80 nginx:latest
a1b2c3d4e5f6789012345678901234567890abcd

# 交互式运行容器
$ docker run -it --name ubuntu-test ubuntu:22.04 /bin/bash
root@a1b2c3d4e5f6:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@a1b2c3d4e5f6:/# exit

# 运行带环境变量的容器
$ docker run -d --name redis-server -e REDIS_PASSWORD=secretpass redis:7.0
b2c3d4e5f6789012345678901234567890abcde

# 挂载卷运行容器
$ docker run -d --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0
c3d4e5f67890123456789012345678901234567

# 限制资源运行容器
$ docker run -d --name limited-app \
  --memory=512m \
  --cpus=0.5 \
  nginx:latest
d4e5f6789012345678901234567890123456789
```

### 内容解析
- **镜像拉取**: 首次运行时自动从仓库拉取镜像
- **容器ID**: 成功启动后返回容器的长ID
- **交互模式**: 提供shell访问容器内部
- **端口映射**: 主机端口与容器端口的映射关系
- **资源限制**: 内存和CPU使用限制

### 常用参数详解
- `-d, --detach`: 后台运行容器
- `-it`: 交互式运行（-i保持STDIN，-t分配伪TTY）
- `--name <name>`: 指定容器名称
- `-p <host>:<container>`: 端口映射
- `-e <key=value>`: 设置环境变量
- `-v <host>:<container>`: 挂载卷
- `--memory <size>`: 限制内存使用
- `--cpus <number>`: 限制CPU使用

### 注意事项
- 合理设置资源限制避免资源争用
- 重要的数据应使用卷挂载持久化
- 生产环境应使用具体的镜像标签而非latest

### 安全风险
- ⚠️ 容器以root权限运行存在安全隐患
- ⚠️ 端口暴露可能带来网络攻击风险
- ⚠️ 敏感信息通过环境变量传递可能泄露

## 3. docker ps (查看容器状态)

### 用途
`docker ps` 用于列出容器实例及其运行状态，是日常容器管理最常用的命令之一。

### 输出示例
```bash
# 查看运行中的容器
$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS        PORTS                                   NAMES
a1b2c3d4e5f6   nginx:latest   "/docker-entrypoint.…"   2 hours ago    Up 2 hours    0.0.0.0:8080->80/tcp                    web-server
b2c3d4e5f678   redis:7.0      "docker-entrypoint.s…"   3 hours ago    Up 3 hours    6379/tcp                                redis-server
c3d4e5f67890   mysql:8.0      "docker-entrypoint.s…"   4 hours ago    Up 4 hours    0.0.0.0:3306->3306/tcp, 33060/tcp       mysql-server

# 查看所有容器（包括停止的）
$ docker ps -a
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS                     PORTS     NAMES
a1b2c3d4e5f6   nginx:latest    "/docker-entrypoint.…"   2 hours ago    Up 2 hours                 80/tcp    web-server
b2c3d4e5f678   redis:7.0       "docker-entrypoint.s…"   3 hours ago    Up 3 hours                 6379/tcp  redis-server
d4e5f6789012   ubuntu:22.04    "/bin/bash"              5 hours ago    Exited (0) 4 hours ago               ubuntu-test
e5f678901234   hello-world     "/hello"                 6 hours ago    Exited (0) 6 hours ago               heuristic_mendel

# 查看容器详细信息
$ docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}"
CONTAINER ID   IMAGE          STATUS        PORTS                                   NAMES
a1b2c3d4e5f6   nginx:latest   Up 2 hours    0.0.0.0:8080->80/tcp                    web-server
b2c3d4e5f678   redis:7.0      Up 3 hours    6379/tcp                                redis-server
c3d4e5f67890   mysql:8.0      Up 4 hours    0.0.0.0:3306->3306/tcp, 33060/tcp       mysql-server

# 过滤显示特定容器
$ docker ps --filter "status=running"
CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS        PORTS                                   NAMES
a1b2c3d4e5f6   nginx:latest   "/docker-entrypoint.…"   2 hours ago    Up 2 hours    0.0.0.0:8080->80/tcp                    web-server
b2c3d4e5f678   redis:7.0      "docker-entrypoint.s…"   3 hours ago    Up 3 hours    6379/tcp                                redis-server
```

### 内容解析
- **容器ID**: 容器的唯一标识符（短格式）
- **镜像**: 容器基于的镜像名称和标签
- **命令**: 容器启动时执行的命令
- **创建时间**: 容器创建的时间
- **状态**: 容器当前状态（运行中、已停止等）
- **端口**: 端口映射信息
- **名称**: 容器名称（可自定义）

### 常用参数详解
- `-a, --all`: 显示所有容器（包括停止的）
- `-l, --latest`: 显示最新创建的容器
- `-n <number>`: 显示最近创建的n个容器
- `-q, --quiet`: 只显示容器ID
- `--format <template>`: 自定义输出格式
- `--filter <key>=<value>`: 过滤显示条件

### 注意事项
- 定期清理停止的容器释放资源
- 监控容器运行状态及时发现问题
- 使用有意义的容器名称便于管理

### 安全风险
- ⚠️ 运行中的容器可能消耗过多资源
- ⚠️ 停止的容器仍可能包含敏感数据
- ⚠️ 容器名称重复可能导致混淆

## 4. docker logs (查看容器日志)

### 用途
`docker logs` 用于查看容器的标准输出和标准错误日志，是排查容器问题的重要工具。

### 输出示例
```bash
# 查看容器全部日志
$ docker logs web-server
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/12/07 10:15:23 [notice] 1#1: start worker processes
2023/12/07 10:15:23 [notice] 1#1: start worker process 31
2023/12/07 10:15:23 [notice] 1#1: start worker process 32

# 实时跟踪日志
$ docker logs -f redis-server
1:C 07 Dec 2023 10:20:15.123 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 07 Dec 2023 10:20:15.123 # Redis version=7.0.8, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 07 Dec 2023 10:20:15.123 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
1:M 07 Dec 2023 10:20:15.124 * monotonic clock: POSIX clock_gettime
1:M 07 Dec 2023 10:20:15.124 * Running mode=standalone, port=6379.
1:M 07 Dec 2023 10:20:15.124 # Server initialized
1:M 07 Dec 2023 10:20:15.124 * Ready to accept connections

# 查看最近的日志行数
$ docker logs --tail 10 mysql-server
2023-12-07T10:25:15.123456Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.33'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
2023-12-07T10:25:15.123456Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
2023-12-07T10:30:22.456789Z 11 [Warning] [MY-013360] [Server] Plugin 'sha256_password' is deprecated and will be removed in a future release. Please use caching_sha2_password instead.
2023-12-07T10:35:45.789012Z 15 [Note] [MY-010053] [Server] Aborted connection 15 to db: 'test_db' user: 'app_user' host: '172.18.0.1' (Got an error reading communication packets)

# 查看特定时间段的日志
$ docker logs --since 1h web-server
172.18.0.1 - - [07/Dec/2023:10:45:23 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
172.18.0.1 - - [07/Dec/2023:10:45:24 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://localhost:8080/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

### 内容解析
- **启动日志**: 容器启动过程中的配置和初始化信息
- **运行日志**: 应用程序运行期间的输出信息
- **错误信息**: 警告和错误级别的日志条目
- **访问日志**: Web服务器等应用的访问记录

### 常用参数详解
- `-f, --follow`: 实时跟踪日志输出
- `--tail <number>`: 显示最后的n行日志
- `--since <timestamp>`: 显示指定时间之后的日志
- `--until <timestamp>`: 显示指定时间之前的日志
- `-t, --timestamps`: 显示时间戳
- `--details`: 显示额外的详细信息

### 注意事项
- 生产环境中应配置日志轮转避免磁盘占满
- 敏感信息不应出现在日志中
- 大量日志输出可能影响性能

### 安全风险
- ⚠️ 日志中可能包含敏感信息（密码、密钥等）
- ⚠️ 详细的错误信息可能暴露系统内部结构
- ⚠️ 日志文件权限设置不当可能被未授权访问

## 5. docker exec (在运行容器中执行命令)

### 用途
`docker exec` 用于在正在运行的容器中执行命令，常用于调试、管理和维护容器。

### 输出示例
```bash
# 进入容器shell
$ docker exec -it web-server /bin/bash
root@a1b2c3d4e5f6:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1   6424  3244 ?        Ss   10:15   0:00 nginx: master process nginx -g daemon off;
root          31  0.0  0.2  10724  5432 ?        S    10:15   0:00 nginx: worker process
root          32  0.0  0.2  10724  5432 ?        S    10:15   0:00 nginx: worker process
root          45  0.0  0.1   4108  3456 pts/0    Ss   11:30   0:00 /bin/bash
root          58  0.0  0.1   5904  2844 pts/0    R+   11:30   0:00 ps aux
root@a1b2c3d4e5f6:/# exit

# 在容器中执行单条命令
$ docker exec redis-server redis-cli ping
PONG

$ docker exec mysql-server mysql -uroot -prootpass -e "SHOW DATABASES;"
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test_db            |
+--------------------+

# 查看容器进程
$ docker exec web-server ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1   6424  3244 ?        Ss   10:15   0:00 nginx: master process nginx -g daemon off;
root          31  0.0  0.2  10724  5432 ?        S    10:15   0:00 nginx: worker process
root          32  0.0  0.2  10724  5432 ?        S    10:15   0:00 nginx: worker process

# 查看容器网络配置
$ docker exec web-server ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
18: eth0@if19: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
    inet 172.18.0.2/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```

### 内容解析
- **交互式执行**: 提供完整的shell环境访问
- **命令执行结果**: 直接返回容器内命令的输出
- **进程信息**: 显示容器内的进程状态
- **网络信息**: 显示容器的网络配置

### 常用参数详解
- `-i, --interactive`: 保持STDIN打开
- `-t, --tty`: 分配伪TTY
- `-u, --user <user>`: 指定执行用户
- `-w, --workdir <path>`: 指定工作目录
- `-e, --env <key=value>`: 设置环境变量
- `-d, --detach`: 后台执行命令

### 注意事项
- 避免在生产环境中执行破坏性命令
- 确保有足够的权限执行所需操作
- 复杂的调试操作建议使用专门的调试工具

### 安全风险
- ⚠️ 在容器中执行命令可能绕过安全限制
- ⚠️ root权限执行命令存在安全风险
- ⚠️ 敏感操作可能留下安全审计痕迹

## 6. docker build (构建镜像)

### 用途
`docker build` 用于从Dockerfile构建新的镜像，是容器化应用部署的关键步骤。

### 输出示例
```bash
# 基本镜像构建
$ docker build -t my-app:latest .
Sending build context to Docker daemon  3.072kB
Step 1/8 : FROM python:3.9-slim
 ---> 9141382ff9da
Step 2/8 : WORKDIR /app
 ---> Running in a1b2c3d4e5f6
 ---> b2c3d4e5f678
Step 3/8 : COPY requirements.txt .
 ---> c3d4e5f67890
Step 4/8 : RUN pip install -r requirements.txt
 ---> Running in d4e5f6789012
Collecting flask==2.3.2
  Downloading Flask-2.3.2-py3-none-any.whl (96 kB)
Collecting gunicorn==20.1.0
  Downloading gunicorn-20.1.0-py3-none-any.whl (79 kB)
Installing collected packages: gunicorn, flask
Successfully installed flask-2.3.2 gunicorn-20.1.0
 ---> e5f678901234
Step 5/8 : COPY . .
 ---> f67890123456
Step 6/8 : EXPOSE 8000
 ---> g78901234567
Step 7/8 : ENV FLASK_APP=app.py
 ---> h89012345678
Step 8/8 : CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
 ---> i90123456789
Successfully built i90123456789
Successfully tagged my-app:latest

# 指定Dockerfile构建
$ docker build -f Dockerfile.prod -t my-app:prod .
Sending build context to Docker daemon  4.096kB
Step 1/10 : FROM python:3.9-slim as base
 ---> 9141382ff9da
Step 2/10 : WORKDIR /app
 ---> Using cache
 ---> b2c3d4e5f678
# ... 构建步骤 ...

# 多阶段构建
$ docker build -t my-app:optimized --target production .
Sending build context to Docker daemon  5.120kB
Step 1/15 : FROM python:3.9-slim as builder
 ---> 9141382ff9da
Step 2/15 : WORKDIR /build
 ---> a1b2c3d4e5f6
# ... 构建阶段 ...
Step 8/15 : FROM python:3.9-alpine as production
 ---> c2d3e4f5g6h7
Step 9/15 : WORKDIR /app
 ---> d3e4f5g6h7i8
# ... 生产阶段 ...

# 构建时传参
$ docker build --build-arg BUILD_VERSION=1.2.3 -t my-app:v1.2.3 .
Sending build context to Docker daemon  3.072kB
Step 1/8 : FROM python:3.9-slim
 ---> 9141382ff9da
Step 2/8 : ARG BUILD_VERSION
 ---> e4f5g6h7i8j9
Step 3/8 : LABEL version=${BUILD_VERSION}
 ---> f5g6h7i8j9k0
# ... 其他步骤 ...
```

### 内容解析
- **构建上下文**: 发送到Docker守护进程的文件大小
- **构建步骤**: 显示每个Dockerfile指令的执行过程
- **层缓存**: 显示使用缓存的步骤（Using cache）
- **镜像ID**: 成功构建后生成的镜像标识符
- **标签信息**: 构建完成后的镜像标签

### 常用参数详解
- `-t, --tag <name:tag>`: 为镜像设置名称和标签
- `-f, --file <path>`: 指定Dockerfile路径
- `--build-arg <key=value>`: 设置构建时参数
- `--target <stage>`: 指定多阶段构建的目标阶段
- `--no-cache`: 不使用缓存构建
- `--pull`: 构建前拉取最新的基础镜像

### 注意事项
- 优化Dockerfile减少层数和镜像大小
- 合理使用.dockerignore文件排除不必要文件
- 生产环境应使用具体的版本标签
- 定期清理构建缓存释放空间

### 安全风险
- ⚠️ Dockerfile中可能包含敏感信息（密钥、密码）
- ⚠️ 基础镜像可能存在安全漏洞
- ⚠️ 构建过程中下载的依赖可能被篡改
- ⚠️ 多阶段构建可能暴露中间层信息

## 7. docker-compose (多容器应用编排)

### 用途
`docker-compose` 用于定义和运行多容器Docker应用程序，通过YAML文件配置服务、网络和卷。

### 输出示例
```bash
# 启动所有服务
$ docker-compose up -d
Creating network "myapp_default" with the default driver
Creating volume "myapp_db-data" with default driver
Creating myapp_redis_1    ... done
Creating myapp_database_1 ... done
Creating myapp_web_1      ... done
Creating myapp_nginx_1    ... done

# 查看服务状态
$ docker-compose ps
        Name                      Command               State           Ports         
-------------------------------------------------------------------------------------
myapp_database_1   docker-entrypoint.sh mysqld      Up      3306/tcp, 33060/tcp   
myapp_nginx_1      /docker-entrypoint.sh ngin ...   Up      0.0.0.0:80->80/tcp    
myapp_redis_1      docker-entrypoint.sh redis ...   Up      6379/tcp              
myapp_web_1        gunicorn --bind 0.0.0.0:8000     Up      8000/tcp              

# 查看服务日志
$ docker-compose logs web
Attaching to myapp_web_1
web_1       | [2023-12-07 11:45:23 +0000] [1] [INFO] Starting gunicorn 20.1.0
web_1       | [2023-12-07 11:45:23 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
web_1       | [2023-12-07 11:45:23 +0000] [1] [INFO] Using worker: sync
web_1       | [2023-12-07 11:45:23 +0000] [8] [INFO] Booting worker with pid: 8

# 执行服务命令
$ docker-compose exec web python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK

# 扩展服务实例
$ docker-compose up -d --scale web=3
myapp_redis_1 is up-to-date
myapp_database_1 is up-to-date
myapp_nginx_1 is up-to-date
Starting myapp_web_1 ... done
Creating myapp_web_2 ... done
Creating myapp_web_3 ... done

# 停止并删除所有服务
$ docker-compose down
Stopping myapp_nginx_1    ... done
Stopping myapp_web_1      ... done
Stopping myapp_database_1 ... done
Stopping myapp_redis_1    ... done
Removing myapp_nginx_1    ... done
Removing myapp_web_1      ... done
Removing myapp_database_1 ... done
Removing myapp_redis_1    ... done
Removing network myapp_default
Removing volume myapp_db-data
```

### 内容解析
- **服务创建**: 显示网络、卷和服务容器的创建过程
- **状态信息**: 显示各服务的运行状态和端口映射
- **日志输出**: 显示服务启动和运行期间的日志
- **扩展操作**: 显示服务实例的扩缩容过程

### 常用参数详解
- `up -d`: 后台启动所有服务
- `ps`: 显示服务状态
- `logs <service>`: 查看指定服务日志
- `exec <service> <command>`: 在服务中执行命令
- `scale <service>=<count>`: 扩展服务实例数
- `down`: 停止并删除所有服务

### 注意事项
- Compose文件应使用版本控制管理
- 生产环境建议使用Swarm或Kubernetes
- 合理配置服务间的依赖关系
- 定期备份重要数据卷

### 安全风险
- ⚠️ Compose文件可能包含敏感配置信息
- ⚠️ 服务间网络通信可能缺乏安全控制
- ⚠️ 默认配置可能存在安全漏洞
- ⚠️ 端口暴露可能带来网络安全风险

## 8. docker system (系统管理)

### 用途
`docker system` 用于管理Docker系统资源，包括清理未使用的数据、查看磁盘使用情况等。

### 输出示例
```bash
# 查看磁盘使用情况
$ docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          25        8         5.234GB   3.124GB (59%)
Containers      12        8         1.045GB   234MB (22%)
Local Volumes   6         4         2.345GB   890MB (38%)
Build Cache     0         0         0B        0B

# 详细磁盘使用情况
$ docker system df -v
Images space usage:

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE                SHARED SIZE         UNIQUE SIZE         CONTAINERS
nginx               latest              605c77e624dd        2 weeks ago         141MB               0B                  141MB               1
redis               7.0                 761a5b0e709d        3 weeks ago         113MB               0B                  113MB               1
python              3.9                 9141382ff9da        4 weeks ago         917MB               917MB               0B                  3
ubuntu              22.04               58db3edaf2be        2 months ago        77.8MB              0B                  77.8MB              0

# 清理未使用的数据
$ docker system prune
WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - all dangling build cache

Are you sure you want to continue? [y/N] y
Deleted Containers:
a1b2c3d4e5f6789012345678901234567890abcd
b2c3d4e5f6789012345678901234567890abcde

Deleted Networks:
myapp_default

Deleted Images:
untagged: my-old-app:latest
deleted: sha256:c3d4e5f678901234567890123456789012345678901234567890123456789012

Total reclaimed space: 234.5MB

# 清理所有未使用数据（包括未使用的镜像）
$ docker system prune -a
WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all images without at least one container associated to them
  - all build cache

Are you sure you want to continue? [y/N] y
Deleted Images:
untagged: old-image:latest
untagged: unused-image:v1.0
deleted: sha256:d4e5f67890123456789012345678901234567890123456789012345678901234
deleted: sha256:e5f6789012345678901234567890123456789012345678901234567890123456

Total reclaimed space: 1.234GB

# 查看事件日志
$ docker system events --since 1h
2023-12-07T12:15:23.456789012Z container create a1b2c3d4e5f6789012345678901234567890abcd (image=nginx:latest, name=web-server)
2023-12-07T12:15:24.123456789Z container start a1b2c3d4e5f6789012345678901234567890abcd (image=nginx:latest, name=web-server)
2023-12-07T12:20:45.987654321Z container die a1b2c3d4e5f6789012345678901234567890abcd (exitCode=0, image=nginx:latest, name=web-server)
```

### 内容解析
- **磁盘使用统计**: 显示镜像、容器、卷和构建缓存的空间占用
- **详细使用情况**: 列出每个镜像的具体使用情况
- **清理操作**: 显示被删除的资源和回收的空间
- **事件日志**: 显示Docker系统的事件记录

### 常用参数详解
- `df`: 显示磁盘使用情况统计
- `df -v`: 显示详细的磁盘使用情况
- `prune`: 清理未使用的数据
- `prune -a`: 清理所有未使用的数据（包括镜像）
- `events`: 显示系统事件日志
- `info`: 显示系统详细信息

### 注意事项
- 定期执行清理操作释放磁盘空间
- 清理前确认不会影响正在运行的服务
- 重要的镜像和数据应做好备份
- 监控磁盘使用情况避免空间不足

### 安全风险
- ⚠️ 清理操作可能误删重要数据
- ⚠️ 事件日志可能包含敏感操作记录
- ⚠️ 系统信息暴露可能带来安全风险
- ⚠️ 未授权的清理操作可能影响服务运行

---

**总结**: 以上是容器技术常用的CLI工具详解。在生产环境中使用这些工具时，务必注意安全配置、资源管理和数据保护，确保容器化应用的稳定性和安全性。