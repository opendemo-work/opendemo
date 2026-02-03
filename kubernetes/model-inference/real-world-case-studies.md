# 大模型推理实际应用案例研究

## 1. 电商智能客服系统

### 1.1 案例背景
某大型电商平台日均处理百万级客户咨询，传统规则引擎无法满足复杂语义理解和个性化服务需求。

### 1.2 技术方案

```python
# ecommerce_customer_service.py
import asyncio
import json
from typing import Dict, List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastapi import FastAPI, WebSocket, HTTPException
import redis
import logging

app = FastAPI(title="E-commerce Customer Service AI")

class EcommerceCustomerService:
    def __init__(self):
        # 加载多个专业模型
        self.intent_classifier = self._load_intent_model()
        self.sentiment_analyzer = self._load_sentiment_model()
        self.product_recommender = self._load_recommendation_model()
        
        # Redis缓存配置
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        # 会话管理
        self.session_store = {}
        
    def _load_intent_model(self):
        """加载意图识别模型"""
        model = AutoModelForSequenceClassification.from_pretrained(
            "bert-base-chinese-finetuned-ecommerce-intent"
        )
        tokenizer = AutoTokenizer.from_pretrained(
            "bert-base-chinese-finetuned-ecommerce-intent"
        )
        return {"model": model, "tokenizer": tokenizer}
    
    def _load_sentiment_model(self):
        """加载情感分析模型"""
        model = AutoModelForSequenceClassification.from_pretrained(
            "chinese-roberta-wwm-ext-sentiment"
        )
        tokenizer = AutoTokenizer.from_pretrained(
            "chinese-roberta-wwm-ext-sentiment"
        )
        return {"model": model, "tokenizer": tokenizer}
    
    def _load_recommendation_model(self):
        """加载商品推荐模型"""
        # 这里可以集成协同过滤或深度学习推荐模型
        return {"type": "hybrid-recommender"}
    
    async def process_customer_query(self, query: str, session_id: str) -> Dict:
        """处理客户查询"""
        # 1. 意图识别
        intent = await self._classify_intent(query)
        
        # 2. 情感分析
        sentiment = await self._analyze_sentiment(query)
        
        # 3. 实体提取
        entities = await self._extract_entities(query)
        
        # 4. 会话历史分析
        context = await self._get_session_context(session_id)
        
        # 5. 生成响应
        response = await self._generate_response(
            query, intent, sentiment, entities, context
        )
        
        # 6. 更新会话状态
        await self._update_session(session_id, query, response)
        
        return {
            "intent": intent,
            "sentiment": sentiment,
            "entities": entities,
            "response": response,
            "confidence": response.get("confidence", 0.0),
            "processing_time": response.get("processing_time", 0)
        }
    
    async def _classify_intent(self, query: str) -> Dict:
        """意图分类"""
        tokenizer = self.intent_classifier["tokenizer"]
        model = self.intent_classifier["model"]
        
        inputs = tokenizer(query, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class = torch.max(predictions, dim=-1)
        
        intents = ["product_inquiry", "order_tracking", "return_request", 
                  "payment_issue", "technical_support", "general_question"]
        
        return {
            "intent": intents[predicted_class.item()],
            "confidence": confidence.item(),
            "probabilities": {
                intent: prob.item() 
                for intent, prob in zip(intents, predictions[0])
            }
        }
    
    async def _analyze_sentiment(self, query: str) -> Dict:
        """情感分析"""
        tokenizer = self.sentiment_analyzer["tokenizer"]
        model = self.sentiment_analyzer["model"]
        
        inputs = tokenizer(query, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class = torch.max(predictions, dim=-1)
        
        sentiments = ["negative", "neutral", "positive"]
        
        return {
            "sentiment": sentiments[predicted_class.item()],
            "confidence": confidence.item(),
            "scores": {
                sentiment: score.item()
                for sentiment, score in zip(sentiments, predictions[0])
            }
        }
    
    async def _extract_entities(self, query: str) -> List[Dict]:
        """实体提取"""
        # 这里可以集成NER模型或规则引擎
        entities = []
        
        # 简单的关键词匹配示例
        product_keywords = ["手机", "电脑", "耳机", "衣服", "鞋子"]
        order_keywords = ["订单", "物流", "快递", "发货", "配送"]
        
        for keyword in product_keywords:
            if keyword in query:
                entities.append({
                    "type": "PRODUCT",
                    "value": keyword,
                    "start": query.find(keyword),
                    "end": query.find(keyword) + len(keyword)
                })
        
        for keyword in order_keywords:
            if keyword in query:
                entities.append({
                    "type": "ORDER",
                    "value": keyword,
                    "start": query.find(keyword),
                    "end": query.find(keyword) + len(keyword)
                })
        
        return entities
    
    async def _get_session_context(self, session_id: str) -> Dict:
        """获取会话上下文"""
        # 从Redis获取会话历史
        session_key = f"session:{session_id}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            return json.loads(session_data)
        return {"history": [], "user_profile": {}}
    
    async def _generate_response(self, query: str, intent: Dict, sentiment: Dict, 
                               entities: List, context: Dict) -> Dict:
        """生成智能响应"""
        start_time = asyncio.get_event_loop().time()
        
        # 根据意图和情感生成不同类型的响应
        response_templates = {
            "product_inquiry": {
                "positive": "很高兴为您介绍我们的产品！",
                "neutral": "关于这个问题，我可以为您提供详细信息。",
                "negative": "很抱歉给您带来困扰，让我帮您解决问题。"
            },
            "order_tracking": {
                "positive": "您的订单状态良好，请稍等我查询详情。",
                "neutral": "正在为您查询订单信息...",
                "negative": "我理解您的担心，立即为您处理订单问题。"
            }
        }
        
        # 选择合适的模板
        intent_type = intent["intent"]
        sentiment_type = sentiment["sentiment"]
        
        base_response = response_templates.get(intent_type, {}).get(
            sentiment_type, "我会尽力帮助您解决这个问题。"
        )
        
        # 添加个性化元素
        personalized_response = await self._personalize_response(
            base_response, context, entities
        )
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return {
            "text": personalized_response,
            "confidence": 0.85,  # 可以基于多个因素计算
            "processing_time": processing_time,
            "suggested_actions": await self._suggest_next_actions(intent, entities)
        }
    
    async def _personalize_response(self, base_response: str, context: Dict, 
                                  entities: List) -> str:
        """个性化响应生成"""
        # 基于用户历史和上下文个性化响应
        user_profile = context.get("user_profile", {})
        history = context.get("history", [])
        
        # 添加用户称呼
        if "name" in user_profile:
            base_response = f"{user_profile['name']}{base_response}"
        
        # 根据历史交互调整语气
        if len(history) > 5:
            base_response += " 感谢您一直以来的支持！"
        
        return base_response
    
    async def _suggest_next_actions(self, intent: Dict, entities: List) -> List[str]:
        """建议下一步行动"""
        suggestions = []
        intent_type = intent["intent"]
        
        if intent_type == "product_inquiry":
            suggestions.extend(["查看商品详情", "比较同类产品", "加入购物车"])
        elif intent_type == "order_tracking":
            suggestions.extend(["查看物流详情", "联系客服", "申请售后服务"])
        
        return suggestions
    
    async def _update_session(self, session_id: str, query: str, response: Dict):
        """更新会话状态"""
        session_key = f"session:{session_id}"
        
        # 获取现有会话数据
        session_data = self.redis_client.get(session_key)
        if session_data:
            session_context = json.loads(session_data)
        else:
            session_context = {"history": [], "user_profile": {}, "interaction_count": 0}
        
        # 更新历史记录
        session_context["history"].append({
            "query": query,
            "response": response["text"],
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # 限制历史记录长度
        if len(session_context["history"]) > 10:
            session_context["history"] = session_context["history"][-10:]
        
        # 更新交互计数
        session_context["interaction_count"] += 1
        
        # 保存到Redis（设置过期时间24小时）
        self.redis_client.setex(
            session_key, 
            86400,  # 24小时
            json.dumps(session_context)
        )

# API端点
@app.post("/customer-service/chat")
async def customer_service_chat(request: Dict):
    """客户服务聊天接口"""
    try:
        query = request.get("query", "")
        session_id = request.get("session_id", "default")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # 处理查询
        result = await service.process_customer_query(query, session_id)
        
        return {
            "session_id": session_id,
            "query": query,
            "result": result
        }
        
    except Exception as e:
        logging.error(f"Error processing customer query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.websocket("/customer-service/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket实时客服"""
    await websocket.accept()
    session_id = f"ws_{int(asyncio.get_event_loop().time())}"
    
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            
            query = request.get("query", "")
            if query:
                result = await service.process_customer_query(query, session_id)
                await websocket.send_text(json.dumps(result))
                
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        await websocket.close()

# 初始化服务
service = EcommerceCustomerService()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 1.3 部署架构

```yaml
# ecommerce-customer-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-customer-service
  namespace: ai-services
spec:
  replicas: 6
  selector:
    matchLabels:
      app: customer-service
  template:
    metadata:
      labels:
        app: customer-service
    spec:
      containers:
      - name: customer-service
        image: your-registry/ecommerce-customer-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: REDIS_HOST
          value: "redis-master.ai-services.svc.cluster.local"
        - name: MODEL_CACHE_SIZE
          value: "2GB"
        - name: MAX_CONCURRENT_SESSIONS
          value: "1000"
        resources:
          requests:
            cpu: "2"
            memory: "8Gi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "4"
            memory: "16Gi"
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: model-cache
          mountPath: /models
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 120
          periodSeconds: 30
      volumes:
      - name: model-cache
        persistentVolumeClaim:
          claimName: model-cache-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: customer-service
  namespace: ai-services
spec:
  selector:
    app: customer-service
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: customer-service-hpa
  namespace: ai-services
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ecommerce-customer-service
  minReplicas: 3
  maxReplicas: 12
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: active_sessions
      target:
        type: AverageValue
        averageValue: "500"
```

## 2. 金融风险评估系统

### 2.1 案例背景
银行需要实时评估贷款申请人的信用风险，传统评分卡模型无法处理复杂的非结构化数据。

### 2.2 技术实现

```python
# financial_risk_assessment.py
import asyncio
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import logging

class FinancialRiskAssessment:
    def __init__(self):
        # 加载预训练模型
        self.text_encoder = self._load_text_encoder()
        self.risk_model = self._load_risk_model()
        self.scaler = self._load_scaler()
        
        # 风险类别定义
        self.risk_levels = ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
        
    def _load_text_encoder(self):
        """加载文本编码器"""
        model = AutoModel.from_pretrained("bert-base-chinese")
        tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
        return {"model": model, "tokenizer": tokenizer}
    
    def _load_risk_model(self):
        """加载风险评估模型"""
        return joblib.load("models/financial_risk_model.pkl")
    
    def _load_scaler(self):
        """加载特征缩放器"""
        return joblib.load("models/feature_scaler.pkl")
    
    async def assess_credit_risk(self, applicant_data: Dict) -> Dict:
        """评估信贷风险"""
        try:
            # 1. 数据预处理
            processed_features = await self._preprocess_applicant_data(applicant_data)
            
            # 2. 特征工程
            engineered_features = await self._engineer_features(processed_features)
            
            # 3. 风险预测
            risk_prediction = await self._predict_risk(engineered_features)
            
            # 4. 生成解释
            explanation = await self._generate_explanation(risk_prediction, engineered_features)
            
            return {
                "risk_level": risk_prediction["risk_level"],
                "risk_score": risk_prediction["risk_score"],
                "confidence": risk_prediction["confidence"],
                "key_factors": explanation["key_factors"],
                "recommendations": explanation["recommendations"],
                "processing_time": risk_prediction["processing_time"]
            }
            
        except Exception as e:
            logging.error(f"Risk assessment error: {e}")
            return {
                "risk_level": "ERROR",
                "risk_score": 0.0,
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def _preprocess_applicant_data(self, data: Dict) -> Dict:
        """预处理申请人数据"""
        processed = {}
        
        # 处理结构化数据
        structured_fields = [
            "age", "income", "employment_years", "debt_ratio", 
            "credit_history_months", "num_credit_cards"
        ]
        
        for field in structured_fields:
            if field in data:
                processed[field] = float(data[field]) if data[field] else 0.0
        
        # 处理文本数据
        text_fields = ["employment_description", "loan_purpose", "additional_info"]
        
        for field in text_fields:
            if field in data and data[field]:
                processed[field] = await self._encode_text(data[field])
            else:
                processed[field] = np.zeros(768)  # BERT embedding dimension
        
        return processed
    
    async def _encode_text(self, text: str) -> np.ndarray:
        """文本编码"""
        tokenizer = self.text_encoder["tokenizer"]
        model = self.text_encoder["model"]
        
        # 编码文本
        inputs = tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512,
            padding=True
        )
        
        # 获取BERT embeddings
        with torch.no_grad():
            outputs = model(**inputs)
            # 使用[CLS] token的表示
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        
        return embeddings.flatten()
    
    async def _engineer_features(self, processed_data: Dict) -> np.ndarray:
        """特征工程"""
        features = []
        
        # 基础特征
        features.extend([
            processed_data.get("age", 0),
            processed_data.get("income", 0),
            processed_data.get("employment_years", 0),
            processed_data.get("debt_ratio", 0),
            processed_data.get("credit_history_months", 0),
            processed_data.get("num_credit_cards", 0)
        ])
        
        # 文本特征（已编码）
        for field in ["employment_description", "loan_purpose", "additional_info"]:
            features.extend(processed_data.get(field, np.zeros(768)))
        
        # 派生特征
        income_age_ratio = processed_data.get("income", 0) / (processed_data.get("age", 1) + 1)
        debt_income_ratio = processed_data.get("debt_ratio", 0) * processed_data.get("income", 0)
        
        features.extend([income_age_ratio, debt_income_ratio])
        
        return np.array(features).reshape(1, -1)
    
    async def _predict_risk(self, features: np.ndarray) -> Dict:
        """风险预测"""
        start_time = asyncio.get_event_loop().time()
        
        # 特征缩放
        scaled_features = self.scaler.transform(features)
        
        # 预测概率
        probabilities = self.risk_model.predict_proba(scaled_features)[0]
        predicted_class = self.risk_model.predict(scaled_features)[0]
        
        # 计算风险分数 (0-100)
        risk_score = probabilities[1] * 100  # 假设1是高风险类
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return {
            "risk_level": self.risk_levels[predicted_class],
            "risk_score": float(risk_score),
            "confidence": float(np.max(probabilities)),
            "probabilities": {
                level: float(prob) 
                for level, prob in zip(self.risk_levels, probabilities)
            },
            "processing_time": processing_time
        }
    
    async def _generate_explanation(self, prediction: Dict, features: np.ndarray) -> Dict:
        """生成风险解释"""
        key_factors = []
        recommendations = []
        
        # 基于特征重要性生成解释
        feature_names = [
            "年龄", "收入", "工作年限", "负债比率", "信用历史", "信用卡数量",
            "工作描述相关性", "贷款用途相关性", "附加信息相关性",
            "收入年龄比", "负债收入比"
        ]
        
        # 简化的特征重要性分析
        feature_importance = np.abs(features.flatten()[:len(feature_names)])
        top_features_idx = np.argsort(feature_importance)[-3:][::-1]
        
        for idx in top_features_idx:
            if idx < len(feature_names):
                key_factors.append({
                    "factor": feature_names[idx],
                    "importance": float(feature_importance[idx])
                })
        
        # 基于风险等级生成建议
        risk_level = prediction["risk_level"]
        if risk_level == "LOW":
            recommendations = [
                "建议批准贷款申请",
                "可考虑提高授信额度",
                "推荐优质客户专属产品"
            ]
        elif risk_level == "MEDIUM":
            recommendations = [
                "需要进一步审核",
                "建议要求提供更多担保",
                "可考虑分期放款"
            ]
        elif risk_level == "HIGH":
            recommendations = [
                "建议拒绝贷款申请",
                "如需放款需严格条件",
                "建议加强贷后监控"
            ]
        else:  # VERY_HIGH
            recommendations = [
                "强烈建议拒绝申请",
                "列入高风险客户名单",
                "建议进行深度尽职调查"
            ]
        
        return {
            "key_factors": key_factors,
            "recommendations": recommendations
        }

# 批量处理服务
class BatchRiskProcessor:
    def __init__(self, risk_assessor: FinancialRiskAssessment):
        self.risk_assessor = risk_assessor
        self.batch_queue = asyncio.Queue()
        self.results = {}
        
    async def submit_batch(self, applicants: List[Dict]) -> str:
        """提交批量处理任务"""
        batch_id = f"batch_{int(asyncio.get_event_loop().time())}"
        
        # 将申请加入队列
        await self.batch_queue.put({
            "batch_id": batch_id,
            "applicants": applicants,
            "submitted_at": asyncio.get_event_loop().time()
        })
        
        return batch_id
    
    async def process_batches(self):
        """处理批量任务"""
        while True:
            try:
                batch_task = await self.batch_queue.get()
                batch_id = batch_task["batch_id"]
                applicants = batch_task["applicants"]
                
                # 并行处理所有申请
                tasks = [
                    self.risk_assessor.assess_credit_risk(applicant)
                    for applicant in applicants
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 存储结果
                self.results[batch_id] = {
                    "results": results,
                    "completed_at": asyncio.get_event_loop().time(),
                    "total_processed": len(applicants)
                }
                
            except Exception as e:
                logging.error(f"Batch processing error: {e}")

# API服务
from fastapi import FastAPI, BackgroundTasks
import uuid

app = FastAPI(title="Financial Risk Assessment Service")

risk_assessor = FinancialRiskAssessment()
batch_processor = BatchRiskProcessor(risk_assessor)

@app.post("/risk-assessment/single")
async def single_risk_assessment(applicant_data: Dict):
    """单个风险评估"""
    result = await risk_assessor.assess_credit_risk(applicant_data)
    return {"assessment_id": str(uuid.uuid4()), "result": result}

@app.post("/risk-assessment/batch")
async def batch_risk_assessment(background_tasks: BackgroundTasks, applicants: List[Dict]):
    """批量风险评估"""
    batch_id = await batch_processor.submit_batch(applicants)
    background_tasks.add_task(batch_processor.process_batches)
    return {"batch_id": batch_id, "status": "submitted"}

@app.get("/risk-assessment/batch/{batch_id}")
async def get_batch_result(batch_id: str):
    """获取批量处理结果"""
    if batch_id in batch_processor.results:
        return batch_processor.results[batch_id]
    else:
        return {"status": "processing", "message": "Batch is still being processed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

## 3. 医疗辅助诊断系统

### 3.1 案例背景
医院需要辅助医生进行疾病诊断，特别是罕见病的早期识别和诊断建议。

### 3.2 技术架构

```python
# medical_diagnosis_assistant.py
import asyncio
import json
from typing import Dict, List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

class MedicalDiagnosisAssistant:
    def __init__(self):
        # 加载医学模型
        self.symptom_analyzer = self._load_symptom_model()
        self.disease_classifier = self._load_disease_model()
        self.medical_knowledge_base = self._load_knowledge_base()
        
        # 知识图谱搜索
        self.knowledge_index = self._build_knowledge_index()
        
    def _load_symptom_model(self):
        """加载症状分析模型"""
        model = AutoModelForSequenceClassification.from_pretrained(
            "medical-bert-symptom-analysis"
        )
        tokenizer = AutoTokenizer.from_pretrained("medical-bert-symptom-analysis")
        return {"model": model, "tokenizer": tokenizer}
    
    def _load_disease_model(self):
        """加载疾病分类模型"""
        model = AutoModelForSequenceClassification.from_pretrained(
            "clinical-bert-disease-classification"
        )
        tokenizer = AutoTokenizer.from_pretrained("clinical-bert-disease-classification")
        return {"model": model, "tokenizer": tokenizer}
    
    def _load_knowledge_base(self):
        """加载医学知识库"""
        # 这里加载医学文献、病例数据库等
        return {"diseases": {}, "symptoms": {}, "treatments": {}}
    
    def _build_knowledge_index(self):
        """构建知识检索索引"""
        # 使用FAISS构建向量索引
        dimension = 768  # BERT embedding dimension
        index = faiss.IndexFlatIP(dimension)  # 内积相似度
        return index
    
    async def diagnose_patient(self, patient_data: Dict) -> Dict:
        """患者诊断"""
        try:
            # 1. 症状分析
            symptoms_analysis = await self._analyze_symptoms(patient_data)
            
            # 2. 疾病预测
            disease_predictions = await self._predict_diseases(symptoms_analysis)
            
            # 3. 知识检索
            relevant_knowledge = await self._retrieve_medical_knowledge(
                symptoms_analysis, disease_predictions
            )
            
            # 4. 生成诊断建议
            diagnosis_report = await self._generate_diagnosis_report(
                symptoms_analysis, disease_predictions, relevant_knowledge
            )
            
            return diagnosis_report
            
        except Exception as e:
            logging.error(f"Diagnosis error: {e}")
            return {"error": str(e)}
    
    async def _analyze_symptoms(self, patient_data: Dict) -> Dict:
        """症状分析"""
        symptoms_text = patient_data.get("symptoms_description", "")
        
        if not symptoms_text:
            return {"symptoms": [], "severity_scores": {}}
        
        tokenizer = self.symptom_analyzer["tokenizer"]
        model = self.symptom_analyzer["model"]
        
        # 文本编码
        inputs = tokenizer(
            symptoms_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # 症状识别
        with torch.no_grad():
            outputs = model(**inputs)
            symptom_probs = torch.sigmoid(outputs.logits).squeeze()
        
        # 症状列表和严重程度
        symptom_categories = [
            "fever", "cough", "headache", "fatigue", "nausea",
            "chest_pain", "shortness_of_breath", "joint_pain"
        ]
        
        identified_symptoms = []
        severity_scores = {}
        
        for i, symptom in enumerate(symptom_categories):
            if symptom_probs[i] > 0.5:  # 阈值可调整
                identified_symptoms.append(symptom)
                severity_scores[symptom] = float(symptom_probs[i])
        
        return {
            "identified_symptoms": identified_symptoms,
            "severity_scores": severity_scores,
            "symptom_text": symptoms_text
        }
    
    async def _predict_diseases(self, symptoms_analysis: Dict) -> List[Dict]:
        """疾病预测"""
        if not symptoms_analysis["identified_symptoms"]:
            return []
        
        # 构造输入文本
        symptom_text = ", ".join(symptoms_analysis["identified_symptoms"])
        
        tokenizer = self.disease_classifier["tokenizer"]
        model = self.disease_classifier["model"]
        
        inputs = tokenizer(
            symptom_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        with torch.no_grad():
            outputs = model(**inputs)
            disease_probs = torch.softmax(outputs.logits, dim=-1).squeeze()
        
        # 疾病类别（示例）
        disease_categories = [
            "common_cold", "flu", "pneumonia", "migraine", 
            "hypertension", "diabetes", "anxiety_disorder"
        ]
        
        predictions = []
        for i, disease in enumerate(disease_categories):
            probability = float(disease_probs[i])
            if probability > 0.1:  # 最低阈值
                predictions.append({
                    "disease": disease,
                    "probability": probability,
                    "confidence": probability
                })
        
        # 按概率排序
        predictions.sort(key=lambda x: x["probability"], reverse=True)
        
        return predictions[:5]  # 返回前5个最可能的疾病
    
    async def _retrieve_medical_knowledge(self, symptoms_analysis: Dict, 
                                        disease_predictions: List[Dict]) -> Dict:
        """检索相关医学知识"""
        # 构造查询向量
        query_text = symptoms_analysis["symptom_text"]
        
        # 使用Sentence-BERT编码查询
        encoder = SentenceTransformer('all-MiniLM-L6-v2')
        query_vector = encoder.encode([query_text])
        
        # 搜索相似的医学文献
        k = 10  # 返回前10个最相关的文档
        similarities, indices = self.knowledge_index.search(query_vector, k)
        
        # 获取相关文献内容
        relevant_documents = []
        for i, (sim, idx) in enumerate(zip(similarities[0], indices[0])):
            if sim > 0.7:  # 相似度阈值
                # 这里应该从实际的知识库中获取文档
                relevant_documents.append({
                    "document_id": int(idx),
                    "similarity": float(sim),
                    "title": f"Medical Document {idx}",
                    "content": "Sample medical content..."
                })
        
        return {
            "relevant_documents": relevant_documents,
            "total_found": len(relevant_documents)
        }
    
    async def _generate_diagnosis_report(self, symptoms_analysis: Dict,
                                       disease_predictions: List[Dict],
                                       knowledge: Dict) -> Dict:
        """生成诊断报告"""
        # 综合分析结果
        primary_disease = disease_predictions[0] if disease_predictions else None
        
        report = {
            "primary_diagnosis": primary_disease["disease"] if primary_disease else "Unknown",
            "confidence_level": primary_disease["confidence"] if primary_disease else 0.0,
            "differential_diagnoses": disease_predictions[1:] if len(disease_predictions) > 1 else [],
            "key_symptoms": symptoms_analysis["identified_symptoms"],
            "symptom_severity": symptoms_analysis["severity_scores"],
            "recommended_tests": await self._suggest_medical_tests(disease_predictions),
            "treatment_options": await self._suggest_treatments(primary_disease),
            "references": knowledge["relevant_documents"],
            "urgent_attention_required": await self._assess_urgency(symptoms_analysis)
        }
        
        return report
    
    async def _suggest_medical_tests(self, diseases: List[Dict]) -> List[str]:
        """建议医学检查"""
        suggested_tests = set()
        
        for disease in diseases:
            disease_name = disease["disease"]
            # 基于疾病类型建议相应检查
            if "pneumonia" in disease_name:
                suggested_tests.update(["胸部X光", "血常规", "痰培养"])
            elif "hypertension" in disease_name:
                suggested_tests.update(["血压监测", "心电图", "肾功能检查"])
            elif "diabetes" in disease_name:
                suggested_tests.update(["血糖检测", "糖化血红蛋白", "胰岛素水平"])
        
        return list(suggested_tests)
    
    async def _suggest_treatments(self, primary_disease: Optional[Dict]) -> List[str]:
        """建议治疗方案"""
        if not primary_disease:
            return ["建议进一步检查确诊"]
        
        disease_name = primary_disease["disease"]
        treatments = []
        
        if "cold" in disease_name or "flu" in disease_name:
            treatments = ["休息充足", "多饮水", "对症治疗", "必要时抗病毒药物"]
        elif "hypertension" in disease_name:
            treatments = ["降压药物", "饮食控制", "规律运动", "定期监测"]
        elif "diabetes" in disease_name:
            treatments = ["血糖控制", "胰岛素治疗", "饮食管理", "并发症预防"]
        
        return treatments
    
    async def _assess_urgency(self, symptoms_analysis: Dict) -> bool:
        """评估紧急程度"""
        urgent_symptoms = ["chest_pain", "shortness_of_breath", "severe_headache"]
        severe_symptoms = [symptom for symptom, severity in 
                          symptoms_analysis["severity_scores"].items() 
                          if severity > 0.8]
        
        return any(symptom in urgent_symptoms for symptom in severe_symptoms)

# API端点
from fastapi import FastAPI

app = FastAPI(title="Medical Diagnosis Assistant")

diagnosis_assistant = MedicalDiagnosisAssistant()

@app.post("/diagnosis/patient")
async def patient_diagnosis(patient_data: Dict):
    """患者诊断接口"""
    result = await diagnosis_assistant.diagnose_patient(patient_data)
    return {"diagnosis_id": str(hash(str(patient_data))), "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

这三个实际应用案例展示了大模型推理在电商客服、金融风控和医疗诊断等核心业务场景中的具体实现，体现了从技术架构到业务价值的完整转化路径。