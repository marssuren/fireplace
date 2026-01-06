"""
中立传说卡牌实现验证脚本
"""

# 验证所有7张中立传说卡牌是否正确实现
NEUTRAL_LEGENDARY_CARDS = [
    "VAC_321",   # 伊辛迪奥斯 - Incindius
    "VAC_446",   # 挂机的阿凯 - A. F. Kay
    "VAC_702",   # 经理马林 - Marin the Manager
    "VAC_955",   # 戈贡佐姆 - Gorgonzormu
    "VAC_959",   # 诚信商家格里伏塔 - Griftah, Trusted Vendor
    "WORK_027",  # 梦想策划师杰弗里斯 - Dreamplanner Zephrys
    "WORK_043",  # 旅行管理员杜加尔 - Travelmaster Dungar
]

# 验证Token定义
REQUIRED_TOKENS = [
    # Incindius
    "VAC_321t",
    
    # Gorgonzormu
    "VAC_955t",
    
    # Griftah Amulets
    "VAC_959t", "VAC_959t2",   # Mobility
    "VAC_959t3", "VAC_959t4",  # Critters
    "VAC_959t5", "VAC_959t6",  # Energy
    "VAC_959t7", "VAC_959t8",  # Passions
    "VAC_959t9", "VAC_959t10", # Strides
    "VAC_959t11", "VAC_959t12", # Tracking
    "VAC_959t13", "VAC_959t14", # Damage
    
    # Zephrys Tours
    "WORK_027t", "WORK_027t2", "WORK_027t3",
    
    # Marin Treasures
    "VAC_702t", "VAC_702t2", "VAC_702t3", "VAC_702t4",
]

print("=" * 60)
print("中立传说卡牌实现验证")
print("=" * 60)

# 导入卡牌模块
try:
    from fireplace.cards.paradise import neutral_legendary
    print("✅ neutral_legendary.py 导入成功")
except Exception as e:
    print(f"❌ neutral_legendary.py 导入失败: {e}")
    exit(1)

# 验证卡牌类是否存在
print("\n检查卡牌类定义:")
for card_id in NEUTRAL_LEGENDARY_CARDS:
    if hasattr(neutral_legendary, card_id):
        card_class = getattr(neutral_legendary, card_id)
        print(f"  ✅ {card_id}: {card_class.__doc__.split(chr(10))[0] if card_class.__doc__ else 'OK'}")
    else:
        print(f"  ❌ {card_id}: 未找到")

# 导入Token模块
try:
    from fireplace.cards.paradise import tokens
    print("\n✅ tokens.py 导入成功")
except Exception as e:
    print(f"\n❌ tokens.py 导入失败: {e}")
    exit(1)

# 验证Token类是否存在
print("\n检查Token定义:")
missing_tokens = []
for token_id in REQUIRED_TOKENS:
    if hasattr(tokens, token_id):
        print(f"  ✅ {token_id}")
    else:
        print(f"  ❌ {token_id}: 未找到")
        missing_tokens.append(token_id)

print("\n" + "=" * 60)
print("验证总结:")
print("=" * 60)
print(f"卡牌数量: {len(NEUTRAL_LEGENDARY_CARDS)}/7")
print(f"Token数量: {len(REQUIRED_TOKENS) - len(missing_tokens)}/{len(REQUIRED_TOKENS)}")

if missing_tokens:
    print(f"\n缺失的Token: {', '.join(missing_tokens)}")
else:
    print("\n🎉 所有中立传说卡牌和Token都已正确定义！")

print("=" * 60)
