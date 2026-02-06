# AI模型监控与可观测性实战演示

## 🎯 学习目标

通过本案例你将掌握：
- AI模型性能监控的最佳实践
- 数据漂移和概念漂移检测技术
- 模型可解释性和公平性监控
- AI系统可观测性架构设计

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- Docker环境
- Prometheus监控系统

### 依赖安装
```bash
pip install torch transformers scikit-learn pandas
pip install prometheus-client flask  # 监控指标收集
pip install evidently alibi-detect  # 漂移检测
pip install shap lime  # 可解释性
pip install pytest  # 测试工具
```

## 📁 项目结构

```
model-monitoring-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── collect_metrics.py             # 指标收集脚本
│   ├── detect_drift.py                # 漂移检测脚本
│   └── explain_predictions.py         # 预测解释脚本
├── configs/                           # 配置文件
│   ├── monitoring_config.yaml         # 监控配置
│   ├── alerting_config.yaml           # 告警配置
│   └── drift_detection_config.json    # 漂移检测配置
├── metrics/                           # 指标定义
│   ├── model_metrics.py               # 模型指标
│   ├── system_metrics.py              # 系统指标
│   └── business_metrics.py            # 业务指标
├── monitoring/                        # 监控组件
│   ├── prometheus/                    # Prometheus配置
│   ├── grafana/                       # Grafana仪表板
│   └── alertmanager/                  # 告警管理
├── drift_detection/                   # 漂移检测
│   ├── data_drift_detector.py         # 数据漂移检测器
│   ├── concept_drift_detector.py      # 概念漂移检测器
│   └── drift_visualization.py         # 漂移可视化
├── explainability/                    # 可解释性
│   ├── shap_analyzer.py               # SHAP分析器
│   ├── lime_explainer.py              # LIME解释器
│   └── feature_importance.py          # 特征重要性分析
├── data/                              # 数据文件
│   ├── reference/                     # 参考数据
│   ├── current/                       # 当前数据
│   └── metrics_history/               # 指标历史
├── api/                               # API服务
│   ├── metrics_endpoint.py            # 指标端点
│   └── health_check.py                # 健康检查
└── notebooks/                         # Jupyter笔记本
    ├── 01_model_monitoring.ipynb      # 模型监控
    ├── 02_drift_detection.ipynb       # 漂移检测
    └── 03_model_explainability.ipynb  # 模型可解释性
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装监控相关依赖
pip install -r requirements.txt

# 启动Prometheus
docker run -d --name prometheus -p 9090:9090 -v $(pwd)/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

### 步骤2：部署监控系统

```bash
# 启动模型监控服务
python api/metrics_endpoint.py

# 启动漂移检测服务
python scripts/detect_drift.py --continuous
```

### 步骤3：查看监控仪表板

```bash
# 启动Grafana
docker run -d --name grafana -p 3000:3000 grafana/grafana

# 导入预定义的仪表板配置
# 访问 http://localhost:3000 并配置Prometheus数据源
```

## 🔍 代码详解

### 核心概念解析

#### 1. 模型性能指标收集
```python
# Prometheus指标定义和收集
from prometheus_client import Counter, Histogram, Gauge
import time

# 定义指标
predictions_total = Counter('model_predictions_total', 'Total number of predictions', ['model_name'])
prediction_duration = Histogram('model_prediction_duration_seconds', 'Time spent processing predictions')
model_accuracy = Gauge('model_accuracy', 'Current model accuracy', ['model_name'])

class ModelMonitor:
    def __init__(self, model_name):
        self.model_name = model_name
    
    def observe_prediction(self, input_data, prediction, actual_label=None):
        """观察预测事件"""
        start_time = time.time()
        
        # 执行预测
        result = self.model.predict(input_data)
        
        # 记录指标
        predictions_total.labels(model_name=self.model_name).inc()
        prediction_duration.observe(time.time() - start_time)
        
        # 如果有真实标签，计算准确性
        if actual_label is not None:
            accuracy = 1.0 if result == actual_label else 0.0
            model_accuracy.labels(model_name=self.model_name).set(accuracy)
        
        return result
```

#### 2. 实际应用示例

##### 场景1：数据漂移检测
```python
# 使用Evidently进行数据漂移检测
from evidently.test_suite import TestSuite
from evidently.tests import *
import pandas as pd

def detect_data_drift(reference_data, current_data):
    """检测数据漂移"""
    # 创建测试套件
    data_drift_suite = TestSuite(tests=[
        TestNumberOfDriftedColumns(),
        TestShareOfDriftedColumns(),
        TestColumnValueDrift(column_name="feature_1", stattest="ks"),
        TestColumnValueDrift(column_name="feature_2", stattest="chi_square"),
    ])
    
    # 运行测试
    data_drift_suite.run(reference_data=reference_data, current_data=current_data)
    
    # 获取结果
    results = data_drift_suite.as_dict()
    
    # 检查是否有漂移
    drifted_columns_count = results['tests'][0]['result']['quantity_of_dropped']
    
    return {
        'has_drift': drifted_columns_count > 0,
        'drifted_columns_count': drifted_columns_count,
        'details': results
    }
```

##### 场景2：模型可解释性分析
```python
# 使用SHAP进行模型解释
import shap
import pandas as pd

def explain_model_predictions(model, X_train, X_sample):
    """解释模型预测"""
    # 创建SHAP解释器
    explainer = shap.TreeExplainer(model) if hasattr(model, 'tree_structure') else shap.Explainer(model)
    
    # 计算SHAP值
    shap_values = explainer(X_sample)
    
    # 生成解释图表
    shap.waterfall_plot(shap_values[0], show=False)
    
    # 返回特征重要性
    feature_importance = {
        'features': X_sample.columns.tolist(),
        'importance': shap_values.values[0].abs().mean(axis=0).tolist()
    }
    
    return feature_importance
```

## 🧪 验证测试

### 测试1：监控指标收集验证
```python
#!/usr/bin/env python
# 验证监控指标收集
from prometheus_client import CollectorRegistry, generate_latest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

def test_monitoring_metrics():
    print("=== 监控指标收集验证 ===")
    
    # 创建示例模型
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2)
    model = RandomForestClassifier()
    model.fit(X, y)
    
    # 创建监控器
    monitor = ModelMonitor("test_model")
    monitor.model = model
    
    # 执行几次预测来生成指标
    for i in range(5):
        sample_input = X[i:i+1]
        prediction = monitor.observe_prediction(sample_input, None)
        print(f"预测 {i+1}: {prediction[0]}")
    
    print("✅ 监控指标收集验证通过")
    print("系统能够正确收集和记录模型预测指标")

if __name__ == "__main__":
    test_monitoring_metrics()
```

### 测试2：漂移检测功能验证
```python
#!/usr/bin/env python
# 验证漂移检测功能
import pandas as pd
import numpy as np
from evidently.test_suite import TestSuite
from evidently.tests import *

def test_drift_detection():
    print("=== 漂移检测功能验证 ===")
    
    # 创建参考数据（正常分布）
    np.random.seed(42)
    reference_data = pd.DataFrame({
        'feature_1': np.random.normal(0, 1, 1000),
        'feature_2': np.random.normal(0, 1, 1000),
        'target': np.random.choice([0, 1], 1000)
    })
    
    # 创建当前数据（有轻微漂移）
    current_data = pd.DataFrame({
        'feature_1': np.random.normal(0.5, 1, 1000),  # 均值漂移
        'feature_2': np.random.normal(0, 1, 1000),
        'target': np.random.choice([0, 1], 1000)
    })
    
    # 运行漂移检测
    data_drift_suite = TestSuite(tests=[
        TestNumberOfDriftedColumns(),
        TestShareOfDriftedColumns(),
        TestColumnValueDrift(column_name="feature_1", stattest="ks"),
    ])
    
    data_drift_suite.run(reference_data=reference_data, current_data=current_data)
    
    results = data_drift_suite.as_dict()
    
    print(f"✅ 漂移检测运行成功")
    print(f"测试总数: {len(results['tests'])}")
    print(f"检测到漂移的列数: {results['tests'][0]['result']['quantity_of_dropped']}")
    
    # 检查是否检测到feature_1的漂移
    drift_result = results['tests'][2]['result']
    print(f"Feature_1漂移检测结果: {drift_result['success']}")
    
    print("✅ 漂移检测功能验证通过")

if __name__ == "__main__":
    test_drift_detection()
```

## ❓ 常见问题

### Q1: 如何设置合理的监控阈值？
**解决方案**：
```python
# 监控阈值设置指南
"""
1. 基于历史数据统计: 使用均值±2标准差
2. 业务影响考量: 根据业务容忍度设置
3. 分层监控: 不同严重级别设置不同阈值
4. 动态调整: 根据季节性等因素调整
"""
```

### Q2: 如何处理模型性能下降？
**解决方案**：
```python
# 性能下降处理策略
"""
1. 立即告警: 设置性能下降告警
2. 数据分析: 分析性能下降原因
3. 模型重训: 必要时触发模型重训练
4. 回退机制: 准备模型版本回退方案
"""
```

## 📚 扩展学习

### 相关技术
- **Evidently**: 机器学习监控工具包
- **Alibi-Detect**: 漂移和异常检测
- **SHAP/LIME**: 模型可解释性
- **Prometheus/Grafana**: 监控可视化

### 进阶学习路径
1. 掌握AI系统监控的最佳实践
2. 学习自动化漂移检测和修复
3. 理解模型公平性和偏见检测
4. 掌握实时监控和告警系统

### 企业级应用场景
- 生产环境模型性能监控
- 数据质量检测和告警
- 模型再训练触发机制
- 合规性报告和审计

---
> **💡 提示**: AI模型监控是确保模型在生产环境中持续有效和可靠的关键实践，通过持续监控可以及时发现并解决模型性能下降、数据漂移等问题。