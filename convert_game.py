"""
转换 game.py 的日志
"""
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = r"D:\Projects\Yolo\fireplace\fireplace\game.py"

print("读取 game.py...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否需要添加导入
if 'from .i18n import _' not in content:
    # 在文件开头添加导入
    lines = content.split('\n')
    # 找到第一个 import 语句的位置
    for i, line in enumerate(lines):
        if line.startswith('from') or line.startswith('import'):
            lines.insert(i, 'from .i18n import _ as translate')
            break
    content = '\n'.join(lines)
    print("[OK] 添加 i18n 导入")

# 替换 self.log 调用
replacements = [
    (r'self\.log\("Setting up game %r", self\)',
     'self.log(translate("setting_up_game", game=self))'),

    (r'self\.log\("Tossing the coin\.\.\. %s wins!", winner\)',
     'self.log(translate("tossing_coin", winner=winner))'),

    (r'self\.log\("Empty stack, refreshing auras and processing deaths"\)',
     'self.log(translate("empty_stack"))'),
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
