"""
存储服务模块

负责文件系统操作和demo库管理。
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
# 修复导入路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger

logger = get_logger(__name__)


class StorageService:
    """存储服务类"""

    def __init__(self, config_service):
        """
        初始化存储服务

        Args:
            config_service: 配置服务实例
        """
        self.config = config_service
        self._builtin_library_path = None
        self._user_library_path = None

    @property
    def builtin_library_path(self) -> Path:
        """获取内置demo库路径"""
        if self._builtin_library_path is None:
            # 内置库在包目录下
            import opendemo

            package_dir = Path(opendemo.__file__).parent
            self._builtin_library_path = package_dir / "builtin_demos"
        return self._builtin_library_path

    @property
    def user_library_path(self) -> Path:
        """获取用户demo库路径"""
        if self._user_library_path is None:
            path = self.config.get("user_demo_library")
            self._user_library_path = Path(path)
            self._user_library_path.mkdir(parents=True, exist_ok=True)
        return self._user_library_path

    def list_demos(self, library: str = "all", language: str = None) -> List[Path]:
        """
        列出demo库中的所有demo

        Args:
            library: 'builtin', 'user' 或 'all'
            language: 过滤特定语言,None表示所有语言

        Returns:
            demo目录路径列表
        """
        demo_paths = []

        # 根据library参数确定搜索路径
        search_paths = []
        if library in ("all", "user"):
            search_paths.append(self.user_library_path)
        if library in ("all", "builtin"):
            search_paths.append(self.builtin_library_path)

        for base_path in search_paths:
            if not base_path.exists():
                continue

            # 如果指定了语言,只搜索该语言目录
            if language:
                lang_path = base_path / language.lower()
                if lang_path.exists():
                    demo_paths.extend(self._find_demos_in_path(lang_path))
            else:
                # 搜索所有语言目录
                demo_paths.extend(self._find_demos_in_path(base_path))

        return demo_paths

    def _find_demos_in_path(self, path: Path) -> List[Path]:
        """
        在指定路径下查找demo目录

        Args:
            path: 搜索路径

        Returns:
            demo目录列表
        """
        demos = []

        if not path.exists():
            return demos

        # 遍历目录,查找包含metadata.json的目录
        for item in path.rglob("*"):
            if item.is_dir() and (item / "metadata.json").exists():
                demos.append(item)

        return demos

    def load_demo_metadata(self, demo_path: Path) -> Optional[Dict[str, Any]]:
        """
        加载demo的元数据

        Args:
            demo_path: demo目录路径

        Returns:
            元数据字典,加载失败返回None
        """
        metadata_file = demo_path / "metadata.json"

        if not metadata_file.exists():
            logger.warning(f"Metadata file not found: {metadata_file}")
            return None

        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            return metadata
        except Exception as e:
            logger.error(f"Failed to load metadata from {metadata_file}: {e}")
            return None

    def save_demo(self, demo_data: Dict[str, Any], target_path: Path) -> bool:
        """
        保存demo到指定路径

        Args:
            demo_data: demo数据,包含metadata和files
            target_path: 目标路径

        Returns:
            保存是否成功
        """
        try:
            # 创建目标目录
            target_path.mkdir(parents=True, exist_ok=True)

            # 保存元数据
            metadata = demo_data.get("metadata", {})
            metadata_file = target_path / "metadata.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            # 保存文件
            files = demo_data.get("files", [])
            for file_info in files:
                file_path = target_path / file_info["path"]
                file_path.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(file_info["content"])

            logger.info(f"Successfully saved demo to {target_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save demo to {target_path}: {e}")
            return False

    def copy_demo(self, source_path: Path, target_path: Path) -> bool:
        """
        复制demo到目标路径

        Args:
            source_path: 源demo路径
            target_path: 目标路径

        Returns:
            复制是否成功
        """
        try:
            if target_path.exists():
                shutil.rmtree(target_path)

            shutil.copytree(source_path, target_path)
            logger.info(f"Successfully copied demo from {source_path} to {target_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to copy demo: {e}")
            return False

    def delete_demo(self, demo_path: Path) -> bool:
        """
        删除demo

        Args:
            demo_path: demo路径

        Returns:
            删除是否成功
        """
        try:
            if demo_path.exists() and demo_path.is_dir():
                shutil.rmtree(demo_path)
                logger.info(f"Successfully deleted demo at {demo_path}")
                return True
            else:
                logger.warning(f"Demo path not found: {demo_path}")
                return False

        except Exception as e:
            logger.error(f"Failed to delete demo at {demo_path}: {e}")
            return False

    def get_output_directory(self) -> Path:
        """
        获取demo输出目录

        Returns:
            输出目录路径
        """
        output_dir = Path(self.config.get("output_directory", "./opendemo_output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def read_file(self, file_path: Path) -> Optional[str]:
        """
        读取文件内容

        Args:
            file_path: 文件路径

        Returns:
            文件内容,失败返回None
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return None

    def write_file(self, file_path: Path, content: str) -> bool:
        """
        写入文件

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            写入是否成功
        """
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return False

    def ensure_directory(self, dir_path: Path) -> bool:
        """
        确保目录存在

        Args:
            dir_path: 目录路径

        Returns:
            是否成功
        """
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {dir_path}: {e}")
            return False

    def check_migration_status(self) -> bool:
        """
        检查是否已执行过库demo迁移

        Returns:
            True表示已迁移，False表示未迁移
        """
        migration_marker = self.get_output_directory() / ".migration_completed"
        return migration_marker.exists()

    def migrate_builtin_libraries(self) -> bool:
        """
        将内置库demo迁移到输出目录

        Returns:
            迁移是否成功
        """
        # 检查是否已迁移
        if self.check_migration_status():
            logger.info("Library migration already completed, skipping...")
            return True

        logger.info("Starting builtin library migration...")
        migrated_libraries = []

        try:
            # 扫描所有语言的libraries目录
            for language_dir in self.builtin_library_path.iterdir():
                if not language_dir.is_dir():
                    continue

                language = language_dir.name
                libraries_dir = language_dir / "libraries"

                if not libraries_dir.exists():
                    continue

                # 遍历每个库
                for library_dir in libraries_dir.iterdir():
                    if not library_dir.is_dir() or library_dir.name.startswith("_"):
                        continue

                    library_name = library_dir.name
                    feature_count = 0

                    # 遍历库中的每个功能demo
                    for feature_dir in library_dir.iterdir():
                        if not feature_dir.is_dir() or feature_dir.name.startswith("_"):
                            continue

                        # 检查是否有metadata.json
                        if not (feature_dir / "metadata.json").exists():
                            continue

                        feature_name = feature_dir.name

                        # 构建目标路径
                        target_path = (
                            self.get_output_directory()
                            / language
                            / "libraries"
                            / library_name
                            / feature_name
                        )

                        # 复制demo
                        if self.copy_demo(feature_dir, target_path):
                            feature_count += 1
                            logger.info(f"Migrated {language}/{library_name}/{feature_name}")
                        else:
                            logger.warning(
                                f"Failed to migrate {language}/{library_name}/{feature_name}"
                            )

                    if feature_count > 0:
                        migrated_libraries.append(
                            {
                                "language": language,
                                "library": library_name,
                                "feature_count": feature_count,
                            }
                        )

            # 创建迁移标记文件
            migration_data = {
                "migrated_at": datetime.now().isoformat(),
                "migrated_libraries": migrated_libraries,
                "version": "1.0",
            }

            migration_marker = self.get_output_directory() / ".migration_completed"
            with open(migration_marker, "w", encoding="utf-8") as f:
                json.dump(migration_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Migration completed: {len(migrated_libraries)} libraries migrated")
            return True

        except Exception as e:
            logger.error(f"Failed to migrate builtin libraries: {e}")
            return False
