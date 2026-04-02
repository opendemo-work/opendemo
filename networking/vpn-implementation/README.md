# VPN Implementation

VPN实现方案演示，包括WireGuard、OpenVPN、IPsec配置。

## VPN类型对比

| 类型 | 协议 | 特点 | 适用场景 |
|------|------|------|----------|
| WireGuard | UDP | 现代、简洁、高性能 | 现代部署首选 |
| OpenVPN | TCP/UDP | 成熟、功能丰富 | 企业环境 |
| IPsec/L2TP | ESP/IKE | 原生支持 | 兼容性要求高 |
| SSL VPN | HTTPS | 无需客户端 | 远程访问 |

## WireGuard快速配置

```bash
# 安装
sudo apt install wireguard

# 生成密钥
wg genkey | tee privatekey | wg pubkey > publickey

# 服务端配置 /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.0.0.2/32

# 启动
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

## OpenVPN配置

```bash
# 安装easy-rsa
sudo apt install openvpn easy-rsa

# 初始化PKI
make-cadir ~/openvpn-ca
cd ~/openvpn-ca
./easyrsa init-pki
./easyrsa build-ca
./easyrsa gen-req server nopass
./easyrsa sign-req server server
./easyrsa gen-dh

# 生成客户端证书
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1
```

## 测试连接

```bash
# 查看状态
sudo wg show

# 检查路由
ip route | grep wg

# 测试连通性
ping 10.0.0.1
```
