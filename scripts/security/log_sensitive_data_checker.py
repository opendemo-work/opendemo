#!/usr/bin/env python3
"""
日志文件敏感数据检查工具
检查日志文件中可能包含的敏感信息
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class LogSensitiveDataChecker:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.findings = []
        
        # 日志文件模式
        self.log_patterns = [
            r'.*\.log$', r'.*\.out$', r'.*\.err$', r'.*\.txt$',
            r'output.*', r'error.*', r'debug.*', r'trace.*'
        ]
        
        # 敏感数据模式
        self.sensitive_patterns = {
            'EMAIL_ADDRESSES': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'IP_ADDRESSES': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'PHONE_NUMBERS': r'\b\d{3}-\d{3}-\d{4}\b|\b\d{10}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b',
            'CREDIT_CARDS': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'SSN_NUMBERS': r'\b\d{3}-\d{2}-\d{4}\b',
            'API_KEYS': r'\b[A-Za-z0-9]{32,}\b',
            'PASSWORDS': r'(?i)(password|pwd|pass)\s*[=:]\s*[^\s]+',
            'TOKENS': r'(?i)(token|auth|bearer)\s*[=:]\s*[^\s]+',
            'PRIVATE_KEYS': r'-----BEGIN.*PRIVATE.*KEY-----',
            'DATABASE_URLS': r'(mysql|postgresql|mongodb|redis)://[^\s]+',
            'AWS_KEYS': r'\b(AKIA|AGPA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b'
        }

    def find_log_files(self) -> list:
        """查找日志文件"""
        log_files = []
        
        for root, dirs, files in os.walk(self.root_path):
            # 排除常见目录
            exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'build'}
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if self._is_log_file(file_path):
                    log_files.append(file_path)
                    
        return log_files

    def _is_log_file(self, file_path: Path) -> bool:
        """判断是否为日志文件"""
        filename = file_path.name.lower()
        
        # 检查文件扩展名和名称
        for pattern in self.log_patterns:
            if re.match(pattern, filename):
                return True
                
        # 检查文件内容特征（简单采样）
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                sample = f.read(1000)  # 读取前1000字符
                
                # 日志文件常见特征
                log_indicators = ['INFO', 'ERROR', 'DEBUG', 'WARN', 'TRACE', 
                                'Exception', 'Stack trace', 'at ', '.java:', '.py:']
                
                if any(indicator in sample for indicator in log_indicators):
                    return True
                    
        except:
            pass
            
        return False

    def scan_log_file(self, log_file: Path) -> list:
        """扫描日志文件中的敏感数据"""
        findings = []
        
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                        
                    # 检查每种敏感数据模式
                    for pattern_name, pattern in self.sensitive_patterns.items():
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            finding = {
                                'file': str(log_file.relative_to(self.root_path)),
                                'line_number': line_num,
                                'pattern_type': pattern_name,
                                'matched_text': match.group(0)[:100],  # 限制长度
                                'context': line[:200],  # 提供上下文
                                'severity': self._get_severity(pattern_name)
                            }
                            findings.append(finding)
                            
        except Exception as e:
            print(f"无法读取日志文件 {log_file}: {e}")
            
        return findings

    def _get_severity(self, pattern_type: str) -> str:
        """根据模式类型确定严重程度"""
        critical_patterns = ['PRIVATE_KEYS']
        high_patterns = ['PASSWORDS', 'TOKENS', 'DATABASE_URLS', 'AWS_KEYS']
        medium_patterns = ['EMAIL_ADDRESSES', 'SSN_NUMBERS', 'CREDIT_CARDS']
        low_patterns = ['IP_ADDRESSES', 'PHONE_NUMBERS', 'API_KEYS']
        
        if pattern_type in critical_patterns:
            return 'CRITICAL'
        elif pattern_type in high_patterns:
            return 'HIGH'
        elif pattern_type in medium_patterns:
            return 'MEDIUM'
        else:
            return 'LOW'

    def check_output_directories(self) -> list:
        """检查输出目录中的敏感文件"""
        findings = []
        output_dirs = ['output', 'logs', 'temp', 'tmp', 'reports']
        
        for output_dir in output_dirs:
            dir_path = self.root_path / output_dir
            if dir_path.exists():
                for file_path in dir_path.rglob('*'):
                    if file_path.is_file() and not self._should_exclude_output_file(file_path):
                        file_findings = self._scan_output_file(file_path)
                        findings.extend(file_findings)
                        
        return findings

    def _should_exclude_output_file(self, file_path: Path) -> bool:
        """判断是否应该排除输出文件"""
        exclude_extensions = {'.gitkeep', '.DS_Store', '.md'}
        return file_path.suffix.lower() in exclude_extensions

    def _scan_output_file(self, file_path: Path) -> list:
        """扫描输出文件"""
        findings = []
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # 检查敏感模式
            for pattern_name, pattern in self.sensitive_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    # 计算行号
                    line_num = content[:match.start()].count('\n') + 1
                    
                    finding = {
                        'file': str(file_path.relative_to(self.root_path)),
                        'line_number': line_num,
                        'pattern_type': pattern_name,
                        'matched_text': match.group(0)[:100],
                        'severity': self._get_severity(pattern_name)
                    }
                    findings.append(finding)
                    
        except Exception as e:
            print(f"无法扫描输出文件 {file_path}: {e}")
            
        return findings

    def run_check(self) -> dict:
        """执行完整检查"""
        print("开始日志和输出文件敏感数据检查...")
        
        all_findings = []
        
        # 检查日志文件
        log_files = self.find_log_files()
        print(f"发现日志文件: {len(log_files)} 个")
        
        for log_file in log_files:
            findings = self.scan_log_file(log_file)
            all_findings.extend(findings)
            
        # 检查输出目录
        output_findings = self.check_output_directories()
        all_findings.extend(output_findings)
        print(f"输出目录敏感数据发现: {len(output_findings)} 个")
        
        # 分类统计
        by_file = defaultdict(list)
        by_pattern = defaultdict(list)
        by_severity = defaultdict(list)
        
        for finding in all_findings:
            by_file[finding['file']].append(finding)
            by_pattern[finding['pattern_type']].append(finding)
            by_severity[finding['severity']].append(finding)
        
        report = {
            'summary': {
                'total_findings': len(all_findings),
                'log_files_checked': len(log_files),
                'files_with_sensitive_data': len(by_file),
                'by_pattern': {k: len(v) for k, v in by_pattern.items()},
                'by_severity': {k: len(v) for k, v in by_severity.items()}
            },
            'findings': all_findings,
            'recommendations': self._generate_recommendations()
        }
        
        return report

    def _generate_recommendations(self) -> list:
        """生成修复建议"""
        return [
            "日志安全管理建议:",
            "==================",
            "1. 日志脱敏处理:",
            "   - 实施日志过滤器，自动屏蔽敏感数据",
            "   - 使用日志脱敏库处理个人信息",
            "   - 配置日志级别，避免调试信息泄露",
            "",
            "2. 访问控制:",
            "   - 限制日志文件访问权限",
            "   - 实施日志文件加密存储",
            "   - 定期清理过期日志文件",
            "",
            "3. 监控和审计:",
            "   - 设置日志访问审计",
            "   - 实施异常日志监控",
            "   - 定期进行日志安全审查",
            "",
            "4. 输出文件管理:",
            "   - 避免在输出文件中记录敏感信息",
            "   - 实施输出文件内容审查机制",
            "   - 使用临时文件处理敏感数据"
        ]

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='日志文件敏感数据检查工具')
    parser.add_argument('--path', default='.', help='项目路径')
    parser.add_argument('--output', help='输出报告文件')
    
    args = parser.parse_args()
    
    checker = LogSensitiveDataChecker(args.path)
    report = checker.run_check()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到: {args.output}")
    else:
        print("\n=== 检查结果 ===")
        print(f"总计发现敏感数据: {report['summary']['total_findings']} 个")
        print(f"检查日志文件数: {report['summary']['log_files_checked']}")
        print(f"含敏感数据文件数: {report['summary']['files_with_sensitive_data']}")
        
        print("\n按模式类型分布:")
        for pattern, count in report['summary']['by_pattern'].items():
            print(f"  {pattern}: {count}")
            
        print("\n按严重程度分布:")
        for severity, count in report['summary']['by_severity'].items():
            print(f"  {severity}: {count}")

if __name__ == "__main__":
    main()