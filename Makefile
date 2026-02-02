# OpenDemo 项目 Makefile
# 用于项目构建、测试和维护的自动化工具

.PHONY: help clean test build docs validate all

# 默认目标
help:
	@echo "OpenDemo 项目自动化工具"
	@echo ""
	@echo "可用命令:"
	@echo "  help          - 显示此帮助信息"
	@echo "  clean         - 清理构建产物和缓存"
	@echo "  test          - 运行所有测试"
	@echo "  build         - 构建项目"
	@echo "  docs          - 生成文档"
	@echo "  validate      - 验证案例质量"
	@echo "  all           - 执行完整构建流程"
	@echo "  setup         - 设置开发环境"
	@echo "  check         - 执行代码质量检查"
	@echo "  update-index  - 更新案例索引"

# 清理目标
clean:
	@echo "清理项目..."
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} +
	@echo "清理完成"

# 测试目标
test:
	@echo "运行测试套件..."
	python -m pytest tests/ -v --tb=short
	@echo "测试完成"

# 构建目标
build:
	@echo "构建项目..."
	pip install -e .
	@echo "构建完成"

# 文档生成
docs:
	@echo "生成文档..."
	python scripts/generate_demo_list.py
	python scripts/update_readme.py
	@echo "文档生成完成"

# 案例验证
validate:
	@echo "验证案例质量..."
	python scripts/java_demo_validator.py --validate-all --report validation_report.json
	@echo "验证完成，报告已生成"

# 完整构建流程
all: clean test build docs validate
	@echo "完整构建流程完成"

# 开发环境设置
setup:
	@echo "设置开发环境..."
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "开发环境设置完成"

# 代码质量检查
check:
	@echo "执行代码质量检查..."
	flake8 cli/ tests/ scripts/
	mypy cli/ tests/
	bandit -r cli/
	@echo "代码质量检查完成"

# 更新案例索引
update-index:
	@echo "更新案例索引..."
	python scripts/generate_demo_list.py
	@echo "索引更新完成"

# 特定技术栈操作
java-test:
	@echo "测试Java案例..."
	cd java && find . -name "*.java" -exec javac {} \;

go-test:
	@echo "测试Go案例..."
	cd go && find . -name "go.mod" -exec go test ./... \;

python-test:
	@echo "测试Python案例..."
	cd python && find . -name "requirements.txt" -exec pip install -r {} \;

# 项目统计
stats:
	@echo "项目统计信息:"
	@echo "总案例数: $$(find . -name "README.md" -path "*/[^.]*/README.md" | wc -l)"
	@echo "Java案例: $$(find java -name "README.md" | wc -l)"
	@echo "Go案例: $$(find go -name "README.md" | wc -l)"
	@echo "Python案例: $$(find python -name "README.md" | wc -l)"
	@echo "Kubernetes案例: $$(find kubernetes -name "README.md" | wc -l)"

# 版本信息
version:
	@echo "OpenDemo 项目版本信息"
	@echo "当前版本: 1.0.0"
	@echo "最后更新: 2026-01-31"
	@echo "Python版本: $$(python --version)"
	@echo "Git分支: $$(git branch --show-current)"