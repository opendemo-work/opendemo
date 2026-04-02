# TPM Security

可信平台模块(TPM)安全实践演示。

## TPM概述

```
TPM架构:
┌─────────────────────────────────────────────────────────┐
│                    应用程序                              │
├─────────────────────────────────────────────────────────┤
│                   TPM Software Stack                    │
│              (TSS - TCG Software Stack)                 │
├─────────────────────────────────────────────────────────┤
│                   TPM Driver                            │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │              TPM Hardware                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │  RSA    │ │  ECC    │ │  SHA    │          │   │
│  │  │Engine   │ │Engine   │ │Engine   │          │   │
│  │  └─────────┘ └─────────┘ └─────────┘          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │  PCR    │ │Key Slots│ │ NVRAM   │          │   │
│  │  │(Platform│ │(持久密钥)│ │(安全存储)│          │   │
│  │  │ Config) │ │         │ │         │          │   │
│  │  └─────────┘ └─────────┘ └─────────┘          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## TPM版本对比

| 特性 | TPM 1.2 | TPM 2.0 |
|------|---------|---------|
| 算法 | 仅RSA/SHA1 | RSA/ECC/SHA256+ |
| 授权 | 单一授权 | 灵活授权策略 |
| 密钥 | 固定层级 | 灵活密钥管理 |
| 哈希 | SHA1 | SHA256/SHA384/SHA512 |

## 检查与初始化

```bash
# 检查TPM存在
dmesg | grep -i tpm
ls /dev/tpm*

# 检查TPM 2.0
cat /sys/class/tpm/tpm0/tpm_version_major
# 输出: 2

# 安装工具
sudo apt install tpm2-tools tpm2-abrmd

# 查看TPM信息
tpm2_getcap properties-fixed
tpm2_getcap algorithms
```

## 密钥密封与解封

```bash
# 创建密封密钥 (与PCR状态绑定)
# PCR 0-7: BIOS/UEFI/Bootloader状态
# PCR 8-15: 内核和模块状态

# 查看当前PCR状态
tpm2_pcrread

# 创建策略 (绑定PCR 0-7)
tpm2_createpolicy --policy-pcr -l sha256:0,1,2,3,4,5,6,7 \
  -L policy.pcr

# 创建密封对象
tpm2_createprimary -C o -g sha256 -G rsa \
  -c primary.ctx

tpm2_create -C primary.ctx -g sha256 \
  -u seal.pub -r seal.priv \
  -L policy.pcr \
  -i secret_data.txt \
  -c seal.ctx

# 解封 (需要相同PCR状态)
tpm2_unseal -c seal.ctx -p pcr:sha256:0,1,2,3,4,5,6,7
```

## LUKS+TPM自动解锁

```bash
# 配置TPM自动解锁LUKS (免密码启动)

# 1. 安装工具
sudo apt install clevis clevis-tpm2 clevis-luks

# 2. 绑定TPM到LUKS
clevis luks bind -d /dev/sdb tpm2 \
  '{"pcr_ids":"0,1,2,3,4,5,6,7"}'

# 3. 验证绑定
cryptsetup luksDump /dev/sdb
# 应显示额外的密钥槽

# 4. 测试自动解锁
# 重启后，如果PCR状态匹配，自动解密

# 5. 添加恢复密钥 (防TPM故障)
clevis luks regen -d /dev/sdb -s 0
```

## 测量启动 (Measured Boot)

```bash
# 查看PCR测量值
tpm2_pcrread sha256:0,1,2,3

# PCR 0: BIOS/UEFI固件
# PCR 1: BIOS配置
# PCR 2: 扩展固件
# PCR 3: 扩展固件配置
# PCR 4: Boot Manager
# PCR 5: GPT分区表
# PCR 6: 恢复/调试状态
# PCR 7: 安全启动策略

# 扩展PCR (手动测量)
echo "data to measure" | \
  tpm2_pcrextend 9:sha256=$(cat | sha256sum | cut -d' ' -f1)
```

## 学习要点

1. TPM 1.2 vs TPM 2.0差异
2. PCR测量与密封存储
3. LUKS+TPM自动解锁
4. 安全启动链验证
5. 密钥生命周期管理
