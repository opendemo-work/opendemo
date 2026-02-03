# 🏢 私有镜像仓库和Harbor部署实战

> 企业级容器镜像管理解决方案：Harbor私有仓库部署、镜像安全扫描、镜像复制等完整镜像管理实践

## 📋 案例概述

本案例详细介绍私有镜像仓库的部署和管理，重点讲解Harbor企业级镜像仓库的完整配置和运维实践。

### 🔧 核心技能点

- **Harbor部署配置**: Helm部署、高可用配置、存储优化
- **镜像安全管理**: 漏洞扫描、镜像签名、访问控制
- **镜像复制同步**: 跨地域镜像复制、同步策略配置
- **用户权限管理**: LDAP集成、项目权限、角色分配
- **性能优化调优**: 存储优化、缓存配置、负载均衡
- **监控告警体系**: Harbor监控、日志收集、健康检查

### 🎯 适用人群

- 容器平台管理员
- DevOps工程师
- 镜像仓库运维人员
- 安全合规专员

---

## 🚀 核心内容

### 1. Harbor Helm部署

```yaml
# values.yaml配置
expose:
  type: ingress
  tls:
    enabled: true
  ingress:
    hosts:
      core: harbor.example.com
      notary: notary.example.com

externalURL: https://harbor.example.com

persistence:
  enabled: true
  resourcePolicy: "keep"
  persistentVolumeClaim:
    registry:
      size: 100Gi
    chartmuseum:
      size: 20Gi
    jobservice:
      size: 10Gi
    database:
      size: 50Gi
    redis:
      size: 10Gi
    trivy:
      size: 20Gi

# 安全扫描配置
trivy:
  enabled: true
  gitHubToken: ""
  skipUpdate: false
```

### 2. 镜像复制配置

```yaml
apiVersion: goharbor.io/v1alpha1
kind: ReplicationPolicy
metadata:
  name: production-sync
spec:
  name: Production Sync Policy
  enabled: true
  srcRegistry:
    id: 1
  destRegistry:
    id: 2
  trigger:
    type: scheduled
    triggerSettings:
      cron: "0 2 * * *"
  filters:
  - type: name
    value: "library/**"
  - type: tag
    value: "v*"
  destNamespace: "sync-library"
  override: true
```

---

## 📋 完整案例文件

包含以下核心内容：
- Harbor完整部署方案
- 镜像安全扫描配置
- 跨地域镜像复制
- 用户权限管理系统
- 性能优化和调优
- 监控告警体系搭建

---