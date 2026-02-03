#!/usr/bin/env python3
"""
敏感信息扫描工具
"""

import os
import re
import sys
from pathlib import Path

def scan_project_for_secrets():
    """扫描项目中的敏感信息"""
    
    sensitive_patterns = [
        (r'password\s*=\s*[\'"][^\'"]{3,}[\'"]', '密码'),
        (r'token\s*=\s*[\'"][^\'"]{10,}[\'"]', '令牌'),
        (r'key\s*=\s*[\'"][^\'"]{10,}[\'"]', '密钥'),
        (r'secret\s*=\s*[\'"][^\'"]{5,}[\'"]', '密钥'),
        (r'api[_-]?key\s*=\s*[\'"][^\'"]{10,}[\'"]', 'API密钥'),
        (r'access[_-]?token\s*=\s*[\'"][^\'"]{10,}[\'"]', '访问令牌'),
    ]
    
    project_root = Path('.')
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'scripts/security'}
    
    findings = []
    
    print("🔍 开始扫描敏感信息...")
    
    for file_path in project_root.rglob('*'):
        # 跳过不需要扫描的目录和文件
        if any(skip_dir in str(file_path) for skip_dir in skip_dirs):
            continue
            
        if file_path.is_file() and file_path.suffix in ['.py', '.js', '.json', '.yaml', '.yml', '.env']:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    for pattern, description in sensitive_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            findings.append({
                                'file': str(file_path),
                                'line': line_num,
                                'content': line.strip(),
                                'type': description
                            })
                            
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {e}")
    
    return findings

def main():
    findings = scan_project_for_secrets()
    
    if findings:
        print(f"\n🚨 发现 {len(findings)} 个潜在敏感信息:")
        print("=" * 50)
        
        for i, finding in enumerate(findings, 1):
            print(f"{i}. 文件: {finding['file']}")
            print(f"   行号: {finding['line']}")
            print(f"   类型: {finding['type']}")
            print(f"   内容: {finding['content'][:100]}...")
            print("-" * 30)
            
        print(f"\n💡 建议:")
        print("1. 将硬编码的敏感信息移到环境变量")
        print("2. 使用配置管理工具")
        print("3. 参考 .env.example 创建安全配置")
    else:
        print("✅ 未发现明显的硬编码敏感信息")
    
    return len(findings)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(min(exit_code, 1))  # 最多返回1，避免过于严格的退出码