"""
转换其他模块的日志 - cards/__init__.py
"""
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = r"D:\Projects\Yolo\fireplace\fireplace\cards\__init__.py"

print("读取 cards/__init__.py...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否需要添加导入
if 'from ..logging import log_info' not in content:
    # 添加 log_info 导入
    content = content.replace(
        'from ..logging import log',
        'from ..logging import log, log_info'
    )
    print("[OK] 添加 log_info 导入")

# 替换日志调用
replacements = [
    (r'log\.info\("Initializing card database"\)',
     'log_info("initializing_card_database")'),
    (r'log\.info\("Merged %i cards", len\(self\)\)',
     'log_info("merged_cards", count=len(self))'),
]

total = 0
for pattern, replacement in replacements:
    count = len(re.findall(pattern, content))
    if count > 0:
        content = re.sub(pattern, replacement, content)
        total += count
        print(f"[OK] 替换 {count} 处")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"完成! 共 {total} 处")
