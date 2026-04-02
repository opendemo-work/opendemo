# BGP Routing

BGP边界网关协议演示，展示互联网核心路由协议。

## BGP基础

```
BGP对等体关系:
┌─────────┐         ┌─────────┐
│  AS100  │◄───────►│  AS200  │
│ (ISP A) │   eBGP  │ (ISP B) │
└────┬────┘         └────┬────┘
     │                   │
     │  ┌─────────────┐  │
     └──┤  AS300      ├──┘
        │ (Enterprise)│
        └─────────────┘
```

## 基本配置

```bash
# 安装BIRD
sudo apt install bird2

# 配置 /etc/bird/bird.conf
router id 192.168.1.1;

protocol bgp {
    local as 65001;
    neighbor 192.168.1.2 as 65002;
    
    ipv4 {
        import all;
        export filter {
            if net ~ 10.0.0.0/8 then accept;
            reject;
        };
    };
}
```

## 常用命令

```bash
# 查看BGP状态
sudo birdc show protocols

# 查看路由表
sudo birdc show route

# 查看BGP邻居
sudo birdc show protocols all bgp1
```
