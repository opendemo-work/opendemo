#!/usr/bin/env python3
"""
批量修复 opendemo 导入路径的脚本
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """修复单个文件中的导入路径"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经修复过
        if '# 修复导入路径' in content:
            print(f"跳过已修复的文件: {file_path}")
            return False
            
        # 替换导入语句
        pattern = r'(from\s+)opendemo\.(\w+(?:\.\w+)*)'
        replacement = r'\1\2'
        
        if re.search(pattern, content):
            # 在文件开头添加路径修复代码
            path_fix = '''# 修复导入路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

'''
            
            # 找到第一个导入语句的位置
            import_match = re.search(r'^import\s+\w+|^from\s+\w+', content, re.MULTILINE)
            if import_match:
                insert_pos = import_match.start()
                # 插入路径修复代码
                content = content[:insert_pos] + path_fix + content[insert_pos:]
                
                # 替换所有的 opendemo. 导入
                content = re.sub(pattern, replacement, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"已修复: {file_path}")
                return True
        
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    root_dir = Path(__file__).parent
    fixed_count = 0
    
    # 需要修复的文件模式
    patterns = [
        "core/*.py",
        "services/*.py", 
        "scripts/*/*.py"
    ]
    
    for pattern in patterns:
        for file_path in root_dir.glob(pattern):
            if file_path.is_file() and file_path.suffix == '.py':
                if fix_imports_in_file(file_path):
                    fixed_count += 1
    
    print(f"\n总共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()