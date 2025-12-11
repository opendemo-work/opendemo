"""
Demo管理器模块

负责demo的加载、保存和管理。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


class Demo:
    """Demo类,表示一个demo"""
    
    def __init__(self, path: Path, metadata: Dict[str, Any]):
        """
        初始化Demo
        
        Args:
            path: demo所在路径
            metadata: demo元数据
        """
        self.path = path
        self.metadata = metadata
    
    @property
    def name(self) -> str:
        """demo名称"""
        return self.metadata.get('name', self.path.name)
    
    @property
    def language(self) -> str:
        """编程语言"""
        return self.metadata.get('language', 'unknown')
    
    @property
    def keywords(self) -> List[str]:
        """关键字列表"""
        return self.metadata.get('keywords', [])
    
    @property
    def description(self) -> str:
        """描述"""
        return self.metadata.get('description', '')
    
    @property
    def difficulty(self) -> str:
        """难度级别"""
        return self.metadata.get('difficulty', 'beginner')
    
    @property
    def verified(self) -> bool:
        """是否已验证"""
        return self.metadata.get('verified', False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'path': str(self.path),
            'name': self.name,
            'language': self.language,
            'keywords': self.keywords,
            'description': self.description,
            'difficulty': self.difficulty,
            'verified': self.verified,
            'metadata': self.metadata
        }


class DemoManager:
    """Demo管理器"""
    
    def __init__(self, storage_service):
        """
        初始化Demo管理器
        
        Args:
            storage_service: 存储服务实例
        """
        self.storage = storage_service
        self._demo_cache = {}
    
    def load_demo(self, demo_path: Path) -> Optional[Demo]:
        """
        加载demo
        
        Args:
            demo_path: demo路径
            
        Returns:
            Demo对象,加载失败返回None
        """
        # 检查缓存
        cache_key = str(demo_path.absolute())
        if cache_key in self._demo_cache:
            return self._demo_cache[cache_key]
        
        # 加载元数据
        metadata = self.storage.load_demo_metadata(demo_path)
        if metadata is None:
            return None
        
        demo = Demo(demo_path, metadata)
        self._demo_cache[cache_key] = demo
        return demo
    
    def load_all_demos(self, library: str = 'all', language: str = None) -> List[Demo]:
        """
        加载所有demo
        
        Args:
            library: 'builtin', 'user' 或 'all'
            language: 过滤特定语言
            
        Returns:
            Demo对象列表
        """
        demo_paths = self.storage.list_demos(library, language)
        demos = []
        
        for path in demo_paths:
            demo = self.load_demo(path)
            if demo:
                demos.append(demo)
        
        return demos
    
    def create_demo(
        self,
        name: str,
        language: str,
        keywords: List[str],
        description: str,
        files: List[Dict[str, str]],
        difficulty: str = 'beginner',
        author: str = '',
        save_to_user_library: bool = False,
        custom_folder_name: str = None
    ) -> Optional[Demo]:
        """
        创建新demo
        
        Args:
            name: demo名称
            language: 编程语言
            keywords: 关键字列表
            description: 描述
            files: 文件列表,每个文件包含path和content
            difficulty: 难度级别
            author: 作者
            save_to_user_library: 是否保存到用户库
            custom_folder_name: 自定义文件夹名称
            
        Returns:
            创建的Demo对象,失败返回None
        """
        # 生成demo目录名
        if custom_folder_name:
            demo_dir_name = custom_folder_name
        else:
            demo_dir_name = self._generate_demo_name(name, language)
        
        # 确定保存路径
        if save_to_user_library:
            base_path = self.storage.user_library_path / language.lower()
        else:
            base_path = self.storage.get_output_directory() / language.lower()
        
        demo_path = base_path / demo_dir_name
        
        # 创建元数据
        metadata = {
            'name': name,
            'language': language,
            'keywords': keywords,
            'description': description,
            'difficulty': difficulty,
            'author': author,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': '1.0.0',
            'dependencies': {},
            'verified': False
        }
        
        # 组织demo数据
        demo_data = {
            'metadata': metadata,
            'files': files
        }
        
        # 保存demo
        if self.storage.save_demo(demo_data, demo_path):
            return self.load_demo(demo_path)
        
        return None
    
    def _generate_demo_name(self, name: str, language: str) -> str:
        """
        生成demo目录名
        
        Args:
            name: demo名称
            language: 编程语言
            
        Returns:
            目录名
        """
        # 将名称转换为合法的目录名
        safe_name = name.lower().replace(' ', '-').replace('_', '-')
        # 移除特殊字符
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '-')
        return f"{language.lower()}-{safe_name}"
    
    def update_demo_metadata(self, demo: Demo, updates: Dict[str, Any]) -> bool:
        """
        更新demo元数据
        
        Args:
            demo: Demo对象
            updates: 要更新的字段
            
        Returns:
            更新是否成功
        """
        try:
            # 更新元数据
            demo.metadata.update(updates)
            demo.metadata['updated_at'] = datetime.now().isoformat()
            
            # 保存到文件
            metadata_file = demo.path / 'metadata.json'
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(demo.metadata, f, ensure_ascii=False, indent=2)
            
            # 清除缓存
            cache_key = str(demo.path.absolute())
            if cache_key in self._demo_cache:
                del self._demo_cache[cache_key]
            
            logger.info(f"Updated metadata for demo {demo.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update demo metadata: {e}")
            return False
    
    def copy_demo_to_output(self, demo: Demo, output_name: str = None) -> Optional[Path]:
        """
        将demo复制到输出目录
        
        Args:
            demo: Demo对象
            output_name: 输出目录名,None则使用默认名称
            
        Returns:
            输出路径,失败返回None
        """
        output_dir = self.storage.get_output_directory()
        target_name = output_name or demo.path.name
        target_path = output_dir / target_name
        
        if self.storage.copy_demo(demo.path, target_path):
            return target_path
        
        return None
    
    def get_demo_files(self, demo: Demo) -> List[Dict[str, Any]]:
        """
        获取demo的所有文件信息
        
        Args:
            demo: Demo对象
            
        Returns:
            文件信息列表
        """
        files = []
        
        # 遍历demo目录下的所有文件
        for file_path in demo.path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(demo.path)
                
                # 跳过某些文件
                if rel_path.name.startswith('.') or '__pycache__' in str(rel_path):
                    continue
                
                files.append({
                    'name': file_path.name,
                    'path': str(rel_path),
                    'full_path': str(file_path),
                    'description': self._get_file_description(file_path)
                })
        
        return files
    
    def _get_file_description(self, file_path: Path) -> str:
        """
        获取文件描述
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件描述
        """
        filename = file_path.name
        
        if filename == 'README.md':
            return '实操指南'
        elif filename == 'metadata.json':
            return 'Demo元数据'
        elif filename == 'requirements.txt':
            return 'Python依赖'
        elif filename in ('pom.xml', 'build.gradle'):
            return 'Java依赖'
        elif file_path.suffix == '.py':
            return 'Python代码'
        elif file_path.suffix == '.java':
            return 'Java代码'
        else:
            return '其他文件'
