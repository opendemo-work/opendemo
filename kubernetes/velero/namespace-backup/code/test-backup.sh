#!/bin/bash
# 命名空间备份与恢复自动化测试脚本

set -e

echo "========================================="
echo "  Velero命名空间备份演示"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 步骤1: 创建示例应用
echo "步骤1: 创建nginx示例应用..."
kubectl apply -f sample-app.yaml
echo -e "${GREEN}✓ 应用已部署${NC}"

# 等待Pod就绪
echo "等待Pod就绪..."
kubectl wait --for=condition=Ready pod -l app=nginx -n nginx-example --timeout=60s
echo -e "${GREEN}✓ Pod已就绪${NC}"
echo ""

# 步骤2: 验证应用运行
echo "步骤2: 验证应用状态..."
kubectl get pods -n nginx-example
kubectl get svc -n nginx-example
echo ""

# 步骤3: 创建备份
echo "步骤3: 创建命名空间备份..."
velero backup create nginx-backup --include-namespaces nginx-example --wait
echo -e "${GREEN}✓ 备份已完成${NC}"
echo ""

# 查看备份详情
echo "备份详细信息:"
velero backup describe nginx-backup --details
echo ""

# 步骤4: 删除命名空间模拟灾难
echo "步骤4: 删除命名空间（模拟灾难）..."
kubectl delete namespace nginx-example
echo -e "${YELLOW}⚠ 命名空间已删除${NC}"
echo ""

# 等待命名空间完全删除
echo "等待命名空间完全删除..."
while kubectl get namespace nginx-example 2>/dev/null; do
  echo "等待中..."
  sleep 2
done
echo -e "${GREEN}✓ 命名空间已完全删除${NC}"
echo ""

# 步骤5: 从备份恢复
echo "步骤5: 从备份恢复..."
velero restore create --from-backup nginx-backup --wait
echo -e "${GREEN}✓ 恢复已完成${NC}"
echo ""

# 步骤6: 验证恢复结果
echo "步骤6: 验证恢复结果..."
kubectl get namespace nginx-example
kubectl get pods -n nginx-example
kubectl get svc -n nginx-example
kubectl get configmap -n nginx-example

# 等待Pod重新就绪
echo ""
echo "等待恢复后的Pod就绪..."
kubectl wait --for=condition=Ready pod -l app=nginx -n nginx-example --timeout=120s
echo -e "${GREEN}✓ 恢复验证成功！${NC}"
echo ""

# 步骤7: 验证ConfigMap数据
echo "步骤7: 验证ConfigMap数据完整性..."
kubectl get configmap nginx-config -n nginx-example -o yaml | grep "Velero Backup Demo"
echo -e "${GREEN}✓ ConfigMap数据一致${NC}"
echo ""

# 清理
echo "========================================="
echo "  清理测试资源"
echo "========================================="
echo ""
echo "删除备份..."
velero backup delete nginx-backup --confirm
echo ""
echo "删除命名空间..."
kubectl delete namespace nginx-example
echo ""
echo -e "${GREEN}✅ 测试完成并清理成功！${NC}"
#!/bin/bash
# 命名空间备份与恢复自动化测试脚本

set -e

echo "========================================="
echo "  Velero命名空间备份演示"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 步骤1: 创建示例应用
echo "步骤1: 创建nginx示例应用..."
kubectl apply -f sample-app.yaml
echo -e "${GREEN}✓ 应用已部署${NC}"

# 等待Pod就绪
echo "等待Pod就绪..."
kubectl wait --for=condition=Ready pod -l app=nginx -n nginx-example --timeout=60s
echo -e "${GREEN}✓ Pod已就绪${NC}"
echo ""

# 步骤2: 验证应用运行
echo "步骤2: 验证应用状态..."
kubectl get pods -n nginx-example
kubectl get svc -n nginx-example
echo ""

# 步骤3: 创建备份
echo "步骤3: 创建命名空间备份..."
velero backup create nginx-backup --include-namespaces nginx-example --wait
echo -e "${GREEN}✓ 备份已完成${NC}"
echo ""

# 查看备份详情
echo "备份详细信息:"
velero backup describe nginx-backup --details
echo ""

# 步骤4: 删除命名空间模拟灾难
echo "步骤4: 删除命名空间（模拟灾难）..."
kubectl delete namespace nginx-example
echo -e "${YELLOW}⚠ 命名空间已删除${NC}"
echo ""

# 等待命名空间完全删除
echo "等待命名空间完全删除..."
while kubectl get namespace nginx-example 2>/dev/null; do
  echo "等待中..."
  sleep 2
done
echo -e "${GREEN}✓ 命名空间已完全删除${NC}"
echo ""

# 步骤5: 从备份恢复
echo "步骤5: 从备份恢复..."
velero restore create --from-backup nginx-backup --wait
echo -e "${GREEN}✓ 恢复已完成${NC}"
echo ""

# 步骤6: 验证恢复结果
echo "步骤6: 验证恢复结果..."
kubectl get namespace nginx-example
kubectl get pods -n nginx-example
kubectl get svc -n nginx-example
kubectl get configmap -n nginx-example

# 等待Pod重新就绪
echo ""
echo "等待恢复后的Pod就绪..."
kubectl wait --for=condition=Ready pod -l app=nginx -n nginx-example --timeout=120s
echo -e "${GREEN}✓ 恢复验证成功！${NC}"
echo ""

# 步骤7: 验证ConfigMap数据
echo "步骤7: 验证ConfigMap数据完整性..."
kubectl get configmap nginx-config -n nginx-example -o yaml | grep "Velero Backup Demo"
echo -e "${GREEN}✓ ConfigMap数据一致${NC}"
echo ""

# 清理
echo "========================================="
echo "  清理测试资源"
echo "========================================="
echo ""
echo "删除备份..."
velero backup delete nginx-backup --confirm
echo ""
echo "删除命名空间..."
kubectl delete namespace nginx-example
echo ""
echo -e "${GREEN}✅ 测试完成并清理成功！${NC}"
