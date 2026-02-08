# 🐍 Python 命令行速查表 (python-cli.md)

> Python开发必备的命令行参考手册，涵盖pip、虚拟环境、调试、测试、性能分析等核心功能，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [pip包管理](#pip包管理)
- [虚拟环境](#虚拟环境)
- [Python调试](#python调试)
- [测试工具](#测试工具)
- [性能分析](#性能分析)
- [代码质量](#代码质量)
- [项目管理](#项目管理)
- [部署工具](#部署工具)
- [版本管理](#版本管理)
- [最佳实践](#最佳实践)

---

## pip包管理

### 基础操作
```bash
# 安装包
pip install requests
pip install django==4.2.0
pip install -r requirements.txt

# 升级包
pip install --upgrade requests
pip install -U pip

# 卸载包
pip uninstall requests

# 查看已安装包
pip list
pip freeze
pip show requests
```

### 依赖管理
```bash
# 生成依赖文件
pip freeze > requirements.txt

# 从文件安装依赖
pip install -r requirements.txt

# 查看包依赖关系
pip show -f requests
pipdeptree

# 安全检查
pip install safety
safety check
```

---

## 虚拟环境

### venv虚拟环境
```bash
# 创建虚拟环境
python -m venv myenv
python3 -m venv myenv

# 激活虚拟环境
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows

# 退出虚拟环境
deactivate

# 删除虚拟环境
rm -rf myenv
```

### conda环境管理
```bash
# 创建环境
conda create -n myenv python=3.9
conda create -n myenv python=3.9 django requests

# 激活环境
conda activate myenv

# 退出环境
conda deactivate

# 删除环境
conda env remove -n myenv
```

---

## Python调试

### pdb调试器
```bash
# 命令行调试
python -m pdb script.py

# 代码中插入断点
import pdb; pdb.set_trace()
# 或者 Python 3.7+
breakpoint()

# pdb常用命令
(Pdb) l  # 列出代码
(Pdb) n  # 下一行
(Pdb) s  # 进入函数
(Pdb) c  # 继续执行
(Pdb) p variable  # 打印变量
(Pdb) pp variable  # 美化打印
```

### ipdb增强调试
```bash
# 安装ipdb
pip install ipdb

# 使用ipdb
import ipdb; ipdb.set_trace()

# 命令行使用
python -m ipdb script.py
```

---

## 测试工具

### unittest单元测试
```python
# test_example.py
import unittest

class TestExample(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)

if __name__ == '__main__':
    unittest.main()
```

```bash
# 运行测试
python -m unittest test_example.py
python -m unittest discover
python -m unittest discover -s tests -p "test_*.py"
```

### pytest测试框架
```bash
# 安装pytest
pip install pytest

# 运行测试
pytest
pytest test_file.py
pytest -v  # 详细输出

# 测试覆盖率
pip install pytest-cov
pytest --cov=src --cov-report=html

# 参数化测试
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6)
])
def test_double(input, expected):
    assert double(input) == expected
```

---

## 性能分析

### cProfile性能分析
```bash
# 命令行分析
python -m cProfile script.py
python -m cProfile -o profile_output.prof script.py

# 代码中分析
import cProfile
cProfile.run('main()')

# 分析结果查看
python -m pstats profile_output.prof
```

### line_profiler行级分析
```bash
# 安装line_profiler
pip install line_profiler

# 标记要分析的函数
@profile
def my_function():
    # 函数代码

# 运行分析
kernprof -l script.py
python -m line_profiler script.py.lprof
```

### memory_profiler内存分析
```bash
# 安装memory_profiler
pip install memory_profiler

# 标记函数
@profile
def my_function():
    # 函数代码

# 运行分析
python -m memory_profiler script.py
```

---

## 代码质量

### flake8代码检查
```bash
# 安装flake8
pip install flake8

# 运行检查
flake8 script.py
flake8 src/

# 配置文件 .flake8
[flake8]
max-line-length = 88
ignore = E203,W503
exclude = .git,__pycache__,venv
```

### black代码格式化
```bash
# 安装black
pip install black

# 格式化代码
black script.py
black src/

# 检查但不修改
black --check src/
```

### pylint静态分析
```bash
# 安装pylint
pip install pylint

# 运行分析
pylint script.py
pylint src/

# 配置文件 .pylintrc
[MESSAGES CONTROL]
disable=C0103,R0903
```

---

## 项目管理

### Poetry依赖管理
```bash
# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 初始化项目
poetry init
poetry new my-project

# 添加依赖
poetry add requests
poetry add pytest --group dev

# 安装依赖
poetry install

# 运行命令
poetry run python script.py
poetry shell
```

### setuptools打包
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
)
```

```bash
# 打包
python setup.py sdist bdist_wheel

# 上传到PyPI
pip install twine
twine upload dist/*
```

---

## 部署工具

### Docker部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
docker build -t myapp .
docker run -p 5000:5000 myapp
```

### Gunicorn WSGI服务器
```bash
# 安装Gunicorn
pip install gunicorn

# 启动应用
gunicorn app:app
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app

# 配置文件 gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 30
```

---

## 版本管理

### pyenv Python版本管理
```bash
# 安装pyenv
curl https://pyenv.run | bash

# 安装Python版本
pyenv install 3.9.16
pyenv install 3.11.2

# 设置版本
pyenv global 3.9.16
pyenv local 3.11.2
pyenv shell 3.9.16
```

### 项目版本配置
```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.9"
django = "^4.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"
```

---

## 最佳实践

### 项目结构模板
```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_module2.py
├── docs/
├── requirements.txt
├── setup.py
├── .gitignore
├── .flake8
└── README.md
```

### Makefile自动化
```makefile
.PHONY: install test lint format clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	flake8 src/
	black --check src/

format:
	black src/
	isort src/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
```

### 环境变量管理
```python
# .env文件
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key

# app.py
import os
from dotenv import load_dotenv

load_dotenv()
debug = os.getenv('DEBUG', 'False').lower() == 'true'
```

---