# Error Budget

错误预算管理策略演示。

## 错误预算概念

```
错误预算计算:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   SLO目标: 99.9%                                        │
│   错误预算: 100% - 99.9% = 0.1%                        │
│                                                         │
│   30天允许错误时间:                                     │
│   0.1% × 30天 = 43.2分钟                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 预算消耗跟踪

```
预算消耗示例:
Week 1: ████████░░░░░░░░░░░░  40% (正常发布)
Week 2: ████████████░░░░░░░░  60% (+促销活动期间)
Week 3: ██████████████░░░░░░  70% (小事故)
Week 4: █████████████████░░░  90% (⚠️ 接近警戒线)

警戒线: 75% - 预警
停发线: 100% - 暂停发布，专注可靠性
```

## 发布策略

```yaml
# 基于错误预算的发布策略
release_policy:
  budget_above_75%:
    action: warn
    message: 错误预算剩余25%，谨慎发布
  
  budget_above_90%:
    action: require_approval
    approvers: [sre-lead, product-manager]
  
  budget_exhausted:
    action: block_release
    exception_process: emergency-change-request
    focus: reliability_improvements
```

## 学习要点

1. 错误预算计算方法
2. 预算消耗跟踪
3. 发布决策策略
4. 跨团队协作机制
