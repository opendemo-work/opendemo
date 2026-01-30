# 大模型训练基础环境Docker镜像
FROM nvidia/cuda:11.8-devel-ubuntu20.04

# 设置非交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 设置Python环境
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace

# 升级pip
RUN pip3 install --upgrade pip

# 安装PyTorch和相关依赖
RUN pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# 安装机器学习相关库
RUN pip3 install \
    transformers>=4.30.0 \
    datasets>=2.12.0 \
    accelerate>=0.20.0 \
    wandb>=0.15.0 \
    numpy>=1.21.0 \
    matplotlib>=3.7.0 \
    scikit-learn>=1.2.0 \
    pandas>=1.5.0

# 安装Kubernetes相关工具
RUN pip3 install \
    kubernetes>=26.1.0 \
    kubeflow-training>=1.7.0

# 复制训练代码
COPY train-simple-example.py .
COPY requirements.txt .

# 设置默认命令
CMD ["python3", "train-simple-example.py", "--help"]