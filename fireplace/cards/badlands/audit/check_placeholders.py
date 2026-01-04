# -*- coding: utf-8 -*-
"""
决战荒芜之地 - 占位符检查工具
检查所有卡牌类中是否还有未实现的 pass 语句
"""
import os
import re
import sys
from pathlib import Path

def main():
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    script_dir = Path(__file__).parent
    target_dir = script_dir.parent
    
    # 扫描所有 Python 文件
    py_files = [f for f in target_dir.glob('*.py') if f.name != '__init__.py']
    
    print("=" * 60)
    print("决战荒芜之地 - 占位符检查")
    print("=" * 60)
    print(f"扫描目录: {target_dir.name}\n")
    
    # 用于匹配类定义和 pass 语句
    class_pattern = re.compile(r'class\s+([A-Z0-9_]+).*?:', re.MULTILINE)
    
    issues_found = []
    total_classes = 0
    
    for py_file in sorted(py_files):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # 找到所有类定义
        classes = class_pattern.finditer(content)
        
        for match in classes:
            class_name = match.group(1)
            start_line = content[:match.start()].count('\n') + 1
            total_classes += 1
            
            # 检查类体中是否只有 pass（简单启发式）
            # 找到类定义后的缩进块
            class_start = match.end()
            
            # 简单检查：如果类定义后紧跟 pass，认为是占位符
            next_lines = content[class_start:class_start+200].strip()
            if next_lines.startswith('pass') or '\n    pass\n' in next_lines[:50]:
                issues_found.append({
                    'file': py_file.name,
                    'class': class_name,
                    'line': start_line
                })
    
    # 输出报告
    if issues_found:
        print(f"[⚠️  发现 {len(issues_found)} 个占位符类]\n")
        
        current_file = None
        for issue in sorted(issues_found, key=lambda x: (x['file'], x['line'])):
            if issue['file'] != current_file:
                print(f"\n📄 {issue['file']}:")
                current_file = issue['file']
            print(f"   第 {issue['line']:3d} 行: class {issue['class']}")
    else:
        print("[✅ 完美] 未发现占位符类！")
    
    print(f"\n总计扫描: {total_classes} 个类定义")
    print(f"占位符率: {len(issues_found)}/{total_classes} ({len(issues_found)/total_classes*100:.1f}%)")

if __name__ == '__main__':
    main()
