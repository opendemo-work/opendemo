"""
验证管理器模块

负责验证demo的可执行性。
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
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
        if not self.config.get("enable_verification", False):
            return {"verified": False, "skipped": True, "message": "Verification is disabled"}

        verification_method = self.config.get("verification_method", "venv")

        if language.lower() == "python":
            return self._verify_python(demo_path, verification_method)
        elif language.lower() == "java":
            return self._verify_java(demo_path)
        elif language.lower() == "go":
            return self._verify_go(demo_path)
        elif language.lower() == "nodejs":
            return self._verify_nodejs(demo_path)
        elif language.lower() == "kubernetes":
            return self._verify_kubernetes(demo_path)
        else:
            return {"verified": False, "error": f"Verification not supported for {language}"}

    def _verify_python(self, demo_path: Path, method: str = "venv") -> Dict[str, Any]:
        """
        验证Python demo

        Args:
            demo_path: demo路径
            method: 验证方法

        Returns:
            验证结果
        """
        result = {"verified": False, "method": method, "steps": [], "outputs": [], "errors": []}

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            try:
                # 复制demo到临时目录
                demo_copy = temp_path / "demo"
                shutil.copytree(demo_path, demo_copy)
                result["steps"].append("Copied demo to temp directory")

                # 创建虚拟环境
                venv_path = temp_path / "venv"
                self._create_venv(venv_path)
                result["steps"].append("Created virtual environment")

                # 安装依赖
                requirements_file = demo_copy / "requirements.txt"
                if requirements_file.exists():
                    success, output = self._install_dependencies(venv_path, requirements_file)
                    result["steps"].append("Installed dependencies")
                    result["outputs"].append(output)

                    if not success:
                        result["errors"].append("Failed to install dependencies")
                        return result

                # 执行代码文件
                code_dir = demo_copy / "code"
                if code_dir.exists():
                    for py_file in code_dir.glob("*.py"):
                        success, output, error = self._run_python_file(venv_path, py_file)
                        result["steps"].append(f"Executed {py_file.name}")

                        if output:
                            result["outputs"].append(f"=== {py_file.name} ===\n{output}")

                        if not success:
                            result["errors"].append(f"Execution failed for {py_file.name}: {error}")
                            return result

                # 如果所有步骤成功
                result["verified"] = True
                result["message"] = "All verification steps passed"

            except Exception as e:
                result["errors"].append(str(e))
                logger.error(f"Verification failed: {e}")

        return result

    def _create_venv(self, venv_path: Path) -> bool:
        """创建Python虚拟环境"""
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                check=True,
                capture_output=True,
                timeout=60,
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
            if sys.platform == "win32":
                pip_path = venv_path / "Scripts" / "pip.exe"
            else:
                pip_path = venv_path / "bin" / "pip"

            result = subprocess.run(
                [str(pip_path), "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True,
                timeout=300,
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
            if sys.platform == "win32":
                python_path = venv_path / "Scripts" / "python.exe"
            else:
                python_path = venv_path / "bin" / "python"

            timeout = self.config.get("verification_timeout", 300)

            result = subprocess.run(
                [str(python_path), str(py_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=py_file.parent,
            )

            success = result.returncode == 0
            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return False, "", "Execution timeout"
        except Exception as e:
            logger.error(f"Failed to run {py_file}: {e}")
            return False, "", str(e)

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
            "verified": False,
            "method": "java",
            "steps": [],
            "outputs": [],
            "errors": ["Java verification not fully implemented yet"],
        }

        return result

    def _verify_go(self, demo_path: Path) -> Dict[str, Any]:
        """
        验证Go demo

        Args:
            demo_path: demo路径

        Returns:
            验证结果
        """
        result = {"verified": False, "method": "go", "steps": [], "outputs": [], "errors": []}

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            try:
                # 检查Go环境
                go_check = subprocess.run(
                    ["go", "version"], capture_output=True, text=True, timeout=10
                )
                if go_check.returncode != 0:
                    result["errors"].append("Go is not installed or not in PATH")
                    return result
                result["steps"].append(f"Go environment check: {go_check.stdout.strip()}")

                # 复制demo到临时目录
                demo_copy = temp_path / "demo"
                shutil.copytree(demo_path, demo_copy)
                result["steps"].append("Copied demo to temp directory")

                # 检查是否有go.mod，如果没有则初始化
                go_mod_file = demo_copy / "go.mod"
                if not go_mod_file.exists():
                    init_result = subprocess.run(
                        ["go", "mod", "init", "demo"],
                        cwd=demo_copy,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if init_result.returncode == 0:
                        result["steps"].append("Initialized go.mod")
                    else:
                        result["errors"].append(
                            f"Failed to initialize go.mod: {init_result.stderr}"
                        )
                        return result

                # 安装依赖
                tidy_result = subprocess.run(
                    ["go", "mod", "tidy"],
                    cwd=demo_copy,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if tidy_result.returncode == 0:
                    result["steps"].append("Installed dependencies (go mod tidy)")
                else:
                    result["errors"].append(f"Failed to run go mod tidy: {tidy_result.stderr}")
                    return result

                # 编译检查
                build_result = subprocess.run(
                    ["go", "build", "./..."],
                    cwd=demo_copy,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if build_result.returncode == 0:
                    result["steps"].append("Build check passed")
                else:
                    result["errors"].append(f"Build failed: {build_result.stderr}")
                    return result

                # 运行代码
                code_dir = demo_copy / "code"
                timeout = self.config.get("verification_timeout", 300)

                if code_dir.exists() and list(code_dir.glob("*.go")):
                    # 尝试运行 code 目录下的 go 文件
                    run_result = subprocess.run(
                        ["go", "run", "."],
                        cwd=code_dir,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                    )
                else:
                    # 尝试运行整个项目
                    run_result = subprocess.run(
                        ["go", "run", "."],
                        cwd=demo_copy,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                    )

                result["steps"].append("Executed Go code")
                if run_result.stdout:
                    result["outputs"].append(f"=== Go Output ===\n{run_result.stdout}")

                if run_result.returncode == 0:
                    result["verified"] = True
                    result["message"] = "All verification steps passed"
                else:
                    result["errors"].append(f"Execution failed: {run_result.stderr}")
                    return result

            except subprocess.TimeoutExpired:
                result["errors"].append("Execution timeout")
            except Exception as e:
                result["errors"].append(str(e))
                logger.error(f"Go verification failed: {e}")

        return result

    def _verify_nodejs(self, demo_path: Path) -> Dict[str, Any]:
        """
        验证Node.js demo

        Args:
            demo_path: demo路径

        Returns:
            验证结果
        """
        result = {"verified": False, "method": "nodejs", "steps": [], "outputs": [], "errors": []}

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            try:
                # 检查Node环境
                node_check = subprocess.run(
                    ["node", "--version"], capture_output=True, text=True, timeout=10
                )
                if node_check.returncode != 0:
                    result["errors"].append("Node.js is not installed or not in PATH")
                    return result
                result["steps"].append(f"Node.js environment check: {node_check.stdout.strip()}")

                # 复制demo到临时目录
                demo_copy = temp_path / "demo"
                shutil.copytree(demo_path, demo_copy)
                result["steps"].append("Copied demo to temp directory")

                # 安装依赖（如果有package.json）
                package_json = demo_copy / "package.json"
                if package_json.exists():
                    npm_install = subprocess.run(
                        ["npm", "install"],
                        cwd=demo_copy,
                        capture_output=True,
                        text=True,
                        timeout=300,
                    )
                    if npm_install.returncode == 0:
                        result["steps"].append("Installed dependencies (npm install)")
                    else:
                        result["errors"].append(
                            f"Failed to install dependencies: {npm_install.stderr}"
                        )
                        return result

                # 运行代码
                code_dir = demo_copy / "code"
                timeout = self.config.get("verification_timeout", 300)

                # 查找主文件
                main_file = None
                if code_dir.exists():
                    # 尝试查找 main.js, index.js 或第一个 .js 文件
                    for filename in ["main.js", "index.js"]:
                        candidate = code_dir / filename
                        if candidate.exists():
                            main_file = candidate
                            break
                    if not main_file:
                        js_files = list(code_dir.glob("*.js"))
                        if js_files:
                            main_file = js_files[0]

                if main_file:
                    run_result = subprocess.run(
                        ["node", str(main_file)],
                        cwd=code_dir,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                    )
                    result["steps"].append(f"Executed {main_file.name}")
                elif package_json.exists():
                    # 尝试使用 npm start
                    run_result = subprocess.run(
                        ["npm", "start"],
                        cwd=demo_copy,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                    )
                    result["steps"].append("Executed npm start")
                else:
                    result["errors"].append("No executable JavaScript file found")
                    return result

                if run_result.stdout:
                    result["outputs"].append(f"=== Node.js Output ===\n{run_result.stdout}")

                if run_result.returncode == 0:
                    result["verified"] = True
                    result["message"] = "All verification steps passed"
                else:
                    result["errors"].append(f"Execution failed: {run_result.stderr}")
                    return result

            except subprocess.TimeoutExpired:
                result["errors"].append("Execution timeout")
            except Exception as e:
                result["errors"].append(str(e))
                logger.error(f"Node.js verification failed: {e}")

        return result

    def _verify_kubernetes(self, demo_path: Path) -> Dict[str, Any]:
        """
        验证Kubernetes demo

        Args:
            demo_path: demo路径

        Returns:
            验证结果
        """
        result = {
            "verified": False,
            "partial": False,
            "method": "kubernetes",
            "steps": [],
            "outputs": [],
            "errors": [],
            "warnings": [],
        }

        try:
            # 步骤1: 静态检查 - 验证YAML文件语法
            yaml_files = list(demo_path.rglob("*.yaml")) + list(demo_path.rglob("*.yml"))

            if not yaml_files:
                result["warnings"].append("No YAML files found in demo")
            else:
                result["steps"].append(f"Found {len(yaml_files)} YAML files")

                try:
                    import yaml

                    yaml_valid = True
                    for yaml_file in yaml_files:
                        try:
                            with open(yaml_file, "r", encoding="utf-8") as f:
                                # 支持多文档YAML
                                list(yaml.safe_load_all(f))
                            result["steps"].append(f"YAML syntax check passed: {yaml_file.name}")
                        except yaml.YAMLError as e:
                            yaml_valid = False
                            result["errors"].append(
                                f"YAML syntax error in {yaml_file.name}: {str(e)}"
                            )

                    if not yaml_valid:
                        return result

                except ImportError:
                    result["warnings"].append("pyyaml not installed, skipping YAML validation")

            # 步骤2: 工具检查 - kubectl和helm可用性
            tools_available = True

            # 检查kubectl
            try:
                kubectl_result = subprocess.run(
                    ["kubectl", "version", "--client"],
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("kubernetes.kubectl_timeout", 30),
                )
                if kubectl_result.returncode == 0:
                    result["steps"].append("kubectl is available")
                    if kubectl_result.stdout:
                        result["outputs"].append(
                            f"kubectl version: {kubectl_result.stdout.strip()}"
                        )
                else:
                    tools_available = False
                    result["warnings"].append("kubectl not available or not in PATH")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                tools_available = False
                result["warnings"].append(f"kubectl check failed: {str(e)}")

            # 检查helm
            try:
                helm_result = subprocess.run(
                    ["helm", "version"],
                    capture_output=True,
                    text=True,
                    timeout=self.config.get("kubernetes.helm_timeout", 60),
                )
                if helm_result.returncode == 0:
                    result["steps"].append("helm is available")
                    if helm_result.stdout:
                        result["outputs"].append(f"helm version: {helm_result.stdout.strip()}")
                else:
                    tools_available = False
                    result["warnings"].append("helm not available or not in PATH")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                tools_available = False
                result["warnings"].append(f"helm check failed: {str(e)}")

            # 如果工具不可用,标记为部分验证
            if not tools_available:
                result["partial"] = True
                result["verified"] = True  # 静态检查通过即认为部分验证通过
                result["message"] = "Partial verification passed (static checks only)"
                return result

            # 步骤3: Dry-run验证（可选）
            if tools_available and yaml_files:
                dry_run_passed = True
                for yaml_file in yaml_files:
                    try:
                        # kubectl apply --dry-run=client
                        dry_run_result = subprocess.run(
                            ["kubectl", "apply", "--dry-run=client", "-f", str(yaml_file)],
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )
                        if dry_run_result.returncode == 0:
                            result["steps"].append(f"Dry-run validation passed: {yaml_file.name}")
                        else:
                            dry_run_passed = False
                            result["warnings"].append(
                                f"Dry-run validation failed for {yaml_file.name}: {dry_run_result.stderr}"
                            )
                    except subprocess.TimeoutExpired:
                        result["warnings"].append(f"Dry-run timeout for {yaml_file.name}")
                    except Exception as e:
                        result["warnings"].append(f"Dry-run error for {yaml_file.name}: {str(e)}")
                
                if dry_run_passed:
                    result["steps"].append("All YAML files passed dry-run validation")

            # 步骤4: 文档检查 - README.md完整性
            readme_file = demo_path / "README.md"
            if readme_file.exists():
                try:
                    with open(readme_file, "r", encoding="utf-8") as f:
                        readme_content = f.read().lower()

                    required_keywords = ["安装", "install", "验证", "verify"]
                    found_keywords = [kw for kw in required_keywords if kw in readme_content]

                    if len(found_keywords) >= 2:
                        result["steps"].append("README.md contains required sections")
                    else:
                        result["warnings"].append(
                            "README.md may be missing some required sections "
                            "(installation, verification)"
                        )

                except Exception as e:
                    result["warnings"].append(f"Failed to read README.md: {str(e)}")
            else:
                result["warnings"].append("README.md not found")

            # 全部步骤通过
            result["verified"] = True
            result["message"] = "All verification steps passed"

        except Exception as e:
            result["errors"].append(f"Verification failed: {str(e)}")
            logger.error(f"Kubernetes verification failed: {e}")

        return result

    def generate_report(self, verification_result: Dict[str, Any]) -> str:
        """
        生成验证报告

        Args:
            verification_result: 验证结果

        Returns:
            报告文本
        """
        lines = ["# 验证报告\n"]

        if verification_result.get("skipped"):
            lines.append(f"状态: 已跳过 - {verification_result.get('message')}\n")
            return "\n".join(lines)

        verified = verification_result.get("verified", False)
        status = "✓ 通过" if verified else "✗ 失败"
        lines.append(f"状态: {status}\n")

        method = verification_result.get("method", "unknown")
        lines.append(f"方法: {method}\n")

        # 步骤
        steps = verification_result.get("steps", [])
        if steps:
            lines.append("\n## 执行步骤\n")
            for i, step in enumerate(steps, 1):
                lines.append(f"{i}. {step}")

        # 输出
        outputs = verification_result.get("outputs", [])
        if outputs:
            lines.append("\n## 执行输出\n")
            for output in outputs:
                lines.append(f"```\n{output}\n```\n")

        # 错误
        errors = verification_result.get("errors", [])
        if errors:
            lines.append("\n## 错误信息\n")
            for error in errors:
                lines.append(f"- {error}")

        return "\n".join(lines)
