"""
验证管理器模块

负责验证demo的可执行性。
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


class DemoVerifier:
    """Demo验证器类"""
    
    def __init__(self, config_service):
        """
        初始化验证器
        
        Args:
            config_service: 配置服务实例
        """
        self.config = config_service
    
    def verify(self, demo_path: Path, language: str) -> Dict[str, Any]:
        """
        验证demo
        
        Args:
            demo_path: demo路径
            language: 编程语言
            
        Returns:
            验证结果字典
        """
        if not self.config.get('enable_verification', False):
            return {
                'verified': False,
                'skipped': True,
                'message': 'Verification is disabled'
            }
        
        verification_method = self.config.get('verification_method', 'venv')
        
        if language.lower() == 'python':
            return self._verify_python(demo_path, verification_method)
        elif language.lower() == 'java':
            return self._verify_java(demo_path)
        else:
            return {
                'verified': False,
                'error': f'Verification not supported for {language}'
            }
    
    def _verify_python(self, demo_path: Path, method: str = 'venv') -> Dict[str, Any]:
        """
        验证Python demo
        
        Args:
            demo_path: demo路径
            method: 验证方法
            
        Returns:
            验证结果
        """
        result = {
            'verified': False,
            'method': method,
            'steps': [],
            'outputs': [],
            'errors': []
        }
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            try:
                # 复制demo到临时目录
                demo_copy = temp_path / 'demo'
                shutil.copytree(demo_path, demo_copy)
                result['steps'].append('Copied demo to temp directory')
                
                # 创建虚拟环境
                venv_path = temp_path / 'venv'
                self._create_venv(venv_path)
                result['steps'].append('Created virtual environment')
                
                # 安装依赖
                requirements_file = demo_copy / 'requirements.txt'
                if requirements_file.exists():
                    success, output = self._install_dependencies(venv_path, requirements_file)
                    result['steps'].append('Installed dependencies')
                    result['outputs'].append(output)
                    
                    if not success:
                        result['errors'].append('Failed to install dependencies')
                        return result
                
                # 执行代码文件
                code_dir = demo_copy / 'code'
                if code_dir.exists():
                    for py_file in code_dir.glob('*.py'):
                        success, output, error = self._run_python_file(venv_path, py_file)
                        result['steps'].append(f'Executed {py_file.name}')
                        
                        if output:
                            result['outputs'].append(f"=== {py_file.name} ===\n{output}")
                        
                        if not success:
                            result['errors'].append(f"Execution failed for {py_file.name}: {error}")
                            return result
                
                # 如果所有步骤成功
                result['verified'] = True
                result['message'] = 'All verification steps passed'
                
            except Exception as e:
                result['errors'].append(str(e))
                logger.error(f"Verification failed: {e}")
        
        return result
    
    def _create_venv(self, venv_path: Path) -> bool:
        """创建Python虚拟环境"""
        try:
            subprocess.run(
                [sys.executable, '-m', 'venv', str(venv_path)],
                check=True,
                capture_output=True,
                timeout=60
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create venv: {e}")
            return False
    
    def _install_dependencies(self, venv_path: Path, requirements_file: Path) -> tuple:
        """
        安装Python依赖
        
        Returns:
            (成功, 输出)
        """
        try:
            # 确定pip路径
            if sys.platform == 'win32':
                pip_path = venv_path / 'Scripts' / 'pip.exe'
            else:
                pip_path = venv_path / 'bin' / 'pip'
            
            result = subprocess.run(
                [str(pip_path), 'install', '-r', str(requirements_file)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return result.returncode == 0, result.stdout
            
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False, str(e)
    
    def _run_python_file(self, venv_path: Path, py_file: Path) -> tuple:
        """
        运行Python文件
        
        Returns:
            (成功, 输出, 错误)
        """
        try:
            # 确定python路径
            if sys.platform == 'win32':
                python_path = venv_path / 'Scripts' / 'python.exe'
            else:
                python_path = venv_path / 'bin' / 'python'
            
            timeout = self.config.get('verification_timeout', 300)
            
            result = subprocess.run(
                [str(python_path), str(py_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=py_file.parent
            )
            
            success = result.returncode == 0
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, '', 'Execution timeout'
        except Exception as e:
            logger.error(f"Failed to run {py_file}: {e}")
            return False, '', str(e)
    
    def _verify_java(self, demo_path: Path) -> Dict[str, Any]:
        """
        验证Java demo
        
        Args:
            demo_path: demo路径
            
        Returns:
            验证结果
        """
        # Java验证的简化实现
        result = {
            'verified': False,
            'method': 'java',
            'steps': [],
            'outputs': [],
            'errors': ['Java verification not fully implemented yet']
        }
        
        return result
    
    def generate_report(self, verification_result: Dict[str, Any]) -> str:
        """
        生成验证报告
        
        Args:
            verification_result: 验证结果
            
        Returns:
            报告文本
        """
        lines = ['# 验证报告\n']
        
        if verification_result.get('skipped'):
            lines.append(f"状态: 已跳过 - {verification_result.get('message')}\n")
            return '\n'.join(lines)
        
        verified = verification_result.get('verified', False)
        status = '✓ 通过' if verified else '✗ 失败'
        lines.append(f"状态: {status}\n")
        
        method = verification_result.get('method', 'unknown')
        lines.append(f"方法: {method}\n")
        
        # 步骤
        steps = verification_result.get('steps', [])
        if steps:
            lines.append('\n## 执行步骤\n')
            for i, step in enumerate(steps, 1):
                lines.append(f"{i}. {step}")
        
        # 输出
        outputs = verification_result.get('outputs', [])
        if outputs:
            lines.append('\n## 执行输出\n')
            for output in outputs:
                lines.append(f"```\n{output}\n```\n")
        
        # 错误
        errors = verification_result.get('errors', [])
        if errors:
            lines.append('\n## 错误信息\n')
            for error in errors:
                lines.append(f"- {error}")
        
        return '\n'.join(lines)
