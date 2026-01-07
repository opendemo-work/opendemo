# Pipeline Experiment Management

## Overview

This demo demonstrates how to create, run, and compare Kubeflow Pipeline experiments to track multiple runs and optimize ML workflows. Experiments provide a way to organize pipeline runs, compare results, and systematically explore different configurations and hyperparameters.

Experiment management is essential for tracking the progress of machine learning model development, enabling data scientists to compare different approaches and identify the best-performing configurations.

## Prerequisites

Before starting this demo, ensure you have:

- A running Kubernetes cluster with Kubeflow Pipelines (v1.8+) installed
- Python 3.8+ installed locally
- Kubeflow Pipelines SDK (kfp) installed: `pip install kfp>=2.0.0`
- kubectl configured with access to your cluster
- Access to the Kubeflow Dashboard
- Basic understanding of ML experiment tracking concepts

## Architecture

### Experiment Management Workflow

```
┌────────────────────────────────────────────────────────────┐
│             Experiment Management System                    │
│                                                            │
│  1. Create Experiments                                     │
│     ┌─────────────────────────────────┐                   │
│     │  Experiment A: Model Selection  │                   │
│     │  Experiment B: Hyperparameter   │                   │
│     │  Experiment C: Feature Eng      │                   │
│     └─────────────────────────────────┘                   │
│                    │                                       │
│                    ▼                                       │
│  2. Run Pipeline Multiple Times                            │
│     ┌─────────────────────────────────┐                   │
│     │  Run 1: params={lr=0.01}        │→ metrics, artifacts│
│     │  Run 2: params={lr=0.001}       │→ metrics, artifacts│
│     │  Run 3: params={lr=0.0001}      │→ metrics, artifacts│
│     └─────────────────────────────────┘                   │
│                    │                                       │
│                    ▼                                       │
│  3. Track & Compare Results                                │
│     ┌─────────────────────────────────┐                   │
│     │  Metrics Comparison Dashboard   │                   │
│     │  ┌─────┬─────┬─────────┐        │                   │
│     │  │Run  │LR   │Accuracy │        │                   │
│     │  ├─────┼─────┼─────────┤        │                   │
│     │  │  1  │0.01 │  0.85   │        │                   │
│     │  │  2  │0.001│  0.92   │ ← Best │                   │
│     │  │  3  │0.0001│ 0.88   │        │                   │
│     │  └─────┴─────┴─────────┘        │                   │
│     └─────────────────────────────────┘                   │
│                    │                                       │
│                    ▼                                       │
│  4. Select Best Configuration                              │
│     ┌─────────────────────────────────┐                   │
│     │  Deploy model from Run 2        │                   │
│     │  with lr=0.001, accuracy=0.92   │                   │
│     └─────────────────────────────────┘                   │
└────────────────────────────────────────────────────────────┘
```

### Experiment Hierarchy

```
Kubeflow Pipelines
    │
    ├── Experiment: "Model Selection"
    │   ├── Run 1: RandomForest
    │   ├── Run 2: XGBoost
    │   └── Run 3: NeuralNet
    │
    ├── Experiment: "Hyperparameter Tuning"
    │   ├── Run 1: lr=0.01, batch=32
    │   ├── Run 2: lr=0.001, batch=64
    │   └── Run 3: lr=0.0001, batch=128
    │
    └── Experiment: "Feature Engineering"
        ├── Run 1: Original features
        ├── Run 2: +Polynomial features
        └── Run 3: +PCA features
```

## Step-by-Step Guide

### Step 1: Install Kubeflow Pipelines SDK

Install the required Python package:

```bash
pip install kfp>=2.0.0
```

### Step 2: Connect to Kubeflow Pipelines

Set up connection to your Kubeflow Pipelines instance:

```python
# See code/experiment_manager.py for connection setup
python code/experiment_manager.py --action connect
```

### Step 3: Create an Experiment

Create a new experiment to organize your pipeline runs:

```bash
# Using the experiment manager script
python code/experiment_manager.py --action create \
  --experiment-name "ml-model-optimization" \
  --description "Experiment for optimizing ML model hyperparameters"
```

Or programmatically:

```python
from kfp import Client

client = Client()
experiment = client.create_experiment(
    name="ml-model-optimization",
    description="Experiment for optimizing ML model hyperparameters"
)
print(f"Created experiment: {experiment.id}")
```

### Step 4: Submit Pipeline Runs with Different Parameters

Run the same pipeline multiple times with different configurations:

```bash
# Run 1: Learning rate 0.01
python code/experiment_manager.py --action run \
  --experiment-name "ml-model-optimization" \
  --run-name "run-lr-001" \
  --param learning_rate=0.01 \
  --param batch_size=32

# Run 2: Learning rate 0.001  
python code/experiment_manager.py --action run \
  --experiment-name "ml-model-optimization" \
  --run-name "run-lr-0001" \
  --param learning_rate=0.001 \
  --param batch_size=32

# Run 3: Learning rate 0.0001
python code/experiment_manager.py --action run \
  --experiment-name "ml-model-optimization" \
  --run-name "run-lr-00001" \
  --param learning_rate=0.0001 \
  --param batch_size=32
```

### Step 5: List All Runs in an Experiment

View all runs within an experiment:

```bash
python code/experiment_manager.py --action list-runs \
  --experiment-name "ml-model-optimization"
```

### Step 6: Compare Run Results

Compare metrics across different runs:

```bash
# Generate comparison report
python code/experiment_manager.py --action compare \
  --experiment-name "ml-model-optimization"
```

### Step 7: View Run Details

Get detailed information about a specific run:

```bash
python code/experiment_manager.py --action get-run \
  --run-id <run-id>
```

### Step 8: Access via Kubeflow Dashboard

View experiments and runs in the Kubeflow UI:

```bash
# Get Dashboard URL
kubectl get svc centraldashboard -n kubeflow

# Navigate to Experiments section
# Compare runs visually
# Download artifacts and logs
```

## Configuration Files

### Experiment Manager Script
See `code/experiment_manager.py` for the complete experiment management implementation.

### Simple Pipeline Definition
See `code/simple_training_pipeline.py` for a sample pipeline to use with experiments.

## Validation

### Verify Experiment Created

```bash
# List all experiments
python code/experiment_manager.py --action list-experiments

# Check experiment details
python code/experiment_manager.py --action get-experiment \
  --experiment-name "ml-model-optimization"
```

### Verify Runs are Tracked

```bash
# Check run status
python code/experiment_manager.py --action list-runs \
  --experiment-name "ml-model-optimization"

# Expected output:
# Run ID | Run Name | Status | Created At
# ------ | -------- | ------ | ----------
# abc123 | run-lr-001 | Succeeded | 2024-01-07 10:00
# def456 | run-lr-0001 | Succeeded | 2024-01-07 10:15
# ghi789 | run-lr-00001 | Running | 2024-01-07 10:30
```

### Compare Metrics Programmatically

```python
from kfp import Client

client = Client()
experiment = client.get_experiment(experiment_name="ml-model-optimization")

# Get all runs
runs = client.list_runs(experiment_id=experiment.id)

# Compare metrics
for run in runs.runs:
    print(f"{run.name}: {run.metrics}")
```

## Expected Results

After completing this demo, you should observe:

1. **Organized Experiments**: Multiple experiments created for different objectives
2. **Multiple Runs**: Several pipeline runs within each experiment
3. **Tracked Metrics**: Metrics logged and accessible for each run
4. **Easy Comparison**: Ability to compare runs side-by-side
5. **Run History**: Complete history of all experiment runs

### Success Indicators

- [ ] Experiments are created successfully
- [ ] Multiple runs execute without errors
- [ ] Metrics are logged correctly
- [ ] Runs appear in Dashboard
- [ ] Comparison functionality works
- [ ] Artifacts are stored and retrievable

## Troubleshooting

### Cannot Create Experiment

**Problem**: Error when creating experiment

**Solution**:
```bash
# Check Kubeflow Pipelines is running
kubectl get pods -n kubeflow | grep ml-pipeline

# Verify API access
curl -k https://your-kubeflow-url/pipeline

# Check Python client connection
python -c "from kfp import Client; print(Client())"
```

### Runs Not Appearing in Experiment

**Problem**: Pipeline runs don't show up in the experiment

**Solution**:
```python
# Verify experiment ID is correct
experiment = client.get_experiment(experiment_name="your-experiment")
print(f"Experiment ID: {experiment.id}")

# Submit run with correct experiment ID
run = client.run_pipeline(
    experiment_id=experiment.id,
    job_name="test-run",
    pipeline_id=pipeline_id
)
```

### Cannot Compare Metrics

**Problem**: Metrics not showing up for comparison

**Solution**:
```python
# Ensure metrics are logged correctly in pipeline
from kfp import dsl

@dsl.component
def train_model(accuracy: dsl.Output[dsl.Metrics]):
    # Log metrics
    accuracy.log_metric("accuracy", 0.95)
    accuracy.log_metric("precision", 0.93)
    accuracy.log_metric("recall", 0.92)
```

### Dashboard Access Issues

**Problem**: Cannot access experiments in Dashboard

**Solution**:
```bash
# Port-forward to Dashboard
kubectl port-forward -n kubeflow svc/centraldashboard 8080:80

# Access at http://localhost:8080
# Navigate to Experiments section

# Check RBAC permissions
kubectl auth can-i list experiments --as=your-user@example.com -n kubeflow-user-example-com
```

## Advanced Usage

### Recurring Experiments

Set up scheduled pipeline runs:

```python
from kfp import Client
from datetime import datetime, timedelta

client = Client()

# Create recurring run
job = client.create_recurring_run(
    experiment_id=experiment.id,
    job_name="daily-training",
    pipeline_id=pipeline_id,
    cron_expression="0 2 * * *",  # Daily at 2 AM
    max_concurrency=1,
    enabled=True
)
```

### Experiment Templates

Create reusable experiment configurations:

```python
EXPERIMENT_CONFIGS = {
    "hyperparameter_tuning": {
        "description": "Systematic hyperparameter optimization",
        "parameters": [
            {"learning_rate": [0.01, 0.001, 0.0001]},
            {"batch_size": [16, 32, 64, 128]},
            {"optimizer": ["adam", "sgd", "rmsprop"]}
        ]
    },
    "model_comparison": {
        "description": "Compare different model architectures",
        "parameters": [
            {"model_type": ["rf", "xgboost", "neural_net"]},
            {"features": ["basic", "engineered", "pca"]}
        ]
    }
}

# Use template
def create_experiment_from_template(template_name):
    config = EXPERIMENT_CONFIGS[template_name]
    return client.create_experiment(
        name=template_name,
        description=config["description"]
    )
```

### Automated Best Model Selection

Automatically find the best run based on metrics:

```python
def find_best_run(experiment_name, metric_name="accuracy", maximize=True):
    experiment = client.get_experiment(experiment_name=experiment_name)
    runs = client.list_runs(experiment_id=experiment.id, sort_by="metrics.accuracy desc").runs
    
    if not runs:
        return None
    
    best_run = runs[0]
    print(f"Best run: {best_run.name}")
    print(f"Metrics: {best_run.metrics}")
    
    return best_run

best = find_best_run("ml-model-optimization", "accuracy", maximize=True)
```

### Archive Completed Experiments

Archive old experiments to keep the workspace clean:

```python
def archive_experiment(experiment_name):
    experiment = client.get_experiment(experiment_name=experiment_name)
    client.archive_experiment(experiment.id)
    print(f"Archived experiment: {experiment_name}")
```

## Best Practices

1. **Naming Conventions**: Use clear, descriptive names for experiments and runs
2. **Organize by Objective**: Create separate experiments for different goals
3. **Consistent Parameters**: Use the same parameter names across runs
4. **Tag Runs**: Add metadata tags to runs for easy filtering
5. **Regular Cleanup**: Archive or delete old experiments
6. **Document Experiments**: Add detailed descriptions
7. **Metrics Standard**: Define standard metrics to log
8. **Version Control**: Track pipeline code versions with runs

## Security Considerations

- Use RBAC to control experiment access
- Separate experiments by namespace for multi-tenancy
- Implement audit logging for experiment changes
- Protect sensitive data in artifacts
- Use secrets for credentials, not pipeline parameters
- Review permissions before sharing experiments

## Cleanup

To remove experiments and runs:

```bash
# Delete specific runs
python code/experiment_manager.py --action delete-run --run-id <run-id>

# Archive experiment
python code/experiment_manager.py --action archive \
  --experiment-name "ml-model-optimization"

# Or delete experiment (careful!)
python code/experiment_manager.py --action delete \
  --experiment-name "ml-model-optimization"
```

## Additional Resources

- [Kubeflow Pipelines Experiments](https://www.kubeflow.org/docs/components/pipelines/overview/concepts/experiment/)
- [KFP SDK Documentation](https://kubeflow-pipelines.readthedocs.io/)
- [ML Experiment Tracking Best Practices](https://www.kubeflow.org/docs/components/pipelines/user-guides/core-functions/tracking-ml-experiments/)
- [Pipeline Metrics and Visualization](https://www.kubeflow.org/docs/components/pipelines/user-guides/visualizations/)

## Related Demos

- [pipeline-python-component](../pipeline-python-component/): Create pipeline components
- [pipeline-workflow-orchestration](../pipeline-workflow-orchestration/): Build ML workflows
- [pipeline-artifact-tracking](../pipeline-artifact-tracking/): Track artifacts
- [katib-hyperparameter-tuning](../katib-hyperparameter-tuning/): Automated hyperparameter tuning

## Summary

This demo covered:
- Creating and organizing pipeline experiments
- Running pipelines multiple times with different parameters
- Tracking metrics and artifacts across runs
- Comparing experiment results
- Best practices for experiment management

Experiment management is crucial for systematic ML model development, enabling data science teams to track progress, compare approaches, and identify optimal configurations efficiently.
