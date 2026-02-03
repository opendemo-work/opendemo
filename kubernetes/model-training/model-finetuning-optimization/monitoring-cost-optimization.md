# 监控指标与成本优化策略

## 1. 微调监控体系

### 1.1 核心监控指标

```python
# 微调监控指标定义
class FineTuningMonitor:
    def __init__(self):
        self.metrics = {
            'training_metrics': self._define_training_metrics(),
            'resource_metrics': self._define_resource_metrics(),
            'quality_metrics': self._define_quality_metrics(),
            'cost_metrics': self._define_cost_metrics()
        }
    
    def _define_training_metrics(self):
        """训练过程核心指标"""
        return {
            'loss_curve': {
                'metric': 'training_loss',
                'threshold': 0.1,
                'alert_condition': 'increasing',
                'collection_interval': '1min'
            },
            'learning_rate': {
                'metric': 'current_lr',
                'expected_range': [1e-6, 1e-3],
                'alert_on_out_of_range': True
            },
            'gradient_norm': {
                'metric': 'grad_norm',
                'threshold': 1.0,
                'alert_on_explode': True
            },
            'throughput': {
                'metric': 'samples_per_second',
                'baseline': 50,
                'degradation_threshold': 0.8
            }
        }
    
    def _define_resource_metrics(self):
        """资源使用指标"""
        return {
            'gpu_utilization': {
                'metric': 'DCGM_FI_DEV_GPU_UTIL',
                'optimal_range': [70, 95],
                'underutilization_threshold': 60,
                'overutilization_threshold': 98
            },
            'gpu_memory': {
                'metric': 'DCGM_FI_DEV_MEM_COPY_UTIL',
                'warning_threshold': 90,
                'critical_threshold': 95
            },
            'cpu_utilization': {
                'metric': 'cpu_usage_percent',
                'optimal_range': [50, 80],
                'alert_threshold': 90
            },
            'memory_usage': {
                'metric': 'memory_usage_bytes',
                'warning_threshold': 0.85,
                'critical_threshold': 0.95
            }
        }
    
    def _define_quality_metrics(self):
        """模型质量指标"""
        return {
            'validation_loss': {
                'metric': 'val_loss',
                'improvement_threshold': 0.05,
                'stagnation_patience': 10
            },
            'domain_accuracy': {
                'metric': 'domain_specific_accuracy',
                'minimum_threshold': 0.85,
                'target_threshold': 0.92
            },
            'convergence_rate': {
                'metric': 'convergence_speed',
                'expected_epochs': 5,
                'slow_convergence_alert': True
            }
        }
    
    def _define_cost_metrics(self):
        """成本相关指标"""
        return {
            'hourly_cost': {
                'metric': 'cost_per_hour',
                'budget_limit': 10.0,
                'forecast_horizon': '24h'
            },
            'resource_efficiency': {
                'metric': 'cost_per_sample_processed',
                'benchmark': 0.001,
                'optimization_target': 0.0005
            }
        }

# 实时监控实现
class RealTimeMonitor:
    def __init__(self, monitor_config):
        self.config = monitor_config
        self.alert_manager = AlertManager()
        self.metric_collector = MetricCollector()
        self.anomaly_detector = AnomalyDetector()
    
    def setup_monitoring(self):
        """设置监控体系"""
        # 配置Prometheus指标采集
        self._setup_prometheus_scraping()
        
        # 配置日志监控
        self._setup_logging_pipeline()
        
        # 配置告警规则
        self._setup_alerting_rules()
        
        # 启动监控代理
        self._start_monitoring_agents()
    
    def collect_metrics(self):
        """收集各类指标"""
        metrics = {}
        
        # 训练指标
        metrics['training'] = self._collect_training_metrics()
        
        # 资源指标
        metrics['resources'] = self._collect_resource_metrics()
        
        # 质量指标
        metrics['quality'] = self._collect_quality_metrics()
        
        # 成本指标
        metrics['cost'] = self._collect_cost_metrics()
        
        return metrics
    
    def detect_anomalies(self, metrics):
        """异常检测"""
        anomalies = []
        
        for category, category_metrics in metrics.items():
            category_anomalies = self.anomaly_detector.detect(
                category_metrics, 
                self.config.metrics[category]
            )
            anomalies.extend(category_anomalies)
        
        return anomalies
    
    def trigger_alerts(self, anomalies):
        """触发告警"""
        for anomaly in anomalies:
            self.alert_manager.send_alert(anomaly)
```

### 1.2 Kubernetes监控集成

```yaml
# Prometheus监控配置
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: finetuning-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: model-finetuning
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s
  - port: http
    path: /health
    interval: 60s
---
# Grafana仪表板配置
apiVersion: integreatly.org/v1alpha1
kind: GrafanaDashboard
metadata:
  name: finetuning-dashboard
  namespace: monitoring
spec:
  json: |
    {
      "dashboard": {
        "title": "Model Fine-tuning Monitoring",
        "panels": [
          {
            "title": "Training Loss Trend",
            "type": "graph",
            "targets": [
              {
                "expr": "training_loss",
                "legendFormat": "Loss"
              }
            ]
          },
          {
            "title": "GPU Utilization",
            "type": "gauge",
            "targets": [
              {
                "expr": "avg(DCGM_FI_DEV_GPU_UTIL)",
                "legendFormat": "GPU %"
              }
            ]
          },
          {
            "title": "Cost Analysis",
            "type": "graph",
            "targets": [
              {
                "expr": "sum(cost_per_hour)",
                "legendFormat": "Hourly Cost"
              }
            ]
          }
        ]
      }
    }
```

## 2. 成本优化策略

### 2.1 资源优化

```python
# 成本优化引擎
class CostOptimizer:
    def __init__(self):
        self.pricing_data = self._load_pricing_information()
        self.resource_profiles = self._load_resource_profiles()
        self.optimization_strategies = self._define_optimization_strategies()
    
    def optimize_training_cost(self, training_config):
        """优化训练成本"""
        optimizations = {}
        
        # 实例类型优化
        optimizations['instance_selection'] = self._optimize_instance_types(training_config)
        
        # Spot实例策略
        optimizations['spot_instances'] = self._configure_spot_instances(training_config)
        
        # 自动扩缩容
        optimizations['autoscaling'] = self._setup_autoscaling(training_config)
        
        # 检查点优化
        optimizations['checkpointing'] = self._optimize_checkpointing(training_config)
        
        return optimizations
    
    def _optimize_instance_types(self, config):
        """优化实例类型选择"""
        # 分析训练需求
        gpu_required = config.get('gpu_count', 1)
        memory_required = config.get('memory_gb', 32)
        cpu_required = config.get('cpu_cores', 8)
        
        # 匹配最优实例类型
        best_instances = []
        for instance in self.pricing_data.instances:
            if (instance.gpu >= gpu_required and 
                instance.memory >= memory_required and 
                instance.cpu >= cpu_required):
                cost_efficiency = instance.performance / instance.hourly_cost
                best_instances.append({
                    'instance_type': instance.type,
                    'cost_efficiency': cost_efficiency,
                    'hourly_cost': instance.hourly_cost
                })
        
        # 按性价比排序
        best_instances.sort(key=lambda x: x['cost_efficiency'], reverse=True)
        return best_instances[:3]
    
    def _configure_spot_instances(self, config):
        """配置Spot实例策略"""
        spot_config = {
            'max_spot_price': config.get('budget_per_hour', 5.0) * 0.7,
            'fallback_strategy': 'on-demand',
            'interruption_handling': {
                'checkpoint_frequency': '5min',
                'graceful_shutdown': True,
                'auto_restart': True
            }
        }
        return spot_config

# 资源调度优化
class ResourceScheduler:
    def __init__(self):
        self.cluster_state = ClusterStateMonitor()
        self.prediction_engine = ResourcePredictionEngine()
    
    def schedule_training_job(self, job_spec):
        """智能调度训练任务"""
        # 预测资源需求
        resource_prediction = self.prediction_engine.predict_resources(job_spec)
        
        # 寻找最优节点
        optimal_nodes = self._find_optimal_nodes(resource_prediction)
        
        # 应用调度策略
        scheduling_decisions = self._apply_scheduling_strategy(
            job_spec, optimal_nodes, resource_prediction
        )
        
        return scheduling_decisions
    
    def _find_optimal_nodes(self, resource_req):
        """寻找最优计算节点"""
        available_nodes = self.cluster_state.get_available_nodes()
        
        suitable_nodes = []
        for node in available_nodes:
            if self._node_suitable(node, resource_req):
                suitability_score = self._calculate_suitability_score(node, resource_req)
                suitable_nodes.append({
                    'node': node,
                    'score': suitability_score,
                    'cost': self._calculate_node_cost(node)
                })
        
        # 按得分和成本排序
        suitable_nodes.sort(key=lambda x: (x['score'], -x['cost']), reverse=True)
        return suitable_nodes
    
    def _node_suitable(self, node, req):
        """检查节点是否适合"""
        return (node.gpu_count >= req.gpu_count and
                node.available_memory >= req.memory_gb and
                node.available_cpu >= req.cpu_cores)
```

### 2.2 预算管理和预警

```python
# 预算管理系统
class BudgetManager:
    def __init__(self, budget_config):
        self.budget_limits = budget_config.get('limits', {})
        self.alert_thresholds = budget_config.get('thresholds', {})
        self.cost_tracker = CostTracker()
        self.forecast_engine = CostForecastEngine()
    
    def monitor_budget(self, training_job):
        """监控预算使用情况"""
        # 实时成本跟踪
        current_cost = self.cost_tracker.get_current_cost(training_job)
        
        # 预算使用率计算
        budget_category = training_job.get('budget_category', 'default')
        budget_limit = self.budget_limits.get(budget_category, 1000)
        usage_percentage = (current_cost / budget_limit) * 100
        
        # 预警检查
        alerts = self._check_budget_alerts(
            budget_category, usage_percentage, current_cost
        )
        
        # 成本预测
        forecast = self.forecast_engine.predict_final_cost(training_job)
        
        return {
            'current_cost': current_cost,
            'usage_percentage': usage_percentage,
            'remaining_budget': budget_limit - current_cost,
            'forecasted_cost': forecast,
            'alerts': alerts
        }
    
    def _check_budget_alerts(self, category, usage_pct, current_cost):
        """检查预算预警"""
        alerts = []
        thresholds = self.alert_thresholds.get(category, [50, 80, 90])
        
        for threshold in thresholds:
            if usage_pct >= threshold:
                alerts.append({
                    'level': self._get_alert_level(threshold),
                    'message': f'Budget usage reached {usage_pct:.1f}% for {category}',
                    'threshold': threshold,
                    'current_cost': current_cost
                })
        
        return alerts
    
    def enforce_budget_limits(self, training_job):
        """强制执行预算限制"""
        budget_status = self.monitor_budget(training_job)
        
        if budget_status['usage_percentage'] >= 95:
            # 接近预算上限，采取措施
            return self._take_budget_enforcement_actions(training_job, budget_status)
        
        return {'status': 'within_budget', 'actions': []}
    
    def _take_budget_enforcement_actions(self, job, status):
        """执行预算强制措施"""
        actions = []
        
        # 降低训练强度
        if status['usage_percentage'] >= 95:
            actions.append({
                'type': 'reduce_batch_size',
                'new_value': job.batch_size // 2
            })
        
        # 启用Spot实例
        if status['usage_percentage'] >= 90:
            actions.append({
                'type': 'switch_to_spot',
                'max_price_multiplier': 0.7
            })
        
        # 提前终止非关键任务
        if status['usage_percentage'] >= 98:
            actions.append({
                'type': 'terminate_non_critical',
                'reason': 'budget_exceeded'
            })
        
        return {'status': 'budget_enforced', 'actions': actions}
```

### 2.3 性能与成本平衡

```python
# 性价比优化器
class PerformanceCostOptimizer:
    def __init__(self):
        self.benchmarks = self._load_performance_benchmarks()
        self.cost_models = self._build_cost_models()
    
    def optimize_performance_cost_ratio(self, training_scenario):
        """优化性能成本比"""
        # 性能基准测试
        baseline_performance = self._run_baseline_benchmark(training_scenario)
        
        # 成本效益分析
        cost_benefit_analysis = self._analyze_cost_benefit(training_scenario)
        
        # 优化建议生成
        optimization_recommendations = self._generate_optimization_recommendations(
            baseline_performance, cost_benefit_analysis
        )
        
        return optimization_recommendations
    
    def _run_baseline_benchmark(self, scenario):
        """运行基线基准测试"""
        benchmark_results = {}
        
        # 测试不同配置的性能
        configs_to_test = self._generate_test_configs(scenario)
        
        for config in configs_to_test:
            performance_metrics = self._execute_benchmark(config)
            cost_metrics = self._calculate_config_cost(config)
            
            benchmark_results[config.name] = {
                'performance': performance_metrics,
                'cost': cost_metrics,
                'performance_cost_ratio': self._calculate_ratio(
                    performance_metrics, cost_metrics
                )
            }
        
        return benchmark_results
    
    def _generate_optimization_recommendations(self, baseline, cost_analysis):
        """生成优化建议"""
        recommendations = []
        
        # 识别最佳性价比配置
        best_ratio_config = self._find_best_performance_cost_ratio(baseline)
        recommendations.append({
            'type': 'configuration_optimization',
            'recommended_config': best_ratio_config,
            'expected_savings': self._calculate_expected_savings(best_ratio_config),
            'performance_impact': self._assess_performance_impact(best_ratio_config)
        })
        
        # 识别潜在优化点
        optimization_opportunities = self._identify_optimization_opportunities(
            baseline, cost_analysis
        )
        recommendations.extend(optimization_opportunities)
        
        return recommendations

# 成本可视化和报告
class CostReporting:
    def __init__(self):
        self.report_templates = self._load_report_templates()
        self.visualization_engine = VisualizationEngine()
    
    def generate_cost_report(self, training_jobs, period='monthly'):
        """生成成本报告"""
        # 数据聚合
        aggregated_data = self._aggregate_cost_data(training_jobs, period)
        
        # 成本分析
        cost_analysis = self._perform_cost_analysis(aggregated_data)
        
        # 可视化生成
        charts = self._generate_visualizations(cost_analysis)
        
        # 报告组装
        report = self._assemble_report(cost_analysis, charts)
        
        return report
    
    def _aggregate_cost_data(self, jobs, period):
        """聚合成本数据"""
        aggregated = {
            'total_cost': 0,
            'cost_by_technique': {},
            'cost_by_domain': {},
            'cost_trend': [],
            'top_cost_drivers': []
        }
        
        for job in jobs:
            # 按时间段过滤
            if self._job_in_period(job, period):
                cost = job.actual_cost
                aggregated['total_cost'] += cost
                
                # 按技术分类
                technique = job.technique
                aggregated['cost_by_technique'][technique] = \
                    aggregated['cost_by_technique'].get(technique, 0) + cost
                
                # 按领域分类
                domain = job.domain
                aggregated['cost_by_domain'][domain] = \
                    aggregated['cost_by_domain'].get(domain, 0) + cost
        
        return aggregated
```

## 3. 自动化运维策略

### 3.1 智能调度和故障恢复

```python
# 智能调度系统
class IntelligentScheduler:
    def __init__(self):
        self.ml_predictor = MLPredictor()
        self.resource_optimizer = ResourceOptimizer()
        self.failure_predictor = FailurePredictor()
    
    def intelligent_scheduling(self, training_requests):
        """智能化训练任务调度"""
        scheduled_jobs = []
        
        for request in training_requests:
            # 预测资源需求
            predicted_resources = self.ml_predictor.predict_resource_needs(request)
            
            # 优化资源配置
            optimized_config = self.resource_optimizer.optimize_configuration(
                request, predicted_resources
            )
            
            # 预测失败风险
            failure_risk = self.failure_predictor.assess_failure_risk(optimized_config)
            
            # 制定调度策略
            scheduling_plan = self._create_scheduling_plan(
                request, optimized_config, failure_risk
            )
            
            scheduled_jobs.append(scheduling_plan)
        
        return scheduled_jobs
    
    def _create_scheduling_plan(self, request, config, risk):
        """创建调度计划"""
        plan = {
            'job_id': request.job_id,
            'resource_allocation': config.resources,
            'scheduling_priority': self._calculate_priority(request, risk),
            'failure_mitigation': self._plan_failure_mitigation(risk),
            'cost_optimization': self._plan_cost_optimization(config)
        }
        
        return plan

# 自动故障恢复
class AutoRecoverySystem:
    def __init__(self):
        self.recovery_strategies = self._load_recovery_strategies()
        self.health_monitor = HealthMonitor()
    
    def monitor_and_recover(self, training_jobs):
        """监控并自动恢复"""
        recovery_actions = []
        
        for job in training_jobs:
            health_status = self.health_monitor.check_health(job)
            
            if not health_status.healthy:
                recovery_action = self._determine_recovery_action(
                    job, health_status.issues
                )
                recovery_actions.append(recovery_action)
                
                # 执行恢复
                self._execute_recovery(recovery_action)
        
        return recovery_actions
    
    def _determine_recovery_action(self, job, issues):
        """确定恢复动作"""
        # 根据问题类型选择恢复策略
        for issue in issues:
            strategy = self.recovery_strategies.get(issue.type)
            if strategy:
                return {
                    'job_id': job.id,
                    'issue_type': issue.type,
                    'strategy': strategy,
                    'parameters': self._configure_recovery_parameters(issue)
                }
        
        # 默认恢复策略
        return {
            'job_id': job.id,
            'issue_type': 'unknown',
            'strategy': 'restart_with_backoff',
            'parameters': {'max_retries': 3, 'backoff_factor': 2}
        }
```

这个完整的监控和成本优化体系提供了：

✅ **全方位监控指标** - 覆盖训练、资源、质量和成本各个维度  
✅ **智能化成本优化** - 实例选择、Spot策略、自动扩缩容  
✅ **预算管控机制** - 实时监控、预警和强制执行  
✅ **自动化运维能力** - 智能调度、故障预测和自动恢复  
✅ **可视化报告系统** - 成本分析和优化建议展示