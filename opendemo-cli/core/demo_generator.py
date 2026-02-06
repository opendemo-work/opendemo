"""Demo生成协调器模块

协调AI服务生成demo，补充元数据。
"""

# 修复导入路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)


class DemoGenerator:
    """Demo生成器类"""

    def __init__(self, ai_service, demo_repository, config_service):
        """
        初始化生成器

        Args:
            ai_service: AI服务实例
            demo_repository: Demo仓库实例
            config_service: 配置服务实例
        """
        self.ai_service = ai_service
        self.repository = demo_repository
        self.config = config_service

    def generate(
        self,
        language: str,
        topic: str,
        difficulty: str = "beginner",
        save_to_user_library: bool = False,
        custom_folder_name: str = None,
        library_name: str = None,
    ) -> Optional[Dict[str, Any]]:
        """
        生成demo

        Args:
            language: 编程语言
            topic: 主题
            difficulty: 难度级别
            save_to_user_library: 是否保存到用户库
            custom_folder_name: 自定义文件夹名称
            library_name: 库名称，如"numpy"，用于库demo生成

        Returns:
            生成结果字典,包含demo路径和信息
        """
        logger.info(f"Generating demo for {language} - {topic}")

        # 调用AI生成
        demo_data = self.ai_service.generate_demo(language, topic, difficulty)

        if not demo_data:
            logger.error("Failed to generate demo from AI")
            return None

        # 提取元数据和文件
        metadata = demo_data.get("metadata", {})
        files = demo_data.get("files", [])

        # 补充元数据
        author = self.config.get("contribution.author_name", "")
        metadata["author"] = author
        metadata["created_at"] = datetime.now().isoformat()
        metadata["updated_at"] = datetime.now().isoformat()
        metadata["version"] = "1.0.0"
        metadata["verified"] = False

        # 创建demo
        # 优先级: custom_folder_name > metadata.folder_name > topic生成
        folder_name = custom_folder_name
        if not folder_name:
            # 使用AI返回的folder_name
            folder_name = metadata.get("folder_name")
        if not folder_name and library_name:
            # 库demo使用topic作为文件夹名
            folder_name = topic.lower().replace(" ", "-").replace("_", "-")

        demo = self.repository.create_demo(
            name=metadata.get("name", f"{language}-{topic}"),
            language=language,
            keywords=metadata.get("keywords", [topic]),
            description=metadata.get("description", f"Demo for {topic}"),
            files=files,
            difficulty=difficulty,
            author=author,
            save_to_user_library=save_to_user_library,
            custom_folder_name=folder_name,
            library_name=library_name,
        )

        if not demo:
            logger.error("Failed to save demo")
            return None

        # 准备返回结果
        result = {
            "demo": demo,
            "path": str(demo.path),
            "language": language,
            "topic": topic,
            "metadata": metadata,
            "files": self.repository.get_demo_files(demo),
            "verified": False,
        }

        logger.info(f"Successfully generated demo at {demo.path}")
        return result

    def regenerate(self, demo_path: Path, difficulty: str = None) -> Optional[Dict[str, Any]]:
        """
        重新生成已存在的demo

        Args:
            demo_path: 已存在的demo路径
            difficulty: 新的难度级别,None表示保持不变

        Returns:
            生成结果字典
        """
        # 加载现有demo
        demo = self.repository.load_demo(demo_path)
        if not demo:
            logger.error(f"Demo not found at {demo_path}")
            return None

        # 使用现有的语言和主题
        language = demo.language
        topic = demo.name
        difficulty = difficulty or demo.difficulty

        # 删除旧demo
        self.repository.storage.delete_demo(demo_path)

        # 生成新demo
        return self.generate(language, topic, difficulty)
