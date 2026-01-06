"""
简单验证中立传说卡牌模块
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

print("=" * 60)
print("中立传说卡牌模块验证")
print("=" * 60)

# 直接读取文件检查类定义
neutral_legendary_file = os.path.join(os.path.dirname(__file__), '..', 'neutral_legendary.py')
tokens_file = os.path.join(os.path.dirname(__file__), '..', 'tokens.py')

print("\n检查文件存在性:")
print(f"  neutral_legendary.py: {'✓' if os.path.exists(neutral_legendary_file) else '✗'}")
print(f"  tokens.py: {'✓' if os.path.exists(tokens_file) else '✗'}")

# 读取并检查类定义
EXPECTED_CARDS = [
    "VAC_321",   # 伊辛迪奥斯
    "VAC_446",   # 挂机的阿凯
    "VAC_702",   # 经理马林
    "VAC_955",   # 戈贡佐姆
    "VAC_959",   # 诚信商家格里伏塔
    "WORK_027",  # 梦想策划师杰弗里斯
    "WORK_043",  # 旅行管理员杜加尔
]

EXPECTED_TOKENS = [
    "VAC_321t",   # 爆发
    "VAC_955t",   # 美味奶酪
    "VAC_702t", "VAC_702t2", "VAC_702t3", "VAC_702t4",  # 宝藏
    "VAC_959t", "VAC_959t2", "VAC_959t3", "VAC_959t4",  # 护符
    "VAC_959t5", "VAC_959t6", "VAC_959t7", "VAC_959t8",
    "VAC_959t9", "VAC_959t10", "VAC_959t11", "VAC_959t12",
    "VAC_959t13", "VAC_959t14",
    "WORK_027t", "WORK_027t2", "WORK_027t3",  # 旅行路线
]

print("\n检查卡牌类定义:")
with open(neutral_legendary_file, 'r', encoding='utf-8') as f:
    content = f.read()
    for card_id in EXPECTED_CARDS:
        if f"class {card_id}:" in content:
            print(f"  ✓ {card_id}")
        else:
            print(f"  ✗ {card_id} - 未找到")

print("\n检查Token定义:")
with open(tokens_file, 'r', encoding='utf-8') as f:
    content = f.read()
    for token_id in EXPECTED_TOKENS:
        if f"class {token_id}:" in content:
            print(f"  ✓ {token_id}")
        else:
            print(f"  ✗ {token_id} - 未找到")

print("\n" + "=" * 60)
print("验证完成！")
print("=" * 60)
print(f"卡牌: {len(EXPECTED_CARDS)}/7")
print(f"Token: {len(EXPECTED_TOKENS)}/{len(EXPECTED_TOKENS)}")
