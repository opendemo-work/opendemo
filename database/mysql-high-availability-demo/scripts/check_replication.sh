#!/usr/bin/env bash
# 检查 MySQL 主从复制状态

set -euo pipefail

echo "=========================================="
echo "MySQL 主从复制状态检查"
echo "=========================================="

if ! docker ps | grep -q mysql-master; then
    echo "❌ mysql-master 容器未运行，请先执行 setup_replication.sh"
    exit 1
fi

if ! docker ps | grep -q mysql-slave; then
    echo "❌ mysql-slave 容器未运行，请先执行 setup_replication.sh"
    exit 1
fi

echo ""
echo "--- 主库状态 ---"
docker exec mysql-master mysql -uroot -prootpass -e "SHOW MASTER STATUS\G"

echo ""
echo "--- 从库 IO/SQL 线程状态 ---"
docker exec mysql-slave mysql -uroot -prootpass -e "SHOW REPLICA STATUS\G" | grep -E "Replica_IO_Running|Replica_SQL_Running|Last_Error|Source_Host|Source_Port"

echo ""
echo "--- 主从数据一致性测试 ---"
docker exec mysql-master mysql -uroot -prootpass -e "CREATE TABLE IF NOT EXISTS demo.ha_test (id INT PRIMARY KEY, name VARCHAR(50)); INSERT INTO demo.ha_test VALUES (1, 'master_write') ON DUPLICATE KEY UPDATE name='master_write';"
sleep 2
docker exec mysql-slave mysql -uroot -prootpass -e "SELECT * FROM demo.ha_test;"

echo ""
echo "✅ 检查完成"
