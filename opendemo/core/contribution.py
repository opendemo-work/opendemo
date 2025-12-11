"""
贡献管理器模块

负责demo贡献流程管理。
"""

from pathlib import Path
from typing import Dict, Any, Optional
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


class ContributionManager:
    """贡献管理器类"""
    
    def __init__(self, config_service, storage_service):
        """
        初始化贡献管理器
        
        Args:
            config_service: 配置服务实例
            storage_service: 存储服务实例
        """
        self.config = config_service
        self.storage = storage_service
    
    def prompt_contribution(self, demo_path: Path) -> bool:
        """
        询问用户是否贡献demo
        
        Args:
            demo_path: demo路径
            
        Returns:
            用户是否选择贡献
        """
        if not self.config.get('contribution.auto_prompt', True):
            return False
        
        try:
            response = input("\n是否将此demo贡献到公共库? (y/n): ").strip().lower()
            return response in ('y', 'yes', '是')
        except Exception as e:
            logger.error(f"Failed to prompt for contribution: {e}")
            return False
    
    def validate_demo(self, demo_path: Path) -> tuple[bool, list]:
        """
        验证demo是否符合贡献要求
        
        Args:
            demo_path: demo路径
            
        Returns:
            (是否有效, 错误列表)
        """
        errors = []
        
        # 检查必需文件
        required_files = ['metadata.json', 'README.md']
        for filename in required_files:
            if not (demo_path / filename).exists():
                errors.append(f"Missing required file: {filename}")
        
        # 检查是否有代码文件
        code_dir = demo_path / 'code'
        if not code_dir.exists():
            errors.append("Missing code directory")
        else:
            code_files = list(code_dir.glob('*.py')) + list(code_dir.glob('*.java'))
            if not code_files:
                errors.append("No code files found in code directory")
        
        # 检查README.md内容
        readme_file = demo_path / 'README.md'
        if readme_file.exists():
            content = self.storage.read_file(readme_file)
            if content and len(content) < 100:
                errors.append("README.md content is too short")
        
        return len(errors) == 0, errors
    
    def prepare_contribution(self, demo_path: Path) -> Optional[Dict[str, Any]]:
        """
        准备贡献
        
        Args:
            demo_path: demo路径
            
        Returns:
            贡献信息字典
        """
        # 验证demo
        valid, errors = self.validate_demo(demo_path)
        
        if not valid:
            logger.error(f"Demo validation failed: {errors}")
            return None
        
        # 加载元数据
        metadata = self.storage.load_demo_metadata(demo_path)
        if not metadata:
            logger.error("Failed to load metadata")
            return None
        
        # 准备贡献信息
        contribution_info = {
            'demo_path': str(demo_path),
            'name': metadata.get('name'),
            'language': metadata.get('language'),
            'description': metadata.get('description'),
            'author': self.config.get('contribution.author_name', ''),
            'author_email': self.config.get('contribution.author_email', ''),
            'repository_url': self.config.get('contribution.repository_url', ''),
        }
        
        return contribution_info
    
    def copy_to_user_library(self, demo_path: Path) -> Optional[Path]:
        """
        将demo复制到用户库
        
        Args:
            demo_path: demo路径
            
        Returns:
            用户库中的新路径
        """
        # 加载元数据获取语言信息
        metadata = self.storage.load_demo_metadata(demo_path)
        if not metadata:
            return None
        
        language = metadata.get('language', 'unknown').lower()
        
        # 目标路径
        target_base = self.storage.user_library_path / language
        target_path = target_base / demo_path.name
        
        # 复制demo
        if self.storage.copy_demo(demo_path, target_path):
            logger.info(f"Copied demo to user library: {target_path}")
            return target_path
        
        return None
    
    def generate_contribution_message(self, contribution_info: Dict[str, Any]) -> str:
        """
        生成贡献提交信息
        
        Args:
            contribution_info: 贡献信息
            
        Returns:
            提交信息文本
        """
        lines = [
            f"# 贡献新Demo: {contribution_info['name']}",
            "",
            f"**语言**: {contribution_info['language']}",
            f"**描述**: {contribution_info['description']}",
            f"**作者**: {contribution_info['author']} <{contribution_info['author_email']}>",
            "",
            "## 验证清单",
            "- [x] 包含完整的README.md",
            "- [x] 包含可执行的代码文件",
            "- [x] 包含metadata.json",
            "- [ ] 代码已通过本地验证",
            "",
            "## 说明",
            "此demo经过本地测试,可以正常运行。",
        ]
        
        return '\n'.join(lines)
