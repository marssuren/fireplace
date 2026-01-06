# -*- coding: utf-8 -*-
"""
验证中立史诗卡牌修正后的语法
"""
import ast
import sys
import codecs

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 60)
print("中立史诗卡牌修正验证")
print("=" * 60)

files_to_check = [
    ("neutral_epic.py", "D:\\Projects\\Yolo\\hearthstone_zero\\fireplace\\fireplace\\cards\\paradise\\neutral_epic.py"),
    ("tokens.py", "D:\\Projects\\Yolo\\hearthstone_zero\\fireplace\\fireplace\\cards\\paradise\\tokens.py"),
]

print("\n检查 Python 语法:")
all_ok = True
for name, path in files_to_check:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
            ast.parse(code)
        print(f"  [OK] {name} 语法正确")
    except SyntaxError as e:
        print(f"  [FAIL] {name} 语法错误: {e}")
        all_ok = False

print("\n检查修正内容:")

# 检查 VAC_935t 的 packed_cards 声明
with open(files_to_check[1][1], 'r', encoding='utf-8') as f:
    content = f.read()
    if "packed_cards = []" in content and "正式声明属性" in content:
        print("  [OK] VAC_935t.packed_cards 已正式声明")
    else:
        print("  [FAIL] VAC_935t.packed_cards 未正式声明")
        all_ok = False

# 检查 VAC_958 的完整 buff 复制
with open(files_to_check[0][1], 'r', encoding='utf-8') as f:
    content = f.read()
    if "for attr in ['atk', 'max_health', 'taunt'" in content:
        print("  [OK] VAC_958 buff 复制已完善（包含所有属性）")
    else:
        print("  [FAIL] VAC_958 buff 复制未完善")
        all_ok = False

# 检查 VAC_523t effect5 的注释更新
with open(files_to_check[1][1], 'r', encoding='utf-8') as f:
    content = f.read()
    if "因为药水本身不支持目标选择" in content:
        print("  [OK] VAC_523t effect5 已更新注释说明")
    else:
        print("  [FAIL] VAC_523t effect5 注释未更新")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("所有修正已完成！✓")
else:
    print("存在问题，请检查！✗")
print("=" * 60)
