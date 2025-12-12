"""
Demo仓库管理模块

统一管理所有Demo资源（普通Demo + 库Demo），提供仓库级别的操作接口。
整合了原 demo_manager, library_manager, library_detector, contribution 的功能。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
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


class DemoRepository:
    """Demo仓库管理类
    
    整合了Demo管理、库管理、库检测和贡献管理功能
    """
    
    def __init__(self, storage_service, config_service=None, ai_service=None):
        """
        初始化Demo仓库
        
        Args:
            storage_service: 存储服务实例
            config_service: 配置服务实例（可选）
            ai_service: AI服务实例（可选，用于智能库名检测）
        """
        self.storage = storage_service
        self.config = config_service
        self.ai_service = ai_service
        
        # 缓存
        self._demo_cache: Dict[str, Demo] = {}
        self._library_metadata_cache: Dict[str, Dict[str, Any]] = {}
        self._library_features_cache: Dict[str, List[Dict[str, Any]]] = {}
        self._supported_libraries_cache: Dict[str, List[str]] = {}
    
    # ==================== Demo基础管理 ====================
    
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
        custom_folder_name: str = None,
        library_name: Optional[str] = None
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
            library_name: 库名称，如"numpy"，用于库demo生成
            
        Returns:
            创建的Demo对象,失败返回None
        """
        # 生成demo目录名
        if custom_folder_name:
            demo_dir_name = custom_folder_name
        else:
            demo_dir_name = self._generate_safe_name(name, language)
        
        # 确定保存路径
        if save_to_user_library:
            base_path = self.storage.user_library_path / language.lower()
        else:
            base_path = self.storage.get_output_directory() / language.lower()
        
        # 如果是库demo，追加libraries和库名层级
        if library_name:
            base_path = base_path / 'libraries' / library_name
        
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
    
    def update_metadata(self, demo: Demo, updates: Dict[str, Any]) -> bool:
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
    
    def copy_to_output(self, demo: Demo, output_name: str = None) -> Optional[Path]:
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
        # 确保目标路径包含语言子目录，保持目录结构一致
        target_path = output_dir / demo.language.lower() / target_name
        
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
    
    # ==================== 库管理功能 ====================
    
    def detect_library_command(
        self,
        language: str,
        keywords: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        检测并解析库命令
        
        Args:
            language: 编程语言
            keywords: 关键字列表
            
        Returns:
            库命令信息字典，包含 library、feature_keywords 等字段；非库命令返回 None
        """
        if not keywords:
            return None
        
        # 获取第一个关键字作为潜在的库名
        potential_library = keywords[0].lower()
        
        # 检查是否在支持的库列表中
        supported_libraries = self.get_supported_libraries(language)
        if potential_library not in supported_libraries:
            return None
        
        # 加载库元数据
        library_metadata = self._load_library_metadata(language, potential_library)
        if not library_metadata:
            logger.warning(f"Library metadata not found for {language}/{potential_library}")
            return None
        
        feature_keywords = keywords[1:] if len(keywords) > 1 else []
        
        return {
            'library': potential_library,
            'language': language,
            'feature_keywords': feature_keywords,
            'metadata': library_metadata
        }
    
    def detect_library_for_new_command(
        self,
        language: str,
        keywords: List[str],
        use_ai: bool = True
    ) -> Optional[str]:
        """
        为 new 命令检测库名（即使库尚未注册）
        
        Args:
            language: 编程语言
            keywords: 关键字列表
            use_ai: 是否使用AI判断（默认True）
            
        Returns:
            检测到的库名，或 None
        """
        if not keywords:
            return None
        
        first_keyword = keywords[0]
        
        # 先检查是否在已知库列表中
        supported_libraries = self.get_supported_libraries(language)
        if first_keyword.lower() in supported_libraries:
            return first_keyword.lower()
        
        # 使用 AI 进行智能判断
        if use_ai and self.ai_service:
            result = self.ai_service.classify_keyword(language, first_keyword)
            
            if result.get('is_library') and result.get('confidence', 0) >= 0.5:
                library_name = result.get('library_name') or first_keyword.lower()
                logger.info(
                    f"AI detected '{first_keyword}' as library: {library_name} "
                    f"(confidence: {result.get('confidence', 0):.2f})"
                )
                return library_name
            else:
                logger.info(
                    f"AI detected '{first_keyword}' as topic, not library "
                    f"(confidence: {result.get('confidence', 0):.2f})"
                )
                return None
        
        # 回退到启发式检测
        if self._looks_like_library_name(first_keyword):
            logger.info(f"Heuristic detected potential library name: {first_keyword}")
            return first_keyword.lower()
        
        return None
    
    def get_supported_libraries(self, language: str) -> List[str]:
        """
        获取支持的库列表
        
        Args:
            language: 编程语言
            
        Returns:
            库名列表
        """
        # 检查缓存
        if language in self._supported_libraries_cache:
            return self._supported_libraries_cache[language]
        
        libraries = []
        
        # 从内置库目录扫描
        builtin_library_path = self.storage.builtin_library_path / language.lower() / 'libraries'
        if builtin_library_path.exists():
            for item in builtin_library_path.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    # 检查是否有 _library.json 文件
                    if (item / '_library.json').exists():
                        libraries.append(item.name)
        
        # 从用户库目录扫描
        user_library_path = self.storage.user_library_path / language.lower() / 'libraries'
        if user_library_path.exists():
            for item in user_library_path.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    if (item / '_library.json').exists() and item.name not in libraries:
                        libraries.append(item.name)
        
        # 缓存结果
        self._supported_libraries_cache[language] = libraries
        logger.info(f"Found {len(libraries)} libraries for {language}: {libraries}")
        
        return libraries
    
    def get_library_info(
        self,
        language: str,
        library: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取库的完整信息
        
        Args:
            language: 编程语言
            library: 库名称
            
        Returns:
            库信息字典，包含元数据和功能列表
        """
        # 加载库元数据
        metadata = self._load_library_metadata(language, library)
        if not metadata:
            return None
        
        # 获取功能列表
        features = self.list_library_features(language, library)
        
        return {
            'metadata': metadata,
            'features': features,
            'feature_count': len(features)
        }
    
    def list_library_features(
        self,
        language: str,
        library: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        列出库的功能模块
        
        Args:
            language: 编程语言
            library: 库名称
            category: 可选的分类过滤
            
        Returns:
            功能模块列表
        """
        cache_key = f"{language}:{library}"
        
        # 检查缓存
        if cache_key in self._library_features_cache:
            features = self._library_features_cache[cache_key]
        else:
            features = []
            
            # 从内置库扫描
            builtin_library_dir = (
                self.storage.builtin_library_path / 
                language.lower() / 
                'libraries' / 
                library
            )
            if builtin_library_dir.exists():
                features.extend(self._scan_library_features(builtin_library_dir))
            
            # 从用户库扫描
            user_library_dir = (
                self.storage.user_library_path / 
                language.lower() / 
                'libraries' / 
                library
            )
            if user_library_dir.exists():
                features.extend(self._scan_library_features(user_library_dir))
            
            # 从输出目录扫描
            output_library_dir = (
                self.storage.get_output_directory() / 
                language.lower() / 
                'libraries' / 
                library
            )
            if output_library_dir.exists():
                output_features = self._scan_library_features(output_library_dir)
                # 去重：输出目录的 demo 可能已存在于内置/用户库
                existing_names = {f['name'] for f in features}
                for feat in output_features:
                    if feat['name'] not in existing_names:
                        features.append(feat)
            
            # 缓存结果
            self._library_features_cache[cache_key] = features
        
        # 按分类过滤
        if category:
            features = [f for f in features if f.get('category') == category]
        
        return features
    
    def get_library_demo(
        self,
        language: str,
        library: str,
        feature: str
    ) -> Optional[Demo]:
        """
        获取具体功能的 demo
        
        Args:
            language: 编程语言
            library: 库名称
            feature: 功能模块名称
            
        Returns:
            Demo 对象，未找到返回 None
        """
        # 优先从输出目录查找
        output_demo_path = (
            self.storage.get_output_directory() / 
            language.lower() / 
            'libraries' / 
            library / 
            feature
        )
        if output_demo_path.exists():
            demo = self.load_demo(output_demo_path)
            if demo:
                return demo
        
        # 从用户库查找
        user_demo_path = (
            self.storage.user_library_path / 
            language.lower() / 
            'libraries' / 
            library / 
            feature
        )
        if user_demo_path.exists():
            demo = self.load_demo(user_demo_path)
            if demo:
                return demo
        
        # 从内置库查找
        builtin_demo_path = (
            self.storage.builtin_library_path / 
            language.lower() / 
            'libraries' / 
            library / 
            feature
        )
        if builtin_demo_path.exists():
            demo = self.load_demo(builtin_demo_path)
            if demo:
                return demo
        
        return None
    
    def copy_library_feature_to_output(
        self,
        language: str,
        library: str,
        feature: str
    ) -> Optional[Path]:
        """
        将库功能 demo 复制到输出目录
        
        Args:
            language: 编程语言
            library: 库名称
            feature: 功能模块名称
            
        Returns:
            输出路径，失败返回 None
        """
        demo = self.get_library_demo(language, library, feature)
        if not demo:
            return None
        
        output_dir = self.storage.get_output_directory()
        target_path = output_dir / language.lower() / 'libraries' / library / feature
        
        if self.storage.copy_demo(demo.path, target_path):
            return target_path
        
        return None
    
    # ==================== 贡献管理功能 ====================
    
    def prompt_contribution(self, demo_path: Path) -> bool:
        """
        询问用户是否贡献demo
        
        Args:
            demo_path: demo路径
            
        Returns:
            用户是否选择贡献
        """
        if not self.config or not self.config.get('contribution.auto_prompt', True):
            return False
        
        try:
            response = input("\n是否将此demo贡献到公共库? (y/n): ").strip().lower()
            return response in ('y', 'yes', '是')
        except Exception as e:
            logger.error(f"Failed to prompt for contribution: {e}")
            return False
    
    def validate_contribution(self, demo_path: Path) -> Tuple[bool, List[str]]:
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
            code_files = list(code_dir.glob('*.py')) + list(code_dir.glob('*.java')) + \
                         list(code_dir.glob('*.go')) + list(code_dir.glob('*.js'))
            if not code_files:
                errors.append("No code files found in code directory")
        
        # 检查README.md内容
        readme_file = demo_path / 'README.md'
        if readme_file.exists():
            content = self.storage.read_file(readme_file)
            if content and len(content) < 100:
                errors.append("README.md content is too short")
        
        return len(errors) == 0, errors
    
    def contribute_to_user_library(self, demo_path: Path) -> Optional[Path]:
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
    
    def prepare_contribution_info(self, demo_path: Path) -> Optional[Dict[str, Any]]:
        """
        准备贡献信息
        
        Args:
            demo_path: demo路径
            
        Returns:
            贡献信息字典
        """
        # 验证demo
        valid, errors = self.validate_contribution(demo_path)
        
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
            'author': self.config.get('contribution.author_name', '') if self.config else '',
            'author_email': self.config.get('contribution.author_email', '') if self.config else '',
            'repository_url': self.config.get('contribution.repository_url', '') if self.config else '',
        }
        
        return contribution_info
    
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
    
    # ==================== 内部辅助方法 ====================
    
    def _generate_safe_name(self, name: str, language: str) -> str:
        """
        生成安全的demo目录名
        
        Args:
            name: demo名称
            language: 编程语言
            
        Returns:
            目录名（纯ASCII英文）
        """
        # 将名称转换为合法的目录名
        safe_name = name.lower().replace(' ', '-').replace('_', '-')
        # 只保留ASCII字母、数字和连字符（移除中文等非ASCII字符）
        safe_name = ''.join(c for c in safe_name if c.isascii() and (c.isalnum() or c == '-'))
        # 移除连续的连字符和首尾连字符
        while '--' in safe_name:
            safe_name = safe_name.replace('--', '-')
        safe_name = safe_name.strip('-')
        # 确保名称不为空
        if not safe_name:
            safe_name = 'demo'
        return f"{language.lower()}-{safe_name}"
    
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
        elif filename == 'go.mod':
            return 'Go依赖'
        elif filename == 'package.json':
            return 'Node.js依赖'
        elif file_path.suffix == '.py':
            return 'Python代码'
        elif file_path.suffix == '.java':
            return 'Java代码'
        elif file_path.suffix == '.go':
            return 'Go代码'
        elif file_path.suffix == '.js':
            return 'JavaScript代码'
        else:
            return '其他文件'
    
    def _load_library_metadata(
        self,
        language: str,
        library: str
    ) -> Optional[Dict[str, Any]]:
        """
        加载库元数据
        
        Args:
            language: 编程语言
            library: 库名称
            
        Returns:
            元数据字典，失败返回 None
        """
        cache_key = f"{language}:{library}"
        
        # 检查缓存
        if cache_key in self._library_metadata_cache:
            return self._library_metadata_cache[cache_key]
        
        # 优先从用户库加载
        user_metadata_path = (
            self.storage.user_library_path / 
            language.lower() / 
            'libraries' / 
            library / 
            '_library.json'
        )
        
        if user_metadata_path.exists():
            try:
                with open(user_metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self._library_metadata_cache[cache_key] = metadata
                    return metadata
            except Exception as e:
                logger.error(f"Failed to load user library metadata: {e}")
        
        # 从内置库加载
        builtin_metadata_path = (
            self.storage.builtin_library_path / 
            language.lower() / 
            'libraries' / 
            library / 
            '_library.json'
        )
        
        if builtin_metadata_path.exists():
            try:
                with open(builtin_metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self._library_metadata_cache[cache_key] = metadata
                    return metadata
            except Exception as e:
                logger.error(f"Failed to load builtin library metadata: {e}")
        
        return None
    
    def _scan_library_features(self, library_dir: Path) -> List[Dict[str, Any]]:
        """
        扫描库目录下的功能模块
        
        Args:
            library_dir: 库目录路径
            
        Returns:
            功能模块列表
        """
        features = []
        
        for item in library_dir.iterdir():
            # 跳过非目录和特殊文件
            if not item.is_dir() or item.name.startswith('_') or item.name.startswith('.'):
                continue
            
            # 尝试读取 metadata.json
            metadata_file = item / 'metadata.json'
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    features.append({
                        'name': item.name,
                        'path': str(item),
                        'title': metadata.get('title', item.name),
                        'description': metadata.get('description', ''),
                        'difficulty': metadata.get('difficulty', 'beginner'),
                        'keywords': metadata.get('keywords', []),
                        'category': metadata.get('category', '未分类'),
                        'library': metadata.get('library', ''),
                        'metadata': metadata
                    })
                except Exception as e:
                    logger.error(f"Failed to load feature metadata from {metadata_file}: {e}")
        
        return features
    
    def _looks_like_library_name(self, keyword: str) -> bool:
        """
        判断关键字是否看起来像库名
        
        库名特征：
        - 单个单词（无空格）
        - 全小写或带连字符/下划线
        - 不包含中文
        - 长度适中（2-30字符）
        
        Args:
            keyword: 待检测的关键字
            
        Returns:
            是否看起来像库名
        """
        if not keyword:
            return False
        
        # 转小写
        kw = keyword.lower().strip()
        
        # 长度检查
        if len(kw) < 2 or len(kw) > 30:
            return False
        
        # 不能包含中文字符
        for char in kw:
            if '\u4e00' <= char <= '\u9fff':
                return False
        
        # 只允许字母、数字、连字符、下划线
        allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789-_')
        if not all(c in allowed_chars for c in kw):
            return False
        
        # 必须以字母开头
        if not kw[0].isalpha():
            return False
        
        return True
    
    def clear_cache(self):
        """清除所有缓存"""
        self._demo_cache.clear()
        self._library_metadata_cache.clear()
        self._library_features_cache.clear()
        self._supported_libraries_cache.clear()
        logger.info("Cleared all repository caches")


# 向后兼容的别名
DemoManager = DemoRepository
