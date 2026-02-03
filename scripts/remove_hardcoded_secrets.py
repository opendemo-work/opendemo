#!/usr/bin/env python3
"""
移除硬编码敏感信息的自动化脚本
将硬编码的密码、密钥等替换为环境变量占位符
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

class HardcodedSecretRemover:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.changes_made = []
        
        # 需要处理的敏感信息模式
        self.secret_patterns = [
            # 数据库密码
            (r'pwd:\s*"[^"]*"', 'pwd: "${GENERIC_PASSWORD}"'),
            (r"pwd:\s*'[^']*'", "pwd: "${GENERIC_PASSWORD}""),
            (r'password["\']?\s*[:=]\s*["\'][^"\']*["\']', 'password: "${GENERIC_PASSWORD}"'),
            (r'PASSWORD\s*=\s*["\'][^"\']*["\']', 'password: "${GENERIC_PASSWORD}"'),
            
            # JWT密钥
            (r'SECRET_KEY\s*=\s*["\'][^"\']*["\']', 'SECRET_KEY = "${JWT_SECRET}"'),
            (r'jwt[_-]?secret["\']?\s*[:=]\s*["\'][^"\']*["\']', 'jwt_secret: "${JWT_SECRET}"'),
            
            # API密钥
            (r'api[_-]?key["\']?\s*[:=]\s*["\'][^"\']*["\']', 'api_key: "${API_KEY}"'),
            (r'API_KEY\s*=\s*["\'][^"\']*["\']', 'api_key: "${API_KEY}"'),
            
            # Redis密码
            (r'redis[_-]?password["\']?\s*[:=]\s*["\'][^"\']*["\']', 'redis_password: "${GENERIC_PASSWORD}"'),
            
            # 通用密码字段
            (r'(password|pwd|pass)["\']?\s*[:=]\s*["\']([^"\']{8,})["\']', r'\1: "${GENERIC_PASSWORD}"'),
        ]
        
        # 需要排除的文件和目录
        self.exclude_patterns = {
            '.git', '__pycache__', 'node_modules', 'venv', 'env',
            '.mypy_cache', 'htmlcov', 'build', 'dist', 'target'
        }

    def is_excluded(self, path: Path) -> bool:
        """判断路径是否应该被排除"""
        return any(exclude in path.parts for exclude in self.exclude_patterns)

    def process_file(self, file_path: Path) -> bool:
        """处理单个文件，移除硬编码敏感信息"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # 应用所有替换规则
            for pattern, replacement in self.secret_patterns:
                # 检查是否匹配
                if re.search(pattern, content, re.IGNORECASE):
                    # 执行替换
                    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                    if new_content != content:
                        changes_made.append({
                            'pattern': pattern,
                            'replacement': replacement
                        })
                        content = new_content
            
            # 如果有更改，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.changes_made.append({
                    'file': str(file_path.relative_to(self.root_path)),
                    'changes': changes_made
                })
                return True
                
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            
        return False

    def process_directory(self, directory: Path = None) -> int:
        """递归处理目录中的文件"""
        if directory is None:
            directory = self.root_path
            
        files_processed = 0
        files_changed = 0
        
        for item in directory.iterdir():
            if self.is_excluded(item):
                continue
                
            if item.is_file():
                files_processed += 1
                if self.process_file(item):
                    files_changed += 1
                    
                if files_processed % 100 == 0:
                    print(f"已处理 {files_processed} 个文件...")
                    
            elif item.is_dir():
                changed_in_subdir = self.process_directory(item)
                files_changed += changed_in_subdir
                
        return files_changed

    def create_env_template(self):
        """创建环境变量模板文件"""
        env_template = """# 环境变量模板文件
# 请将此文件复制为 .env 并填入实际值

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USERNAME=app_user
DB_PASSWORD=your_database_password_here
DB_ADMIN_PASSWORD=your_admin_password_here

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password_here

# 安全配置
JWT_SECRET=your_jwt_secret_here
API_KEY=your_api_key_here

# 应用配置
APP_ENV=development
DEBUG=false

# 注意事项:
# 1. 请勿将此文件提交到版本控制系统
# 2. 在生产环境中使用密钥管理服务
# 3. 定期轮换敏感凭据
"""
        
        template_path = self.root_path / '.env.template'
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(env_template)
        
        print(f"环境变量模板已创建: {template_path}")

    def create_security_notice(self):
        """创建安全注意事项文件"""
        notice_content = """# 安全注意事项

## ⚠️ 重要提醒

本项目已移除所有硬编码的敏感信息。请按照以下步骤正确配置：

### 1. 生成安全凭据
```bash
# 使用提供的脚本生成安全密码
./scripts/generate_secure_credentials.sh
```

### 2. 配置环境变量
```bash
# 复制模板并填写实际值
cp .env.template .env
# 编辑 .env 文件，填入生成的安全凭据
```

### 3. 验证配置
```bash
# 测试环境变量是否正确加载
python scripts/validate_env_config.py
```

## 🛡️ 安全最佳实践

- 永不在代码中硬编码敏感信息
- 使用环境变量或密钥管理服务
- 定期轮换密码和密钥
- 实施最小权限原则
- 启用审计日志

## 📚 了解更多
请查看 SECURITY_BEST_PRACTICES.md 获取详细的安全部署指南。
"""
        
        notice_path = self.root_path / 'SECURITY_NOTICE.md'
        with open(notice_path, 'w', encoding='utf-8') as f:
            f.write(notice_content)
        
        print(f"安全注意事项已创建: {notice_path}")

    def generate_report(self) -> Dict:
        """生成处理报告"""
        report = {
            'summary': {
                'files_processed': len(self.changes_made),
                'total_changes': sum(len(file_changes['changes']) for file_changes in self.changes_made)
            },
            'changed_files': self.changes_made,
            'recommendations': [
                "1. 检查所有更改的文件确保替换正确",
                "2. 使用提供的脚本生成安全的凭据",
                "3. 配置适当的环境变量",
                "4. 在生产环境中使用专业的密钥管理服务"
            ]
        }
        return report

    def run_cleanup(self) -> Dict:
        """执行完整的清理过程"""
        print("开始清理硬编码的敏感信息...")
        print(f"处理路径: {self.root_path}")
        
        # 处理文件
        changed_files = self.process_directory()
        
        print(f"\n处理完成!")
        print(f"修改文件数: {changed_files}")
        print(f"总变更数: {len(self.changes_made)}")
        
        # 创建辅助文件
        self.create_env_template()
        self.create_security_notice()
        
        # 生成报告
        report = self.generate_report()
        
        # 保存报告
        report_path = self.root_path / 'secret_removal_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"详细报告已保存到: {report_path}")
        
        return report

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='移除硬编码敏感信息')
    parser.add_argument('--path', default='.', help='项目根路径')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要进行的更改，不实际修改文件')
    
    args = parser.parse_args()
    
    remover = HardcodedSecretRemover(args.path)
    
    if args.dry_run:
        print("=== 干运行模式 ===")
        print("将显示需要修改的文件，但不会实际修改")
        # 这里可以实现预览功能
    else:
        report = remover.run_cleanup()
        
        print("\n=== 清理完成 ===")
        print(f"共修改 {report['summary']['files_processed']} 个文件")
        print(f"总变更 {report['summary']['total_changes']} 处")

if __name__ == "__main__":
    main()