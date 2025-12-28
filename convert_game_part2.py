"""
转换 game.py 剩余的日志 - 第2部分
"""
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = r"D:\Projects\Yolo\fireplace\fireplace\game.py"

print("读取 game.py...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换剩余的日志
replacements = [
    (r'self\.log\("Entering mulligan phase"\)',
     'self.log(translate("entering_mulligan"))'),

    (r'self\.log\("%s gets The Coin \(%s\)", self\.player2, THE_COIN\)',
     'self.log(translate("player_gets_coin", player=self.player2))'),
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
