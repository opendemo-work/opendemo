#!/usr/bin/env python3
"""
综合性密钥和敏感信息检查工具
针对大型项目进行深度扫描
"""

import os
import re
import json
import base64
import hashlib
from pathlib import Path
from collections import defaultdict
import argparse

class ComprehensiveSecretChecker:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.findings = []
        self.file_count = 0
        self.directory_count = 0
        
        # 扩展的敏感信息模式
        self.patterns = {
            # 各种API密钥
            'AWS_KEYS': [
                r'(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}',
                r'(?i)(aws_access_key_id|aws_secret_access_key).*[=\'\"]([^\'\"\s]+)'
            ],
            'GOOGLE_KEYS': [
                r'AIza[0-9A-Za-z\\-_]{35}',
                r'[0-9]+-[a-zA-Z0-9_]{32}\.apps\.googleusercontent\.com'
            ],
            'GITHUB_TOKENS': [
                r'(?:ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{36,255}',
                r'[a-f0-9]{40}'
            ],
            'AZURE_KEYS': [
                r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
            ],
            
            # 数据库连接
            'DATABASE_CONNECTIONS': [
                r'(mysql|postgresql|mongodb|redis|mssql|oracle)://[^:\s]*:[^@\s]*@[^/\s]+',
                r'(server|host)=([^;]+);.*?(password|pwd)=([^;]+)',
                r'jdbc:(mysql|postgresql|sqlserver)://[^:]+:[^@]+@[^/]+'
            ],
            
            # 加密和认证
            'PRIVATE_KEYS': [
                r'-----BEGIN(?: (?:RSA|DSA|EC|OPENSSH))? PRIVATE KEY-----[\s\S]*?-----END(?: (?:RSA|DSA|EC|OPENSSH))? PRIVATE KEY-----',
                r'-----BEGIN CERTIFICATE-----[\s\S]*?-----END CERTIFICATE-----'
            ],
            'JWT_SECRETS': [
                r'(?:jwt[_-]?(?:secret|key)|secret[_-]?key)[\'\"]?\s*[=:]\s*[\'\"]([^\'\"\s]+)',
                r'HS256.*[\'\"]([a-zA-Z0-9+/=]{32,})[\'\"]'
            ],
            
            # 密码字段
            'PASSWORD_FIELDS': [
                r'(?:password|passwd|pwd|pass)[\'\"]?\s*[=:]\s*[\'\"]([^\'\"&\s]{8,})[\'\"]',
                r'"(password)":\s*"([^"]{8,})"',
                r"'(password)':\s*'([^']{8,})'"
            ],
            
            # 通用密钥模式
            'GENERIC_SECRETS': [
                r'(?:api[_-]?key|secret|token|access[_-]?key)[\'\"]?\s*[=:]\s*[\'\"]([^\'\"\s]{16,})[\'\"]',
                r'"(api[_-]?key|secret|token)":\s*"([^"]{16,})"',
                r"'(api[_-]?key|secret|token)':\s*'([^']{16,})'"
            ],
            
            # 敏感URL和端点
            'SENSITIVE_ENDPOINTS': [
                r'https?://[^/\s]+:[0-9]{4,}/[^?\s]*[?&](?:key|token|secret|password)=[^&\s]+',
                r'(internal|private|admin)\.[^/\s]+\.[^/\s]+'
            ]
        }
        
        # 支持的文件类型
        self.supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.swift', '.kt', '.rs', '.scala', '.groovy',
            '.yaml', '.yml', '.json', '.xml', '.toml', '.ini', '.cfg', '.conf',
            '.env', '.env.local', '.env.production', '.env.development',
            '.md', '.txt', '.sh', '.bash', '.zsh', '.ps1', '.bat', '.cmd',
            '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.vue', '.svelte'
        }
        
        # 排除目录
        self.exclude_dirs = {
            'node_modules', '__pycache__', '.git', '.svn', '.hg',
            '.idea', '.vscode', '.settings', 
            'venv', 'env', 'virtualenv', '.venv',
            'build', 'dist', 'target', 'out', 'bin', 'obj',
            'coverage', 'htmlcov', '.pytest_cache',
            'logs', 'log', '*.log',
            'tmp', 'temp', '.tmp', '.temp',
            'backup', 'backups', '.backup'
        }

    def is_excluded_path(self, path: Path) -> bool:
        """检查路径是否应该被排除"""
        path_parts = set(path.parts)
        
        # 检查目录排除
        if path_parts & self.exclude_dirs:
            return True
            
        # 检查文件扩展名
        if path.is_file() and path.suffix.lower() not in self.supported_extensions:
            return True
            
        return False

    def is_binary_content(self, content: str) -> bool:
        """检查内容是否可能包含二进制数据"""
        try:
            # 尝试解码为UTF-8，如果失败可能是二进制
            content.encode('utf-8')
            return False
        except UnicodeEncodeError:
            return True

    def scan_file_for_secrets(self, file_path: Path) -> list:
        """扫描文件中的敏感信息"""
        findings = []
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 跳过可能的二进制文件
            if self.is_binary_content(content) and len(content) > 1000:
                return findings
                
            # 按类别扫描
            for category, patterns in self.patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
                    for match in matches:
                        # 获取行号
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # 提取上下文
                        lines = content.split('\n')
                        context_start = max(0, line_num - 3)
                        context_end = min(len(lines), line_num + 2)
                        context = '\n'.join(lines[context_start:context_end])
                        
                        finding = {
                            'category': category,
                            'file': str(file_path.relative_to(self.root_path)),
                            'line_number': line_num,
                            'matched_text': match.group(0)[:200],  # 限制长度
                            'full_match': match.group(0),
                            'context': context.strip(),
                            'severity': self._get_severity(category)
                        }
                        findings.append(finding)
                        
        except Exception as e:
            print(f"警告: 无法扫描文件 {file_path}: {e}")
            
        return findings

    def _get_severity(self, category: str) -> str:
        """根据类别确定严重程度"""
        severity_map = {
            'PRIVATE_KEYS': 'CRITICAL',
            'AWS_KEYS': 'HIGH',
            'DATABASE_CONNECTIONS': 'HIGH',
            'GITHUB_TOKENS': 'HIGH',
            'PASSWORD_FIELDS': 'HIGH',
            'JWT_SECRETS': 'MEDIUM',
            'GENERIC_SECRETS': 'MEDIUM',
            'GOOGLE_KEYS': 'MEDIUM',
            'AZURE_KEYS': 'MEDIUM',
            'SENSITIVE_ENDPOINTS': 'LOW'
        }
        return severity_map.get(category, 'LOW')

    def walk_project(self) -> tuple:
        """遍历项目目录"""
        findings = []
        file_stats = defaultdict(int)
        
        print(f"开始扫描目录: {self.root_path}")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            # 移除需要排除的目录
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs and not d.startswith('.')]
            
            # 处理当前目录下的文件
            for file in files:
                file_path = root_path / file
                
                if self.is_excluded_path(file_path):
                    continue
                    
                self.file_count += 1
                file_stats[file_path.suffix] += 1
                
                # 显示进度
                if self.file_count % 500 == 0:
                    print(f"已扫描 {self.file_count} 个文件...")
                
                # 扫描文件
                file_findings = self.scan_file_for_secrets(file_path)
                findings.extend(file_findings)
        
        return findings, dict(file_stats)

    def generate_comprehensive_report(self, findings: list, file_stats: dict) -> dict:
        """生成综合报告"""
        # 按严重程度分组
        findings_by_severity = defaultdict(list)
        findings_by_category = defaultdict(list)
        findings_by_file = defaultdict(list)
        
        for finding in findings:
            findings_by_severity[finding['severity']].append(finding)
            findings_by_category[finding['category']].append(finding)
            findings_by_file[finding['file']].append(finding)
        
        # 统计信息
        severity_counts = {severity: len(items) for severity, items in findings_by_severity.items()}
        category_counts = {category: len(items) for category, items in findings_by_category.items()}
        
        report = {
            'scan_metadata': {
                'root_path': str(self.root_path),
                'total_files_scanned': self.file_count,
                'total_findings': len(findings),
                'scan_timestamp': __import__('datetime').datetime.now().isoformat()
            },
            'statistics': {
                'by_severity': severity_counts,
                'by_category': category_counts,
                'file_types': file_stats
            },
            'findings': {
                'by_severity': dict(findings_by_severity),
                'by_category': dict(findings_by_category),
                'by_file': dict(findings_by_file)
            },
            'security_assessment': self._generate_security_assessment(severity_counts),
            'remediation_guidance': self._generate_remediation_guidance(findings)
        }
        
        return report

    def _generate_security_assessment(self, severity_counts: dict) -> dict:
        """生成安全评估"""
        total_issues = sum(severity_counts.values())
        
        assessment = {
            'risk_level': 'LOW',
            'summary': '',
            'details': []
        }
        
        if severity_counts.get('CRITICAL', 0) > 0:
            assessment['risk_level'] = 'CRITICAL'
            assessment['summary'] = '发现严重安全风险'
            assessment['details'].append(f"发现 {severity_counts['CRITICAL']} 个严重问题")
        elif severity_counts.get('HIGH', 0) > 5:
            assessment['risk_level'] = 'HIGH'
            assessment['summary'] = '存在较高安全风险'
            assessment['details'].append(f"发现 {severity_counts['HIGH']} 个高风险问题")
        elif total_issues > 20:
            assessment['risk_level'] = 'MEDIUM'
            assessment['summary'] = '存在中等安全风险'
            assessment['details'].append(f"共发现 {total_issues} 个潜在问题")
        else:
            assessment['risk_level'] = 'LOW'
            assessment['summary'] = '安全状况良好'
            assessment['details'].append(f"发现 {total_issues} 个低风险问题")
            
        return assessment

    def _generate_remediation_guidance(self, findings: list) -> list:
        """生成修复指导"""
        guidance = [
            "安全修复建议:",
            "===============",
            "1. 立即行动项:",
            "   - 将所有硬编码的密钥移至环境变量或密钥管理系统",
            "   - 撤销已泄露的访问令牌和API密钥",
            "   - 更新受影响的密码和凭证",
            "",
            "2. 预防措施:",
            "   - 实施.gitignore确保敏感文件不被版本控制",
            "   - 使用专用的密钥管理服务（如Vault, AWS Secrets Manager）",
            "   - 建立代码审查流程检查敏感信息",
            "   - 定期轮换密钥和证书",
            "",
            "3. 监控和检测:",
            "   - 在CI/CD管道中集成密钥扫描工具",
            "   - 设置安全监控告警",
            "   - 定期进行安全审计"
        ]
        
        # 根据发现的具体问题提供针对性建议
        categories_found = set(f['category'] for f in findings)
        
        if 'PRIVATE_KEYS' in categories_found:
            guidance.extend([
                "",
                "私钥相关建议:",
                "- 立即撤销并重新生成私钥",
                "- 使用SSH代理避免私钥暴露",
                "- 考虑使用硬件安全模块(HSM)"
            ])
            
        if 'DATABASE_CONNECTIONS' in categories_found:
            guidance.extend([
                "",
                "数据库安全建议:",
                "- 使用连接池和最小权限原则",
                "- 实施数据库防火墙",
                "- 启用数据库审计日志"
            ])
        
        return guidance

    def run_comprehensive_check(self) -> dict:
        """执行全面检查"""
        print("启动综合性密钥检查...")
        
        # 执行扫描
        findings, file_stats = self.walk_project()
        self.findings = findings
        
        print(f"\n扫描完成!")
        print(f"总文件数: {self.file_count}")
        print(f"发现问题: {len(findings)}")
        
        # 生成报告
        report = self.generate_comprehensive_report(findings, file_stats)
        return report

def main():
    parser = argparse.ArgumentParser(description='综合性密钥和敏感信息检查工具')
    parser.add_argument('--path', default='.', help='项目根路径')
    parser.add_argument('--output', help='输出报告文件')
    parser.add_argument('--format', choices=['json', 'html'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    checker = ComprehensiveSecretChecker(args.path)
    report = checker.run_comprehensive_check()
    
    # 输出结果
    if args.format == 'json':
        output_content = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output_content = generate_html_report(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"\n报告已保存到: {args.output}")
    else:
        print("\n" + "="*60)
        print("扫描结果摘要:")
        print("="*60)
        print(f"风险等级: {report['security_assessment']['risk_level']}")
        print(f"总文件数: {report['scan_metadata']['total_files_scanned']}")
        print(f"发现问题: {report['scan_metadata']['total_findings']}")
        print("\n按严重程度分布:")
        for severity, count in report['statistics']['by_severity'].items():
            print(f"  {severity}: {count}")

def generate_html_report(report: dict) -> str:
    """生成HTML格式报告"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>密钥扫描报告</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            .section { margin: 20px 0; }
            .finding { border: 1px solid #ddd; margin: 10px 0; padding: 10px; border-radius: 3px; }
            .critical { border-color: #ff0000; background: #ffe6e6; }
            .high { border-color: #ff6600; background: #fff0e6; }
            .medium { border-color: #ffcc00; background: #fff8e6; }
            .low { border-color: #00cc00; background: #e6ffe6; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
            .stat-card { background: #f8f9fa; padding: 15px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>密钥扫描报告</h1>
            <p><strong>项目路径:</strong> {root_path}</p>
            <p><strong>扫描时间:</strong> {timestamp}</p>
            <p><strong>风险等级:</strong> <span style="color: {risk_color};">{risk_level}</span></p>
        </div>
        
        <div class="section">
            <h2>统计概览</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>文件统计</h3>
                    <p>总文件数: {total_files}</p>
                    <p>发现问题: {total_findings}</p>
                </div>
                <div class="stat-card">
                    <h3>严重程度分布</h3>
                    {severity_stats}
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>详细发现</h2>
            {detailed_findings}
        </div>
    </body>
    </html>
    """
    
    # 填充模板数据
    risk_colors = {
        'CRITICAL': '#ff0000',
        'HIGH': '#ff6600', 
        'MEDIUM': '#ffcc00',
        'LOW': '#00cc00'
    }
    
    severity_stats = ""
    for severity, count in report['statistics']['by_severity'].items():
        color = risk_colors.get(severity, '#666666')
        severity_stats += f'<p style="color: {color}">{severity}: {count}</p>'
    
    detailed_findings = ""
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        findings = report['findings']['by_severity'].get(severity, [])
        if findings:
            detailed_findings += f"<h3>{severity} 级别问题 ({len(findings)} 个)</h3>"
            for finding in findings[:5]:  # 只显示前5个
                css_class = severity.lower()
                detailed_findings += f"""
                <div class="finding {css_class}">
                    <strong>文件:</strong> {finding['file']}<br>
                    <strong>行号:</strong> {finding['line_number']}<br>
                    <strong>匹配内容:</strong> {finding['matched_text']}
                </div>
                """
    
    return html_template.format(
        root_path=report['scan_metadata']['root_path'],
        timestamp=report['scan_metadata']['scan_timestamp'],
        risk_level=report['security_assessment']['risk_level'],
        risk_color=risk_colors.get(report['security_assessment']['risk_level'], '#666666'),
        total_files=report['scan_metadata']['total_files_scanned'],
        total_findings=report['scan_metadata']['total_findings'],
        severity_stats=severity_stats,
        detailed_findings=detailed_findings
    )

if __name__ == "__main__":
    main()