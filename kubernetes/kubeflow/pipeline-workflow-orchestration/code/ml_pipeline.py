"""
机器学习Pipeline工作流编排示例

演示完整的ML工作流，包括数据处理、训练、评估和部署
"""

from kfp import dsl
from typing import NamedTuple


@dsl.component(packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0'])
def load_data(data_path: str) -> NamedTuple('Outputs', [('dataset', str)]):
    """加载数据组件"""
    import pandas as pd
    from collections import namedtuple
    
    # 模拟数据加载
    print(f"Loading data from: {data_path}")
    
    # 在实际应用中，这里会从存储加载真实数据
    # 这里使用sklearn的iris数据集作为示例
    from sklearn.datasets import load_iris
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    # 保存到文件
    output_path = '/tmp/dataset.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Dataset loaded with {len(df)} rows")
    
    outputs = namedtuple('Outputs', ['dataset'])
    return outputs(output_path)


@dsl.component(packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0'])
def preprocess_data(
    input_data: str
) -> NamedTuple('Outputs', [('train_data', str), ('test_data', str)]):
    """数据预处理组件"""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from collections import namedtuple
    
    print("Preprocessing data...")
    
    # 读取数据
    df = pd.read_csv(input_data)
    
    # 分割特征和标签
    X = df.drop('target', axis=1)
    y = df['target']
    
    # 训练集和测试集分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 保存处理后的数据
    train_path = '/tmp/train_data.csv'
    test_path = '/tmp/test_data.csv'
    
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Train set: {len(train_df)} samples")
    print(f"Test set: {len(test_df)} samples")
    
    outputs = namedtuple('Outputs', ['train_data', 'test_data'])
    return outputs(train_path, test_path)


@dsl.component(packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0', 'joblib==1.3.0'])
def train_model(
    train_data: str,
    test_data: str
) -> NamedTuple('Outputs', [('model', str), ('metrics', dict)]):
    """模型训练组件"""
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    from collections import namedtuple
    
    print("Training model...")
    
    # 加载训练数据
    train_df = pd.read_csv(train_data)
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    
    # 训练模型
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 保存模型
    model_path = '/tmp/model.pkl'
    joblib.dump(model, model_path)
    
    # 计算训练集指标
    train_score = model.score(X_train, y_train)
    
    metrics = {
        'train_accuracy': float(train_score),
        'n_estimators': 100
    }
    
    print(f"Model trained with accuracy: {train_score:.4f}")
    
    outputs = namedtuple('Outputs', ['model', 'metrics'])
    return outputs(model_path, metrics)


@dsl.component(packages_to_install=['pandas==2.0.0', 'scikit-learn==1.3.0', 'joblib==1.3.0'])
def evaluate_model(
    model: str,
    test_data: str
) -> NamedTuple('Outputs', [('accuracy', float), ('report', dict)]):
    """模型评估组件"""
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score, classification_report
    from collections import namedtuple
    
    print("Evaluating model...")
    
    # 加载模型和测试数据
    model_obj = joblib.load(model)
    test_df = pd.read_csv(test_data)
    
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    
    # 预测
    y_pred = model_obj.predict(X_test)
    
    # 计算指标
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Classification Report:")
    print(classification_report(y_test, y_pred))
    
    outputs = namedtuple('Outputs', ['accuracy', 'report'])
    return outputs(float(accuracy), report)


@dsl.component
def deploy_model(model: str, model_name: str) -> str:
    """模型部署组件"""
    print(f"Deploying model: {model_name}")
    
    # 在实际应用中，这里会将模型部署到KServe或其他服务
    # 这里仅作演示
    deployment_status = f"Model {model_name} deployed successfully"
    
    print(deployment_status)
    return deployment_status


@dsl.pipeline(
    name='ml-training-pipeline',
    description='Complete ML workflow with data processing, training, evaluation and deployment'
)
def ml_training_pipeline(
    data_path: str = 's3://my-bucket/iris-data.csv',
    model_name: str = 'iris-classifier',
    accuracy_threshold: float = 0.85
):
    """
    完整的机器学习Pipeline
    
    Args:
        data_path: 数据路径
        model_name: 模型名称
        accuracy_threshold: 部署的最小准确率阈值
    """
    # 步骤1: 加载数据
    load_task = load_data(data_path=data_path)
    
    # 步骤2: 数据预处理
    preprocess_task = preprocess_data(
        input_data=load_task.outputs['dataset']
    )
    
    # 步骤3: 训练模型
    train_task = train_model(
        train_data=preprocess_task.outputs['train_data'],
        test_data=preprocess_task.outputs['test_data']
    )
    
    # 步骤4: 评估模型
    eval_task = evaluate_model(
        model=train_task.outputs['model'],
        test_data=preprocess_task.outputs['test_data']
    )
    
    # 条件部署: 只有准确率达标才部署
    with dsl.Condition(eval_task.outputs['accuracy'] >= accuracy_threshold):
        deploy_task = deploy_model(
            model=train_task.outputs['model'],
            model_name=model_name
        )
        deploy_task.set_display_name('Deploy Model (Conditional)')


if __name__ == '__main__':
    from kfp import compiler
    
    compiler.Compiler().compile(
        pipeline_func=ml_training_pipeline,
        package_path='ml_training_pipeline.yaml'
    )
    
    print("Pipeline compiled successfully!")
    print("Generated file: ml_training_pipeline.yaml")
