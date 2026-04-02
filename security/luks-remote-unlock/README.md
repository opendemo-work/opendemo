# LUKS Remote Unlock

LUKS远程解锁与Dropbear initramfs实践。

## 场景需求

```
远程解锁场景:
┌─────────────────────────────────────────────────────────┐
│                    数据中心                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │           加密服务器 (无显示器/键盘)              │   │
│  │                                                 │   │
│  │  ┌─────────────┐      ┌─────────────────────┐   │   │
│  │  │  Dropbear   │◄────►│   SSH连接 (远程)     │   │   │
│  │  │  (initramfs)│      │   输入解锁密码       │   │   │
│  │  └──────┬──────┘      └─────────────────────┘   │   │
│  │         │                                       │   │
│  │  ┌──────┴──────┐                                │   │
│  │  │  cryptsetup │                                │   │
│  │  │  luksOpen   │                                │   │
│  │  └─────────────┘                                │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 配置Dropbear

```bash
# 安装dropbear-initramfs
sudo apt install dropbear-initramfs

# 配置网络
# /etc/initramfs-tools/initramfs.conf
DEVICE=eth0
IP=192.168.1.100::192.168.1.1:255.255.255.0::eth0:off

# 或使用DHCP
IP=dhcp

# 配置dropbear
# /etc/dropbear-initramfs/config
DROPBEAR_OPTIONS="-I 300 -j -k -p 2222 -s"

# 添加SSH公钥
cat ~/.ssh/id_rsa.pub | \
  sudo tee /etc/dropbear-initramfs/authorized_keys

# 更新initramfs
sudo update-initramfs -u
```

## 解锁脚本

```bash
# /etc/initramfs-tools/scripts/local-top/unlock
#!/bin/sh
PREREQ=""
prereqs() {
    echo "$PREREQ"
}

case $1 in
prereqs)
    prereqs
    exit 0
    ;;
esac

. /scripts/functions

# 等待网络
wait_for_network() {
    while ! ip route | grep -q default; do
        sleep 1
    done
}

# 解锁函数
crypt_unlock() {
    if [ -f /lib/cryptsetup/askpass ]; then
        /lib/cryptsetup/askpass "Unlock password: " | \
          cryptsetup luksOpen /dev/sda3 root -
    fi
}

wait_for_network
```

## 远程解锁流程

```bash
# 1. 服务器重启，进入initramfs
# 2. 自动启动dropbear，监听2222端口

# 3. 远程连接
ssh -p 2222 root@192.168.1.100

# 4. 在initramfs环境中解锁
cryptroot-unlock
Enter passphrase: ********

# 或手动解锁
cryptsetup luksOpen /dev/sda3 root
# 然后退出SSH，系统继续启动

# 5. 系统正常启动后，SSH到正式系统
ssh admin@192.168.1.100
```

## 增强安全性

```bash
# 配置IP白名单
# /etc/dropbear-initramfs/config
DROPBEAR_OPTIONS="-I 300 -j -k -p 2222 -s -a"

# 仅允许特定IP (通过iptables)
iptables -A INPUT -p tcp --dport 2222 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 2222 -j DROP

# 使用证书认证 (禁用密码)
DROPBEAR_OPTIONS="-s -g -p 2222"
```

## 学习要点

1. initramfs工作流程
2. Dropbear轻量级SSH
3. 远程解锁安全加固
4. 网络配置与故障排查
