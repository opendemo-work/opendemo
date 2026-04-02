# Capacity Planning

容量规划与预测方法演示。

## 容量规划模型

```
规划层次:
┌─────────────────────────────────────────────────────────┐
│  长期规划(1-3年)                                         │
│  - 业务增长预测                                          │
│  - 基础设施投资                                          │
├─────────────────────────────────────────────────────────┤
│  中期规划(3-12月)                                        │
│  - 季节性扩容                                            │
│  - 新服务上线准备                                        │
├─────────────────────────────────────────────────────────┤
│  短期规划(1-4周)                                         │
│  - 促销活动期间                                          │
│  - 临时扩容                                              │
└─────────────────────────────────────────────────────────┘
```

## 预测方法

### 趋势分析
```python
import pandas as pd
from prophet import Prophet

# 容量预测模型
df = pd.read_csv('resource_usage.csv')
df.columns = ['ds', 'y']

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(df)

# 预测90天
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

# 建议容量 = 预测值 × 安全系数(1.3)
capacity_recommendation = forecast['yhat'].iloc[-1] * 1.3
```

### 利用率红线
```yaml
capacity_thresholds:
  cpu:
    warning: 60%
    critical: 80%
    scaling_trigger: 70%
  
  memory:
    warning: 70%
    critical: 85%
    scaling_trigger: 80%
  
  disk:
    warning: 75%
    critical: 90%
    scaling_trigger: 85%
    prediction_days: 30  # 提前30天预警
```

## 自动扩缩容

```yaml
# HPA配置
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

## 学习要点

1. 容量预测模型
2. 季节性波动处理
3. 自动扩缩容策略
4. 成本与性能平衡
