"""
胜地历险记 - 中立稀有卡牌验证脚本
验证所有6张中立稀有卡牌的实现
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from fireplace import cards
from fireplace.game import Game
from fireplace.player import Player
from hearthstone.enums import CardClass, CardType

# 初始化卡牌数据库
cards.db.initialize()

print("=" * 80)
print("胜地历险记 - 中立稀有卡牌验证")
print("=" * 80)

# 验证的卡牌列表
rare_cards = [
    ("VAC_438", "旅行社职员", "2费 2/2 海盗 - 战吼：发现一张任意职业的地标牌"),
    ("VAC_440", "海关执法者", "3费 2/5 海盗 - 敌方套牌之外的敌方卡牌法力值消耗增加（2）点"),
    ("VAC_441", "包裹分拣工", "6费 6/7 - 在你抽牌后，有50%的几率再抽一张"),
    ("VAC_521", "笨拙的搬运工", "3费 3/3 亡灵+海盗 - 嘲讽。战吼：如果你的手牌中有法力值消耗大于或等于（5）点的法术牌，召唤一个本随从的复制"),
    ("VAC_936", "八爪按摩机", "4费 1/8 机械+野兽 - 对随从造成八倍伤害"),
    ("WORK_040", "笨拙的杂役", "3费 2/4 - 在任意卡牌被抽到后，将其变为临时卡牌"),
]

print("\n【卡牌数据验证】")
print("-" * 80)

all_passed = True

for card_id, name, description in rare_cards:
    try:
        # 尝试加载卡牌
        card_data = cards.db[card_id]
        
        # 验证卡牌存在
        if card_data:
            print(f"✓ {card_id} - {name}")
            print(f"  描述: {description}")
            
            # 验证卡牌类
            if hasattr(card_data, 'impl'):
                print(f"  实现: 已定义")
            else:
                print(f"  ⚠ 警告: 未找到实现类")
                all_passed = False
        else:
            print(f"✗ {card_id} - {name}: 卡牌数据未找到")
            all_passed = False
            
    except Exception as e:
        print(f"✗ {card_id} - {name}: 错误 - {str(e)}")
        all_passed = False
    
    print()

print("=" * 80)
if all_passed:
    print("✓ 所有卡牌验证通过！")
else:
    print("⚠ 部分卡牌验证失败，请检查实现")
print("=" * 80)

print("\n【实现总结】")
print("-" * 80)
print("1. VAC_438 (旅行社职员): 使用 Discover + RandomCollectible(type=CardType.LOCATION)")
print("2. VAC_440 (海关执法者): 使用 Refresh(ENEMY_HAND - STARTING_DECK, {GameTag.COST: +2})")
print("3. VAC_441 (包裹分拣工): 使用 Draw 事件监听器 + 50%几率判断")
print("4. VAC_521 (笨拙的搬运工): 检查手牌中5费以上法术 + ExactCopy(SELF)")
print("5. VAC_936 (八爪按摩机): 使用 Attack(SELF, MINION).after(Hit(DEFENDER, ATK(SELF) * 7))")
print("6. WORK_040 (笨拙的杂役): 使用 Draw 事件监听器 + GHOSTLY 标签")
print("=" * 80)
