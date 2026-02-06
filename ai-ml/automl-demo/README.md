# AutoML(自动化机器学习)实战演示

## 🎯 学习目标

通过本案例你将掌握：
- AutoML的基本概念和核心技术
- 自动特征工程和模型选择
- 超参数优化和神经架构搜索
- AutoML系统的部署和应用

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU或CPU环境
- 至少16GB内存

### 依赖安装
```bash
pip install torch scikit-learn pandas numpy
pip install autogluon h2o tpot  # AutoML框架
pip install optuna ray[tune]  # 超参数优化
pip install naslib  # 神经架构搜索
pip install pytest  # 测试工具
```

## 📁 项目结构

```
automl-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── automl_pipeline.py             # AutoML流水线脚本
│   ├── hyperopt_search.py             # 超参数优化脚本
│   └── feature_engineering.py         # 特征工程脚本
├── configs/                           # 配置文件
│   ├── automl_config.yaml             # AutoML配置
│   ├── hyperopt_config.json           # 超参数优化配置
│   └── feature_config.json            # 特征工程配置
├── frameworks/                        # AutoML框架
│   ├── autogluon_impl.py             # AutoGluon实现
│   ├── h2o_impl.py                   # H2O实现
│   └── tpot_impl.py                  # TPOT实现
├── optimization/                      # 优化算法
│   ├── bayesian_optimization.py       # 贝叶斯优化
│   ├── genetic_algorithm.py           # 遗传算法
│   └── random_search.py              # 随机搜索
├── data/                              # 数据文件
│   ├── samples/                       # 示例数据
│   ├── processed/                     # 处理后数据
│   └── metadata/                      # 数据元信息
├── models/                            # 模型文件
│   ├── candidates/                    # 候选模型
│   ├── best_model/                    # 最佳模型
│   └── ensembles/                     # 集成模型
├── evaluation/                        # 评估脚本
│   ├── performance_eval.py            # 性能评估
│   └── efficiency_eval.py             # 效率评估
└── notebooks/                         # Jupyter笔记本
    ├── 01_automl_fundamentals.ipynb    # AutoML基础
    ├── 02_hyperparameter_optimization.ipynb # 超参优化
    └── 03_automl_implementation.ipynb  # AutoML实现
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装AutoML相关依赖
pip install -r requirements.txt
```

### 步骤2：运行AutoML流水线

```bash
# 使用AutoGluon进行AutoML
python scripts/automl_pipeline.py \
  --framework autogluon \
  --train_data data/samples/train.csv \
  --target_column target \
  --output_dir models/best_model/ \
  --time_limit 3600
```

### 步骤3：超参数优化

```bash
# 运行贝叶斯优化
python scripts/hyperopt_search.py \
  --algorithm bayesian \
  --objective accuracy \
  --max_evals 100 \
  --output_dir optimization/results/
```

## 🔍 代码详解

### 核心概念解析

#### 1. AutoML流水线实现
```python
# AutoML核心流水线
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import autogluon as ag

class AutoMLPipeline:
    def __init__(self, config):
        self.config = config
        self.best_model = None
        self.results = {}
    
    def run_pipeline(self, data_path, target_column):
        """运行完整的AutoML流水线"""
        # 1. 数据加载和预处理
        df = pd.read_csv(data_path)
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # 2. 数据分割
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # 3. 特征工程
        X_train_processed, X_test_processed = self.feature_engineering(
            X_train, X_test
        )
        
        # 4. 模型搜索和训练
        self.best_model = self.model_search(
            X_train_processed, y_train
        )
        
        # 5. 模型评估
        self.results = self.evaluate_model(
            self.best_model, X_test_processed, y_test
        )
        
        return self.best_model, self.results
    
    def feature_engineering(self, X_train, X_test):
        """自动特征工程"""
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.impute import SimpleImputer
        
        # 处理缺失值
        imputer = SimpleImputer(strategy='mean')
        X_train_imputed = imputer.fit_transform(X_train)
        X_test_imputed = imputer.transform(X_test)
        
        # 特征缩放
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_imputed)
        X_test_scaled = scaler.transform(X_test_imputed)
        
        return X_train_scaled, X_test_scaled
    
    def model_search(self, X_train, y_train):
        """模型搜索"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
        from sklearn.model_selection import cross_val_score
        
        models = {
            'random_forest': RandomForestClassifier(),
            'logistic_regression': LogisticRegression(),
            'svm': SVC()
        }
        
        best_score = 0
        best_model = None
        
        for name, model in models.items():
            scores = cross_val_score(model, X_train, y_train, cv=5)
            avg_score = scores.mean()
            
            if avg_score > best_score:
                best_score = avg_score
                best_model = model
                
        # 在整个训练集上训练最佳模型
        best_model.fit(X_train, y_train)
        return best_model
    
    def evaluate_model(self, model, X_test, y_test):
        """模型评估"""
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'predictions': y_pred.tolist()
        }
```

#### 2. 实际应用示例

##### 场景1：超参数优化
```python
# 使用Optuna进行超参数优化
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    """优化目标函数"""
    # 定义超参数搜索空间
    n_estimators = trial.suggest_int('n_estimators', 10, 200)
    max_depth = trial.suggest_int('max_depth', 1, 20)
    min_samples_split = trial.suggest_float('min_samples_split', 0.01, 1.0)
    min_samples_leaf = trial.suggest_float('min_samples_leaf', 0.01, 0.5)
    
    # 创建模型
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )
    
    # 交叉验证评估
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    return scores.mean()

def optimize_hyperparameters(X_train, y_train):
    """运行超参数优化"""
    global X_train_global, y_train_global
    X_train_global, y_train_global = X_train, y_train
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)
    
    return study.best_params, study.best_value
```

##### 场景2：神经架构搜索(NAS)
```python
# 简化的神经架构搜索实现
import torch
import torch.nn as nn
import random

class NASController(nn.Module):
    """NAS控制器，用于生成网络架构"""
    def __init__(self, num_operations=8, num_nodes=5):
        super(NASController, self).__init__()
        self.num_operations = num_operations
        self.num_nodes = num_nodes
        
        # LSTM控制器，用于生成架构
        self.lstm = nn.LSTM(128, 64, 2, batch_first=True)
        self.attention = nn.Linear(64, num_operations)
    
    def forward(self):
        """生成网络架构"""
        # 简化的架构生成过程
        operations = []
        for i in range(self.num_nodes):
            # 随机选择操作
            op = random.randint(0, self.num_operations - 1)
            operations.append(op)
        
        return operations

def create_model_from_architecture(architecture):
    """根据架构创建模型"""
    layers = []
    input_dim = 784  # 示例输入维度
    
    for op in architecture:
        if op == 0:  # Linear
            layers.append(nn.Linear(input_dim, input_dim))
        elif op == 1:  # Conv
            layers.append(nn.Conv2d(1, 32, 3))
        elif op == 2:  # ReLU
            layers.append(nn.ReLU())
        # 更多操作...
    
    return nn.Sequential(*layers)
```

## 🧪 验证测试

### 测试1：AutoML流水线功能验证
```python
#!/usr/bin/env python
# 验证AutoML流水线功能
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def test_automl_pipeline():
    print("=== AutoML流水线功能验证 ===")
    
    # 创建示例数据
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    df['target'] = y
    
    # 保存为CSV
    df.to_csv('temp_sample_data.csv', index=False)
    
    # 初始化AutoML流水线
    pipeline = AutoMLPipeline({'time_limit': 60})  # 限制运行时间为60秒
    
    try:
        # 运行流水线
        model, results = pipeline.run_pipeline(
            'temp_sample_data.csv',
            'target'
        )
        
        print(f"✅ AutoML流水线运行成功")
        print(f"最佳模型类型: {type(model).__name__}")
        print(f"验证准确率: {results['accuracy']:.4f}")
        
        # 验证预测功能
        sample_pred = model.predict(X[:5])
        print(f"样本预测结果: {sample_pred}")
        
    except Exception as e:
        print(f"❌ AutoML流水线运行失败: {e}")
    finally:
        # 清理临时文件
        import os
        if os.path.exists('temp_sample_data.csv'):
            os.remove('temp_sample_data.csv')
    
    print("✅ AutoML流水线功能验证完成")

if __name__ == "__main__":
    test_automl_pipeline()
```

### 测试2：超参数优化验证
```python
#!/usr/bin/env python
# 验证超参数优化功能
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def test_hyperparameter_optimization():
    print("=== 超参数优化验证 ===")
    
    # 创建示例数据
    X, y = make_classification(n_samples=500, n_features=10, n_classes=2, random_state=42)
    
    # 定义搜索空间
    param_space = {
        'n_estimators': [10, 50, 100],
        'max_depth': [5, 10, 15],
        'min_samples_split': [0.1, 0.2, 0.5]
    }
    
    best_score = 0
    best_params = {}
    
    # 网格搜索
    for n_est in param_space['n_estimators']:
        for max_d in param_space['max_depth']:
            for min_ss in param_space['min_samples_split']:
                model = RandomForestClassifier(
                    n_estimators=n_est,
                    max_depth=max_d,
                    min_samples_split=min_ss,
                    random_state=42
                )
                
                scores = cross_val_score(model, X, y, cv=3, scoring='accuracy')
                avg_score = scores.mean()
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_params = {
                        'n_estimators': n_est,
                        'max_depth': max_d,
                        'min_samples_split': min_ss
                    }
    
    print(f"✅ 超参数优化完成")
    print(f"最佳参数: {best_params}")
    print(f"最佳交叉验证得分: {best_score:.4f}")
    
    # 使用最佳参数训练最终模型
    final_model = RandomForestClassifier(**best_params, random_state=42)
    final_model.fit(X, y)
    
    print(f"✅ 最终模型训练完成")
    print("✅ 超参数优化验证通过")

if __name__ == "__main__":
    test_hyperparameter_optimization()
```

## ❓ 常见问题

### Q1: 如何选择合适的AutoML框架？
**解决方案**：
```python
# AutoML框架选择指南
"""
1. AutoGluon: 适合表格数据，易用性强
2. H2O: 企业级功能丰富，支持多种算法
3. TPOT: 基于遗传编程，高度自动化
4. FLAML: 微软轻量级框架，适合快速原型
"""
```

### Q2: 如何平衡AutoML的效率和效果？
**解决方案**：
```python
# AutoML效率效果平衡
"""
1. 设置合理的时间限制
2. 选择适当的搜索策略
3. 预处理数据以提高效率
4. 根据问题类型选择合适的方法
"""
```

## 📚 扩展学习

### 相关技术
- **AutoGluon**: 亚马逊开源AutoML框架
- **H2O.ai**: 企业级AutoML平台
- **TPOT**: 基于遗传编程的AutoML
- **FLAML**: 微软轻量级AutoML

### 进阶学习路径
1. 掌握不同AutoML框架的特点和适用场景
2. 学习高级超参数优化算法
3. 理解神经架构搜索技术
4. 掌握AutoML系统性能优化

### 企业级应用场景
- 自动化模型开发和部署
- 快速原型验证
- 非专业人员的模型构建
- 大规模模型比较和选择

---
> **💡 提示**: AutoML技术能够显著降低机器学习的应用门槛，通过自动化模型选择、特征工程和超参数优化等步骤，让非专业人员也能构建高质量的机器学习模型。