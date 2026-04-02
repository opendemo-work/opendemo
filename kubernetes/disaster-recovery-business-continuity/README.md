# Disaster Recovery & Business Continuity

K8s灾难恢复与业务连续性方案演示。

## DR策略

```
灾难恢复架构:
┌────────────────────────┐      ┌────────────────────────┐
│      Primary Cluster    │      │    DR Cluster         │
│     (Region A)          │◄────►│    (Region B)         │
│                         │ 复制  │                       │
├────────────────────────┤      ├────────────────────────┤
│ ┌────────────────────┐ │      │ ┌────────────────────┐ │
│ │  Velero Backups    │ │─────►│ │  Velero Restore    │ │
│ └────────────────────┘ │      │ └────────────────────┘ │
│ ┌────────────────────┐ │      │ ┌────────────────────┐ │
│ │  DRDB Replication  │ │─────►│ │  DRDB Standby      │ │
│ └────────────────────┘ │      │ └────────────────────┘ │
└────────────────────────┘      └────────────────────────┘
```

## 关键措施

```bash
# 跨区域备份
velero backup create dr-backup \
  --volume-snapshot-locations aws-east \
  --storage-location aws-s3-east

# 应用级健康检查
kubectl apply -f - <<EOF
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: app-canary
spec:
  analysis:
    interval: 30s
    threshold: 5
    webhooks:
    - name: load-test
      url: http://flagger-loadtester.test/
EOF
```

## 学习要点

1. RPO/RTO设计
2. 跨区域复制
3. 自动故障转移
4. 恢复演练
