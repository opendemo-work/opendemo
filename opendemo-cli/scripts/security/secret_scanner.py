#!/usr/bin/env python3
"""
密钥和敏感信息扫描器
用于检测代码库中的各种敏感信息
"""

import os
import re
import json
import base64
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple
import argparse

class SecretScanner:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.findings = []
        self.scanned_files = 0
        
        # 敏感信息模式定义
        self.patterns = {
            # API Keys 和密钥
            'AWS_ACCESS_KEY': r'(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}',
            'AWS_SECRET_KEY': r'(?i)(aws|amazon)(.{0,20})?[\'\"]([A-Za-z0-9/+=]{40})[\'\"]',
            'GOOGLE_API_KEY': r'AIza[0-9A-Za-z\\-_]{35}',
            'GOOGLE_OAUTH_ID': r'[0-9]+-[a-zA-Z0-9_]{32}\.apps\.googleusercontent\.com',
            'GITHUB_TOKEN': r'(?:ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{36,255}',
            'GITHUB_CLASSIC_TOKEN': r'[a-f0-9]{40}',
            
            # 数据库连接字符串
            'DATABASE_URL': r'(?:mysql|postgresql|mongodb|redis)://[^:\s]*:[^@\s]*@[^/\s]+',
            'DB_PASSWORD': r'(?:password|pwd)=([^&\s\'\"]+)',
            
            # 加密相关
            'PRIVATE_KEY': r'-----BEGIN(?: (?:RSA|DSA|EC|OPENSSH))? PRIVATE KEY-----',
            'SSH_PRIVATE_KEY': r'-----BEGIN OPENSSH PRIVATE KEY-----',
            'JWT_SECRET': r'(?:jwt[_-]?secret|secret[_-]?key)[\'\"]?\s*[=:]\s*[\'\"]?([^\'\"\s]+)',
            
            # 通用密码模式
            'PASSWORD_FIELD': r'(?:password|passwd|pwd|pass)[\'\"]?\s*[=:]\s*[\'\"]([^\'\"]{8,})[\'\"]',
            'SECRET_FIELD': r'(?:secret|token|key|apikey)[\'\"]?\s*[=:]\s*[\'\"]([^\'\"]{16,})[\'\"]',
            
            # 信用卡号（简化版）
            'CREDIT_CARD': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            
            # IP地址和端口
            'IP_ADDRESS': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b',
        }
        
        # 文件扩展名白名单（避免扫描二进制文件）
        self.allowed_extensions = {
            '.py', '.js', '.ts', '.java', '.go', '.cpp', '.c', '.h', '.hpp',
            '.yaml', '.yml', '.json', '.xml', '.env', '.cfg', '.conf', '.ini',
            '.md', '.txt', '.sh', '.bash', '.ps1', '.sql', '.html', '.css'
        }
        
        # 排除的目录和文件
        self.exclude_patterns = {
            'node_modules', '__pycache__', '.git', '.idea', '.vscode',
            'venv', 'env', 'build', 'dist', 'target', 'bin', 'obj',
            '*.log', '*.tmp', '*.bak', '*.swp'
        }

    def is_binary_file(self, file_path: Path) -> bool:
        """判断是否为二进制文件"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except:
            return True

    def should_exclude_file(self, file_path: Path) -> bool:
        """判断是否应该排除该文件"""
        # 检查文件扩展名
        if file_path.suffix.lower() not in self.allowed_extensions:
            return True
            
        # 检查路径中的排除模式
        path_str = str(file_path).lower()
        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return True
                
        # 检查是否为二进制文件
        if self.is_binary_file(file_path):
            return True
            
        return False

    def scan_file(self, file_path: Path) -> List[Dict]:
        """扫描单个文件"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern_name, pattern in self.patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    finding = {
                        'file': str(file_path.relative_to(self.root_path)),
                        'pattern': pattern_name,
                        'line_number': content[:match.start()].count('\n') + 1,
                        'matched_text': match.group(0)[:100],  # 限制长度
                        'full_match': match.group(0),
                        'severity': self.get_severity(pattern_name)
                    }
                    findings.append(finding)
                    
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
            
        return findings

    def get_severity(self, pattern_name: str) -> str:
        """根据模式名称确定严重程度"""
        high_severity = {'PRIVATE_KEY', 'SSH_PRIVATE_KEY', 'AWS_ACCESS_KEY', 'AWS_SECRET_KEY'}
        medium_severity = {'DATABASE_URL', 'PASSWORD_FIELD', 'SECRET_FIELD', 'GITHUB_TOKEN'}
        
        if pattern_name in high_severity:
            return 'HIGH'
        elif pattern_name in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'

    def scan_directory(self, directory: Path = None) -> List[Dict]:
        """递归扫描目录"""
        if directory is None:
            directory = self.root_path
            
        all_findings = []
        
        for item in directory.iterdir():
            if item.is_file() and not self.should_exclude_file(item):
                self.scanned_files += 1
                findings = self.scan_file(item)
                all_findings.extend(findings)
                
                if self.scanned_files % 100 == 0:
                    print(f"已扫描 {self.scanned_files} 个文件...")
                    
            elif item.is_dir() and not self.should_exclude_file(item):
                sub_findings = self.scan_directory(item)
                all_findings.extend(sub_findings)
                
        return all_findings

    def generate_report(self) -> Dict:
        """生成扫描报告"""
        findings_by_severity = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
        findings_by_type = {}
        
        for finding in self.findings:
            severity = finding['severity']
            findings_by_severity[severity].append(finding)
            
            pattern = finding['pattern']
            if pattern not in findings_by_type:
                findings_by_type[pattern] = []
            findings_by_type[pattern].append(finding)
        
        report = {
            'scan_summary': {
                'total_files_scanned': self.scanned_files,
                'total_findings': len(self.findings),
                'findings_by_severity': {
                    severity: len(findings) 
                    for severity, findings in findings_by_severity.items()
                }
            },
            'findings_by_severity': findings_by_severity,
            'findings_by_type': findings_by_type,
            'recommendations': self.get_recommendations()
        }
        
        return report

    def get_recommendations(self) -> List[str]:
        """提供修复建议"""
        recommendations = [
            "1. 将敏感信息移至环境变量或专用配置管理工具",
            "2. 使用密钥管理服务（如HashiCorp Vault, AWS Secrets Manager）",
            "3. 实施.gitignore确保敏感文件不被提交",
            "4. 定期轮换密钥和密码",
            "5. 对敏感配置文件进行加密存储",
            "6. 建立代码审查流程检查敏感信息泄露",
            "7. 使用专门的密钥扫描工具作为CI/CD的一部分"
        ]
        return recommendations

    def run_scan(self) -> Dict:
        """执行完整扫描"""
        print("开始密钥扫描...")
        print(f"扫描路径: {self.root_path}")
        
        self.findings = self.scan_directory()
        
        print(f"\n扫描完成!")
        print(f"总文件数: {self.scanned_files}")
        print(f"发现问题: {len(self.findings)}")
        
        return self.generate_report()

def main():
    parser = argparse.ArgumentParser(description='密钥和敏感信息扫描器')
    parser.add_argument('--path', default='.', help='扫描路径')
    parser.add_argument('--output', help='输出报告文件路径')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    scanner = SecretScanner(args.path)
    report = scanner.run_scan()
    
    if args.format == 'json':
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output = format_text_report(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n报告已保存到: {args.output}")
    else:
        print("\n" + "="*50)
        print("扫描报告:")
        print("="*50)
        print(output)

def format_text_report(report: Dict) -> str:
    """格式化文本报告"""
    lines = []
    
    # 摘要
    summary = report['scan_summary']
    lines.append("密钥扫描报告摘要")
    lines.append("=" * 30)
    lines.append(f"扫描文件数: {summary['total_files_scanned']}")
    lines.append(f"发现问题总数: {summary['total_findings']}")
    lines.append("")
    
    # 按严重程度统计
    lines.append("按严重程度分类:")
    for severity, count in summary['findings_by_severity'].items():
        lines.append(f"  {severity}: {count}")
    lines.append("")
    
    # 详细发现
    lines.append("详细发现:")
    lines.append("-" * 20)
    
    for severity in ['HIGH', 'MEDIUM', 'LOW']:
        findings = report['findings_by_severity'][severity]
        if findings:
            lines.append(f"\n{severity} 级别问题 ({len(findings)} 个):")
            for finding in findings[:10]:  # 只显示前10个
                lines.append(f"  文件: {finding['file']}")
                lines.append(f"  行号: {finding['line_number']}")
                lines.append(f"  类型: {finding['pattern']}")
                lines.append(f"  内容: {finding['matched_text']}")
                lines.append("")
    
    # 建议
    lines.append("修复建议:")
    lines.append("-" * 15)
    for rec in report['recommendations']:
        lines.append(rec)
    
    return "\n".join(lines)

if __name__ == "__main__":
    main()