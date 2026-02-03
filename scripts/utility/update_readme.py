from pathlib import Path
from opendemo.services.config_service import ConfigService
from opendemo.services.storage_service import StorageService
from opendemo.core.readme_updater import ReadmeUpdater

output_dir = Path("opendemo_output")
readme_path = Path("README.md")
updater = ReadmeUpdater(output_dir, readme_path)
success = updater.update()
print(f"README更新{'成功' if success else '失败'}")
print(f"统计信息: {updater.get_summary()}")
