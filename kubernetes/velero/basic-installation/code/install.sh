#!/bin/bash
# Velero基础安装脚本
# 用途：一键安装MinIO和Velero到Kubernetes集群

set -e

echo "========================================="
echo "  Velero基础安装脚本"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查前置条件
echo "步骤1: 检查前置条件..."
command -v kubectl >/dev/null 2>&1 || { echo -e "${RED}错误: kubectl未安装${NC}"; exit 1; }
command -v helm >/dev/null 2>&1 || { echo -e "${RED}错误: helm未安装${NC}"; exit 1; }
echo -e "${GREEN}✓ kubectl和helm已安装${NC}"

# 检查集群连接
kubectl cluster-info >/dev/null 2>&1 || { echo -e "${RED}错误: 无法连接到Kubernetes集群${NC}"; exit 1; }
echo -e "${GREEN}✓ Kubernetes集群连接正常${NC}"
echo ""

# 创建namespace
echo "步骤2: 创建velero命名空间..."
kubectl create namespace velero --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace已创建或已存在${NC}"
echo ""

# 部署MinIO
echo "步骤3: 部署MinIO对象存储..."
kubectl apply -f minio-deployment.yaml
kubectl apply -f minio-service.yaml
echo -e "${GREEN}✓ MinIO部署文件已应用${NC}"

echo "等待MinIO Pod就绪（最长120秒）..."
kubectl wait --for=condition=Ready pod -l app=minio -n velero --timeout=120s
echo -e "${GREEN}✓ MinIO Pod已就绪${NC}"

# 验证MinIO服务
echo ""
echo "验证MinIO服务状态..."
kubectl get pods -n velero -l app=minio
kubectl get svc -n velero -l app=minio
echo ""

# 创建MinIO bucket (使用kubectl exec)
echo "步骤4: 创建MinIO bucket..."
MINIO_POD=$(kubectl get pods -n velero -l app=minio -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n velero $MINIO_POD -- sh -c "mkdir -p /data/velero" 2>/dev/null || true
echo -e "${GREEN}✓ MinIO bucket已创建${NC}"
echo ""

# 添加Velero Helm仓库
echo "步骤5: 添加Velero Helm仓库..."
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts 2>/dev/null || true
helm repo update
echo -e "${GREEN}✓ Helm仓库已更新${NC}"
echo ""

# 安装Velero
echo "步骤6: 安装Velero..."
helm install velero vmware-tanzu/velero \
  --namespace velero \
  --values velero-values.yaml \
  --wait \
  --timeout 5m
echo -e "${GREEN}✓ Velero已安装${NC}"
echo ""

# 等待Velero Pod就绪
echo "等待Velero Pod就绪..."
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=velero -n velero --timeout=120s
echo -e "${GREEN}✓ Velero Pod已就绪${NC}"
echo ""

# 验证安装
echo "========================================="
echo "  验证安装结果"
echo "========================================="
echo ""

echo "1. Pod状态:"
kubectl get pods -n velero
echo ""

echo "2. BackupStorageLocation状态:"
kubectl get backupstoragelocation -n velero
echo ""

# 检查velero CLI
if command -v velero >/dev/null 2>&1; then
    echo "3. Velero版本信息:"
    velero version
    echo ""
    
    echo "4. Backup Storage Location详细信息:"
    velero backup-location get
    echo ""
else
    echo -e "${YELLOW}⚠ Velero CLI未安装，请参考README安装CLI工具${NC}"
    echo ""
fi

# 安装完成
echo "========================================="
echo -e "${GREEN}  ✅ Velero安装完成！${NC}"
echo "========================================="
echo ""
echo "后续步骤:"
echo "1. 验证BackupStorageLocation状态为Available"
echo "2. 创建测试备份: velero backup create test-backup --include-namespaces velero"
echo "3. 查看备份列表: velero backup get"
echo "4. 查看Demo完整文档: 参考README.md"
echo ""
echo "如需卸载Velero:"
echo "  helm uninstall velero -n velero"
echo "  kubectl delete namespace velero"
echo ""
