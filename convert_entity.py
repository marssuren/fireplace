"""
转换 entity.py 的常见日志
"""
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = r"D:\Projects\Yolo\fireplace\fireplace\entity.py"

print("读取 entity.py...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 添加导入
if 'from .i18n import _' not in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('from') or line.startswith('import'):
            lines.insert(i, 'from .i18n import _ as translate')
            break
    content = '\n'.join(lines)
    print("[OK] 添加 i18n 导入")

# 替换常见的日志
replacements = [
    (r'self\.log\("Empty stack, refreshing auras and processing deaths"\)',
     'self.log(translate("empty_stack"))'),

    (r'self\.log\("%s shuffles their deck", self\)',
     'self.log(translate("player_shuffles_deck", player=self))'),

    (r'self\.log\("Entering mulligan phase"\)',
     'self.log(translate("entering_mulligan"))'),
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
