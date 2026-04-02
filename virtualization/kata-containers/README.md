# Kata Containers

Kata安全容器运行时演示。

## Kata vs Docker

```
Docker (runc):              Kata:
┌─────────┐                ┌─────────┐
│  App    │                │  App    │
├─────────┤                ├─────────┤
│ RunC    │                │ Agent   │
├─────────┤                ├─────────┤
│ Host    │                │  MiniOS │
│ Kernel  │                │ (VM)    │
└─────────┘                ├─────────┤
                           │  Host   │
                           │  Kernel │
                           └─────────┘
                            
安全性: 进程隔离           安全性: VM级隔离
启动速度: ~100ms           启动速度: ~300ms
```

## 安装配置

```bash
# 安装
sudo apt install kata-runtime kata-proxy kata-shim

# Docker配置
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "runtimes": {
    "kata-runtime": {
      "path": "/usr/bin/kata-runtime"
    }
  }
}
