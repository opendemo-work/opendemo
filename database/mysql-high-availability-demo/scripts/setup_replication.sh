#!/usr/bin/env bash
# MySQL 主从复制配置脚本（基于 Docker Compose 环境）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=========================================="
echo "MySQL 主从复制一键配置"
echo "=========================================="

# 1. 启动容器
echo "[1/5] 启动 MySQL 主从容器..."
docker-compose up -d

# 2. 等待主库就绪
echo "[2/5] 等待主库就绪..."
until docker exec mysql-master mysqladmin ping -h localhost -uroot -prootpass --silent; do
    sleep 2
done

# 3. 创建复制用户
echo "[3/5] 在主库创建复制用户..."
docker exec -i mysql-master mysql -uroot -prootpass <<'EOF'
CREATE USER IF NOT EXISTS 'repl'@'%' IDENTIFIED WITH mysql_native_password BY 'replpass';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
EOF

# 4. 获取主库 GTID 位置（MySQL 8.0 使用 GTID）
echo "[4/5] 获取主库 GTID 状态..."
docker exec mysql-master mysql -uroot -prootpass -e "SHOW MASTER STATUS\G"

# 5. 配置从库
echo "[5/5] 配置从库连接主库..."
docker exec -i mysql-slave mysql -uroot -prootpass <<'EOF'
STOP REPLICA;
RESET REPLICA ALL;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-master',
    SOURCE_PORT=3306,
    SOURCE_USER='repl',
    SOURCE_PASSWORD='replpass',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF

# 6. 检查复制状态
echo ""
echo "=========================================="
echo "复制状态检查"
echo "=========================================="
sleep 3
docker exec mysql-slave mysql -uroot -prootpass -e "SHOW REPLICA STATUS\G" | grep -E "Replica_IO_Running|Replica_SQL_Running|Source_Host"

echo ""
echo "✅ 主从复制配置完成"
echo "主库连接: mysql -h127.0.0.1 -P3306 -uroot -prootpass"
echo "从库连接: mysql -h127.0.0.1 -P3307 -uroot -prootpass"
