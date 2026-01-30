# 模型微调与优化

## 1. 案例概述

本案例提供从入门到生产环境的完整大模型微调与优化实战指南，系统性地涵盖参数高效微调(PEFT)、模型量化、知识蒸馏、行业应用等全维度技术，帮助在有限资源下实现高效的模型定制化和生产部署。

### 1.1 案例体系结构

```mermaid
tree
    A[模型微调与优化]
    ├── B[参数高效微调技术]
    │   ├── B1[LoRA低秩适配]
    │   ├── B2[QLoRA量化微调]
    │   ├── B3[Adapter适配器]
    │   ├── B4[Prefix Tuning前缀调优]
    │   └── B5[Prompt Tuning提示调优]
    ├── C[模型量化技术]
    │   ├── C1[训练后量化(PTQ)]
    │   ├── C2[量化感知训练(QAT)]
    │   └── C3[GPTQ量化]
    ├── D[知识蒸馏技术]
    │   ├── D1[基础蒸馏]
    │   ├── D2[特征蒸馏]
    │   └── D3[关系蒸馏]
    ├── E[行业应用场景]
    │   ├── E1[医疗领域微调]
    │   ├── E2[金融领域微调]
    │   └── E3[法律领域微调]
    ├── F[生产环境部署]
    │   ├── F1[Kubernetes配置]
    │   ├── F2[监控告警]
    │   └── F3[成本优化]
    └── G[效果评估体系]
        ├── G1[性能指标]
        ├── G2[A/B测试]
        └── G3[风险管控]
```

### 1.2 学习目标

**核心技术掌握**:
- 精通主流参数高效微调技术(LoRA、QLoRA、Adapter、Prefix Tuning、Prompt Tuning)
- 深入理解模型量化原理和多种实践方法
- 掌握知识蒸馏和模型压缩的完整技术栈

**应用能力培养**:
- 具备针对不同行业的模型微调定制能力
- 掌握生产环境的部署和运维技能
- 建立完善的微调效果评估和风险管控体系

**工程实践提升**:
- 能够设计和实施端到端的微调解决方案
- 具备成本控制和性能优化的工程思维
- 掌握监控告警和故障处理的最佳实践

### 1.2 适用人群

- 需要定制化大模型的开发者
- 关注模型效率和成本的工程师
- 对模型压缩技术感兴趣的研究人员

## 2. 参数高效微调(PEFT)技术

### 2.1 LoRA (Low-Rank Adaptation)

```python
# LoRA实现示例
import torch
import torch.nn as nn
from torch.nn.parameter import Parameter

class LoRALayer(nn.Module):
    def __init__(self, in_features, out_features, rank=8, alpha=16):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        
        # 原始权重矩阵的低秩分解
        self.lora_A = Parameter(torch.zeros(in_features, rank))
        self.lora_B = Parameter(torch.zeros(rank, out_features))
        
        # 缩放因子
        self.scaling = alpha / rank
        
        # 初始化
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        nn.init.zeros_(self.lora_B)
    
    def forward(self, x):
        # 原始前向传播 + LoRA适配
        return x + (x @ self.lora_A @ self.lora_B) * self.scaling

class LoRALinear(nn.Linear):
    def __init__(self, in_features, out_features, rank=8, alpha=16, **kwargs):
        super().__init__(in_features, out_features, **kwargs)
        self.lora_layer = LoRALayer(in_features, out_features, rank, alpha)
    
    def forward(self, x):
        # 冻结原始权重，只训练LoRA参数
        with torch.no_grad():
            original_output = super().forward(x)
        lora_output = self.lora_layer(x)
        return original_output + lora_output

# 在Transformer中应用LoRA
class LoraTransformer(nn.Module):
    def __init__(self, base_model, lora_config):
        super().__init__()
        self.base_model = base_model
        self.lora_config = lora_config
        
        # 替换指定层为LoRA层
        self._replace_with_lora()
    
    def _replace_with_lora(self):
        """将模型中的线性层替换为LoRA层"""
        for name, module in self.base_model.named_modules():
            if isinstance(module, nn.Linear) and self._should_apply_lora(name):
                # 创建LoRA包装器
                lora_linear = LoRALinear(
                    module.in_features,
                    module.out_features,
                    rank=self.lora_config.rank,
                    alpha=self.lora_config.alpha,
                    bias=module.bias is not None
                )
                
                # 复制原始权重
                lora_linear.weight.data = module.weight.data.clone()
                if module.bias is not None:
                    lora_linear.bias.data = module.bias.data.clone()
                
                # 替换模块
                parent_module = self._get_parent_module(name)
                attr_name = name.split('.')[-1]
                setattr(parent_module, attr_name, lora_linear)
    
    def _should_apply_lora(self, name):
        """判断是否应该在该层应用LoRA"""
        # 通常在注意力机制和前馈网络中应用
        return any(pattern in name for pattern in [
            'q_proj', 'k_proj', 'v_proj', 'o_proj',  # 注意力投影层
            'gate_proj', 'up_proj', 'down_proj'      # MLP层
        ])
    
    def _get_parent_module(self, name):
        """获取父模块"""
        modules = name.split('.')
        parent = self.base_model
        for module_name in modules[:-1]:
            parent = getattr(parent, module_name)
        return parent

# 使用示例
def train_lora_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    # 加载预训练模型
    model_name = "meta-llama/Llama-2-7b-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    base_model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # LoRA配置
    class LoraConfig:
        def __init__(self):
            self.rank = 8
            self.alpha = 16
            self.dropout = 0.1
    
    lora_config = LoraConfig()
    
    # 创建LoRA模型
    lora_model = LoraTransformer(base_model, lora_config)
    
    # 冻结原始模型参数
    for param in lora_model.base_model.parameters():
        param.requires_grad = False
    
    # 只训练LoRA参数
    trainable_params = sum(p.numel() for p in lora_model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in lora_model.parameters())
    
    print(f"可训练参数: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
    print(f"总参数: {total_params:,}")
    
    return lora_model, tokenizer
```

### 2.2 QLoRA (Quantized LoRA)

```python
# QLoRA实现 - 结合4-bit量化和LoRA
import bitsandbytes as bnb
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def create_qlora_model(model_name, quantization_config):
    """创建QLoRA模型"""
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig
    
    # 4-bit量化配置
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    # 加载量化模型
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    # 准备模型进行k-bit训练
    model = prepare_model_for_kbit_training(model)
    
    # LoRA配置
    lora_config = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # 应用LoRA
    model = get_peft_model(model, lora_config)
    
    return model

# 训练脚本
def train_qlora():
    model = create_qlora_model("meta-llama/Llama-2-7b-hf", {})
    
    # 训练配置
    training_args = TrainingArguments(
        output_dir="./qlora-results",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        max_steps=1000,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=20,
        save_steps=200,
        optim="paged_adamw_8bit"  # 8-bit优化器
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer
    )
    
    # 开始训练
    trainer.train()
```

### 2.3 Adapter微调

```python
# Adapter实现
class AdapterLayer(nn.Module):
    def __init__(self, hidden_size, bottleneck_size=64, dropout=0.1):
        super().__init__()
        self.hidden_size = hidden_size
        self.bottleneck_size = bottleneck_size
        
        # Adapter结构：Down projection -> Non-linearity -> Up projection
        self.down_proj = nn.Linear(hidden_size, bottleneck_size)
        self.activation = nn.GELU()
        self.up_proj = nn.Linear(bottleneck_size, hidden_size)
        self.dropout = nn.Dropout(dropout)
        
        # LayerNorm
        self.adapter_norm = nn.LayerNorm(hidden_size)
        
        # 初始化
        nn.init.normal_(self.down_proj.weight, std=1e-3)
        nn.init.zeros_(self.down_proj.bias)
        nn.init.normal_(self.up_proj.weight, std=1e-3)
        nn.init.zeros_(self.up_proj.bias)
    
    def forward(self, x):
        # 残差连接
        residual = x
        x = self.adapter_norm(x)
        x = self.down_proj(x)
        x = self.activation(x)
        x = self.up_proj(x)
        x = self.dropout(x)
        return residual + x

class AdapterTransformer(nn.Module):
    def __init__(self, base_model, adapter_config):
        super().__init__()
        self.base_model = base_model
        self.adapter_config = adapter_config
        
        # 在指定位置插入Adapter
        self._insert_adapters()
    
    def _insert_adapters(self):
        """在Transformer层中插入Adapter"""
        for name, module in self.base_model.named_modules():
            if self._should_insert_adapter(name, module):
                # 创建Adapter包装器
                adapter_wrapper = self._create_adapter_wrapper(module)
                
                # 替换模块
                parent_module = self._get_parent_module(name)
                attr_name = name.split('.')[-1]
                setattr(parent_module, attr_name, adapter_wrapper)
    
    def _should_insert_adapter(self, name, module):
        """判断是否应该插入Adapter"""
        # 在注意力输出和FFN输出后插入
        return isinstance(module, nn.Linear) and any(pattern in name for pattern in [
            'attention.output.dense',  # 注意力输出
            'output.dense'             # FFN输出
        ])

# 使用HuggingFace PEFT库的Adapter
from peft import AdaLoraConfig, get_peft_model

def create_adapter_model(model_name):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # AdaLora配置
    adalora_config = AdaLoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, adalora_config)
    return model
```

### 2.4 Prefix Tuning (前缀调优)

```python
# Prefix Tuning实现
class PrefixTuningLayer(nn.Module):
    def __init__(self, config, num_virtual_tokens=20):
        super().__init__()
        self.num_virtual_tokens = num_virtual_tokens
        self.hidden_size = config.hidden_size
        
        # 虚拟token的前缀参数
        self.prefix_embeddings = nn.Embedding(num_virtual_tokens, self.hidden_size)
        
        # MLP网络生成key和value前缀
        self.prefix_mlp = nn.Sequential(
            nn.Linear(self.hidden_size, self.hidden_size),
            nn.Tanh(),
            nn.Linear(self.hidden_size, 2 * config.num_hidden_layers * self.hidden_size)
        )
        
        # 初始化
        nn.init.normal_(self.prefix_embeddings.weight, std=0.02)
    
    def forward(self, batch_size):
        # 生成虚拟token
        virtual_tokens = self.prefix_embeddings.weight.unsqueeze(0).expand(batch_size, -1, -1)
        
        # 通过MLP生成前缀
        prefix_projections = self.prefix_mlp(virtual_tokens)
        
        # 重塑为key和value格式
        prefix_projections = prefix_projections.view(
            batch_size, self.num_virtual_tokens, 
            2, config.num_hidden_layers, self.hidden_size
        )
        
        past_key_values = tuple(
            (prefix_projections[:, :, 0, layer_idx], prefix_projections[:, :, 1, layer_idx])
            for layer_idx in range(config.num_hidden_layers)
        )
        
        return past_key_values

class PrefixTuningModel(nn.Module):
    def __init__(self, base_model, num_virtual_tokens=20):
        super().__init__()
        self.base_model = base_model
        self.config = base_model.config
        
        # 冻结原始模型
        for param in self.base_model.parameters():
            param.requires_grad = False
        
        # 添加前缀调优层
        self.prefix_layer = PrefixTuningLayer(self.config, num_virtual_tokens)
        
        # 只训练前缀参数
        self.trainable_params = sum(p.numel() for p in self.prefix_layer.parameters())
        self.total_params = sum(p.numel() for p in self.parameters())
        
        print(f"前缀调优参数: {self.trainable_params:,} ({self.trainable_params/self.total_params*100:.2f}%)")
    
    def forward(self, input_ids, attention_mask=None, labels=None):
        batch_size = input_ids.shape[0]
        
        # 生成前缀
        past_key_values = self.prefix_layer(batch_size)
        
        # 前向传播
        outputs = self.base_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            past_key_values=past_key_values,
            labels=labels
        )
        
        return outputs
```

### 2.5 Prompt Tuning (提示调优)

```python
# Prompt Tuning实现
class PromptTuningLayer(nn.Module):
    def __init__(self, config, num_virtual_tokens=50):
        super().__init__()
        self.num_virtual_tokens = num_virtual_tokens
        self.hidden_size = config.hidden_size
        
        # 可学习的提示token嵌入
        self.prompt_embeddings = nn.Embedding(num_virtual_tokens, self.hidden_size)
        
        # 初始化为接近词汇表平均值
        self._init_prompt_embeddings(config)
    
    def _init_prompt_embeddings(self, config):
        """初始化提示嵌入"""
        # 从词汇表中采样初始化
        vocab_size = config.vocab_size
        sample_indices = torch.randint(0, vocab_size, (self.num_virtual_tokens,))
        
        # 这里需要访问模型的词嵌入层来获取初始值
        # 在实际使用中需要传入embedding层
        pass
    
    def forward(self, input_embeds):
        batch_size = input_embeds.shape[0]
        
        # 生成提示嵌入
        prompt_embeds = self.prompt_embeddings.weight.unsqueeze(0).expand(batch_size, -1, -1)
        
        # 拼接提示和输入
        combined_embeds = torch.cat([prompt_embeds, input_embeds], dim=1)
        
        return combined_embeds

class PromptTuningModel(nn.Module):
    def __init__(self, base_model, num_virtual_tokens=50):
        super().__init__()
        self.base_model = base_model
        self.config = base_model.config
        
        # 冻结原始模型
        for param in self.base_model.parameters():
            param.requires_grad = False
        
        # 添加提示调优层
        self.prompt_layer = PromptTuningLayer(self.config, num_virtual_tokens)
        
        # 只训练提示参数
        self.trainable_params = sum(p.numel() for p in self.prompt_layer.parameters())
        self.total_params = sum(p.numel() for p in self.parameters())
        
        print(f"提示调优参数: {self.trainable_params:,} ({self.trainable_params/self.total_params*100:.2f}%)")
    
    def forward(self, input_ids, attention_mask=None, labels=None):
        # 获取输入嵌入
        input_embeds = self.base_model.get_input_embeddings()(input_ids)
        
        # 应用提示调优
        combined_embeds = self.prompt_layer(input_embeds)
        
        # 构造新的attention mask
        batch_size = input_ids.shape[0]
        prompt_attention_mask = torch.ones(
            batch_size, self.prompt_layer.num_virtual_tokens, 
            device=input_ids.device
        )
        
        if attention_mask is not None:
            combined_attention_mask = torch.cat([prompt_attention_mask, attention_mask], dim=1)
        else:
            combined_attention_mask = None
        
        # 前向传播
        outputs = self.base_model(
            inputs_embeds=combined_embeds,
            attention_mask=combined_attention_mask,
            labels=labels
        )
        
        return outputs

# 使用HuggingFace PEFT库的Prompt Tuning
from peft import PromptTuningConfig, get_peft_model

def create_prompt_tuning_model(model_name, num_virtual_tokens=50):
    from transformers import AutoModelForCausalLM
    
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Prompt Tuning配置
    prompt_config = PromptTuningConfig(
        task_type="CAUSAL_LM",
        num_virtual_tokens=num_virtual_tokens,
        prompt_tuning_init="TEXT",
        prompt_tuning_init_text="Classify if the sentiment of this review is positive or negative: ",
        tokenizer_name_or_path=model_name
    )
    
    model = get_peft_model(model, prompt_config)
    return model
```

## 3. 模型量化技术

### 3.1 Post-Training Quantization (PTQ)

```python
# 训练后量化示例
import torch.quantization as quant

class QuantizableModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.AdaptiveAvgPool2d((1, 1))
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(128, 10)
    
    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = self.flatten(x)
        x = self.fc(x)
        return x

def post_training_quantization():
    # 创建模型
    model = QuantizableModel()
    
    # 设置量化配置
    model.qconfig = quant.get_default_qconfig('fbgemm')
    
    # 准备量化
    quant.prepare(model, inplace=True)
    
    # 校准 - 使用校准数据集
    calibration_data = get_calibration_dataset()
    model.eval()
    with torch.no_grad():
        for data, _ in calibration_data:
            model(data)
    
    # 转换为量化模型
    quant.convert(model, inplace=True)
    
    return model

# 使用Intel Neural Compressor
from neural_compressor import QuantizationAwareTrainingConfig
from neural_compressor.training import prepare_compression

def intel_quantization_training():
    model = create_model()
    train_dataloader = get_train_dataloader()
    
    # 量化感知训练配置
    conf = QuantizationAwareTrainingConfig(
        approach="quant_aware_training",
        recipes={
            "smooth_quant": True,
            "smooth_quant_args": {
                "alpha": 0.5
            }
        }
    )
    
    # 准备压缩
    compression_manager = prepare_compression(model, conf)
    compression_manager.callbacks.on_train_begin()
    
    # 训练循环
    model = compression_manager.model
    for epoch in range(num_epochs):
        for batch in train_dataloader:
            # 正常训练步骤
            loss = train_step(model, batch)
            compression_manager.callbacks.on_step_end()
    
    compression_manager.callbacks.on_train_end()
    return model
```

### 3.2 Quantization-Aware Training (QAT)

```python
# 量化感知训练
def quantization_aware_training():
    from torch.quantization import fuse_modules, prepare_qat, convert
    
    # 创建模型并融合模块
    model = create_model()
    model.eval()
    
    # 融合可以融合的模块
    model = fuse_modules(model, [['conv1', 'relu1'], ['conv2', 'relu2']])
    
    # 设置QAT配置
    model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
    
    # 准备QAT
    model.train()
    prepare_qat(model, inplace=True)
    
    # QAT训练
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(qat_epochs):
        for data, target in train_loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
    
    # 转换为量化模型
    model.eval()
    convert(model, inplace=True)
    
    return model
```

### 3.3 GPTQ量化

```python
# GPTQ量化实现
import numpy as np
from tqdm import tqdm

class GPTQQuantizer:
    def __init__(self, bits=4, group_size=128):
        self.bits = bits
        self.group_size = group_size
        self.max_q = 2 ** bits - 1
        
    def quantize_weight(self, weight):
        """GPTQ量化单个权重矩阵"""
        # 按组处理权重
        out_features, in_features = weight.shape
        new_weight = weight.clone()
        
        # 计算组数
        num_groups = (in_features + self.group_size - 1) // self.group_size
        
        scales = []
        zeros = []
        
        for i in range(num_groups):
            start_idx = i * self.group_size
            end_idx = min((i + 1) * self.group_size, in_features)
            
            # 提取当前组
            group_weight = weight[:, start_idx:end_idx]
            
            # 计算每组的scale和zero point
            w_max = group_weight.max(dim=1, keepdim=True)[0]
            w_min = group_weight.min(dim=1, keepdim=True)[0]
            
            scale = (w_max - w_min) / self.max_q
            zero_point = (-w_min / scale).round()
            
            # 量化
            quant_weight = ((group_weight / scale + zero_point).round().clamp(0, self.max_q))
            
            # 反量化验证
            dequant_weight = (quant_weight - zero_point) * scale
            
            # 更新权重
            new_weight[:, start_idx:end_idx] = dequant_weight
            
            scales.append(scale)
            zeros.append(zero_point)
        
        return new_weight, scales, zeros

def apply_gptq_quantization(model, dataloader):
    """应用GPTQ量化到整个模型"""
    quantizer = GPTQQuantizer(bits=4, group_size=128)
    
    # 收集Hessian信息
    hessian_dict = {}
    
    # Hook函数收集二阶导数信息
    def hessian_hook(module, grad_input, grad_output):
        if isinstance(module, nn.Linear):
            weight = module.weight.data
            hessian = grad_output[0].pow(2).mean(dim=0)
            hessian_dict[id(module)] = hessian
    
    # 注册hooks
    hooks = []
    for module in model.modules():
        if isinstance(module, nn.Linear):
            hook = module.register_backward_hook(hessian_hook)
            hooks.append(hook)
    
    # 前向传播收集Hessian
    model.eval()
    for batch in tqdm(dataloader, desc="Collecting Hessian"):
        try:
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
        except:
            pass
    
    # 移除hooks
    for hook in hooks:
        hook.remove()
    
    # 应用量化
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear) and id(module) in hessian_dict:
            # 使用Hessian信息进行更精确的量化
            hessian = hessian_dict[id(module)]
            original_weight = module.weight.data
            
            # GPTQ量化
            quantized_weight, scales, zeros = quantizer.quantize_weight(original_weight)
            
            # 更新模块权重
            module.weight.data = quantized_weight
            
            # 保存量化参数
            module.scales = scales
            module.zeros = zeros

# 使用AutoGPTQ库
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

def autogptq_quantization(model_name, quantize_config):
    # 量化配置
    quantize_config = BaseQuantizeConfig(
        bits=4,
        group_size=128,
        damp_percent=0.01,
        desc_act=False,
        static_groups=False,
        sym=True,
        true_sequential=True
    )
    
    # 加载模型
    model = AutoGPTQForCausalLM.from_pretrained(model_name, quantize_config)
    
    # 准备数据集
    examples = get_quantization_examples()
    
    # 量化模型
    model.quantize(examples)
    
    # 保存量化模型
    model.save_quantized("./gptq-quantized-model")
    
    return model
```

## 4. 知识蒸馏技术

### 4.1 基础知识蒸馏

```python
# 知识蒸馏实现
class DistillationTrainer:
    def __init__(self, student_model, teacher_model, temperature=4.0, alpha=0.7):
        self.student = student_model
        self.teacher = teacher_model
        self.temperature = temperature
        self.alpha = alpha
        
        # 冻结教师模型
        for param in self.teacher.parameters():
            param.requires_grad = False
    
    def distillation_loss(self, student_logits, teacher_logits, true_labels):
        """计算蒸馏损失"""
        # 软标签损失 (KL散度)
        soft_student = torch.softmax(student_logits / self.temperature, dim=-1)
        soft_teacher = torch.softmax(teacher_logits / self.temperature, dim=-1)
        
        kl_loss = torch.nn.KLDivLoss(reduction='batchmean')(
            torch.log(soft_student), soft_teacher
        ) * (self.temperature ** 2)
        
        # 硬标签损失
        hard_loss = torch.nn.CrossEntropyLoss()(student_logits, true_labels)
        
        # 组合损失
        total_loss = self.alpha * kl_loss + (1 - self.alpha) * hard_loss
        return total_loss

def train_distilled_model():
    # 创建教师和学生模型
    teacher = AutoModelForSequenceClassification.from_pretrained("bert-large-uncased")
    student = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
    
    # 创建蒸馏训练器
    trainer = DistillationTrainer(student, teacher, temperature=4.0, alpha=0.7)
    
    # 训练循环
    optimizer = torch.optim.Adam(student.parameters(), lr=2e-5)
    
    for epoch in range(num_epochs):
        for batch in train_dataloader:
            # 教师模型预测
            with torch.no_grad():
                teacher_outputs = teacher(**batch)
                teacher_logits = teacher_outputs.logits
            
            # 学生模型预测
            student_outputs = student(**batch)
            student_logits = student_outputs.logits
            
            # 计算蒸馏损失
            loss = trainer.distillation_loss(
                student_logits, teacher_logits, batch["labels"]
            )
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

### 4.2 特征蒸馏

```python
# 特征层蒸馏
class FeatureDistillationTrainer:
    def __init__(self, student_model, teacher_model, feature_layers):
        self.student = student_model
        self.teacher = teacher_model
        self.feature_layers = feature_layers
        
        # 注册hook提取特征
        self.teacher_features = {}
        self.student_features = {}
        
        self._register_hooks()
    
    def _register_hooks(self):
        """注册特征提取hook"""
        # 教师模型hook
        for name, module in self.teacher.named_modules():
            if name in self.feature_layers:
                module.register_forward_hook(
                    lambda module, input, output, name=name: 
                    self.teacher_features.update({name: output})
                )
        
        # 学生模型hook
        for name, module in self.student.named_modules():
            if name in self.feature_layers:
                module.register_forward_hook(
                    lambda module, input, output, name=name: 
                    self.student_features.update({name: output})
                )
    
    def feature_loss(self):
        """计算特征蒸馏损失"""
        loss = 0
        for layer_name in self.feature_layers:
            if layer_name in self.teacher_features and layer_name in self.student_features:
                teacher_feat = self.teacher_features[layer_name]
                student_feat = self.student_features[layer_name]
                
                # 特征匹配损失
                feat_loss = torch.nn.MSELoss()(
                    student_feat, teacher_feat.detach()
                )
                loss += feat_loss
        
        return loss

# 使用示例
def train_with_feature_distillation():
    teacher = create_teacher_model()
    student = create_student_model()
    
    # 选择要蒸馏的特征层
    feature_layers = ["encoder.layer.6", "encoder.layer.10"]
    
    trainer = FeatureDistillationTrainer(student, teacher, feature_layers)
    
    # 训练
    for batch in train_dataloader:
        # 前向传播收集特征
        _ = teacher(**batch)
        _ = student(**batch)
        
        # 计算特征损失
        feat_loss = trainer.feature_loss()
        
        # 结合其他损失进行训练
        total_loss = classification_loss + 0.5 * feat_loss
```

## 5. 模型压缩与优化

### 5.1 权重剪枝

```python
# 结构化剪枝
class PruningManager:
    def __init__(self, model, pruning_ratio=0.5):
        self.model = model
        self.pruning_ratio = pruning_ratio
        self.masks = {}
        
    def compute_importance(self, dataloader):
        """计算权重重要性"""
        importance_scores = {}
        
        # 使用泰勒展开近似计算重要性
        for name, param in self.model.named_parameters():
            if 'weight' in name:
                # 基于梯度和权重计算重要性
                importance = torch.abs(param * param.grad) if param.grad is not None else torch.zeros_like(param)
                importance_scores[name] = importance
        
        return importance_scores
    
    def create_pruning_mask(self, importance_scores):
        """创建剪枝掩码"""
        for name, scores in importance_scores.items():
            # 计算阈值
            threshold = torch.quantile(scores.flatten(), self.pruning_ratio)
            
            # 创建掩码
            mask = (scores > threshold).float()
            self.masks[name] = mask
    
    def apply_pruning(self):
        """应用剪枝"""
        for name, param in self.model.named_parameters():
            if name in self.masks:
                param.data *= self.masks[name]

def iterative_pruning_training():
    model = create_model()
    pruning_manager = PruningManager(model, pruning_ratio=0.3)
    
    for pruning_step in range(5):  # 迭代剪枝5次
        # 正常训练
        train_model(model, train_dataloader)
        
        # 计算重要性并剪枝
        importance_scores = pruning_manager.compute_importance(train_dataloader)
        pruning_manager.create_pruning_mask(importance_scores)
        pruning_manager.apply_pruning()
        
        # 微调
        fine_tune_model(model, train_dataloader, epochs=2)
```

### 5.2 知识图谱蒸馏

```python
# 知识图谱蒸馏
class KnowledgeGraphDistiller:
    def __init__(self, teacher_model, student_model):
        self.teacher = teacher_model
        self.student = student_model
    
    def extract_relations(self, texts):
        """从文本中提取关系三元组"""
        # 使用预训练的关系抽取模型
        relations = []
        for text in texts:
            # 这里应该是实际的关系抽取逻辑
            extracted_relations = self.extract_triples(text)
            relations.extend(extracted_relations)
        return relations
    
    def relation_preservation_loss(self, student_relations, teacher_relations):
        """关系保持损失"""
        # 计算关系相似度损失
        loss = 0
        for s_rel, t_rel in zip(student_relations, teacher_relations):
            # 关系嵌入相似度
            rel_sim = torch.cosine_similarity(s_rel, t_rel, dim=-1)
            loss += (1 - rel_sim).mean()
        return loss

# 使用Transformers.js进行轻量化部署
def export_for_edge_deployment(model):
    """导出模型用于边缘设备部署"""
    
    # 1. 模型量化
    quantized_model = torch.quantization.quantize_dynamic(
        model, {nn.Linear}, dtype=torch.qint8
    )
    
    # 2. ONNX导出
    dummy_input = torch.randn(1, 512)  # 示例输入
    torch.onnx.export(
        quantized_model,
        dummy_input,
        "model_quantized.onnx",
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size', 1: 'sequence'},
            'output': {0: 'batch_size', 1: 'sequence'}
        }
    )
    
    # 3. TensorFlow Lite转换
    import tensorflow as tf
    
    # 转换ONNX到TensorFlow
    converter = tf.lite.TFLiteConverter.from_saved_model("tf_model")
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    
    tflite_model = converter.convert()
    
    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)
```

## 6. 微调效果评估

### 6.1 评估指标体系

```python
# 微调效果综合评估
class ModelEvaluator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def evaluate_task_performance(self, test_dataset):
        """任务性能评估"""
        self.model.eval()
        predictions = []
        true_labels = []
        
        with torch.no_grad():
            for batch in test_dataset:
                outputs = self.model(**batch)
                preds = torch.argmax(outputs.logits, dim=-1)
                predictions.extend(preds.cpu().tolist())
                true_labels.extend(batch["labels"].cpu().tolist())
        
        # 计算指标
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, average='macro')
        recall = recall_score(true_labels, predictions, average='macro')
        f1 = f1_score(true_labels, predictions, average='macro')
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def evaluate_efficiency(self):
        """效率评估"""
        # 模型大小
        model_size = sum(p.numel() for p in self.model.parameters()) * 4 / (1024**2)  # MB
        
        # 推理时间
        dummy_input = self.tokenizer("test text", return_tensors="pt")
        start_time = time.time()
        with torch.no_grad():
            _ = self.model(**dummy_input)
        inference_time = (time.time() - start_time) * 1000  # ms
        
        # 内存使用
        torch.cuda.reset_peak_memory_stats()
        with torch.no_grad():
            _ = self.model(**dummy_input)
        memory_usage = torch.cuda.max_memory_allocated() / (1024**2)  # MB
        
        return {
            'model_size_mb': model_size,
            'inference_time_ms': inference_time,
            'memory_usage_mb': memory_usage
        }
    
    def evaluate_robustness(self, perturbation_tests):
        """鲁棒性评估"""
        self.model.eval()
        robustness_scores = []
        
        for perturbation_func in perturbation_tests:
            original_preds = []
            perturbed_preds = []
            
            for text in test_texts:
                # 原始预测
                inputs = self.tokenizer(text, return_tensors="pt")
                with torch.no_grad():
                    orig_pred = self.model(**inputs).logits
                original_preds.append(orig_pred)
                
                # 扰动后预测
                perturbed_text = perturbation_func(text)
                inputs = self.tokenizer(perturbed_text, return_tensors="pt")
                with torch.no_grad():
                    pert_pred = self.model(**inputs).logits
                perturbed_preds.append(pert_pred)
            
            # 计算预测一致性
            consistency = self._calculate_consistency(original_preds, perturbed_preds)
            robustness_scores.append(consistency)
        
        return {
            'average_robustness': np.mean(robustness_scores),
            'robustness_by_type': dict(zip(
                [func.__name__ for func in perturbation_tests], 
                robustness_scores
            ))
        }
    
    def _calculate_consistency(self, orig_preds, pert_preds):
        """计算预测一致性"""
        consistent = 0
        for orig, pert in zip(orig_preds, pert_preds):
            if torch.argmax(orig) == torch.argmax(pert):
                consistent += 1
        return consistent / len(orig_preds)

# 使用示例
def comprehensive_evaluation():
    evaluator = ModelEvaluator(model, tokenizer)
    
    # 任务性能评估
    task_metrics = evaluator.evaluate_task_performance(test_dataloader)
    
    # 效率评估
    efficiency_metrics = evaluator.evaluate_efficiency()
    
    # 鲁棒性评估
    perturbations = [
        lambda x: x.lower(),  # 小写扰动
        lambda x: ''.join([c if random.random() > 0.1 else '' for c in x]),  # 字符删除
        lambda x: ' '.join(x.split()[::-1])  # 词序颠倒
    ]
    robustness_metrics = evaluator.evaluate_robustness(perturbations)
    
    # 综合报告
    report = {
        'task_performance': task_metrics,
        'efficiency': efficiency_metrics,
        'robustness': robustness_metrics,
        'overall_score': self._calculate_overall_score(
            task_metrics, efficiency_metrics, robustness_metrics
        )
    }
    
    return report
```

### 6.2 A/B测试框架

```python
# A/B测试实现
class ABTester:
    def __init__(self, model_a, model_b, traffic_split=0.5):
        self.models = {'A': model_a, 'B': model_b}
        self.traffic_split = traffic_split
        self.results = {'A': [], 'B': []}
    
    def route_request(self, request):
        """路由请求到不同模型"""
        if random.random() < self.traffic_split:
            return 'A', self.models['A']
        else:
            return 'B', self.models['B']
    
    def collect_metrics(self, model_id, response_time, accuracy, user_feedback):
        """收集指标"""
        self.results[model_id].append({
            'response_time': response_time,
            'accuracy': accuracy,
            'feedback': user_feedback,
            'timestamp': time.time()
        })
    
    def analyze_results(self):
        """分析A/B测试结果"""
        analysis = {}
        for model_id in ['A', 'B']:
            results = self.results[model_id]
            if results:
                analysis[model_id] = {
                    'avg_response_time': np.mean([r['response_time'] for r in results]),
                    'accuracy': np.mean([r['accuracy'] for r in results]),
                    'sample_size': len(results)
                }
        
        # 统计显著性检验
        if len(self.results['A']) > 0 and len(self.results['B']) > 0:
            a_times = [r['response_time'] for r in self.results['A']]
            b_times = [r['response_time'] for r in self.results['B']]
            
            # t检验
            t_stat, p_value = scipy.stats.ttest_ind(a_times, b_times)
            analysis['statistical_test'] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        return analysis

# 在线评估系统
class OnlineEvaluator:
    def __init__(self, reference_model):
        self.reference_model = reference_model
        self.metrics_buffer = []
    
    def evaluate_online(self, input_text, predicted_output, true_output=None):
        """在线评估单个预测"""
        metrics = {}
        
        # 如果有真实标签，计算准确性
        if true_output is not None:
            metrics['accuracy'] = self._calculate_accuracy(predicted_output, true_output)
        
        # 计算与参考模型的一致性
        ref_prediction = self._get_reference_prediction(input_text)
        metrics['consistency'] = self._calculate_consistency(predicted_output, ref_prediction)
        
        # 计算响应时间
        metrics['response_time'] = self._measure_response_time(input_text)
        
        self.metrics_buffer.append(metrics)
        
        # 定期清理缓冲区
        if len(self.metrics_buffer) > 1000:
            self.metrics_buffer = self.metrics_buffer[-500:]
        
        return metrics
    
    def get_summary_statistics(self):
        """获取汇总统计"""
        if not self.metrics_buffer:
            return {}
        
        df = pd.DataFrame(self.metrics_buffer)
        return {
            'accuracy_mean': df['accuracy'].mean() if 'accuracy' in df.columns else None,
            'consistency_mean': df['consistency'].mean(),
            'response_time_mean': df['response_time'].mean(),
            'total_samples': len(df)
        }
```

## 7. 最佳实践总结

### 7.1 微调策略选择指南

| 场景 | 推荐方法 | 理由 |
|------|----------|------|
| 资源极度有限 | LoRA (r=8-16) | 参数效率最高 |
| 中等资源 | QLoRA | 平衡效果和效率 |
| 需要最大精度 | Full fine-tuning | 效果最好但资源消耗大 |
| 快速原型验证 | Adapter | 插拔方便，适合实验 |

### 7.2 量化策略对比

| 量化方法 | 精度损失 | 速度提升 | 内存节省 | 适用场景 |
|----------|----------|----------|----------|----------|
| 8-bit动态量化 | 低(1-2%) | 2-3x | 2x | 推理部署 |
| 4-bit GPTQ | 中(3-5%) | 3-4x | 4x | 大模型部署 |
| 2-bit量化 | 高(8-15%) | 5-6x | 8x | 边缘设备 |

### 7.3 监控要点

✅ **性能监控**
- 训练损失收敛曲线
- 验证集性能指标
- 训练速度和吞吐量

✅ **资源监控**
- GPU内存使用率
- CPU利用率
- 网络带宽使用

✅ **质量监控**
- 梯度范数和更新幅度
- 参数统计信息
- 预测分布变化

## 8. 总结

本案例全面介绍了大模型微调与优化的核心技术，包括：

✅ 参数高效微调(LoRA、QLoRA、Adapter)  
✅ 模型量化技术(PTQ、QAT、GPTQ)  
✅ 知识蒸馏和模型压缩  
✅ 微调效果评估体系  
✅ 生产环境最佳实践  

通过本案例的学习，您应该能够：
- 根据具体需求选择合适的微调策略
- 实施高效的模型量化和压缩
- 建立完善的微调效果评估体系
- 在资源约束下实现最优的模型性能
- 构建可监控、可维护的微调流程

下一步建议学习生产环境部署案例，了解如何将优化后的模型部署到实际生产环境中。# #   8 .   L�N�^(u:Wof 
 