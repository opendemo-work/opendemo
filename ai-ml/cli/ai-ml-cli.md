# 🤖 AI/ML 命令行速查表 (ai-ml-cli.md)

> AI/ML开发和部署必备的命令行参考手册，涵盖机器学习、深度学习、大模型训练等核心工具链，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [Python ML环境](#python-ml环境)
- [深度学习框架](#深度学习框架)
- [AutoML工具](#automl工具)
- [大模型训练](#大模型训练)
- [数据处理](#数据处理)
- [模型部署](#模型部署)
- [实验跟踪](#实验跟踪)
- [性能监控](#性能监控)
- [分布式训练](#分布式训练)
- [模型优化](#模型优化)
- [推理服务](#推理服务)
- [可视化分析](#可视化分析)
- [测试验证](#测试验证)
- [最佳实践](#最佳实践)

---

## Python ML环境

### 环境管理
```bash
# 创建ML专用环境
conda create -n ml-env python=3.9
conda activate ml-env

# 安装基础科学计算库
pip install numpy scipy pandas matplotlib seaborn

# 安装Jupyter环境
pip install jupyter jupyterlab ipywidgets
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

# 虚拟环境管理
python -m venv ml_project
source ml_project/bin/activate  # Linux/Mac
ml_project\Scripts\activate     # Windows
```

### 核心ML库安装
```bash
# Scikit-learn生态系统
pip install scikit-learn scikit-optimize imbalanced-learn

# 数据处理和特征工程
pip install pandas numpy polars dask featuretools

# 统计分析
pip install statsmodels pingouin

# 时间序列分析
pip install prophet pmdarima tsfresh

# 强化学习
pip install gymnasium stable-baselines3 ray[rllib]
```

### GPU环境配置
```bash
# CUDA环境检查
nvidia-smi
nvcc --version

# PyTorch GPU版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# TensorFlow GPU版本
pip install tensorflow[and-cuda]

# JAX GPU支持
pip install "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

---

## 深度学习框架

### PyTorch生态
```bash
# 核心PyTorch安装
pip install torch torchvision torchaudio

# PyTorch扩展库
pip install torch-geometric  # 图神经网络
pip install pytorch-lightning  # 训练框架
pip install torchmetrics  # 指标计算
pip install torchsummary  # 模型摘要

# 计算机视觉
pip install torchvision timm efficientnet-pytorch

# 自然语言处理
pip install transformers datasets tokenizers

# 优化加速
pip install apex  # NVIDIA Apex混合精度训练
pip install deepspeed  # 微软DeepSpeed
pip install flash-attn  # 闪存注意力优化
```

### TensorFlow/Keras生态
```bash
# TensorFlow核心
pip install tensorflow

# Keras扩展
pip install keras-tuner  # 超参数调优
pip install tf-agents  # 强化学习
pip install tensorflow-probability  # 概率建模

# TensorFlow扩展
pip install tensorflow-addons
pip install tensorflow-datasets
pip install tensorflow-model-optimization

# TensorBoard工具
pip install tensorboard tensorboard-plugin-profile
tensorboard --logdir=./logs --bind_all
```

### 其他深度学习框架
```bash
# JAX生态
pip install jax jaxlib flax optax

# MXNet
pip install mxnet-cu112

# PaddlePaddle
pip install paddlepaddle-gpu

# MindSpore
pip install mindspore-gpu
```

---

## AutoML工具

### AutoML框架
```bash
# AutoGluon
pip install autogluon
python -c "from autogluon.tabular import TabularPredictor; print('AutoGluon ready')"

# H2O.ai
pip install h2o
h2o.init()

# TPOT (遗传编程)
pip install tpot
python -c "from tpot import TPOTClassifier; print('TPOT ready')"

# Auto-sklearn
pip install auto-sklearn

# MLBox
pip install mlbox
```

### 超参数优化
```bash
# Optuna
pip install optuna
python -c "import optuna; print('Optuna ready')"

# Ray Tune
pip install ray[tune]
ray start --head

# Hyperopt
pip install hyperopt

# Scikit-Optimize
pip install scikit-optimize

# Ax Platform (Facebook)
pip install ax-platform
```

### 神经架构搜索
```bash
# NASLib
pip install naslib

# DARTS
pip install darts

# EfficientNet搜索
pip install efficientnet-pytorch
```

---

## 大模型训练

### LLM训练框架
```bash
# Hugging Face Transformers
pip install transformers accelerate datasets peft

# 大模型训练工具
pip install deepspeed  # 微软分布式训练
pip install megatron-lm  # NVIDIA大模型训练
pip install alpa  # Google自动并行化

# 模型量化和压缩
pip install bitsandbytes  # 4-bit量化
pip install auto-gptq  # GPTQ量化
```

### 训练脚本示例
```bash
# 单机多卡训练
torchrun --nproc_per_node=4 train_script.py

# 分布式训练启动
deepspeed --num_gpus=8 train.py --deepspeed ds_config.json

# 混合精度训练
python train.py --fp16 --gradient_checkpointing

# 梯度累积
python train.py --gradient_accumulation_steps=4
```

### 训练监控
```bash
# Weights & Biases
pip install wandb
wandb login YOUR_API_KEY

# MLflow
pip install mlflow
mlflow ui --host 0.0.0.0 --port 5000

# TensorBoard
tensorboard --logdir=./runs --bind_all
```

---

## 数据处理

### 数据加载和预处理
```python
# PyTorch数据处理
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

# TensorFlow数据处理
import tensorflow as tf
from tensorflow.data import Dataset

# HuggingFace数据集
from datasets import load_dataset
dataset = load_dataset('glue', 'mrpc')

# Pandas数据处理
import pandas as pd
df = pd.read_csv('data.csv')
```

### 特征工程
```bash
# FeatureTools自动化特征工程
pip install featuretools

# 数据清洗
pip install pandas-profiling

# 类别特征编码
pip install category_encoders

# 特征选择
pip install scikit-feature
```

### 数据增强
```bash
# 图像增强
pip install albumentations imgaug

# 文本增强
pip install nlpaug

# 音频增强
pip install audiomentations
```

---

## 模型部署

### 模型转换和优化
```bash
# ONNX转换
pip install onnx onnxruntime
python -m tf2onnx.convert --saved-model ./model --output model.onnx

# TensorRT优化
pip install tensorrt

# OpenVINO优化
pip install openvino

# TorchScript编译
torch.jit.trace(model, example_inputs)
```

### 推理服务框架
```bash
# FastAPI部署
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Flask部署
pip install flask flask-restful

# Triton Inference Server
docker run --gpus=1 --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 nvcr.io/nvidia/tritonserver:23.01-py3 tritonserver --model-repository=/models

# TorchServe
torch-model-archiver --model-name my_model --version 1.0 --model-file model.py --serialized-file model.pth --handler image_classifier
torchserve --start --model-store model_store
```

### 容器化部署
```bash
# Docker构建
docker build -t ml-model:v1 .

# Kubernetes部署
kubectl apply -f model-deployment.yaml

# Helm Chart
helm install ml-model ./ml-model-chart
```

---

## 实验跟踪

### Weights & Biases
```bash
# 初始化项目
wandb init --project my-project

# 记录指标
import wandb
wandb.log({"accuracy": 0.95, "loss": 0.1})

# 配置跟踪
wandb.config.update({"learning_rate": 0.001, "batch_size": 32})
```

### MLflow
```bash
# 启动MLflow服务器
mlflow server --host 0.0.0.0 --port 5000

# Python API使用
import mlflow
mlflow.start_run()
mlflow.log_param("learning_rate", 0.01)
mlflow.log_metric("accuracy", 0.95)
mlflow.end_run()
```

### Neptune.ai
```bash
pip install neptune
neptune.init(project="your-project")
```

---

## 性能监控

### GPU监控
```bash
# 实时GPU监控
watch -n 1 nvidia-smi

# GPU详细信息
nvidia-smi -q -d MEMORY,UTILIZATION,POWER,CLOCK,COMPUTE

# 进程GPU使用
nvidia-smi pmon

# GPU拓扑查看
nvidia-smi topo -m
```

### 系统性能监控
```bash
# 系统资源监控
htop
iotop
nethogs

# 内存分析
python -m memory_profiler script.py

# CPU性能分析
perf record -g python script.py
perf report

# I/O监控
iostat -x 1
```

### 训练性能分析
```bash
# PyTorch Profiler
from torch.profiler import profile, record_function, ProfilerActivity
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    # 训练代码
    pass
prof.export_chrome_trace("trace.json")

# TensorFlow Profiler
tf.profiler.experimental.start('logdir')
# 训练代码
tf.profiler.experimental.stop()
```

---

## 分布式训练

### PyTorch分布式
```bash
# 单机多卡
torchrun --nproc_per_node=4 train.py

# 多机多卡
torchrun --nnodes=2 --nproc_per_node=4 --master_addr="192.168.1.1" --master_port=1234 train.py

# 初始化分布式环境
import torch.distributed as dist
dist.init_process_group(backend='nccl', init_method='env://')
```

### DeepSpeed配置
```json
{
    "train_batch_size": 32,
    "gradient_accumulation_steps": 1,
    "optimizer": {
        "type": "Adam",
        "params": {
            "lr": 0.001
        }
    },
    "fp16": {
        "enabled": true
    },
    "zero_optimization": {
        "stage": 2
    }
}
```

### Horovod
```bash
pip install horovod[pytorch]
horovodrun -np 4 -H localhost:4 python train.py
```

---

## 模型优化

### 模型量化
```python
# PyTorch量化
import torch.quantization as quantization
model_quantized = quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

# TensorFlow Lite量化
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()
```

### 模型剪枝
```python
# PyTorch剪枝
import torch.nn.utils.prune as prune
prune.l1_unstructured(module, name="weight", amount=0.3)

# TensorFlow Model Optimization
import tensorflow_model_optimization as tfmot
prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude
```

### 知识蒸馏
```python
# 教师-学生网络训练
teacher_model = TeacherModel()
student_model = StudentModel()

# 蒸馏损失函数
def distillation_loss(student_logits, teacher_logits, labels, temperature=3.0):
    soft_targets = F.softmax(teacher_logits / temperature, dim=-1)
    soft_prob = F.log_softmax(student_logits / temperature, dim=-1)
    distill_loss = F.kl_div(soft_prob, soft_targets, reduction='batchmean')
    return distill_loss
```

---

## 推理服务

### 模型服务化
```bash
# TorchServe部署
torch-model-archiver --model-name resnet50 --version 1.0 \
    --model-file model.py --serialized-file resnet50.pth \
    --handler image_classifier --extra-files index_to_name.json

torchserve --start --model-store model_store --models resnet50=resnet50.mar

# 请求示例
curl -X POST http://localhost:8080/predictions/resnet50 -T image.jpg
```

### API服务构建
```python
# FastAPI示例
from fastapi import FastAPI, File, UploadFile
import torch
from PIL import Image

app = FastAPI()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file)
    # 预处理和推理
    return {"prediction": result.tolist()}
```

### 批量推理
```python
# 批量处理脚本
def batch_inference(model, data_loader, batch_size=32):
    results = []
    model.eval()
    with torch.no_grad():
        for batch in data_loader:
            outputs = model(batch)
            results.extend(outputs.cpu().numpy())
    return results
```

---

## 可视化分析

### 训练可视化
```python
# Matplotlib基础绘图
import matplotlib.pyplot as plt
plt.plot(epochs, train_loss, label='Training Loss')
plt.plot(epochs, val_loss, label='Validation Loss')
plt.legend()
plt.show()

# Seaborn美化
import seaborn as sns
sns.lineplot(data=df, x='epoch', y='loss')

# Plotly交互式图表
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=epochs, y=train_acc, name='Train Accuracy'))
```

### 混淆矩阵和ROC曲线
```python
# Scikit-learn评估
from sklearn.metrics import confusion_matrix, roc_curve, auc
import seaborn as sns

# 混淆矩阵
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d')

# ROC曲线
fpr, tpr, _ = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)
```

### 特征重要性可视化
```python
# SHAP值分析
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X)

# LIME局部解释
from lime import lime_tabular
explainer = lime_tabular.LimeTabularExplainer(training_data)
exp = explainer.explain_instance(instance, model.predict_proba)
```

---

## 测试验证

### 单元测试
```bash
# PyTest基础
pip install pytest pytest-cov
pytest test_model.py -v

# 覆盖率报告
pytest --cov=model --cov-report=html

# 参数化测试
@pytest.mark.parametrize("input,output", [(1, 2), (2, 4)])
def test_double(input, output):
    assert double(input) == output
```

### 模型验证
```python
# 交叉验证
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)

# 学习曲线
from sklearn.model_selection import learning_curve
train_sizes, train_scores, val_scores = learning_curve(model, X, y)

# 验证曲线
from sklearn.model_selection import validation_curve
param_range = [0.001, 0.01, 0.1, 1.0]
train_scores, val_scores = validation_curve(model, X, y, param_name="C", param_range=param_range)
```

### 性能基准测试
```python
# 时间性能测试
import time
start_time = time.time()
result = model.predict(X_test)
end_time = time.time()
print(f"Inference time: {end_time - start_time:.4f} seconds")

# 内存使用监控
import tracemalloc
tracemalloc.start()
# 模型推理代码
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
```

---

## 最佳实践

### 代码组织规范
```python
# 项目结构示例
project/
├── src/
│   ├── data/
│   ├── models/
│   ├── utils/
│   └── __init__.py
├── configs/
├── notebooks/
├── tests/
├── requirements.txt
└── README.md

# 配置管理
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

### 版本控制
```bash
# Git LFS大文件管理
git lfs install
git lfs track "*.pth"
git add .gitattributes

# DVC数据版本控制
dvc init
dvc add data/train.csv
dvc push
```

### CI/CD流水线
```yaml
# GitHub Actions示例
name: ML Pipeline
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/
```

### 安全和合规
```bash
# 模型安全检查
pip install modelscan  # 模型文件安全扫描

# 数据隐私保护
pip install opacus  # 差分隐私训练

# 模型公平性评估
pip install aif360  # AI公平性工具包
```

---