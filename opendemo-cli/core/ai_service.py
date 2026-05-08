"""
AI服务模块

负责与LLM API交互,生成demo代码。
"""

import json
import time
import requests
from typing import Dict, Any, Optional
# 修复导入路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import get_logger

logger = get_logger(__name__)


class AIService:
    """AI服务类"""

    def __init__(self, config_service):
        """
        初始化AI服务

        Args:
            config_service: 配置服务实例
        """
        self.config = config_service
        self._api_key = None
        self._api_endpoint = None
        self._model = None

    def _load_config(self):
        """加载AI配置"""
        if self._api_key is None:
            self._api_key = self.config.get("ai.api_key")
            self._api_endpoint = (
                self.config.get("ai.api_endpoint") or "https://api.openai.com/v1/chat/completions"
            )
            self._model = self.config.get("ai.model", "gpt-4")

    def generate_demo(
        self, language: str, topic: str, difficulty: str = "beginner"
    ) -> Optional[Dict[str, Any]]:
        """
        生成demo代码

        Args:
            language: 编程语言
            topic: 主题
            difficulty: 难度级别

        Returns:
            包含代码和文档的字典,失败返回None
        """
        self._load_config()

        if not self._api_key:
            logger.error("AI API key is not configured")
            return None

        # 构建prompt
        prompt = self._build_prompt(language, topic, difficulty)

        # 调用API
        retry_times = self.config.get("ai.retry_times", 3)
        retry_interval = self.config.get("ai.retry_interval", 5)

        for attempt in range(retry_times):
            try:
                response = self._call_api(prompt)
                if response:
                    # 解析响应
                    demo_data = self._parse_response(response, language, topic)
                    if demo_data:
                        return demo_data

            except Exception as e:
                logger.error(f"API call failed (attempt {attempt + 1}/{retry_times}): {e}")

                if attempt < retry_times - 1:
                    time.sleep(retry_interval)
                    continue

        logger.error("Failed to generate demo after all retries")
        return None

    def _build_prompt(self, language: str, topic: str, difficulty: str) -> str:
        """
        构建生成prompt

        Args:
            language: 编程语言
            topic: 主题
            difficulty: 难度级别

        Returns:
            prompt文本
        """
        # 根据语言确定规范
        coding_standard = {"python": "PEP 8", "java": "Google Java Style Guide"}.get(
            language.lower(), "industry best practices"
        )

        # 根据语言确定依赖文件
        dependency_file = {"python": "requirements.txt", "java": "pom.xml or build.gradle"}.get(
            language.lower(), "dependency file"
        )

        prompt = f"""你是一位经验丰富的{language}编程导师和代码示例生成器。

任务:为"{topic}"主题生成一个完整的、可执行的{language} demo示例。

要求:
1. 生成1-3个代码文件,每个文件聚焦一个具体场景,展示不同的用法
2. 代码必须包含详细的中文注释,解释关键逻辑和概念
3. 严格遵循{language}的{coding_standard}编码规范
4. 生成完整的README.md实操文档(中文),必须包含:
   - Demo标题和简介
   - 学习目标
   - 环境要求(Python/Java版本等)
   - 安装依赖的详细步骤
   - 文件说明
   - 逐步实操指南(每一步都要有具体命令和预期输出)
   - 代码解析(解释关键代码段)
   - 预期输出示例
   - 常见问题解答
   - 扩展学习建议
5. 生成{dependency_file}依赖声明文件
6. 提供metadata.json元数据,包含:
   - name: demo名称
   - language: {language}
   - keywords: 关键字数组(3-5个)
   - description: 简短描述(一句话)
   - difficulty: {difficulty}
   - dependencies: 依赖信息对象

输出格式:
请以JSON格式返回,结构如下:
{{
  "metadata": {{
    "name": "demo名称(必须是英文,如: nodejs-callback-functions-demo)",
    "folder_name": "目录名称(必须是英文,小写,用连字符分隔,如: callback-functions-demo)",
    "language": "{language}",
    "keywords": ["关键字1", "关键字2", "关键字3"],
    "description": "简短描述",
    "difficulty": "{difficulty}",
    "dependencies": {{}}
  }},
  "files": [
    {{
      "path": "README.md",
      "content": "完整的README内容"
    }},
    {{
      "path": "code/example1.py",
      "content": "代码文件内容"
    }},
    {{
      "path": "{dependency_file.split()[0]}",
      "content": "依赖声明内容"
    }}
  ]
}}

约束:
- 代码总行数控制在50-300行之间
- 使用稳定版本的库和API
- 确保Windows/Linux/Mac跨平台兼容
- 代码必须可以直接运行,不需要额外修改
- README.md必须包含完整的操作步骤,让初学者也能轻松运行

请直接返回JSON,不要包含任何其他文字说明。"""

        return prompt

    def _call_api(self, prompt: str) -> Optional[str]:
        """
        调用LLM API

        Args:
            prompt: 提示文本

        Returns:
            API响应内容,失败返回None
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self._api_key}"}

        data = {
            "model": self._model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的编程教学助手,擅长生成高质量的代码示例和教程。",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self.config.get("ai.temperature", 0.7),
            "max_tokens": self.config.get("ai.max_tokens", 4000),
        }

        timeout = self.config.get("ai.timeout", 60)

        logger.info(f"Calling AI API with model {self._model}")

        response = requests.post(self._api_endpoint, headers=headers, json=data, timeout=timeout)

        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        return content

    def _parse_response(self, response: str, language: str, topic: str) -> Optional[Dict[str, Any]]:
        """
        解析AI响应

        Args:
            response: AI响应内容
            language: 编程语言
            topic: 主题

        Returns:
            解析后的demo数据,失败返回None
        """
        try:
            # 提取JSON内容
            response = response.strip()

            # 尝试找到JSON部分
            # 如果直接以 { 开头，就是纯JSON，直接解析
            if response.startswith("{"):
                pass  # 直接解析
            elif "```json" in response:
                # 找到```json后的内容，使用最后一个```作为结束
                start = response.find("```json") + 7
                end = response.rfind("```")
                if end > start:
                    response = response[start:end].strip()
            elif response.startswith("```"):
                # 响应以```开头但不是```json
                start = response.find("\n") + 1
                end = response.rfind("```")
                if end > start:
                    response = response[start:end].strip()

            # 解析JSON
            data = json.loads(response)

            # 验证必需字段
            if "metadata" not in data or "files" not in data:
                logger.error("Response missing required fields")
                return None

            # 确保metadata包含必需字段
            metadata = data["metadata"]
            if "name" not in metadata:
                metadata["name"] = f"{language}-{topic}"
            if "language" not in metadata:
                metadata["language"] = language
            if "keywords" not in metadata:
                metadata["keywords"] = [topic]

            # 如果没有folder_name，从name或topic生成一个英文的folder_name
            if "folder_name" not in metadata or not metadata["folder_name"]:
                # 尝试从topic生成
                folder_name = topic.lower().replace(" ", "-").replace("_", "-")
                # 只保留ASCII字符
                folder_name = "".join(
                    c for c in folder_name if c.isascii() and (c.isalnum() or c == "-")
                )
                while "--" in folder_name:
                    folder_name = folder_name.replace("--", "-")
                folder_name = folder_name.strip("-")
                if folder_name:
                    metadata["folder_name"] = folder_name
                else:
                    # 最后回退：使用时间戳
                    import time

                    metadata["folder_name"] = f"demo-{int(time.time())}"

            logger.info(f"Successfully parsed AI response for {metadata['name']}")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {response[:500]}")
            return None
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            return None

    def validate_api_key(self) -> bool:
        """
        验证API密钥是否有效

        Returns:
            是否有效
        """
        self._load_config()

        if not self._api_key:
            return False

        try:
            # 发送一个简单的测试请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            }

            data = {
                "model": self._model,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5,
            }

            response = requests.post(self._api_endpoint, headers=headers, json=data, timeout=10)

            return response.status_code == 200

        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False

    def classify_keyword(self, language: str, keyword: str) -> Dict[str, Any]:
        """
        使用AI判断关键字是库名还是编程主题

        Args:
            language: 编程语言
            keyword: 待判断的关键字

        Returns:
            包含分类结果的字典:
            {
                'is_library': True/False,
                'confidence': 0.0-1.0,
                'library_name': '库名' 或 None,
                'description': '描述'
            }
        """
        self._load_config()

        if not self._api_key:
            logger.warning("AI API key not configured, using heuristic detection")
            return self._heuristic_classify(language, keyword)

        prompt = f"""你是一个编程语言库/包识别专家。

请判断以下关键字在 {language} 语言中是一个“库/包/框架名称”还是一个“编程主题/概念”。

关键字: "{keyword}"
语言: {language}

判断标准:
- 库/包/框架名称: 像 numpy, pandas, requests, django, flask, spring, gin, express 这类可以通过包管理器安装的第三方库
- 编程主题/概念: 像 "异步编程", "数据处理", "HTTP请求", "设计模式", "logging", "threading" 这类描述编程概念或功能的词

注意:
- 标准库模块（如 Python 的 os, sys, json）视为“编程主题”，不是第三方库
- 中文关键字通常是“编程主题”
- 英文单词要仔细判断是否为常见的第三方库

请以JSON格式返回:
{{
  "is_library": true/false,
  "confidence": 0.0-1.0,
  "library_name": "库名称"或null,
  "description": "简短解释"
}}

只返回JSON，不要其他文字。"""

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            }

            data = {
                "model": self._model,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个编程语言库识别专家，只返回JSON格式结果。",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.1,  # 低温度以获得更稳定的结果
                "max_tokens": 200,
            }

            timeout = self.config.get("ai.timeout", 30)

            logger.info(f"Classifying keyword '{keyword}' for language {language}")

            response = requests.post(
                self._api_endpoint, headers=headers, json=data, timeout=timeout
            )

            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()

            # 解析JSON响应
            return self._parse_classify_response(content, keyword)

        except Exception as e:
            logger.warning(f"AI classification failed: {e}, using heuristic detection")
            return self._heuristic_classify(language, keyword)

    def _parse_classify_response(self, response: str, keyword: str) -> Dict[str, Any]:
        """
        解析分类AI响应

        Args:
            response: AI响应内容
            keyword: 原始关键字

        Returns:
            解析后的分类结果
        """
        try:
            # 尝试提取JSON
            response = response.strip()
            if response.startswith("```"):
                start = response.find("\n") + 1
                end = response.rfind("```")
                if end > start:
                    response = response[start:end].strip()

            data = json.loads(response)

            return {
                "is_library": data.get("is_library", False),
                "confidence": data.get("confidence", 0.5),
                "library_name": data.get("library_name") if data.get("is_library") else None,
                "description": data.get("description", ""),
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse classify response: {e}")
            return {
                "is_library": False,
                "confidence": 0.0,
                "library_name": None,
                "description": "Failed to parse AI response",
            }

    def _heuristic_classify(self, language: str, keyword: str) -> Dict[str, Any]:
        """
        启发式关键字分类（当AI不可用时使用）

        Args:
            language: 编程语言
            keyword: 待分类的关键字

        Returns:
            分类结果
        """
        kw = keyword.lower().strip()

        # 检查是否包含中文
        has_chinese = any("\u4e00" <= char <= "\u9fff" for char in kw)
        if has_chinese:
            return {
                "is_library": False,
                "confidence": 0.9,
                "library_name": None,
                "description": "包含中文，判断为编程主题",
            }

        # 常见的第三方库列表（按语言分类）
        common_libraries = {
            "python": {
                "numpy",
                "pandas",
                "requests",
                "flask",
                "django",
                "fastapi",
                "scikit-learn",
                "sklearn",
                "tensorflow",
                "pytorch",
                "torch",
                "matplotlib",
                "seaborn",
                "sqlalchemy",
                "celery",
                "redis",
                "beautifulsoup",
                "bs4",
                "scrapy",
                "selenium",
                "pytest",
                "pydantic",
                "httpx",
                "aiohttp",
                "uvicorn",
                "gunicorn",
                "pillow",
                "opencv",
                "cv2",
                "boto3",
                "pymongo",
                "psycopg2",
            },
            "java": {
                "spring",
                "spring-boot",
                "springboot",
                "hibernate",
                "mybatis",
                "junit",
                "mockito",
                "lombok",
                "jackson",
                "gson",
                "okhttp",
                "retrofit",
                "netty",
                "kafka",
                "rabbitmq",
                "redis",
                "jedis",
                "elasticsearch",
                "log4j",
                "slf4j",
                "logback",
                "guava",
            },
            "go": {
                "gin",
                "echo",
                "fiber",
                "beego",
                "gorm",
                "cobra",
                "viper",
                "zap",
                "logrus",
                "testify",
                "wire",
                "fx",
                "grpc",
                "protobuf",
            },
            "nodejs": {
                "express",
                "koa",
                "fastify",
                "nest",
                "nestjs",
                "next",
                "react",
                "vue",
                "angular",
                "axios",
                "lodash",
                "moment",
                "mongoose",
                "sequelize",
                "typeorm",
                "prisma",
                "jest",
                "mocha",
                "webpack",
                "vite",
                "socket.io",
                "redis",
                "bull",
            },
            "kubernetes": {
                "kubeskoop",
                "istio",
                "cilium",
                "linkerd",
                "calico",
                "flannel",
                "weave",
                "helm",
                "kustomize",
                "argocd",
                "flux",
                "prometheus-operator",
                "grafana",
                "loki",
                "falco",
                "kubevirt",
                "knative",
                "cert-manager",
            },
        }

        lang_libs = common_libraries.get(language.lower(), set())

        if kw in lang_libs:
            return {
                "is_library": True,
                "confidence": 0.95,
                "library_name": kw,
                "description": f"{kw} 是 {language} 常见的第三方库",
            }

        # 检查是否符合库名特征（全小写、无空格、合理长度）
        if (
            len(kw) >= 2
            and len(kw) <= 30
            and kw[0].isalpha()
            and all(c.isalnum() or c in "-_" for c in kw)
        ):
            return {
                "is_library": True,
                "confidence": 0.6,
                "library_name": kw,
                "description": "符合库名特征，可能是库名",
            }

        return {
            "is_library": False,
            "confidence": 0.7,
            "library_name": None,
            "description": "不符合库名特征，判断为编程主题",
        }
