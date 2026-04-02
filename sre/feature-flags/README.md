# Feature Flags

特性开关管理演示。

## 特性开关类型

```
开关分类:
┌─────────────────┬─────────────────┬─────────────────┐
│   发布开关       │   实验开关       │   运维开关       │
├─────────────────┼─────────────────┼─────────────────┤
│ • 功能灰度      │ • A/B测试       │ • 熔断开关      │
│ • 逐步上线      │ • 用户分组      │ • 降级开关      │
│ • 回滚控制      │ • 流量分配      │ • 限流开关      │
└─────────────────┴─────────────────┴─────────────────┘
```

## LaunchDarkly示例

```python
from ldclient import LDClient

ld_client = LDClient(sdk_key="sdk-key")

# 检查特性开关
if ld_client.variation("new-checkout-flow", user, False):
    show_new_checkout()
else:
    show_old_checkout()

# 动态配置
timeout = ld_client.variation("api-timeout", user, 30)
```

## 学习要点

1. 开关设计模式
2. 灰度发布策略
3. 实验数据分析
4. 技术债管理
