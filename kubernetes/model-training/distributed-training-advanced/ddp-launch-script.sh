#!/bin/bash
# 分布式训练启动脚本
# 支持多节点DDP训练

set -e

# 配置参数
export MASTER_ADDR=${MASTER_ADDR:-"localhost"}
export MASTER_PORT=${MASTER_PORT:-"12355"}
export WORLD_SIZE=${WORLD_SIZE:-"1"}
export NODE_RANK=${NODE_RANK:-"0"}

echo "Starting distributed training..."
echo "Master: $MASTER_ADDR:$MASTER_PORT"
echo "World Size: $WORLD_SIZE"
echo "Node Rank: $NODE_RANK"

# 获取本地GPU数量
NUM_GPUS=$(nvidia-smi --query-gpu=count --format=csv,noheader,nounits | head -1)
echo "Local GPUs: $NUM_GPUS"

# 构建训练命令
TRAINING_CMD="python3 -m torch.distributed.run \
    --nproc_per_node=$NUM_GPUS \
    --nnodes=$WORLD_SIZE \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --master_port=$MASTER_PORT \
    train_ddp.py \
    --epochs=50 \
    --batch-size=32 \
    --lr=0.001"

echo "Executing: $TRAINING_CMD"
exec $TRAINING_CMD