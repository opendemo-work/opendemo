# AI/ML 技术栈命名大全

本文件定义了AI/ML技术栈中各类组件、变量、函数、类等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、核心概念命名规范

### 1.1 模型相关命名
```python
# 模型实例命名
model_instance = ModelClass()
bert_classifier = BertClassifier()
resnet_backbone = ResNetBackbone()

# 模型版本控制
model_v1_0_0 = load_model("model_v1.0.0.pkl")
latest_model = load_model("model_latest.pkl")
production_model = load_model("model_production.pkl")

# 模型状态标识
model_status_ready = "READY"
model_status_training = "TRAINING" 
model_status_degraded = "DEGRADED"
model_status_failed = "FAILED"
```

### 1.2 数据集命名
```python
# 训练数据集
train_dataset = load_dataset("train")
training_data_clean = preprocess_data(raw_train_data)
train_samples_balanced = balance_dataset(train_samples)

# 验证数据集  
validation_set = load_dataset("validation")
val_data_processed = preprocess_validation_data(val_raw)
cross_val_folds = create_cross_validation_splits(data, k=5)

# 测试数据集
test_dataset = load_dataset("test")
test_data_final = prepare_final_test_set(test_raw)
holdout_set = create_holdout_dataset(full_data, ratio=0.2)
```

### 1.3 特征工程命名
```python
# 特征提取
feature_extractor = FeatureExtractor()
text_features_bert = extract_bert_features(text_data)
image_features_cnn = extract_cnn_features(image_data)

# 特征预处理
feature_scaler = StandardScaler()
normalized_features = feature_scaler.fit_transform(raw_features)
encoded_categorical = one_hot_encode(categorical_features)

# 特征选择
feature_selector = SelectKBest()
important_features = feature_selector.fit_transform(X, y)
selected_features_mask = get_feature_importance_mask(model, threshold=0.01)
```

## 二、训练过程命名规范

### 2.1 训练配置
```python
# 训练参数
training_config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 100,
    "early_stopping_patience": 10
}

# 超参数调优
hyperparam_grid = {
    "learning_rate": [0.001, 0.01, 0.1],
    "batch_size": [16, 32, 64],
    "dropout_rate": [0.1, 0.3, 0.5]
}

best_params = hyperparameter_tuning(hyperparam_grid, cv_folds=5)
```

### 2.2 训练监控
```python
# 损失函数追踪
train_loss_history = []
val_loss_history = []
epoch_losses = {"train": [], "validation": []}

# 性能指标监控
accuracy_scores = []
f1_scores_history = []
confusion_matrices = []

# 训练状态检查
training_status_ok = check_training_health(loss_curve)
convergence_reached = detect_convergence(loss_history, threshold=0.001)
overfitting_detected = detect_overfitting(train_acc, val_acc, gap_threshold=0.15)
```

### 2.3 模型评估
```python
# 评估结果存储
evaluation_results = {}
metrics_classification = calculate_classification_metrics(y_true, y_pred)
regression_metrics = calculate_regression_metrics(y_true, y_pred)

# 交叉验证结果
cv_scores_accuracy = cross_validate_model(model, X, y, scoring="accuracy")
cv_results_detailed = perform_detailed_cv(model, X, y, cv=10)

# 错误分析
misclassified_samples = find_misclassified_predictions(y_true, y_pred)
error_analysis_report = generate_error_analysis(predictions, ground_truth)
confusion_details = analyze_confusion_matrix(confusion_mat)
```

## 三、部署运维命名规范

### 3.1 模型服务化
```python
# 模型API端点
model_api_endpoint = "/api/v1/models/predict"
health_check_endpoint = "/api/v1/health"
metrics_endpoint = "/api/v1/metrics"

# 服务实例管理
model_server_instance = ModelServer()
prediction_service = PredictionService()
model_registry = ModelRegistry()

# 负载均衡配置
load_balancer_config = {
    "algorithm": "round_robin",
    "health_check_interval": 30,
    "timeout": 5
}
```

### 3.2 监控告警
```python
# 性能监控指标
latency_metrics = {"p50": 0.1, "p95": 0.5, "p99": 1.2}  # 秒
throughput_metrics = {"requests_per_second": 1000, "concurrent_users": 50}
error_rate_metrics = {"http_errors": 0.01, "prediction_errors": 0.02}

# 告警阈值设置
alert_thresholds = {
    "latency_p95": 1.0,      # 秒
    "error_rate": 0.05,      # 5%
    "cpu_utilization": 0.8,  # 80%
    "memory_usage": 0.85     # 85%
}

# 健康检查
service_health_status = check_service_health()
model_performance_degraded = monitor_model_drift(predictions_stream)
data_quality_issues = detect_data_drift(training_data, inference_data)
```

### 3.3 日志记录
```python
# 请求日志
request_log_entry = {
    "timestamp": current_time,
    "request_id": generate_uuid(),
    "model_version": "v1.2.3",
    "input_shape": input_tensor.shape,
    "processing_time_ms": processing_duration
}

# 错误日志
error_log_critical = {
    "level": "CRITICAL",
    "error_type": "MODEL_LOADING_FAILED",
    "model_path": "/models/production/model.pkl",
    "stack_trace": traceback.format_exc()
}

# 性能日志
performance_log = {
    "metric": "prediction_latency",
    "value": prediction_time,
    "unit": "milliseconds",
    "percentile": "p95"
}
```

## 四、故障排查命名规范

### 4.1 内存问题诊断
```python
# 内存监控
memory_usage_current = get_memory_usage()
memory_leak_detected = detect_memory_leak(memory_snapshots, threshold=0.1)
gpu_memory_allocated = get_gpu_memory_info()

# 缓存管理
cache_hit_rate = calculate_cache_efficiency(cache_stats)
cache_eviction_count = monitor_cache_evictions()
model_cache_size = get_cached_model_size(model)

# 资源释放检查
unreleased_resources = find_orphaned_objects()
garbage_collection_stats = monitor_gc_activity()
memory_profiling_results = profile_memory_usage(during_inference)
```

### 4.2 性能瓶颈分析
```python
# 瓶颈识别
bottleneck_location = identify_performance_bottleneck(profile_data)
slow_operations = find_slow_functions(execution_profile)
resource_contention_points = detect_resource_locks(thread_dumps)

# 优化建议
optimization_recommendations = generate_performance_tips(bottleneck_analysis)
scaling_requirements = calculate_scaling_needs(throughput_data)
caching_opportunities = identify_cacheable_operations(frequent_requests)
```

### 4.3 模型退化检测
```python
# 数据漂移监测
data_drift_score = calculate_data_drift_score(training_data, current_data)
feature_distribution_changes = compare_feature_distributions(old_data, new_data)
concept_drift_detected = detect_concept_drift(predictions_accuracy_timeline)

# 模型性能衰退
model_performance_drop = detect_performance_degradation(
    current_metrics, baseline_metrics, threshold=0.1
)
prediction_confidence_decline = monitor_prediction_certainty(scores_history)
accuracy_regression = compare_current_accuracy_with_historical(weekly_metrics)
```

## 五、安全合规命名规范

### 5.1 数据安全
```python
# 敏感数据处理
pii_data_masked = mask_personal_identifiers(raw_data)
encrypted_model_weights = encrypt_model_parameters(model_state_dict)
access_control_policy = define_data_access_rules(user_roles)

# 合规检查
gdpr_compliance_status = check_gdpr_compliance(data_processing_pipeline)
audit_trail_enabled = enable_audit_logging(sensitive_operations)
data_retention_policy = configure_data_lifecycle_management(retention_days=365)
```

### 5.2 模型安全
```python
# 对抗攻击防护
adversarial_attack_detected = detect_adversarial_examples(input_samples)
model_robustness_score = evaluate_model_robustness(against_attacks=True)
defense_mechanisms_active = activate_adversarial_defense_layers()

# 模型解释性
feature_importance_shap = calculate_shap_values(model, sample_data)
prediction_explanation_lime = generate_lime_explanation(model, instance)
model_interpretability_score = assess_model_explainability(complexity_metrics)
```

## 六、版本管理命名规范

### 6.1 模型版本控制
```python
# 版本号格式
model_version_semantic = "v1.2.3"  # 主版本.次版本.修订版本
experiment_id_unique = f"exp_{timestamp}_{random_suffix}"

# 版本元数据
version_metadata = {
    "version": "v1.2.3",
    "created_at": timestamp,
    "created_by": "ml_engineer_001",
    "training_data_version": "data_v2.1.0",
    "performance_metrics": evaluation_results,
    "deployment_status": "production"
}

# 实验追踪
experiment_tracking = MLflowClient()
run_parameters = log_experiment_parameters(config)
artifacts_saved = save_experiment_artifacts(model_artifacts, logs_dir)
```

### 6.2 部署版本管理
```python
# 环境标识
environment_development = "dev"
environment_staging = "staging" 
environment_production = "prod"

# 部署策略
deployment_strategy_blue_green = "blue-green"
deployment_strategy_canary = "canary"
rollback_version = "v1.1.5"  # 回滚到的版本

# 流量控制
traffic_split_ratio = {"current": 0.9, "new": 0.1}  # 金丝雀发布
deployment_progress = monitor_deployment_status(service_name)
health_check_passed = verify_deployment_health(new_version_endpoint)
```

## 七、最佳实践示例

### 7.1 生产环境模型加载
```python
class ProductionModelManager:
    def __init__(self):
        self.model_registry = ModelRegistry()
        self.health_checker = HealthCheckService()
        self.logger = setup_structured_logger("model_manager")
        
    def load_model_safely(self, model_path, timeout=30):
        """安全加载模型，包含超时和健康检查"""
        try:
            start_time = time.time()
            model = self._load_with_timeout(model_path, timeout)
            
            # 验证模型完整性
            if not self._validate_model_integrity(model):
                raise ModelIntegrityError("Model validation failed")
                
            # 性能基准测试
            baseline_performance = self._benchmark_model(model)
            self.logger.info(f"Model loaded successfully. Baseline latency: {baseline_performance}")
            
            return model
            
        except Exception as e:
            self.logger.error(f"Failed to load model {model_path}: {str(e)}")
            raise ModelLoadingError(f"Model loading failed: {str(e)}")
    
    def _validate_model_integrity(self, model):
        """验证模型完整性和基本功能"""
        try:
            # 基本预测测试
            test_input = self._generate_test_input()
            prediction = model.predict(test_input)
            
            # 输出格式验证
            if not self._validate_prediction_format(prediction):
                return False
                
            return True
        except Exception:
            return False
```

### 7.2 异常处理和恢复
```python
class ModelFailureHandler:
    def __init__(self):
        self.fallback_models = {}
        self.alert_system = AlertNotificationService()
        self.recovery_attempts = {}
        
    def handle_model_failure(self, model_id, error_info):
        """处理模型故障，尝试自动恢复"""
        self.logger.critical(f"Model {model_id} failed: {error_info}")
        
        # 记录故障信息
        failure_record = {
            "timestamp": datetime.now(),
            "model_id": model_id,
            "error_type": type(error_info).__name__,
            "error_message": str(error_info),
            "stack_trace": traceback.format_exc()
        }
        
        # 尝试降级方案
        if self._attempt_fallback(model_id):
            self.alert_system.send_alert(
                level="WARNING",
                message=f"Model {model_id} using fallback. Investigate root cause."
            )
            return True
            
        # 触发紧急告警
        self.alert_system.send_alert(
            level="CRITICAL",
            message=f"Model {model_id} failure. No fallback available. Service degraded."
        )
        return False
        
    def _attempt_fallback(self, model_id):
        """尝试使用备用模型"""
        if model_id in self.fallback_models:
            try:
                fallback_model = self.fallback_models[model_id]
                # 验证备用模型可用性
                if self._test_model_availability(fallback_model):
                    self.logger.info(f"Successfully switched to fallback model for {model_id}")
                    return True
            except Exception as e:
                self.logger.error(f"Fallback model also failed: {str(e)}")
        return False
```

### 7.3 监控仪表板关键指标
```python
class ModelMonitoringDashboard:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.anomaly_detector = AnomalyDetectionEngine()
        
    def get_production_metrics(self):
        """获取生产环境关键监控指标"""
        return {
            # 性能指标
            "latency_p50": self.metrics_collector.get_percentile("latency", 50),
            "latency_p95": self.metrics_collector.get_percentile("latency", 95),
            "latency_p99": self.metrics_collector.get_percentile("latency", 99),
            "throughput_rps": self.metrics_collector.get_rate("requests"),
            
            # 准确性指标
            "accuracy_current": self.metrics_collector.get_gauge("model_accuracy"),
            "accuracy_baseline": self.metrics_collector.get_gauge("baseline_accuracy"),
            "accuracy_degradation": self._calculate_accuracy_drift(),
            
            # 系统健康指标
            "cpu_utilization": self.metrics_collector.get_gauge("cpu_percent"),
            "memory_usage": self.metrics_collector.get_gauge("memory_percent"),
            "gpu_utilization": self.metrics_collector.get_gauge("gpu_percent"),
            
            # 服务质量指标
            "error_rate": self.metrics_collector.get_rate("errors"),
            "success_rate": self.metrics_collector.get_ratio("successful_requests", "total_requests"),
            "saturation_level": self._calculate_system_saturation()
        }
    
    def _calculate_accuracy_drift(self):
        """计算准确性漂移程度"""
        current = self.metrics_collector.get_gauge("model_accuracy")
        baseline = self.metrics_collector.get_gauge("baseline_accuracy")
        return abs(current - baseline) / baseline if baseline > 0 else 0
    
    def _calculate_system_saturation(self):
        """计算系统饱和度"""
        cpu_load = self.metrics_collector.get_gauge("cpu_percent") / 100
        memory_load = self.metrics_collector.get_gauge("memory_percent") / 100
        return max(cpu_load, memory_load)
```

---

**注意事项：**
1. 所有命名应具有明确的业务含义，避免使用模糊的缩写
2. 在生产环境中，优先考虑可观察性和可调试性
3. 关键业务逻辑必须包含详细的日志记录和错误处理
4. 定期审查和更新命名规范以适应业务发展