#!/usr/bin/env python3
"""
环境变量和配置文件敏感信息检查工具
专门检查常见的配置文件和环境变量设置
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class EnvConfigChecker:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.findings = []
        
        # 常见的配置文件名模式
        self.config_patterns = [
            r'.*\.env$', r'.*\.env\..*', r'config.*\.json$', r'config.*\.yaml$', 
            r'config.*\.yml$', r'.*config\.py$', r'settings.*\.py$', r'.*\.conf$',
            r'.*\.ini$', r'docker-compose.*\.yml$', r'docker-compose.*\.yaml$'
        ]
        
        # 敏感环境变量模式
        self.sensitive_env_vars = [
            r'^(DATABASE|DB)_(URL|PASSWORD|PASS|PWD)', 
            r'^REDIS_(URL|PASSWORD|PASS)',
            r'^MONGO(DB)?_(URL|PASSWORD|PASS)',
            r'^MYSQL_(URL|PASSWORD|PASS)',
            r'^POSTGRES_(URL|PASSWORD|PASS)',
            r'^AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)',
            r'^GOOGLE_(API_KEY|SERVICE_ACCOUNT)',
            r'^GITHUB_(TOKEN|PAT)',
            r'^GITLAB_(TOKEN|PAT)',
            r'^SLACK_(TOKEN|WEBHOOK)',
            r'^DISCORD_(TOKEN|WEBHOOK)',
            r'^API_KEY', r'^SECRET_KEY', r'^JWT_SECRET',
            r'^PRIVATE_KEY', r'^SSH_KEY',
            r'^ENCRYPTION_KEY', r'^CRYPTO_KEY'
        ]

    def check_env_files(self):
        """检查环境变量文件"""
        env_findings = []
        
        # 查找所有可能的环境文件
        for pattern in ['*.env', '*.env.*']:
            for env_file in self.root_path.rglob(pattern):
                if self._should_exclude_file(env_file):
                    continue
                    
                findings = self._scan_env_file(env_file)
                env_findings.extend(findings)
                
        return env_findings

    def check_config_files(self):
        """检查配置文件"""
        config_findings = []
        
        # 查找配置文件
        for pattern in ['*.json', '*.yaml', '*.yml', '*.conf', '*.ini']:
            for config_file in self.root_path.rglob(pattern):
                if self._should_exclude_file(config_file):
                    continue
                    
                findings = self._scan_config_file(config_file)
                config_findings.extend(findings)
                
        return config_findings

    def _should_exclude_file(self, file_path: Path) -> bool:
        """判断是否应该排除文件"""
        exclude_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env', 'build', 'dist'}
        return any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs)

    def _scan_env_file(self, file_path: Path) -> list:
        """扫描环境变量文件"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    # 检查是否包含敏感值
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        if self._is_sensitive_env_var(key) and value and not self._is_placeholder(value):
                            finding = {
                                'type': 'ENV_FILE',
                                'file': str(file_path.relative_to(self.root_path)),
                                'line': line_num,
                                'variable': key,
                                'value_preview': value[:50] + ('...' if len(value) > 50 else ''),
                                'severity': self._get_env_severity(key)
                            }
                            findings.append(finding)
                            
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
            
        return findings

    def _scan_config_file(self, file_path: Path) -> list:
        """扫描配置文件"""
        findings = []
        
        try:
            if file_path.suffix.lower() in ['.json']:
                findings = self._scan_json_config(file_path)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                findings = self._scan_yaml_config(file_path)
            elif file_path.suffix.lower() in ['.conf', '.ini']:
                findings = self._scan_ini_config(file_path)
                
        except Exception as e:
            print(f"无法解析配置文件 {file_path}: {e}")
            
        return findings

    def _scan_json_config(self, file_path: Path) -> list:
        """扫描JSON配置文件"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单的正则匹配，避免复杂的JSON解析
                sensitive_patterns = [
                    r'"(password|pwd|pass)":\s*"([^"]+)"',
                    r'"(api[_-]?key|secret[_-]?key)":\s*"([^"]+)"',
                    r'"(database[_-]?url|db[_-]?url)":\s*"([^"]+)"'
                ]
                
                for pattern in sensitive_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        finding = {
                            'type': 'CONFIG_JSON',
                            'file': str(file_path.relative_to(self.root_path)),
                            'line': content[:match.start()].count('\n') + 1,
                            'key': match.group(1),
                            'value_preview': match.group(2)[:50],
                            'severity': 'HIGH'
                        }
                        findings.append(finding)
                        
        except Exception as e:
            print(f"JSON解析错误 {file_path}: {e}")
            
        return findings

    def _scan_yaml_config(self, file_path: Path) -> list:
        """扫描YAML配置文件"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                sensitive_keys = ['password', 'pass', 'pwd', 'api_key', 'secret', 'token']
                
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    if ':' in line:
                        key_part, value_part = line.split(':', 1)
                        key = key_part.strip().rstrip(':')
                        value = value_part.strip().strip('"\'')
                        
                        if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                            if value and not value.startswith('${') and value != '~':
                                finding = {
                                    'type': 'CONFIG_YAML',
                                    'file': str(file_path.relative_to(self.root_path)),
                                    'line': line_num,
                                    'key': key,
                                    'value_preview': value[:50],
                                    'severity': 'HIGH'
                                }
                                findings.append(finding)
                                
        except Exception as e:
            print(f"YAML解析错误 {file_path}: {e}")
            
        return findings

    def _scan_ini_config(self, file_path: Path) -> list:
        """扫描INI配置文件"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                current_section = ''
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    
                    # 检查节标题
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        continue
                        
                    # 检查键值对
                    if '=' in line and not line.startswith('#') and not line.startswith(';'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        if self._is_sensitive_config_key(key) and value:
                            finding = {
                                'type': 'CONFIG_INI',
                                'file': str(file_path.relative_to(self.root_path)),
                                'line': line_num,
                                'section': current_section,
                                'key': key,
                                'value_preview': value[:50],
                                'severity': 'HIGH'
                            }
                            findings.append(finding)
                            
        except Exception as e:
            print(f"INI解析错误 {file_path}: {e}")
            
        return findings

    def _is_sensitive_env_var(self, var_name: str) -> bool:
        """判断环境变量是否敏感"""
        var_name_upper = var_name.upper()
        for pattern in self.sensitive_env_vars:
            if re.match(pattern, var_name_upper):
                return True
        return False

    def _is_sensitive_config_key(self, key_name: str) -> bool:
        """判断配置键是否敏感"""
        sensitive_keys = [
            'password', 'pwd', 'pass', 'secret', 'key', 'token', 'apikey',
            'database_url', 'db_url', 'connection_string'
        ]
        key_lower = key_name.lower()
        return any(sensitive_key in key_lower for sensitive_key in sensitive_keys)

    def _is_placeholder(self, value: str) -> bool:
        """判断值是否为占位符"""
        placeholders = [
            '${', '#{', '<!--', '-->', 'your-', 'example', 'placeholder',
            'changeme', 'TODO', 'FIXME', 'dummy', 'test'
        ]
        value_lower = value.lower()
        return any(placeholder in value_lower for placeholder in placeholders)

    def _get_env_severity(self, var_name: str) -> str:
        """根据环境变量名确定严重程度"""
        critical_vars = ['AWS_SECRET_ACCESS_KEY', 'PRIVATE_KEY', 'SSH_KEY']
        high_vars = ['PASSWORD', 'SECRET', 'API_KEY', 'TOKEN']
        
        var_name_upper = var_name.upper()
        if any(critical in var_name_upper for critical in critical_vars):
            return 'CRITICAL'
        elif any(high in var_name_upper for high in high_vars):
            return 'HIGH'
        else:
            return 'MEDIUM'

    def run_check(self) -> dict:
        """执行完整检查"""
        print("开始环境变量和配置文件检查...")
        
        # 检查环境文件
        env_findings = self.check_env_files()
        print(f"发现环境文件敏感信息: {len(env_findings)} 个")
        
        # 检查配置文件
        config_findings = self.check_config_files()
        print(f"发现配置文件敏感信息: {len(config_findings)} 个")
        
        all_findings = env_findings + config_findings
        
        # 分类统计
        by_type = defaultdict(list)
        by_severity = defaultdict(list)
        
        for finding in all_findings:
            by_type[finding['type']].append(finding)
            by_severity[finding['severity']].append(finding)
        
        report = {
            'summary': {
                'total_findings': len(all_findings),
                'by_type': {k: len(v) for k, v in by_type.items()},
                'by_severity': {k: len(v) for k, v in by_severity.items()}
            },
            'findings': all_findings,
            'recommendations': self._generate_recommendations()
        }
        
        return report

    def _generate_recommendations(self) -> list:
        """生成修复建议"""
        return [
            "环境变量安全建议:",
            "1. 使用.dockerignore排除.env文件",
            "2. 在生产环境中使用密钥管理服务",
            "3. 实施环境变量注入而非硬编码",
            "4. 定期轮换敏感环境变量",
            "",
            "配置文件安全建议:",
            "1. 使用模板文件和占位符",
            "2. 将敏感配置外部化",
            "3. 实施配置文件权限控制",
            "4. 使用配置管理工具"
        ]

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='环境变量和配置文件安全检查')
    parser.add_argument('--path', default='.', help='项目路径')
    parser.add_argument('--output', help='输出文件')
    
    args = parser.parse_args()
    
    checker = EnvConfigChecker(args.path)
    report = checker.run_check()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到: {args.output}")
    else:
        print("\n=== 检查结果 ===")
        print(f"总计发现: {report['summary']['total_findings']} 个敏感信息")
        print("\n按类型分布:")
        for type_name, count in report['summary']['by_type'].items():
            print(f"  {type_name}: {count}")
        print("\n按严重程度分布:")
        for severity, count in report['summary']['by_severity'].items():
            print(f"  {severity}: {count}")

if __name__ == "__main__":
    main()