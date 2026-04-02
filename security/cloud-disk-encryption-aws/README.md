# Cloud Disk Encryption - AWS

AWS云磁盘加密实践演示。

## AWS加密服务概览

```
AWS加密服务栈:
┌─────────────────────────────────────────────────────────┐
│                    应用程序层                            │
├─────────────────────────────────────────────────────────┤
│  AWS KMS (Key Management Service)                       │
│  - CMK (Customer Master Keys)                           │
│  - 自动密钥轮换                                         │
│  - 访问控制策略                                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   EBS       │  │   S3        │  │  RDS        │     │
│  │ Encryption  │  │ Encryption  │  │ Encryption  │     │
│  │ (AES-256)   │  │ (SSE-KMS)   │  │ (TDE)       │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  EC2        │  │  Lambda     │  │  EFS        │     │
│  │  Nitro      │  │  Enclave    │  │  Encryption │     │
│  │  Enclaves   │  │  (机密计算)  │  │  (TLS+AES)  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## EBS加密

### 默认加密配置
```bash
# 启用EBS默认加密
aws ec2 enable-ebs-encryption-by-default

# 验证默认加密
aws ec2 get-ebs-encryption-by-default

# 创建加密EBS卷
aws ec2 create-volume \
    --volume-type gp3 \
    --size 100 \
    --encrypted \
    --kms-key-id alias/aws/ebs \
    --availability-zone us-east-1a

# 使用客户管理的CMK
aws ec2 create-volume \
    --volume-type io2 \
    --size 500 \
    --encrypted \
    --kms-key-id arn:aws:kms:us-east-1:123456789:key/12345678-1234-1234-1234-123456789012 \
    --iops 16000 \
    --availability-zone us-east-1a
```

### CloudFormation模板
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'EBS Encryption Configuration'

Resources:
  # KMS Key for EBS
  EBSKMSKey:
    Type: AWS::KMS::Key
    Properties:
      Description: 'KMS key for EBS encryption'
      EnableKeyRotation: true
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: 'Enable IAM User Permissions'
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: 'Allow EC2 Service'
            Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action:
              - 'kms:Encrypt'
              - 'kms:Decrypt'
              - 'kms:ReEncrypt*'
              - 'kms:GenerateDataKey*'
              - 'kms:DescribeKey'
            Resource: '*'

  # 默认加密配置
  EBSEncryptionDefaults:
    Type: AWS::EC2::EBSEncryptionDefaults
    Properties:
      Encrypted: true
      KmsKeyId: !Ref EBSKMSKey

  # 加密EBS卷
  EncryptedVolume:
    Type: AWS::EC2::Volume
    Properties:
      Size: 100
      VolumeType: gp3
      Encrypted: true
      KmsKeyId: !Ref EBSKMSKey
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: EncryptedDataVolume
        - Key: Encryption
          Value: CMK
```

## S3加密

### 服务器端加密
```bash
# 创建带SSE-KMS的S3桶
aws s3api create-bucket \
    --bucket my-encrypted-bucket \
    --region us-east-1

# 配置默认加密
aws s3api put-bucket-encryption \
    --bucket my-encrypted-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "arn:aws:kms:us-east-1:123456789:key/my-key"
            },
            "BucketKeyEnabled": true
        }]
    }'

# 上传加密对象
aws s3 cp sensitive-data.txt s3://my-encrypted-bucket/ \
    --sse aws:kms \
    --sse-kms-key-id alias/my-key
```

### 桶策略强制加密
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyUnencryptedUploads",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::my-encrypted-bucket/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": "aws:kms"
                }
            }
        },
        {
            "Sid": "DenyIncorrectKMSKey",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::my-encrypted-bucket/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption-aws-kms-key-id": "arn:aws:kms:us-east-1:123456789:key/my-key"
                }
            }
        }
    ]
}
```

## RDS加密

### 创建加密数据库实例
```bash
# 创建加密RDS实例
aws rds create-db-instance \
    --db-instance-identifier my-encrypted-db \
    --db-instance-class db.t3.medium \
    --engine mysql \
    --master-username admin \
    --master-user-password supersecret123 \
    --allocated-storage 100 \
    --storage-encrypted \
    --kms-key-id alias/aws/rds \
    --backup-retention-period 7

# 验证加密
aws rds describe-db-instances \
    --db-instance-identifier my-encrypted-db \
    --query 'DBInstances[0].[StorageEncrypted,KmsKeyId]'
```

## Lambda加密环境变量

```python
import boto3
import os
from base64 import b64decode

kms = boto3.client('kms')

# 加密的环境变量需要在部署时加密
ENCRYPTED_DB_PASSWORD = os.environ['DB_PASSWORD']

# 运行时解密
def decrypt_password(encrypted_value):
    """解密KMS加密的环境变量"""
    try:
        decrypted = kms.decrypt(
            CiphertextBlob=b64decode(encrypted_value)
        )
        return decrypted['Plaintext'].decode('utf-8')
    except Exception as e:
        print(f"Decryption failed: {e}")
        raise

# Lambda处理函数
def lambda_handler(event, context):
    db_password = decrypt_password(ENCRYPTED_DB_PASSWORD)
    
    # 使用解密后的密码连接数据库
    # ...
    
    return {
        'statusCode': 200,
        'body': 'Successfully processed with encrypted credentials'
    }
```

## 加密监控与审计

```python
# AWS加密监控脚本
import boto3
import json
from datetime import datetime, timedelta

class AWSEncryptionMonitor:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')
        self.rds = boto3.client('rds')
        self.cloudtrail = boto3.client('cloudtrail')
    
    def check_unencrypted_ebs(self):
        """检查未加密的EBS卷"""
        response = self.ec2.describe_volumes()
        unencrypted = []
        
        for volume in response['Volumes']:
            if not volume.get('Encrypted', False):
                unencrypted.append({
                    'VolumeId': volume['VolumeId'],
                    'Size': volume['Size'],
                    'State': volume['State'],
                    'CreateTime': volume['CreateTime'].isoformat()
                })
        
        return unencrypted
    
    def check_s3_encryption(self):
        """检查S3桶加密配置"""
        buckets = self.s3.list_buckets()['Buckets']
        results = []
        
        for bucket in buckets:
            try:
                encryption = self.s3.get_bucket_encryption(
                    Bucket=bucket['Name']
                )
                rules = encryption['ServerSideEncryptionConfiguration']['Rules']
                results.append({
                    'Bucket': bucket['Name'],
                    'Encrypted': True,
                    'Algorithm': rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
                })
            except self.s3.exceptions.ClientError as e:
                if 'ServerSideEncryptionConfigurationNotFoundError' in str(e):
                    results.append({
                        'Bucket': bucket['Name'],
                        'Encrypted': False,
                        'Algorithm': None
                    })
        
        return results
    
    def generate_encryption_report(self):
        """生成加密状态报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'unencrypted_ebs': self.check_unencrypted_ebs(),
            's3_encryption': self.check_s3_encryption()
        }
        
        # 保存报告
        with open(f"encryption_report_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

# 使用
monitor = AWSEncryptionMonitor()
report = monitor.generate_encryption_report()
print(json.dumps(report, indent=2))
```

## 学习要点

1. AWS KMS密钥管理
2. EBS/S3/RDS加密配置
3. 默认加密策略
4. 加密监控与审计
5. 合规性检查自动化
