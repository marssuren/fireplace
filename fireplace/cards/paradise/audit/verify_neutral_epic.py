"""
验证中立史诗卡牌实现
"""
import sys
sys.path.insert(0, 'D:\\Projects\\Yolo\\hearthstone_zero\\fireplace')

from fireplace import cards
from fireplace.game import Game
from fireplace.player import Player

# 初始化卡牌数据库
cards.db.initialize()

print("=" * 60)
print("中立史诗卡牌实现验证")
print("=" * 60)

# 检查所有卡牌是否存在
neutral_epic_ids = [
    "VAC_439",    # 海滨巨人
    "VAC_447",    # 恐惧的逃亡者
    "VAC_523",    # 混调师
    "VAC_935",    # 随行肉虫
    "VAC_958",    # 进化融合怪
    "WORK_042",   # 食肉格块
]

print("\n1. 检查卡牌是否存在于数据库:")
for card_id in neutral_epic_ids:
    if card_id in cards.db:
        card_data = cards.db[card_id]
        print(f"  ✓ {card_id}: {card_data.name}")
    else:
        print(f"  ✗ {card_id}: 不存在")

# 检查 Token
print("\n2. 检查 Token 是否存在:")
token_ids = [
    "VAC_523t",   # 抽牌药水
    "VAC_523t2",  # 伤害药水
    "VAC_523t3",  # 治疗药水
    "VAC_935t",   # 手提箱
]

for token_id in token_ids:
    if token_id in cards.db:
        token_data = cards.db[token_id]
        print(f"  ✓ {token_id}: {token_data.name}")
    else:
        print(f"  ✗ {token_id}: 不存在")

# 检查核心引擎扩展
print("\n3. 检查核心引擎扩展:")
try:
    # 创建测试玩家
    deck = ["VAC_439"] * 30
    player = Player("Test", deck, "HERO_01")
    
    # 检查 locations_used_this_game 属性
    if hasattr(player, 'locations_used_this_game'):
        print(f"  ✓ Player.locations_used_this_game 已添加 (初始值: {player.locations_used_this_game})")
    else:
        print("  ✗ Player.locations_used_this_game 未添加")
except Exception as e:
    print(f"  ✗ 创建玩家失败: {e}")

print("\n4. 检查卡牌实现:")
try:
    from fireplace.cards.paradise import neutral_epic
    
    # 检查每个卡牌类是否存在
    card_classes = [
        ("VAC_439", "海滨巨人"),
        ("VAC_447", "恐惧的逃亡者"),
        ("VAC_523", "混调师"),
        ("VAC_935", "随行肉虫"),
        ("VAC_958", "进化融合怪"),
        ("WORK_042", "食肉格块"),
    ]
    
    for card_id, card_name in card_classes:
        if hasattr(neutral_epic, card_id):
            print(f"  ✓ {card_id} ({card_name}) 类已定义")
        else:
            print(f"  ✗ {card_id} ({card_name}) 类未定义")
            
except Exception as e:
    print(f"  ✗ 导入失败: {e}")

print("\n" + "=" * 60)
print("验证完成！")
print("=" * 60)
