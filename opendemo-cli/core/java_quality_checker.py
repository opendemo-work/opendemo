"""
Java质量检查器模块

负责检查Java demo的代码质量、文档完整性和结构规范性。
"""

import re
from pathlib import Path
from typing import Dict, List, Any
# 修复导入路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger

logger = get_logger(__name__)


class JavaQualityChecker:
    """Java质量检查器类"""

    def __init__(self, config_service):
        """
        初始化质量检查器
        
        Args:
            config_service: 配置服务实例
        """
        self.config = config_service
        self.minimum_readme_length = config_service.get("minimum_readme_length", 500)
        self.required_files = ["README.md", "metadata.json"]

    def check_quality(self, demo_path: Path) -> Dict[str, Any]:
        """
        检查Java demo质量
        
        Args:
            demo_path: demo路径
            
        Returns:
            质量检查结果字典
        """
        result = {
            "passed": False,
            "score": 0,
            "total_checks": 0,
            "passed_checks": 0,
            "checks": {},
            "issues": [],
            "recommendations": []
        }

        # 基本文件检查
        self._check_required_files(demo_path, result)
        
        # README质量检查
        self._check_readme_quality(demo_path, result)
        
        # 代码质量检查
        self._check_code_quality(demo_path, result)
        
        # 文档结构检查
        self._check_documentation_structure(demo_path, result)
        
        # 最佳实践检查
        self._check_best_practices(demo_path, result)
        
        # 计算总分
        if result["total_checks"] > 0:
            result["score"] = int((result["passed_checks"] / result["total_checks"]) * 100)
            result["passed"] = result["score"] >= 80  # 80分以上为通过

        return result

    def _check_required_files(self, demo_path: Path, result: Dict[str, Any]):
        """检查必需文件是否存在"""
        check_name = "required_files"
        result["total_checks"] += 1
        
        missing_files = []
        for required_file in self.required_files:
            if not (demo_path / required_file).exists():
                missing_files.append(required_file)
        
        if not missing_files:
            result["passed_checks"] += 1
            result["checks"][check_name] = {"passed": True, "message": "所有必需文件存在"}
        else:
            result["checks"][check_name] = {
                "passed": False, 
                "message": f"缺少文件: {', '.join(missing_files)}"
            }
            result["issues"].append(f"缺少必需文件: {', '.join(missing_files)}")

    def _check_readme_quality(self, demo_path: Path, result: Dict[str, Any]):
        """检查README质量"""
        readme_path = demo_path / "README.md"
        check_name = "readme_quality"
        result["total_checks"] += 1
        
        if not readme_path.exists():
            result["checks"][check_name] = {"passed": False, "message": "README.md文件不存在"}
            result["issues"].append("缺少README.md文件")
            return

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查文件长度
            if len(content) < self.minimum_readme_length:
                result["checks"][check_name] = {
                    "passed": False,
                    "message": f"README内容过短 ({len(content)} 字符，要求至少 {self.minimum_readme_length} 字符)"
                }
                result["issues"].append(f"README内容需要扩充至{self.minimum_readme_length}字符以上")
                return
            
            # 检查必需章节
            required_sections = [
                "学习目标", "环境准备", "项目结构", "快速开始",
                "代码详解", "验证测试", "常见问题"
            ]
            
            missing_sections = []
            for section in required_sections:
                if not re.search(rf"[#]+.*{section}", content):
                    missing_sections.append(section)
            
            if not missing_sections:
                result["passed_checks"] += 1
                result["checks"][check_name] = {
                    "passed": True, 
                    "message": "README质量良好，包含所有必需章节"
                }
            else:
                result["checks"][check_name] = {
                    "passed": False,
                    "message": f"缺少章节: {', '.join(missing_sections)}"
                }
                result["issues"].append(f"README缺少章节: {', '.join(missing_sections)}")
                
        except Exception as e:
            result["checks"][check_name] = {
                "passed": False,
                "message": f"读取README文件失败: {str(e)}"
            }
            result["issues"].append(f"README文件读取异常: {str(e)}")

    def _check_code_quality(self, demo_path: Path, result: Dict[str, Any]):
        """检查代码质量"""
        check_name = "code_quality"
        result["total_checks"] += 1
        
        java_files = self._find_java_files(demo_path)
        if not java_files:
            result["checks"][check_name] = {"passed": False, "message": "未找到Java源文件"}
            result["issues"].append("项目中没有Java源代码文件")
            return

        issues = []
        good_practices = 0
        total_files = len(java_files)

        for java_file in java_files:
            file_issues = self._analyze_java_file(java_file)
            issues.extend([f"{java_file.name}: {issue}" for issue in file_issues])
            
            # 检查良好实践
            if self._has_good_practices(java_file):
                good_practices += 1

        if not issues and good_practices == total_files:
            result["passed_checks"] += 1
            result["checks"][check_name] = {
                "passed": True,
                "message": f"所有{total_files}个Java文件质量良好"
            }
        else:
            result["checks"][check_name] = {
                "passed": False,
                "message": f"发现{len(issues)}个代码质量问题"
            }
            result["issues"].extend(issues)
            
            if good_practices < total_files:
                result["recommendations"].append(
                    f"建议在{total_files - good_practices}个文件中添加更多最佳实践"
                )

    def _check_documentation_structure(self, demo_path: Path, result: Dict[str, Any]):
        """检查文档结构"""
        check_name = "documentation_structure"
        result["total_checks"] += 1
        
        # 检查标准目录结构
        expected_dirs = ["src/main/java"]
        missing_dirs = []
        
        for expected_dir in expected_dirs:
            if not (demo_path / expected_dir).exists():
                missing_dirs.append(expected_dir)
        
        # 检查metadata.json结构
        metadata_issues = self._validate_metadata(demo_path)
        
        if not missing_dirs and not metadata_issues:
            result["passed_checks"] += 1
            result["checks"][check_name] = {
                "passed": True,
                "message": "文档结构符合标准"
            }
        else:
            messages = []
            if missing_dirs:
                messages.append(f"缺少目录: {', '.join(missing_dirs)}")
            if metadata_issues:
                messages.extend(metadata_issues)
            
            result["checks"][check_name] = {
                "passed": False,
                "message": "; ".join(messages)
            }
            result["issues"].extend(messages)

    def _check_best_practices(self, demo_path: Path, result: Dict[str, Any]):
        """检查最佳实践"""
        check_name = "best_practices"
        result["total_checks"] += 1
        
        practices_score = 0
        total_practices = 5  # 总共检查5个最佳实践
        
        # 1. 检查是否有包声明
        java_files = self._find_java_files(demo_path)
        if java_files and self._has_package_declarations(java_files):
            practices_score += 1
        
        # 2. 检查是否有注释
        if self._has_adequate_comments(java_files):
            practices_score += 1
            
        # 3. 检查类命名规范
        if self._follows_naming_conventions(java_files):
            practices_score += 1
            
        # 4. 检查是否有异常处理
        if self._has_exception_handling(java_files):
            practices_score += 1
            
        # 5. 检查代码复杂度
        if self._has_reasonable_complexity(java_files):
            practices_score += 1
        
        score_percentage = (practices_score / total_practices) * 100
        if score_percentage >= 80:
            result["passed_checks"] += 1
            result["checks"][check_name] = {
                "passed": True,
                "message": f"最佳实践得分: {score_percentage:.1f}% ({practices_score}/{total_practices})"
            }
        else:
            result["checks"][check_name] = {
                "passed": False,
                "message": f"最佳实践得分偏低: {score_percentage:.1f}% ({practices_score}/{total_practices})"
            }
            result["recommendations"].append(
                f"建议改进代码以达到80%以上的最佳实践标准"
            )

    def _find_java_files(self, demo_path: Path) -> List[Path]:
        """查找所有Java源文件"""
        java_files = []
        src_dirs = [demo_path / "src" / "main" / "java", demo_path / "src"]
        
        for src_dir in src_dirs:
            if src_dir.exists():
                java_files.extend(src_dir.rglob("*.java"))
        
        java_files.extend(demo_path.glob("*.java"))
        return java_files

    def _analyze_java_file(self, java_file: Path) -> List[str]:
        """分析单个Java文件的质量问题"""
        issues = []
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # 检查行长度
            for i, line in enumerate(lines, 1):
                if len(line) > 120:
                    issues.append(f"第{i}行超过120字符限制")
            
            # 检查TODO注释
            todo_count = content.count('TODO')
            if todo_count > 0:
                issues.append(f"包含{todo_count}个TODO注释")
            
            # 检查System.out.println使用
            print_count = content.count('System.out.println')
            if print_count > 3:
                issues.append(f"过多使用System.out.println ({print_count}次)")
                
        except Exception as e:
            issues.append(f"文件分析失败: {str(e)}")
            
        return issues

    def _has_good_practices(self, java_file: Path) -> bool:
        """检查文件是否包含良好的编程实践"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含必要的元素
            has_package = 'package ' in content
            has_imports = 'import ' in content
            has_class = 'class ' in content
            has_methods = 'public ' in content or 'private ' in content
            
            return has_package and has_imports and has_class and has_methods
            
        except Exception:
            return False

    def _has_package_declarations(self, java_files: List[Path]) -> bool:
        """检查是否有包声明"""
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'package ' in content:
                        return True
            except Exception:
                continue
        return False

    def _has_adequate_comments(self, java_files: List[Path]) -> bool:
        """检查是否有足够的注释"""
        total_lines = 0
        comment_lines = 0
        
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    
                    for line in lines:
                        stripped = line.strip()
                        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                            comment_lines += 1
            except Exception:
                continue
        
        return total_lines > 0 and (comment_lines / total_lines) >= 0.1  # 至少10%注释率

    def _follows_naming_conventions(self, java_files: List[Path]) -> bool:
        """检查是否遵循命名约定"""
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查类名（大驼峰）
                import re
                class_matches = re.findall(r'class\s+(\w+)', content)
                for class_name in class_matches:
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_name):
                        return False
                
                # 检查方法名（小驼峰）
                method_matches = re.findall(r'(public|private|protected).*?\s+(\w+)\s*\(', content)
                for _, method_name in method_matches:
                    if not re.match(r'^[a-z][a-zA-Z0-9]*$', method_name) and method_name not in ['main']:
                        return False
                        
            except Exception:
                continue
        return True

    def _has_exception_handling(self, java_files: List[Path]) -> bool:
        """检查是否有异常处理"""
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'try' in content and 'catch' in content:
                        return True
            except Exception:
                continue
        return False

    def _has_reasonable_complexity(self, java_files: List[Path]) -> bool:
        """检查代码复杂度是否合理"""
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 检查单个方法是否过长
                method_lines = 0
                in_method = False
                
                for line in lines:
                    stripped = line.strip()
                    if '{' in stripped and ('public' in stripped or 'private' in stripped):
                        in_method = True
                        method_lines = 1
                    elif in_method:
                        method_lines += 1
                        if '}' in stripped:
                            if method_lines > 50:  # 方法超过50行认为复杂度过高
                                return False
                            in_method = False
                
                # 检查嵌套层级
                max_indent = 0
                for line in lines:
                    indent = len(line) - len(line.lstrip())
                    max_indent = max(max_indent, indent // 4)  # 假设4个空格为一个缩进
                
                if max_indent > 5:  # 嵌套超过5层认为复杂度过高
                    return False
                    
            except Exception:
                continue
        return True

    def _validate_metadata(self, demo_path: Path) -> List[str]:
        """验证metadata.json文件"""
        issues = []
        metadata_path = demo_path / "metadata.json"
        
        if not metadata_path.exists():
            issues.append("缺少metadata.json文件")
            return issues
            
        try:
            import json
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            required_fields = ["name", "language", "description", "difficulty"]
            for field in required_fields:
                if field not in metadata:
                    issues.append(f"metadata.json缺少必需字段: {field}")
                    
        except Exception as e:
            issues.append(f"metadata.json格式错误: {str(e)}")
            
        return issues