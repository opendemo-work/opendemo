#!/usr/bin/env python3
"""批量生成K8s案例metadata.json文件"""

import os
import json

def generate_metadata(dir_name):
    """生成metadata.json文件"""
    # 根据目录名推断信息
    name = dir_name.replace('-', ' ').title()
    
    # 推断难度
    if 'advanced' in dir_name or 'security' in dir_name:
        difficulty = 'advanced'
    elif 'basic' in dir_name or 'fundamentals' in dir_name:
        difficulty = 'beginner'
    else:
        difficulty = 'intermediate'
    
    # 推断技术栈
    tech_stack = ['Kubernetes']
    if 'istio' in dir_name:
        tech_stack.append('Istio')
    if 'helm' in dir_name:
        tech_stack.append('Helm')
    if 'argo' in dir_name:
        tech_stack.append('ArgoCD')
    if 'monitoring' in dir_name or 'prometheus' in dir_name:
        tech_stack.append('Prometheus')
    if 'cicd' in dir_name or 'ci-cd' in dir_name:
        tech_stack.append('CI/CD')
    
    metadata = {
        "name": name,
        "category": "kubernetes",
        "tech_stack": tech_stack,
        "description": f"Kubernetes {name} demonstration and best practices",
        "difficulty": difficulty,
        "dependencies": ["kubectl"]
    }
    
    metadata_path = os.path.join(dir_name, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"✅ 创建 {metadata_path}")

def main():
    """主函数"""
    count = 0
    
    # 获取所有目录
    for item in os.listdir('.'):
        if os.path.isdir(item) and item not in ['cli', '.git']:
            metadata_path = os.path.join(item, "metadata.json")
            if not os.path.exists(metadata_path):
                try:
                    generate_metadata(item)
                    count += 1
                except Exception as e:
                    print(f"❌ 错误 {item}: {e}")
    
    print(f"\n🎉 共生成 {count} 个metadata.json文件")

if __name__ == '__main__':
    main()
