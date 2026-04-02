# KVM Monitoring

KVM虚拟化环境监控方案演示。

## 监控架构

```
监控体系:
┌─────────────────────────────────────────────────────────┐
│                    Grafana Dashboard                    │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
┌─────────────────────┐   ┌─────────────────────┐
│   Prometheus        │   │   Libvirt Exporter  │
│   (指标存储)         │   │   (KVM指标)          │
└─────────────────────┘   └─────────────────────┘
              │                     │
              └──────────┬──────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Node       │ │   Domain     │ │   Network    │
│   Exporter   │ │   Metrics    │ │   Stats      │
└──────────────┘ └──────────────┘ └──────────────┘
```

## libvirt_exporter

```bash
# 安装
wget https://github.com/kumina/libvirt_exporter/releases/latest/download/libvirt_exporter
cp libvirt_exporter /usr/local/bin/

# 启动
libvirt_exporter --web.listen-address=:9177

# Prometheus配置
scrape_configs:
  - job_name: 'libvirt'
    static_configs:
      - targets: ['localhost:9177']
```

## 关键指标

```promql
# 虚拟机CPU使用率
libvirt_domain_info_cpu_time / 1e9

# 内存使用率
libvirt_domain_memory_stats_used / libvirt_domain_memory_stats_usable * 100

# 磁盘I/O
rate(libvirt_domain_block_stats_read_bytes[5m])
rate(libvirt_domain_block_stats_write_bytes[5m])

# 网络流量
rate(libvirt_domain_interface_stats_receive_bytes[5m])
```

## 告警规则

```yaml
groups:
  - name: kvm_alerts
    rules:
      - alert: VMHighCPU
        expr: libvirt_domain_info_cpu_time / 1e9 > 80
        for: 5m
        annotations:
          summary: "VM {{ $labels.domain }} CPU high"
      
      - alert: VMDown
        expr: libvirt_domain_info_state{state="running"} == 0
        for: 1m
        annotations:
          summary: "VM {{ $labels.domain }} is down"
```
