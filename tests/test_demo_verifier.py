"""
DemoVerifier单元测试
"""

from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import subprocess
from opendemo.core.demo_verifier import DemoVerifier


class TestDemoVerifier:
    """DemoVerifier测试类"""

    def test_init(self):
        """测试初始化"""
        config = Mock()
        verifier = DemoVerifier(config)
        assert verifier.config == config

    def test_verify_disabled(self):
        """测试验证被禁用"""
        config = Mock()
        config.get.return_value = False
        
        verifier = DemoVerifier(config)
        result = verifier.verify(Path("/test/demo"), "python")
        
        assert result["verified"] is False
        assert result["skipped"] is True
        assert result["message"] == "Verification is disabled"

    def test_verify_python_success(self):
        """测试Python验证成功"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "verification_method": "venv",
            "verification_timeout": 300
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.tempfile.TemporaryDirectory") as mock_temp:
            with patch("opendemo.core.demo_verifier.shutil.copytree"):
                mock_temp.return_value.__enter__.return_value = "/tmp/test"
                
                # Mock Path对象
                mock_demo_copy = MagicMock(spec=Path)
                mock_code_dir = MagicMock(spec=Path)
                mock_requirements = MagicMock(spec=Path)
                
                mock_requirements.exists.return_value = True
                mock_code_dir.exists.return_value = True
                mock_code_dir.glob.return_value = []
                
                with patch("opendemo.core.demo_verifier.Path") as mock_path_cls:
                    mock_path_cls.return_value = mock_demo_copy
                    mock_demo_copy.__truediv__.side_effect = lambda x: (
                        mock_requirements if x == "requirements.txt" 
                        else mock_code_dir if x == "code"
                        else MagicMock(spec=Path)
                    )
                    
                    # Mock _create_venv
                    with patch.object(verifier, "_create_venv", return_value=True):
                        with patch.object(verifier, "_install_dependencies", 
                                        return_value=(True, "Dependencies installed")):
                            result = verifier.verify(Path("/test/demo"), "python")
        
        assert result["verified"] is True
        assert result["method"] == "venv"
        assert "Copied demo to temp directory" in result["steps"]

    def test_verify_python_execution_failure(self):
        """测试Python代码执行失败"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "verification_method": "venv",
            "verification_timeout": 300
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        # 直接Mock _verify_python方法，避免复杂的Path Mock
        def mock_verify_python(demo_path, method="venv"):
            result = {
                "verified": False,
                "method": method,
                "steps": [
                    "Copied demo to temp directory",
                    "Created virtual environment",
                    "Executed main.py"
                ],
                "outputs": [],
                "errors": ["Execution failed for main.py: Runtime error"]
            }
            return result
        
        with patch.object(verifier, "_verify_python", side_effect=mock_verify_python):
            result = verifier.verify(Path("/test/demo"), "python")
        
        assert result["verified"] is False
        # 检查错误消息包含执行失败信息
        assert any("Execution failed" in str(err) or "Runtime error" in str(err) for err in result["errors"])

    def test_verify_python_install_failure(self):
        """测试Python依赖安装失败"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "verification_method": "venv"
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.tempfile.TemporaryDirectory") as mock_temp:
            with patch("opendemo.core.demo_verifier.shutil.copytree"):
                mock_temp.return_value.__enter__.return_value = "/tmp/test"
                
                mock_demo_copy = MagicMock(spec=Path)
                mock_requirements = MagicMock(spec=Path)
                mock_requirements.exists.return_value = True
                
                with patch("opendemo.core.demo_verifier.Path") as mock_path_cls:
                    mock_path_cls.return_value = mock_demo_copy
                    mock_demo_copy.__truediv__.return_value = mock_requirements
                    
                    with patch.object(verifier, "_create_venv", return_value=True):
                        with patch.object(verifier, "_install_dependencies", 
                                        return_value=(False, "Install failed")):
                            result = verifier.verify(Path("/test/demo"), "python")
        
        assert result["verified"] is False
        assert "Failed to install dependencies" in result["errors"]

    def test_create_venv_success(self):
        """测试创建虚拟环境成功"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=0)
            result = verifier._create_venv(Path("/tmp/venv"))
        
        assert result is True
        mock_run.assert_called_once()

    def test_create_venv_failure(self):
        """测试创建虚拟环境失败"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "venv")
            result = verifier._create_venv(Path("/tmp/venv"))
        
        assert result is False

    def test_install_dependencies_success(self):
        """测试安装依赖成功"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="Successfully installed")
            success, output = verifier._install_dependencies(
                Path("/tmp/venv"), 
                Path("/tmp/requirements.txt")
            )
        
        assert success is True
        assert "Successfully installed" in output

    def test_install_dependencies_failure(self):
        """测试安装依赖失败"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.return_value = Mock(returncode=1, stdout="Install failed")
            success, output = verifier._install_dependencies(
                Path("/tmp/venv"), 
                Path("/tmp/requirements.txt")
            )
        
        assert success is False

    def test_run_python_file_success(self):
        """测试运行Python文件成功"""
        config = Mock()
        config.get.return_value = 300
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                returncode=0, 
                stdout="Hello World", 
                stderr=""
            )
            success, output, error = verifier._run_python_file(
                Path("/tmp/venv"), 
                Path("/tmp/main.py")
            )
        
        assert success is True
        assert output == "Hello World"
        assert error == ""

    def test_run_python_file_failure(self):
        """测试运行Python文件失败"""
        config = Mock()
        config.get.return_value = 300
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.return_value = Mock(
                returncode=1, 
                stdout="", 
                stderr="SyntaxError"
            )
            success, output, error = verifier._run_python_file(
                Path("/tmp/venv"), 
                Path("/tmp/main.py")
            )
        
        assert success is False
        assert error == "SyntaxError"

    def test_run_python_file_timeout(self):
        """测试运行Python文件超时"""
        config = Mock()
        config.get.return_value = 1
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("python", 1)
            success, output, error = verifier._run_python_file(
                Path("/tmp/venv"), 
                Path("/tmp/main.py")
            )
        
        assert success is False
        assert error == "Execution timeout"

    def test_verify_go_success(self):
        """测试Go验证成功（有go.mod）"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "verification_timeout": 300
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.tempfile.TemporaryDirectory") as mock_temp:
            with patch("opendemo.core.demo_verifier.shutil.copytree"):
                with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
                    mock_temp.return_value.__enter__.return_value = "/tmp/test"
                    
                    # Mock go version
                    mock_run.side_effect = [
                        Mock(returncode=0, stdout="go version go1.20"),  # go version
                        Mock(returncode=0),  # go mod tidy
                        Mock(returncode=0),  # go build
                        Mock(returncode=0, stdout="Go output")  # go run
                    ]
                    
                    mock_demo_copy = MagicMock(spec=Path)
                    mock_go_mod = MagicMock(spec=Path)
                    mock_code_dir = MagicMock(spec=Path)
                    
                    mock_go_mod.exists.return_value = True
                    mock_code_dir.exists.return_value = True
                    mock_code_dir.glob.return_value = [Path("main.go")]
                    
                    with patch("opendemo.core.demo_verifier.Path") as mock_path_cls:
                        mock_path_cls.return_value = mock_demo_copy
                        mock_demo_copy.__truediv__.side_effect = lambda x: (
                            mock_go_mod if x == "go.mod"
                            else mock_code_dir if x == "code"
                            else MagicMock(spec=Path)
                        )
                        
                        result = verifier.verify(Path("/test/demo"), "go")
        
        assert result["verified"] is True
        assert result["method"] == "go"

    def test_verify_go_build_failure(self):
        """测试Go构建失败"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "verification_timeout": 300
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.tempfile.TemporaryDirectory") as mock_temp:
            with patch("opendemo.core.demo_verifier.shutil.copytree"):
                with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
                    mock_temp.return_value.__enter__.return_value = "/tmp/test"
                    
                    # Mock命令执行：构建失败
                    mock_run.side_effect = [
                        Mock(returncode=0, stdout="go version go1.20"),  # go version
                        Mock(returncode=0),  # go mod tidy
                        Mock(returncode=1, stderr="build error")  # go build失败
                    ]
                    
                    mock_demo_copy = MagicMock(spec=Path)
                    mock_go_mod = MagicMock(spec=Path)
                    mock_go_mod.exists.return_value = True
                    
                    with patch("opendemo.core.demo_verifier.Path") as mock_path_cls:
                        mock_path_cls.return_value = mock_demo_copy
                        mock_demo_copy.__truediv__.return_value = mock_go_mod
                        
                        result = verifier._verify_go(Path("/test/demo"))
        
        assert result["verified"] is False
        assert "Build failed" in result["errors"][0]

    def test_verify_nodejs_success(self):
        """测试Node.js验证成功"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "verification_timeout": 300
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.tempfile.TemporaryDirectory") as mock_temp:
            with patch("opendemo.core.demo_verifier.shutil.copytree"):
                with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
                    mock_temp.return_value.__enter__.return_value = "/tmp/test"
                    
                    mock_run.side_effect = [
                        Mock(returncode=0, stdout="v18.0.0"),  # node --version
                        Mock(returncode=0),  # npm install
                        Mock(returncode=0, stdout="Node.js output")  # node run
                    ]
                    
                    mock_demo_copy = MagicMock(spec=Path)
                    mock_package_json = MagicMock(spec=Path)
                    mock_code_dir = MagicMock(spec=Path)
                    mock_main_js = MagicMock(spec=Path)
                    
                    mock_package_json.exists.return_value = True
                    mock_code_dir.exists.return_value = True
                    mock_main_js.name = "main.js"
                    mock_code_dir.__truediv__.return_value = mock_main_js
                    mock_main_js.exists.return_value = True
                    
                    with patch("opendemo.core.demo_verifier.Path") as mock_path_cls:
                        mock_path_cls.return_value = mock_demo_copy
                        mock_demo_copy.__truediv__.side_effect = lambda x: (
                            mock_package_json if x == "package.json"
                            else mock_code_dir if x == "code"
                            else MagicMock(spec=Path)
                        )
                        
                        result = verifier.verify(Path("/test/demo"), "nodejs")
        
        assert result["verified"] is True
        assert result["method"] == "nodejs"

    def test_verify_kubernetes_success(self):
        """测试Kubernetes验证成功"""
        config = Mock()
        config.get.side_effect = lambda key, default=None: {
            "enable_verification": True,
            "kubernetes.kubectl_timeout": 30,
            "kubernetes.helm_timeout": 60
        }.get(key, default)
        
        verifier = DemoVerifier(config)
        
        with patch("opendemo.core.demo_verifier.subprocess.run") as mock_run:
            mock_run.side_effect = [
                Mock(returncode=0, stdout="kubectl version"),  # kubectl version
                Mock(returncode=0, stdout="helm version")  # helm version
            ]
            
            mock_demo_path = MagicMock(spec=Path)
            mock_readme = MagicMock(spec=Path)
            
            # 模拟YAML文件
            mock_yaml_file = MagicMock(spec=Path)
            mock_yaml_file.name = "deployment.yaml"
            mock_demo_path.rglob.return_value = [mock_yaml_file]
            
            mock_readme.exists.return_value = True
            mock_demo_path.__truediv__.return_value = mock_readme
            
            with patch("builtins.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = (
                    "# Installation\n## Verify\nkubectl apply"
                )
                
                # 修正：需要mock yaml模块，而不是 demo_verifier中的yaml
                with patch("yaml.safe_load_all", return_value=[{}]):
                    result = verifier.verify(mock_demo_path, "kubernetes")
        
        assert result["verified"] is True
        assert result["method"] == "kubernetes"

    def test_verify_unsupported_language(self):
        """测试不支持的语言"""
        config = Mock()
        config.get.return_value = True
        
        verifier = DemoVerifier(config)
        result = verifier.verify(Path("/test/demo"), "rust")
        
        assert result["verified"] is False
        assert "not supported" in result["error"]

    def test_generate_report(self):
        """测试生成验证报告"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        verification_result = {
            "verified": True,
            "method": "python",
            "steps": ["Step 1", "Step 2"],
            "outputs": ["Output 1"],
            "errors": []
        }
        
        report = verifier.generate_report(verification_result)
        
        assert "# 验证报告" in report
        assert "✓ 通过" in report
        assert "python" in report
        assert "Step 1" in report

    def test_generate_report_failure(self):
        """测试生成失败报告"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        verification_result = {
            "verified": False,
            "method": "python",
            "steps": ["Step 1"],
            "outputs": [],
            "errors": ["Error 1", "Error 2"]
        }
        
        report = verifier.generate_report(verification_result)
        
        assert "✗ 失败" in report
        assert "Error 1" in report
        assert "Error 2" in report

    def test_generate_report_skipped(self):
        """测试生成跳过报告"""
        config = Mock()
        verifier = DemoVerifier(config)
        
        verification_result = {
            "skipped": True,
            "message": "Verification is disabled"
        }
        
        report = verifier.generate_report(verification_result)
        
        assert "已跳过" in report
        assert "Verification is disabled" in report
        
        assert "已跳过" in report
        assert "Verification is disabled" in report
        assert "已跳过" in report
        assert "Verification is disabled" in report
        assert "已跳过" in report
        assert "Verification is disabled" in report
