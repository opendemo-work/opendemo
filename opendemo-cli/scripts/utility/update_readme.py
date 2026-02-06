# 修复导入路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pathlib import Path
from services.config_service import ConfigService
from services.storage_service import StorageService
from core.readme_updater import ReadmeUpdater

output_dir = Path("opendemo_output")
readme_path = Path("README.md")
updater = ReadmeUpdater(output_dir, readme_path)
success = updater.update()
print(f"README更新{'成功' if success else '失败'}")
print(f"统计信息: {updater.get_summary()}")
