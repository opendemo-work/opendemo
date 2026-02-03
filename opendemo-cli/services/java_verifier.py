"""
Java验证服务模块

负责Java demo的编译和运行验证。
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


class JavaVerifier:
    """Java验证器类"""

    def __init__(self, config_service):
        """
        初始化Java验证器
        
        Args:
            config_service: 配置服务实例
        """
        self.config = config_service
        self.timeout = config_service.get("verification_timeout", 300)

    def verify(self, demo_path: Path) -> Dict[str, Any]:
        """
        验证Java demo
        
        Args:
            demo_path: demo路径
            
        Returns:
            验证结果字典
        """
        result = {
            "verified": False,
            "language": "java",
            "method": "compilation_and_execution",
            "steps": [],
            "outputs": [],
            "errors": [],
            "java_version": None,
            "compilation_success": False,
            "execution_success": False
        }

        # 检查Java环境
        java_version = self._check_java_environment()
        if not java_version:
            result["errors"].append("Java环境未安装或不在PATH中")
            return result
        
        result["java_version"] = java_version
        result["steps"].append(f"Java环境检查通过: {java_version}")

        # 创建临时工作目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            try:
                # 复制demo到临时目录
                demo_copy = temp_path / "demo"
                shutil.copytree(demo_path, demo_copy)
                result["steps"].append("复制demo到临时目录")

                # 查找Java源文件
                java_files = self._find_java_files(demo_copy)
                if not java_files:
                    result["errors"].append("未找到Java源文件(.java)")
                    return result
                
                result["steps"].append(f"找到 {len(java_files)} 个Java文件")

                # 创建项目结构（如果需要）
                project_structure = self._setup_project_structure(demo_copy, java_files)
                if project_structure:
                    result["steps"].append("项目结构调整完成")

                # 编译Java文件
                compile_success, compile_output = self._compile_java_files(demo_copy, java_files)
                result["compilation_success"] = compile_success
                result["steps"].append("Java编译完成")
                
                if compile_output:
                    result["outputs"].append(f"=== 编译输出 ===\n{compile_output}")
                
                if not compile_success:
                    result["errors"].append("Java编译失败")
                    return result

                # 运行编译后的类文件
                run_results = self._run_compiled_classes(demo_copy, java_files)
                result["execution_success"] = run_results["success"]
                result["steps"].append("Java程序执行完成")
                
                if run_results["outputs"]:
                    result["outputs"].extend(run_results["outputs"])
                
                if run_results["errors"]:
                    result["errors"].extend(run_results["errors"])

                # 最终验证结果
                result["verified"] = compile_success and run_results["success"]
                if result["verified"]:
                    result["message"] = "Java demo验证通过：编译和执行均成功"
                else:
                    result["message"] = "Java demo验证失败"

            except Exception as e:
                result["errors"].append(f"验证过程异常: {str(e)}")
                logger.error(f"Java验证失败: {e}")

        return result

    def _check_java_environment(self) -> str:
        """检查Java环境"""
        try:
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # java -version 输出到stderr
                version_info = result.stderr.strip().split('\n')[0]
                return version_info
            else:
                return None
                
        except (subprocess.SubprocessError, FileNotFoundError):
            return None

    def _find_java_files(self, demo_path: Path) -> List[Path]:
        """查找所有Java源文件"""
        java_files = []
        
        # 在src目录下查找
        src_dirs = [demo_path / "src" / "main" / "java", demo_path / "src"]
        for src_dir in src_dirs:
            if src_dir.exists():
                java_files.extend(src_dir.rglob("*.java"))
        
        # 在根目录查找
        java_files.extend(demo_path.glob("*.java"))
        
        return java_files

    def _setup_project_structure(self, demo_path: Path, java_files: List[Path]) -> bool:
        """设置标准的Java项目结构"""
        try:
            # 如果没有src目录，创建标准结构
            src_main_java = demo_path / "src" / "main" / "java"
            if not src_main_java.exists():
                src_main_java.mkdir(parents=True, exist_ok=True)
                
                # 移动Java文件到正确位置
                for java_file in java_files:
                    if java_file.parent != src_main_java:
                        # 创建包目录结构
                        package_path = self._extract_package_path(java_file)
                        if package_path:
                            target_dir = src_main_java / package_path
                            target_dir.mkdir(parents=True, exist_ok=True)
                            target_file = target_dir / java_file.name
                            
                            if not target_file.exists():
                                shutil.move(str(java_file), str(target_file))
                        else:
                            # 没有包声明，直接移动到src/main/java
                            target_file = src_main_java / java_file.name
                            if not target_file.exists():
                                shutil.move(str(java_file), str(target_file))
                
                return True
            return False
            
        except Exception as e:
            logger.warning(f"项目结构调整失败: {e}")
            return False

    def _extract_package_path(self, java_file: Path) -> str:
        """从Java文件中提取包路径"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('package '):
                        package_decl = line[8:].rstrip(';').strip()
                        return package_decl.replace('.', '/')
            return ""
        except Exception:
            return ""

    def _compile_java_files(self, demo_path: Path, java_files: List[Path]) -> Tuple[bool, str]:
        """编译Java文件"""
        try:
            # 确定编译目录
            compile_dir = demo_path / "src" / "main" / "java"
            if not compile_dir.exists():
                compile_dir = demo_path

            # 收集所有Java文件路径
            java_file_paths = [str(f) for f in java_files]
            
            # 执行编译命令
            compile_cmd = ["javac", "-encoding", "UTF-8", "-d", str(demo_path / "target" / "classes")] + java_file_paths
            
            # 创建输出目录
            (demo_path / "target" / "classes").mkdir(parents=True, exist_ok=True)
            
            result = subprocess.run(
                compile_cmd,
                cwd=str(compile_dir.parent if compile_dir.name == "java" else compile_dir),
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr if result.stderr else result.stdout
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "编译超时"
        except Exception as e:
            return False, f"编译异常: {str(e)}"

    def _run_compiled_classes(self, demo_path: Path, java_files: List[Path]) -> Dict[str, Any]:
        """运行编译后的Java类"""
        result = {
            "success": False,
            "outputs": [],
            "errors": []
        }
        
        try:
            class_dir = demo_path / "target" / "classes"
            if not class_dir.exists():
                result["errors"].append("编译输出目录不存在")
                return result

            # 查找主类（包含main方法的类）
            main_classes = self._find_main_classes(java_files)
            
            if not main_classes:
                result["errors"].append("未找到包含main方法的类")
                # 尝试运行所有类
                all_classes = list(class_dir.rglob("*.class"))
                if not all_classes:
                    result["errors"].append("未找到编译后的类文件")
                    return result
                main_classes = [self._class_file_to_class_name(cls, class_dir) for cls in all_classes[:3]]

            # 运行主类
            for main_class in main_classes[:3]:  # 限制运行前3个类
                success, output, error = self._run_java_class(class_dir, main_class)
                
                if output:
                    result["outputs"].append(f"=== {main_class} 运行输出 ===\n{output}")
                
                if error:
                    result["errors"].append(f"{main_class} 运行错误: {error}")
                
                if success:
                    result["success"] = True
                    break
                    
        except Exception as e:
            result["errors"].append(f"运行类文件异常: {str(e)}")
            
        return result

    def _find_main_classes(self, java_files: List[Path]) -> List[str]:
        """查找包含main方法的类"""
        main_classes = []
        
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 简单检查是否包含main方法
                if 'public static void main' in content:
                    # 提取类名
                    class_name = self._extract_class_name(content)
                    if class_name:
                        package_path = self._extract_package_path(java_file)
                        if package_path:
                            full_class_name = f"{package_path.replace('/', '.')}.{class_name}"
                        else:
                            full_class_name = class_name
                        main_classes.append(full_class_name)
                        
            except Exception:
                continue
                
        return main_classes

    def _extract_class_name(self, content: str) -> str:
        """从Java文件内容中提取类名"""
        import re
        # 匹配 public class ClassName 或 class ClassName
        pattern = r'(?:public\s+)?class\s+(\w+)'
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _class_file_to_class_name(self, class_file: Path, class_dir: Path) -> str:
        """将.class文件路径转换为类名"""
        try:
            relative_path = class_file.relative_to(class_dir)
            class_name = str(relative_path.with_suffix('')).replace('/', '.')
            return class_name
        except Exception:
            return class_file.stem

    def _run_java_class(self, class_dir: Path, class_name: str) -> Tuple[bool, str, str]:
        """运行指定的Java类"""
        try:
            result = subprocess.run(
                ["java", "-cp", str(class_dir), class_name],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(class_dir)
            )
            
            success = result.returncode == 0
            output = result.stdout if result.stdout else ""
            error = result.stderr if result.stderr else ""
            
            return success, output, error
            
        except subprocess.TimeoutExpired:
            return False, "", "执行超时"
        except Exception as e:
            return False, "", f"执行异常: {str(e)}"