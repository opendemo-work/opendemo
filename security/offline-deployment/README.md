# Offline Deployment

离线环境FDE部署方案演示。

## 离线部署挑战

```
离线部署场景:
┌─────────────────────────────────────────────────────────┐
│ 场景1: 隔离网络 (政府/金融/军工)                          │
│ ├── 无互联网连接                                          │
│ ├── 无法使用云KMS                                         │
│ └── 需要本地密钥管理                                       │
├─────────────────────────────────────────────────────────┤
│ 场景2: 远程站点 (海上平台/矿山)                          │
│ ├── 带宽受限                                              │
│ ├── 延迟高                                                │
│ └── 需要本地自治能力                                       │
├─────────────────────────────────────────────────────────┤
│ 场景3: 安全实验室                                         │
│ ├── 物理隔离                                              │
│ ├── 无外部服务依赖                                        │
│ └── 需要完全离线方案                                       │
└─────────────────────────────────────────────────────────┘
```

## 离线部署架构

```
离线部署组件:
┌─────────────────────────────────────────────────────────┐
│              离线部署服务器 (预配置)                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │  • 本地密钥管理服务 (Vault/HSM)                  │   │
│  │  • 软件仓库镜像                                  │   │
│  │  • 部署脚本和工具                                │   │
│  │  • 恢复密钥数据库                                │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    目标设备 (离线)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 安装介质    │  │ 密钥注入    │  │ 状态报告    │     │
│  │ (USB/DVD)  │  │ (Token/HSM) │  │ (USB导出)   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 本地Vault部署

```bash
# 1. 准备离线Vault服务器
# 下载Vault二进制文件和依赖

# 2. 配置本地Vault
cat > vault-offline.hcl << 'EOF'
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = true  # 内部网络，或配置本地证书
}

api_addr = "http://127.0.0.1:8200"
disable_mlock = true
EOF

# 3. 启动Vault
vault server -config=vault-offline.hcl &

# 4. 初始化 (仅一次)
export VAULT_ADDR='http://127.0.0.1:8200'
vault operator init -key-shares=5 -key-threshold=3 > vault-init.txt

# 5. 保存根令牌和解封密钥
ROOT_TOKEN=$(grep 'Initial Root Token' vault-init.txt | awk '{print $NF}')
export VAULT_TOKEN=$ROOT_TOKEN

# 6. 启用密钥引擎
vault secrets enable -path=recovery-keys kv-v2

# 7. 配置策略
cat > fde-policy.hcl << 'EOF'
path "recovery-keys/data/*" {
  capabilities = ["create", "read", "update", "delete"]
}
EOF

vault policy write fde-policy fde-policy.hcl
```

## 离线部署脚本

```python
#!/usr/bin/env python3
"""
FDE离线部署工具
"""
import os
import json
import subprocess
import hashlib
from pathlib import Path

class OfflineFDEDeployment:
    def __init__(self, config_file: str):
        with open(config_file) as f:
            self.config = json.load(f)
        
        self.offline_repo = Path(self.config['offline_repo_path'])
        self.key_token = Path(self.config['key_token_path'])
        
    def prepare_offline_media(self):
        """准备离线安装介质"""
        print("Preparing offline installation media...")
        
        # 创建目录结构
        media_dir = Path('/mnt/offline-fde-media')
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制必要的软件包
        packages = [
            'cryptsetup',
            'cryptsetup-initramfs',
            'tpm2-tools',
            'clevis'
        ]
        
        for pkg in packages:
            self.download_package(pkg, media_dir / 'packages')
        
        # 复制部署脚本
        self.copy_deployment_scripts(media_dir / 'scripts')
        
        # 生成离线密钥包
        self.generate_key_bundle(media_dir / 'keys')
        
        print(f"Offline media prepared at: {media_dir}")
        return media_dir
    
    def download_package(self, package: str, dest_dir: Path):
        """下载软件包及依赖"""
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # 使用apt-offline或手动下载
        subprocess.run([
            'apt-get', 'download',
            '--allow-downgrades',
            '-o', 'Dir::Cache::Archives=' + str(dest_dir),
            package
        ], check=True)
    
    def generate_key_bundle(self, dest_dir: Path):
        """生成离线密钥包"""
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成本地恢复密钥
        key = os.urandom(32)
        key_hash = hashlib.sha256(key).hexdigest()
        
        # 加密存储
        with open(dest_dir / 'recovery-key.enc', 'wb') as f:
            f.write(key)
        
        with open(dest_dir / 'key-checksum.txt', 'w') as f:
            f.write(key_hash)
        
        print(f"Key bundle generated: {key_hash[:16]}...")
    
    def install_from_offline_media(self, media_path: Path):
        """从离线介质安装"""
        print("Installing FDE from offline media...")
        
        # 1. 安装软件包
        packages_dir = media_path / 'packages'
        subprocess.run([
            'dpkg', '-i', 
            str(packages_dir / '*.deb')
        ], shell=True, check=True)
        
        # 2. 修复依赖
        subprocess.run(['apt-get', 'install', '-f', '-y'], check=True)
        
        # 3. 配置LUKS
        self.configure_luks_offline(media_path / 'keys')
        
        print("Offline installation complete")
    
    def configure_luks_offline(self, keys_dir: Path):
        """离线配置LUKS"""
        # 读取离线密钥
        with open(keys_dir / 'recovery-key.enc', 'rb') as f:
            recovery_key = f.read()
        
        # 配置加密 (使用本地密钥，不依赖云服务)
        device = self.config['target_device']
        
        # 创建LUKS容器
        subprocess.run([
            'cryptsetup', 'luksFormat',
            '--type', 'luks2',
            '--cipher', 'aes-xts-plain64',
            '--key-size', '512',
            '--batch-mode',
            device
        ], input=recovery_key.hex(), text=True, check=True)
        
        # 配置自动解锁 (使用本地TPM或密钥文件)
        self.configure_offline_unlock(device, recovery_key)
    
    def configure_offline_unlock(self, device: str, key: bytes):
        """配置离线自动解锁"""
        # 方案1: 使用本地密钥文件 (需要安全存储)
        keyfile_path = '/root/.luks-keyfile'
        with open(keyfile_path, 'wb') as f:
            f.write(key)
        os.chmod(keyfile_path, 0o600)
        
        # 添加密钥槽
        subprocess.run([
            'cryptsetup', 'luksAddKey',
            device, keyfile_path
        ], input=key.hex(), text=True, check=True)
        
        # 配置crypttab
        with open('/etc/crypttab', 'a') as f:
            f.write(f"secure-disk UUID=$(blkid -s UUID -o value {device}) {keyfile_path} luks\n")

# 使用示例
if __name__ == "__main__":
    deployment = OfflineFDEDeployment('offline-config.json')
    
    # 准备介质
    media = deployment.prepare_offline_media()
    
    # 安装
    deployment.install_from_offline_media(media)
```

## 离线配置清单

```yaml
# 离线部署要求
offline_requirements:
  infrastructure:
    - 本地密钥管理服务 (Vault/HSM)
    - 离线软件仓库
    - 部署工作站
    
  media:
    - USB 3.0+ 驱动器 (16GB+)
    - 或 DVD-R (如果适用)
    - 写保护开关 (推荐)
    
  security:
    - 物理介质加密
    - 传输中的介质保护
    - 密钥分发安全
    
  documentation:
    - 离线部署手册
    - 故障排除指南
    - 紧急联系信息
```

## 学习要点

1. 离线部署架构设计
2. 本地密钥管理
3. 离线介质准备
4. 安全传输考虑
5. 无网络环境运维
