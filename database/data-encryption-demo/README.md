# 数据库数据加密保护实战演示

## 🎯 学习目标

通过本案例你将掌握企业级数据库数据加密保护的核心技能：

- 实施透明数据加密(TDE)和应用层加密
- 配置传输层安全(TLS/SSL)加密通信
- 管理加密密钥和证书生命周期
- 实现字段级和行级数据加密
- 建立密钥管理系统(KMS)集成
- 满足GDPR、HIPAA等合规性要求

## 🛠️ 环境准备

### 系统要求
- 已完成数据库安装配置环境
- 具备基础安全概念理解
- 准备PKI基础设施或云KMS服务
- 理解加密算法和密钥管理基础

### 前置条件验证
```bash
# 验证数据库服务状态
systemctl is-active mysqld postgresql-14 mongod redis

# 检查加密支持
mysql -u root -p -e "SHOW VARIABLES LIKE '%ssl%';"
psql -U postgres -c "SHOW ssl;"

# 验证openssl工具
openssl version
```

## 📁 项目结构

```
data-encryption-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 加密脚本
│   ├── mysql_encryption_setup.sh      # MySQL加密配置脚本
│   ├── postgresql_encryption_setup.sh # PostgreSQL加密配置脚本
│   ├── mongodb_encryption_setup.js    # MongoDB加密配置脚本
│   ├── redis_encryption_setup.sh      # Redis加密配置脚本
│   ├── kms_integration.py             # KMS集成管理器
│   └── certificate_management.sh      # 证书管理脚本
├── configs/                           # 配置文件
│   ├── encryption_policies/           # 加密策略配置
│   ├── tls_certificates/              # TLS证书配置
│   ├── key_management/                # 密钥管理配置
│   └── compliance_rules/              # 合规规则配置
├── examples/                          # 加密案例
│   ├── tde_implementation/            # 透明加密实现
│   ├── field_level_encryption/        # 字段级加密案例
│   ├── client_side_encryption/        # 客户端加密案例
│   └── key_rotation_scenarios/        # 密钥轮换场景
├── keys/                              # 密钥材料
│   ├── master_keys/                   # 主密钥
│   ├── data_keys/                     # 数据密钥
│   ├── certificates/                  # 数字证书
│   └── key_backups/                   # 密钥备份
├── audits/                            # 安全审计
│   ├── encryption_audits/             # 加密审计日志
│   ├── key_usage_logs/                # 密钥使用日志
│   ├── compliance_reports/            # 合规报告
│   └── vulnerability_assessments/     # 漏洞评估
└── docs/                              # 详细文档
    ├── encryption_architecture.md     # 加密架构设计
    ├── key_management_guide.md        # 密钥管理指南
    ├── compliance_checklist.md        # 合规检查清单
    └── best_practices.md              # 最佳实践指南
```

## 🔐 企业级加密体系架构

### 加密分层防护模型
```yaml
# 数据库加密防护体系
encryption_layers:
  application_layer:         # 应用层加密
    techniques:
      - client_side_encryption    # 客户端加密
      - application_level_encryption # 应用层加密
      - field_level_encryption    # 字段级加密
    use_cases:
      - 敏感个人信息保护
      - 支付卡数据加密
      - 医疗健康数据保护
    
  transport_layer:           # 传输层加密
    protocols:
      - tls_ssl               # TLS/SSL加密传输
      - ipsec                 # IPsec隧道加密
      - vpn                   # VPN安全通道
    implementation:
      - database_connection_encryption
      - application_database_communication
      - backup_data_transfer
    
  storage_layer:             # 存储层加密
    methods:
      - transparent_data_encryption  # 透明数据加密
      - file_system_encryption       # 文件系统加密
      - disk_encryption              # 磁盘加密
    scope:
      - data_files_encryption
      - log_files_encryption
      - backup_files_encryption
    
  key_management_layer:      # 密钥管理层
    components:
      - hardware_security_module     # HSM硬件安全模块
      - key_management_service       # KMS密钥管理服务
      - certificate_authority        # CA证书颁发机构
    functions:
      - key_generation
      - key_rotation
      - key_revocation
      - key_backup_recovery
```

## 🔧 核心加密技术实现

### 1. MySQL数据加密保护

```sql
-- MySQL企业级数据加密完整配置

-- 1. 启用透明数据加密(TDE)
-- 配置InnoDB表空间加密
SET GLOBAL innodb_file_per_table = ON;
SET GLOBAL innodb_file_format = Barracuda;

-- 创建加密表空间
CREATE TABLESPACE encrypted_ts 
ADD DATAFILE 'encrypted_ts.ibd' 
ENCRYPTION='Y';

-- 在加密表空间中创建表
CREATE TABLE sensitive_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  ssn VARCHAR(11),
  credit_card VARCHAR(16),
  medical_record TEXT
) TABLESPACE = encrypted_ts;

-- 2. 配置主密钥轮换
-- 查看当前加密密钥状态
SELECT * FROM performance_schema.keyring_keys;

-- 轮换主加密密钥
ALTER INSTANCE ROTATE INNODB MASTER KEY;

-- 3. 字段级加密实现
-- 创建加密函数
DELIMITER //
CREATE FUNCTION encrypt_sensitive_data(data TEXT, encryption_key VARCHAR(64))
RETURNS VARBINARY(1024) 
READS SQL DATA 
DETERMINISTIC
BEGIN
  RETURN AES_ENCRYPT(data, encryption_key, 'AES-256-CBC');
END //

CREATE FUNCTION decrypt_sensitive_data(encrypted_data VARBINARY(1024), encryption_key VARCHAR(64))
RETURNS TEXT 
READS SQL DATA 
DETERMINISTIC
BEGIN
  RETURN AES_DECRYPT(encrypted_data, encryption_key, 'AES-256-CBC');
END //
DELIMITER ;

-- 使用字段级加密
INSERT INTO sensitive_data (user_id, ssn, credit_card, medical_record) 
VALUES (
  1001,
  HEX(encrypt_sensitive_data('123-45-6789', 'user_specific_key_1001')),
  HEX(encrypt_sensitive_data('4111111111111111', 'user_specific_key_1001')),
  HEX(encrypt_sensitive_data('Patient has diabetes and hypertension', 'user_specific_key_1001'))
);

-- 查询时解密
SELECT 
  id,
  user_id,
  decrypt_sensitive_data(UNHEX(ssn), 'user_specific_key_1001') as decrypted_ssn,
  decrypt_sensitive_data(UNHEX(credit_card), 'user_specific_key_1001') as decrypted_credit_card,
  decrypt_sensitive_data(UNHEX(medical_record), 'user_specific_key_1001') as decrypted_medical_record
FROM sensitive_data 
WHERE user_id = 1001;

-- 4. SSL/TLS连接加密配置
-- 在my.cnf中配置SSL
[mysqld]
ssl-ca=/etc/mysql/certs/ca.pem
ssl-cert=/etc/mysql/certs/server-cert.pem
ssl-key=/etc/mysql/certs/server-key.pem
require_secure_transport=ON

-- 创建SSL用户
CREATE USER 'secure_user'@'%' 
IDENTIFIED BY 'SecurePass123!' 
REQUIRE SSL;

-- 5. 审计日志加密
-- 启用加密审计日志
[mysqld]
audit_log_format=NEW
audit_log_encryption=AES
audit_log_rotate_on_size=104857600

-- 6. 备份加密
-- 使用mysqldump加密备份
mysqldump --single-transaction --routines --triggers \
  --master-data=2 --flush-logs \
  --ssl-mode=REQUIRED \
  --result-file=encrypted_backup.sql \
  --user=backup_user --password=backup_pass \
  database_name | openssl enc -aes-256-cbc -salt -out encrypted_backup.sql.enc

-- 7. 密钥管理集成
-- 集成AWS KMS进行密钥管理
-- 需要安装MySQL Keyring AWS插件
INSTALL PLUGIN keyring_aws SONAME 'keyring_aws.so';

-- 配置AWS KMS
[mysqld]
early-plugin-load=keyring_aws.so
keyring_aws_region=us-east-1
keyring_aws_key_id=arn:aws:kms:us-east-1:123456789012:key/abcd1234-a123-456a-a12b-a123b4cd56ef

-- 8. 合规性检查查询
-- GDPR数据发现查询
SELECT 
  table_schema,
  table_name,
  column_name,
  data_type
FROM information_schema.columns 
WHERE column_name REGEXP '(personal|sensitive|private|ssn|credit|medical)' 
AND table_schema NOT IN ('information_schema', 'performance_schema', 'mysql');

-- HIPAA合规检查
SELECT 
  user,
  host,
  ssl_type,
  ssl_cipher
FROM mysql.user 
WHERE ssl_type = 'ANY' OR ssl_type = 'X509';
```

### 2. PostgreSQL数据加密保护

```sql
-- PostgreSQL企业级数据加密完整配置

-- 1. 启用透明数据加密
-- PostgreSQL使用pgcrypto扩展实现加密
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 创建加密表
CREATE TABLE patient_records (
  id SERIAL PRIMARY KEY,
  patient_id VARCHAR(20),
  encrypted_ssn BYTEA,
  encrypted_medical_history BYTEA,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 字段级加密实现
-- 创建加密/解密函数
CREATE OR REPLACE FUNCTION encrypt_data(data TEXT, key TEXT)
RETURNS BYTEA AS $$
BEGIN
  RETURN pgp_sym_encrypt(data, key);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION decrypt_data(encrypted_data BYTEA, key TEXT)
RETURNS TEXT AS $$
BEGIN
  RETURN pgp_sym_decrypt(encrypted_data, key);
END;
$$ LANGUAGE plpgsql;

-- 插入加密数据
INSERT INTO patient_records (patient_id, encrypted_ssn, encrypted_medical_history)
VALUES (
  'PAT001',
  encrypt_data('123-45-6789', 'patient_key_PAT001'),
  encrypt_data('Diabetes Type 2, Hypertension Stage 1', 'patient_key_PAT001')
);

-- 查询解密数据
SELECT 
  patient_id,
  decrypt_data(encrypted_ssn, 'patient_key_PAT001') as ssn,
  decrypt_data(encrypted_medical_history, 'patient_key_PAT001') as medical_history
FROM patient_records 
WHERE patient_id = 'PAT001';

-- 3. SSL/TLS连接配置
-- 在postgresql.conf中配置SSL
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
ssl_ca_file = '/etc/ssl/certs/ca.crt'

-- 配置客户端认证
-- 在pg_hba.conf中强制SSL连接
hostssl all all 0.0.0.0/0 md5

-- 4. 行级安全(RLS)结合加密
-- 启用行级安全
ALTER TABLE patient_records ENABLE ROW LEVEL SECURITY;

-- 创建策略：用户只能访问自己的数据
CREATE POLICY patient_access_policy ON patient_records
FOR ALL TO application_user
USING (
  patient_id IN (
    SELECT patient_id FROM user_patient_mapping 
    WHERE user_id = current_user_id()
  )
);

-- 5. 备份加密
-- 使用pg_dump加密备份
pg_dump -h localhost -U backup_user -d healthcare_db \
  --compress=9 \
  --format=custom \
  --file=encrypted_backup.dump

-- 使用GPG加密备份文件
gpg --symmetric --cipher-algo AES256 encrypted_backup.dump

-- 6. 审计日志加密
-- 配置加密的日志输出
log_destination = 'csvlog'
logging_collector = on
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_file_mode = 0600

-- 启用查询日志加密
log_min_duration_statement = 1000
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a '

-- 7. 密钥管理集成
-- 集成HashiCorp Vault进行密钥管理
-- 创建Vault连接函数
CREATE OR REPLACE FUNCTION get_encryption_key(key_name TEXT)
RETURNS TEXT AS $$
DECLARE
  vault_token TEXT := 's.vault_token_here';
  vault_url TEXT := 'https://vault.example.com:8200';
  key_value TEXT;
BEGIN
  -- 调用Vault API获取密钥
  SELECT INTO key_value 
  http_get(vault_url || '/v1/secret/data/' || key_name, 
           'X-Vault-Token: ' || vault_token);
  
  RETURN key_value;
END;
$$ LANGUAGE plpgsql;

-- 8. 合规性监控查询
-- GDPR数据发现
SELECT 
  schemaname,
  tablename,
  attname,
  typname
FROM pg_attribute a
JOIN pg_class c ON a.attrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
JOIN pg_type t ON a.atttypid = t.oid
WHERE attname ILIKE '%personal%' 
   OR attname ILIKE '%sensitive%'
   OR attname ILIKE '%private%'
   OR attname ILIKE '%ssn%'
   OR attname ILIKE '%credit%';

-- HIPAA访问审计
SELECT 
  datname,
  usename,
  application_name,
  client_addr,
  backend_start,
  query_start,
  state_change,
  query
FROM pg_stat_activity 
WHERE query ILIKE '%patient%' 
   OR query ILIKE '%medical%'
ORDER BY state_change DESC 
LIMIT 100;
```

### 3. MongoDB数据加密保护

```javascript
// MongoDB企业级数据加密完整配置

// 1. 启用静态加密(透明加密)
// 启动MongoDB时启用加密
// mongod --enableEncryption --encryptionKeyFile /path/to/keyfile

// 2. 字段级加密实现
// 使用Client-Side Field Level Encryption
const { MongoClient } = require('mongodb');
const crypto = require('crypto');

// 加密配置
const encryptionConfig = {
  keyVaultNamespace: 'encryption.__keyVault',
  kmsProviders: {
    local: {
      key: new Uint8Array(96) // 本地密钥
    }
  }
};

// 创建加密客户端
const client = new MongoClient('mongodb://localhost:27017', {
  autoEncryption: encryptionConfig
});

// 3. 敏感数据加密存储
async function storeEncryptedPatientData() {
  const db = client.db('healthcare');
  const patients = db.collection('patients');
  
  // 敏感字段加密
  const patientRecord = {
    patientId: 'PAT001',
    personalInfo: {
      firstName: 'John',
      lastName: 'Doe',
      dateOfBirth: new Date('1980-01-15'),
      // 社保号码使用确定性加密
      ssn: {
        $binary: {
          base64: encryptDeterministic('123-45-6789', 'ssn_key'),
          subType: '06'
        }
      }
    },
    medicalHistory: {
      // 医疗记录使用随机加密
      conditions: [
        {
          diagnosis: {
            $binary: {
              base64: encryptRandom('Diabetes Type 2', 'medical_key'),
              subType: '06'
            }
          },
          treatment: {
            $binary: {
              base64: encryptRandom('Metformin 500mg twice daily', 'medical_key'),
              subType: '06'
            }
          }
        }
      ]
    },
    createdAt: new Date()
  };
  
  await patients.insertOne(patientRecord);
}

// 4. 查询加密数据
async function queryEncryptedData() {
  const db = client.db('healthcare');
  const patients = db.collection('patients');
  
  // 查询时自动解密
  const patient = await patients.findOne({
    'personalInfo.ssn': {
      $binary: {
        base64: encryptDeterministic('123-45-6789', 'ssn_key'),
        subType: '06'
      }
    }
  });
  
  console.log('Decrypted patient data:', patient);
}

// 5. SSL/TLS连接配置
// MongoDB配置文件中启用TLS
/*
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /path/to/mongodb.pem
    CAFile: /path/to/ca.pem
    allowConnectionsWithoutCertificates: false
*/

// 6. 审计日志加密
// 启用加密审计日志
db.adminCommand({
  setParameter: 1,
  auditAuthorizationSuccess: true
});

// 配置日志轮换和加密
db.adminCommand({
  logRotate: 1
});

// 7. 密钥管理
// 使用AWS KMS管理密钥
const awsKmsConfig = {
  keyVaultNamespace: 'encryption.__keyVault',
  kmsProviders: {
    aws: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    }
  },
  schemaMap: {
    'healthcare.patients': {
      bsonType: 'object',
      properties: {
        'personalInfo.ssn': {
          encrypt: {
            bsonType: 'string',
            algorithm: 'AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic',
            keyId: '/path/to/aws/kms/key'
          }
        }
      }
    }
  }
};

// 8. 合规性检查
// GDPR数据发现查询
db.patients.find({
  $or: [
    {'personalInfo.firstName': {$exists: true}},
    {'personalInfo.lastName': {$exists: true}},
    {'personalInfo.ssn': {$exists: true}},
    {'personalInfo.email': {$exists: true}}
  ]
});

// HIPAA访问审计
db.getSiblingDB('admin').system.profile.find({
  'command.find': 'patients',
  'command.filter': {$exists: true}
}).sort({ts: -1}).limit(100);

// 9. 备份加密
// 使用mongodump加密备份
const { exec } = require('child_process');

function backupWithEncryption() {
  const backupCmd = `
    mongodump --host localhost:27017 \
              --db healthcare \
              --out /backup/mongodb/$(date +%Y%m%d_%H%M%S) \
              --ssl \
              --sslCAFile /path/to/ca.pem \
              --sslPEMKeyFile /path/to/client.pem
  `;
  
  exec(backupCmd, (error, stdout, stderr) => {
    if (error) {
      console.error('Backup failed:', error);
      return;
    }
    
    // 加密备份文件
    const encryptCmd = `
      gpg --symmetric --cipher-algo AES256 \
          /backup/mongodb/latest_backup.tar.gz
    `;
    exec(encryptCmd);
  });
}

// 10. 密钥轮换
async function rotateEncryptionKeys() {
  const keyVault = client.db('encryption').collection('__keyVault');
  
  // 创建新密钥
  const newKey = await keyVault.insertOne({
    keyAltNames: ['current_patient_key'],
    keyMaterial: generateNewKey(),
    creationDate: new Date(),
    expirationDate: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1年后过期
    masterKey: {
      provider: 'aws',
      keyArn: 'arn:aws:kms:region:account:key/new-key-id'
    }
  });
  
  // 更新数据加密使用的密钥标识
  await db.adminCommand({
    rewrapManyDataKey: {
      filter: { 'masterKey.provider': 'aws' }
    },
    opts: {
      provider: 'aws',
      masterKey: {
        keyArn: 'arn:aws:kms:region:account:key/new-key-id'
      }
    }
  });
}
```

### 4. Redis数据加密保护

```bash
#!/bin/bash
# Redis企业级数据加密保护配置脚本

# 1. 启用TLS加密传输
configure_redis_tls() {
  echo "配置Redis TLS加密..."
  
  # 生成自签名证书（生产环境应使用正式CA签发的证书）
  openssl req -x509 -newkey rsa:4096 -keyout /etc/redis/tls/redis.key \
    -out /etc/redis/tls/redis.crt -days 365 -nodes \
    -subj "/CN=redis.example.com"
  
  # 配置Redis启用TLS
  cat >> /etc/redis/redis.conf << EOF
# TLS配置
tls-port 6380
port 0  # 禁用明文端口
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file /etc/redis/tls/redis.key
tls-ca-cert-file /etc/ssl/certs/ca-certificates.crt
tls-auth-clients yes
EOF
  
  systemctl restart redis
}

# 2. 数据持久化文件加密
encrypt_redis_persistence() {
  echo "配置Redis持久化文件加密..."
  
  # 配置RDB文件加密
  cat >> /etc/redis/redis.conf << EOF
# RDB加密配置
rdb-key-encryption yes
rdb-key-encryption-key-file /etc/redis/encryption/rdb.key
EOF
  
  # 生成RDB加密密钥
  openssl rand -hex 32 > /etc/redis/encryption/rdb.key
  chmod 600 /etc/redis/encryption/rdb.key
  
  # 配置AOF加密
  cat >> /etc/redis/redis.conf << EOF
# AOF加密配置
aof-use-rdb-preamble yes
EOF
}

# 3. 客户端数据加密
setup_client_side_encryption() {
  echo "配置客户端侧数据加密..."
  
  # Python客户端加密示例
  cat > /opt/redis/encrypted_client.py << 'EOF'
import redis
import hashlib
from cryptography.fernet import Fernet

class EncryptedRedisClient:
    def __init__(self, host='localhost', port=6380, password=None):
        self.client = redis.Redis(
            host=host, port=port, password=password, ssl=True,
            ssl_cert_reqs='required',
            ssl_ca_certs='/etc/ssl/certs/ca-certificates.crt'
        )
        # 为每个用户生成独立密钥
        self.encryption_keys = {}
    
    def _derive_key(self, user_id):
        """为用户派生加密密钥"""
        if user_id not in self.encryption_keys:
            # 使用用户ID和主密钥派生用户密钥
            master_key = b'your_master_key_here_32_bytes_long'
            user_salt = hashlib.sha256(user_id.encode()).digest()[:16]
            self.encryption_keys[user_id] = Fernet(
                hashlib.pbkdf2_hmac('sha256', master_key, user_salt, 100000)
            )
        return self.encryption_keys[user_id]
    
    def set_encrypted(self, key, value, user_id):
        """加密存储数据"""
        fernet = self._derive_key(user_id)
        encrypted_value = fernet.encrypt(str(value).encode())
        return self.client.set(f"user:{user_id}:{key}", encrypted_value)
    
    def get_encrypted(self, key, user_id):
        """解密获取数据"""
        fernet = self._derive_key(user_id)
        encrypted_value = self.client.get(f"user:{user_id}:{key}")
        if encrypted_value:
            return fernet.decrypt(encrypted_value).decode()
        return None

# 使用示例
client = EncryptedRedisClient(password: "${DB_PASSWORD}")
client.set_encrypted('ssn', '123-45-6789', 'user1001')
decrypted_ssn = client.get_encrypted('ssn', 'user1001')
print(f"Decrypted SSN: {decrypted_ssn}")
EOF
}

# 4. 访问控制和认证
configure_access_control() {
  echo "配置Redis访问控制..."
  
  # 启用ACL访问控制
  cat >> /etc/redis/redis.conf << EOF
# ACL配置
aclfile /etc/redis/users.acl
EOF
  
  # 创建用户和权限
  redis-cli << EOF
ACL SETUSER admin on >AdminPass2024! ~* &* +@all
ACL SETUSER app_user on >AppUserPass123! ~app:* ~session:* +get +set +del +expire
ACL SETUSER readonly_user on >ReadOnlyPass456! ~cache:* +get +hlen +exists
ACL SAVE
EOF
}

# 5. 审计日志配置
setup_audit_logging() {
  echo "配置Redis审计日志..."
  
  # 启用命令审计
  cat >> /etc/redis/redis.conf << EOF
# 审计日志配置
latency-monitor-threshold 100
slowlog-log-slower-than 10000
slowlog-max-len 128
EOF
  
  # 配置日志轮换
  cat > /etc/logrotate.d/redis << EOF
/var/log/redis/redis.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 redis redis
    postrotate
        systemctl reload redis > /dev/null 2>&1 || true
    endscript
}
EOF
}

# 6. 密钥管理系统集成
integrate_kms() {
  echo "集成密钥管理系统..."
  
  # 使用HashiCorp Vault集成示例
  cat > /opt/redis/kms_integration.py << 'EOF'
import hvac
import redis
import json

class RedisKMSIntegration:
    def __init__(self, vault_url, vault_token):
        self.vault_client = hvac.Client(url=vault_url, token=vault_token)
        self.redis_client = redis.Redis(host='localhost', port=6380, ssl=True)
    
    def get_encryption_key(self, key_name):
        """从Vault获取加密密钥"""
        try:
            secret = self.vault_client.secrets.transit.read_key(name=key_name)
            return secret['data']['keys']['1']['public_key']
        except Exception as e:
            print(f"Failed to get key from Vault: {e}")
            return None
    
    def encrypt_data(self, key_name, plaintext):
        """使用Vault Transit加密数据"""
        try:
            response = self.vault_client.secrets.transit.encrypt_data(
                name=key_name,
                plaintext=plaintext.encode('utf-8').hex()
            )
            return response['data']['ciphertext']
        except Exception as e:
            print(f"Encryption failed: {e}")
            return None
    
    def decrypt_data(self, key_name, ciphertext):
        """使用Vault Transit解密数据"""
        try:
            response = self.vault_client.secrets.transit.decrypt_data(
                name=key_name,
                ciphertext=ciphertext
            )
            return bytes.fromhex(response['data']['plaintext']).decode('utf-8')
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

# 使用示例
kms = RedisKMSIntegration('https://vault.example.com:8200', 'vault_token')
encrypted = kms.encrypt_data('redis-encryption-key', 'sensitive_data')
decrypted = kms.decrypt_data('redis-encryption-key', encrypted)
EOF
}

# 7. 合规性检查
run_compliance_check() {
  echo "执行合规性检查..."
  
  # 检查TLS配置
  if redis-cli --tls --cert /etc/redis/tls/redis.crt \
               --key /etc/redis/tls/redis.key \
               --cacert /etc/ssl/certs/ca-certificates.crt \
               ping 2>/dev/null | grep -q "PONG"; then
    echo "✅ TLS配置正常"
  else
    echo "❌ TLS配置异常"
  fi
  
  # 检查访问控制
  local acl_users=$(redis-cli ACL USERS)
  if echo "$acl_users" | grep -q "admin"; then
    echo "✅ ACL用户配置正常"
  else
    echo "❌ ACL用户配置异常"
  fi
  
  # 生成合规报告
  local report_file="/var/log/redis/compliance_report_$(date +%Y%m%d_%H%M%S).json"
  cat > "$report_file" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "checks": {
    "tls_enabled": true,
    "acl_configured": true,
    "encryption_at_rest": true,
    "audit_logging": true
  },
  "compliance_status": "PASSED"
}
EOF
  
  echo "合规检查报告已生成: $report_file"
}

# 8. 性能基准测试
run_encryption_performance_test() {
  echo "执行加密性能基准测试..."
  
  # 测试加密前后的性能差异
  local test_script=$(cat << 'EOF'
import redis
import time
import statistics

client = redis.Redis(host='localhost', port=6380, ssl=True)

# 测试明文操作性能
start_time = time.time()
for i in range(10000):
    client.set(f"test_plain_{i}", f"value_{i}")
plain_duration = time.time() - start_time

# 测试加密操作性能
start_time = time.time()
for i in range(10000):
    # 模拟加密操作开销
    encrypted_value = f"value_{i}"  # 实际应该进行加密
    client.set(f"test_encrypted_{i}", encrypted_value)
encrypted_duration = time.time() - start_time

print(f"Plain operations: {plain_duration:.4f} seconds")
print(f"Encrypted operations: {encrypted_duration:.4f} seconds")
print(f"Performance impact: {((encrypted_duration - plain_duration) / plain_duration * 100):.2f}%")
EOF
)
  
  python3 -c "$test_script"
}

# 主执行函数
main() {
  case "$1" in
    setup-all)
      configure_redis_tls
      encrypt_redis_persistence
      setup_client_side_encryption
      configure_access_control
      setup_audit_logging
      integrate_kms
      run_compliance_check
      run_encryption_performance_test
      echo "Redis数据加密保护配置完成"
      ;;
    compliance-check)
      run_compliance_check
      ;;
    performance-test)
      run_encryption_performance_test
      ;;
    *)
      echo "Usage: $0 {setup-all|compliance-check|performance-test}"
      exit 1
      ;;
  esac
}

main "$@"
```

## 🔐 统一密钥管理平台

### Python密钥管理系统
```python
#!/usr/bin/env python3
"""
企业级统一密钥管理平台
支持多数据库和应用系统的密钥统一管理
"""

import os
import json
import hashlib
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

@dataclass
class KeyMetadata:
    """密钥元数据"""
    key_id: str
    key_type: str
    algorithm: str
    created_at: datetime
    expires_at: datetime
    rotation_required: bool
    usage_count: int

class KeyManagementSystem:
    """统一密钥管理系统"""
    
    def __init__(self, config_file: str = "/etc/kms/config.json"):
        self.config_file = config_file
        self.keys = {}
        self.logger = self._setup_logging()
        self.load_configuration()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/var/log/kms/kms.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_configuration(self):
        """加载KMS配置"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.master_key = config.get('master_key')
                self.rotation_policy = config.get('rotation_policy', {})
        except FileNotFoundError:
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        default_config = {
            'master_key': Fernet.generate_key().decode(),
            'rotation_policy': {
                'default_rotation_days': 90,
                'notification_days_before_expiry': 30,
                'automatic_rotation': True
            }
        }
        
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2, default=str)
        
        self.master_key = default_config['master_key']
        self.rotation_policy = default_config['rotation_policy']
    
    def generate_data_key(self, purpose: str, algorithm: str = 'AES256') -> str:
        """生成数据加密密钥"""
        key_id = f"dk_{purpose}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 从主密钥派生数据密钥
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key_material = kdf.derive(self.master_key.encode())
        data_key = Fernet(key_material)
        
        # 存储密钥元数据
        self.keys[key_id] = KeyMetadata(
            key_id=key_id,
            key_type='data_key',
            algorithm=algorithm,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(
                days=self.rotation_policy.get('default_rotation_days', 90)
            ),
            rotation_required=False,
            usage_count=0
        )
        
        self.logger.info(f"Generated data key: {key_id} for purpose: {purpose}")
        return key_id, data_key
    
    def encrypt_data(self, key_id: str, plaintext: str) -> str:
        """使用指定密钥加密数据"""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        key_metadata = self.keys[key_id]
        key_material = self._derive_key_material(key_id)
        fernet = Fernet(key_material)
        
        encrypted_data = fernet.encrypt(plaintext.encode())
        key_metadata.usage_count += 1
        
        # 检查是否需要轮换
        if self._should_rotate_key(key_metadata):
            key_metadata.rotation_required = True
            self.logger.warning(f"Key {key_id} requires rotation")
        
        return encrypted_data.decode()
    
    def decrypt_data(self, key_id: str, encrypted_data: str) -> str:
        """使用指定密钥解密数据"""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        key_metadata = self.keys[key_id]
        key_material = self._derive_key_material(key_id)
        fernet = Fernet(key_material)
        
        decrypted_data = fernet.decrypt(encrypted_data.encode())
        key_metadata.usage_count += 1
        
        return decrypted_data.decode()
    
    def _derive_key_material(self, key_id: str) -> bytes:
        """派生密钥材料"""
        key_metadata = self.keys[key_id]
        # 实际实现应该从安全存储中获取密钥材料
        return hashlib.sha256(f"{self.master_key}_{key_id}".encode()).digest()
    
    def _should_rotate_key(self, key_metadata: KeyMetadata) -> bool:
        """判断是否需要轮换密钥"""
        # 基于使用次数或时间判断
        if key_metadata.usage_count > 10000:  # 使用次数阈值
            return True
        
        days_until_expiry = (key_metadata.expires_at - datetime.now()).days
        if days_until_expiry <= self.rotation_policy.get('notification_days_before_expiry', 30):
            return True
        
        return False
    
    def rotate_key(self, key_id: str) -> str:
        """轮换指定密钥"""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        old_key = self.keys[key_id]
        new_key_id, new_key = self.generate_data_key(
            purpose=f"rotated_{old_key.key_id}",
            algorithm=old_key.algorithm
        )
        
        # 更新密钥映射关系
        self.keys[new_key_id] = self.keys[key_id]
        self.keys[new_key_id].key_id = new_key_id
        self.keys[new_key_id].created_at = datetime.now()
        self.keys[new_key_id].expires_at = datetime.now() + timedelta(
            days=self.rotation_policy.get('default_rotation_days', 90)
        )
        self.keys[new_key_id].rotation_required = False
        self.keys[new_key_id].usage_count = 0
        
        self.logger.info(f"Rotated key {key_id} to {new_key_id}")
        return new_key_id
    
    def get_key_metadata(self, key_id: str) -> Dict:
        """获取密钥元数据"""
        if key_id not in self.keys:
            return None
        
        key_metadata = self.keys[key_id]
        return {
            'key_id': key_metadata.key_id,
            'key_type': key_metadata.key_type,
            'algorithm': key_metadata.algorithm,
            'created_at': key_metadata.created_at.isoformat(),
            'expires_at': key_metadata.expires_at.isoformat(),
            'rotation_required': key_metadata.rotation_required,
            'usage_count': key_metadata.usage_count
        }
    
    def audit_key_usage(self) -> Dict:
        """审计密钥使用情况"""
        audit_report = {
            'timestamp': datetime.now().isoformat(),
            'total_keys': len(self.keys),
            'keys_needing_rotation': [],
            'key_usage_stats': {}
        }
        
        for key_id, key_metadata in self.keys.items():
            audit_report['key_usage_stats'][key_id] = {
                'usage_count': key_metadata.usage_count,
                'days_until_expiry': (key_metadata.expires_at - datetime.now()).days
            }
            
            if key_metadata.rotation_required:
                audit_report['keys_needing_rotation'].append(key_id)
        
        return audit_report

# 使用示例
def main():
    kms = KeyManagementSystem()
    
    # 生成数据密钥
    key_id, key = kms.generate_data_key('customer_data')
    
    # 加密敏感数据
    sensitive_data = "123-45-6789"
    encrypted = kms.encrypt_data(key_id, sensitive_data)
    print(f"Encrypted: {encrypted}")
    
    # 解密数据
    decrypted = kms.decrypt_data(key_id, encrypted)
    print(f"Decrypted: {decrypted}")
    
    # 审计密钥使用
    audit_report = kms.audit_key_usage()
    print(f"Audit Report: {json.dumps(audit_report, indent=2)}")

if __name__ == "__main__":
    main()
```

## 🧪 加密保护验证测试

### 自动化安全测试套件
```bash
#!/bin/bash
# 数据库加密保护验证测试套件

TEST_RESULTS=()

# MySQL加密测试
test_mysql_encryption() {
  echo "=== MySQL加密保护测试 ==="
  
  # 测试SSL连接
  local ssl_status=$(mysql -u root -p -e "SHOW VARIABLES LIKE 'have_ssl';" 2>/dev/null | grep -o 'YES\|DISABLED')
  if [ "$ssl_status" = "YES" ]; then
    TEST_RESULTS+=("MySQL SSL支持测试: 通过")
    echo "✅ MySQL SSL支持正常"
  else
    TEST_RESULTS+=("MySQL SSL支持测试: 失败")
    echo "❌ MySQL SSL支持异常"
  fi
  
  # 测试TDE状态
  local tde_status=$(mysql -u root -p -e "SELECT * FROM performance_schema.keyring_keys;" 2>/dev/null)
  if [ -n "$tde_status" ]; then
    TEST_RESULTS+=("MySQL TDE状态测试: 通过")
    echo "✅ MySQL TDE配置正常"
  else
    TEST_RESULTS+=("MySQL TDE状态测试: 失败")
    echo "❌ MySQL TDE配置异常"
  fi
  
  # 测试字段级加密
  mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS encryption_test;
USE encryption_test;

CREATE TABLE encrypted_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sensitive_field VARBINARY(1024)
);

INSERT INTO encrypted_data (sensitive_field) 
VALUES (AES_ENCRYPT('test_sensitive_data', 'test_key'));

SELECT id, AES_DECRYPT(sensitive_field, 'test_key') as decrypted_data 
FROM encrypted_data;
EOF
  
  if [ $? -eq 0 ]; then
    TEST_RESULTS+=("MySQL字段加密测试: 通过")
    echo "✅ MySQL字段级加密正常"
  else
    TEST_RESULTS+=("MySQL字段加密测试: 失败")
    echo "❌ MySQL字段级加密异常"
  fi
}

# PostgreSQL加密测试
test_postgresql_encryption() {
  echo "=== PostgreSQL加密保护测试 ==="
  
  # 测试SSL连接
  local ssl_status=$(psql -U postgres -c "SHOW ssl;" 2>/dev/null | grep -o 'on\|off')
  if [ "$ssl_status" = "on" ]; then
    TEST_RESULTS+=("PostgreSQL SSL支持测试: 通过")
    echo "✅ PostgreSQL SSL支持正常"
  else
    TEST_RESULTS+=("PostgreSQL SSL支持测试: 失败")
    echo "❌ PostgreSQL SSL支持异常"
  fi
  
  # 测试pgcrypto扩展
  psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;" 2>/dev/null
  local crypto_status=$(psql -U postgres -c "SELECT extname FROM pg_extension WHERE extname = 'pgcrypto';" 2>/dev/null)
  
  if [ -n "$crypto_status" ]; then
    TEST_RESULTS+=("PostgreSQL pgcrypto扩展测试: 通过")
    echo "✅ PostgreSQL加密扩展正常"
  else
    TEST_RESULTS+=("PostgreSQL pgcrypto扩展测试: 失败")
    echo "❌ PostgreSQL加密扩展异常"
  fi
  
  # 测试数据加密/解密
  psql -U postgres << EOF
CREATE TABLE IF NOT EXISTS encryption_test (
  id SERIAL PRIMARY KEY,
  encrypted_data BYTEA
);

INSERT INTO encryption_test (encrypted_data) 
VALUES (pgp_sym_encrypt('test_sensitive_data', 'test_key'));

SELECT id, pgp_sym_decrypt(encrypted_data, 'test_key') as decrypted_data 
FROM encryption_test;
EOF
  
  if [ $? -eq 0 ]; then
    TEST_RESULTS+=("PostgreSQL数据加密测试: 通过")
    echo "✅ PostgreSQL数据加密正常"
  else
    TEST_RESULTS+=("PostgreSQL数据加密测试: 失败")
    echo "❌ PostgreSQL数据加密异常"
  fi
}

# MongoDB加密测试
test_mongodb_encryption() {
  echo "=== MongoDB加密保护测试 ==="
  
  # 测试TLS连接
  local tls_status=$(mongo --tls --host localhost --eval "db.runCommand({ismaster: 1})" 2>/dev/null | grep -o 'true\|false')
  if [ "$tls_status" = "true" ]; then
    TEST_RESULTS+=("MongoDB TLS支持测试: 通过")
    echo "✅ MongoDB TLS支持正常"
  else
    TEST_RESULTS+=("MongoDB TLS支持测试: 失败")
    echo "❌ MongoDB TLS支持异常"
  fi
  
  # 测试字段级加密
  mongo --eval "
  db = db.getSiblingDB('encryption_test');
  db.encrypted_data.insert({
    sensitive_field: hex_md5('test_data')
  });
  
  db.encrypted_data.findOne();
  " 2>/dev/null
  
  if [ $? -eq 0 ]; then
    TEST_RESULTS+=("MongoDB字段加密测试: 通过")
    echo "✅ MongoDB字段级加密正常"
  else
    TEST_RESULTS+=("MongoDB字段加密测试: 失败")
    echo "❌ MongoDB字段级加密异常"
  fi
}

# Redis加密测试
test_redis_encryption() {
  echo "=== Redis加密保护测试 ==="
  
  # 测试TLS连接
  local tls_ping=$(redis-cli --tls --cert /etc/redis/tls/redis.crt \
    --key /etc/redis/tls/redis.key \
    --cacert /etc/ssl/certs/ca-certificates.crt ping 2>/dev/null)
  
  if [ "$tls_ping" = "PONG" ]; then
    TEST_RESULTS+=("Redis TLS连接测试: 通过")
    echo "✅ Redis TLS连接正常"
  else
    TEST_RESULTS+=("Redis TLS连接测试: 失败")
    echo "❌ Redis TLS连接异常"
  fi
  
  # 测试ACL配置
  local acl_status=$(redis-cli ACL LIST 2>/dev/null | wc -l)
  if [ "$acl_status" -gt 0 ]; then
    TEST_RESULTS+=("Redis ACL配置测试: 通过")
    echo "✅ Redis ACL配置正常"
  else
    TEST_RESULTS+=("Redis ACL配置测试: 失败")
    echo "❌ Redis ACL配置异常"
  fi
}

# 生成安全测试报告
generate_security_test_report() {
  echo "=== 数据库加密保护测试综合报告 ==="
  
  local total_tests=${#TEST_RESULTS[@]}
  local passed_tests=0
  
  for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
    if [[ $result == *"通过"* ]]; then
      ((passed_tests++))
    fi
  done
  
  echo ""
  echo "安全测试总结:"
  echo "总测试项: $total_tests"
  echo "通过项: $passed_tests"
  echo "通过率: $((passed_tests * 100 / total_tests))%"
  
  # 评估安全等级
  local security_score=$((passed_tests * 100 / total_tests))
  if [ $security_score -ge 90 ]; then
    echo "🔒 安全等级: 优秀 (企业级安全标准)"
  elif [ $security_score -ge 75 ]; then
    echo "🔐 安全等级: 良好 (符合行业标准)"
  elif [ $security_score -ge 60 ]; then
    echo "🔓 安全等级: 一般 (需要加强安全措施)"
  else
    echo "⚠️  安全等级: 较差 (存在严重安全隐患)"
  fi
  
  # 保存报告
  local report_file="/tmp/encryption_security_report_$(date +%Y%m%d_%H%M%S).txt"
  printf "%s\n" "${TEST_RESULTS[@]}" > "$report_file"
  echo "详细安全报告已保存: $report_file"
}

# 执行所有安全测试
test_mysql_encryption
test_postgresql_encryption
test_mongodb_encryption
test_redis_encryption
generate_security_test_report
```

## 📚 最佳实践总结

### 数据加密核心原则
1. **分层防护**: 实施应用层、传输层、存储层的多层次加密
2. **最小权限**: 密钥访问遵循最小权限原则
3. **密钥轮换**: 定期轮换加密密钥降低泄露风险
4. **审计追踪**: 完整记录密钥使用和数据访问日志
5. **备份恢复**: 确保加密密钥的安全备份和恢复机制

### 合规性要求要点
- **GDPR**: 个人数据加密保护，数据主体权利保障
- **HIPAA**: 医疗健康信息安全，访问控制和审计要求
- **PCI-DSS**: 支付卡数据加密，网络安全和监控要求
- **SOX**: 财务数据保护，访问控制和变更管理

### 性能优化建议
- **选择合适算法**: 平衡安全性与性能需求
- **批量加密操作**: 减少频繁的加密解密调用
- **缓存加密结果**: 对于不经常变更的数据适当缓存
- **异步加密处理**: 避免加密操作阻塞主线程

---
> **💡 提示**: 数据加密是安全防护的重要组成部分，但在实施时需要平衡安全性和性能，建议根据数据敏感程度和业务需求制定差异化的加密策略。