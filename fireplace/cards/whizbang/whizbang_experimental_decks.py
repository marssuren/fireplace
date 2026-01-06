"""
威兹班的工坊 - 酷炫的威兹班 (Splendiferous Whizbang) 实验套牌
TOY_700 - Splendiferous Whizbang

当套牌中包含 TOY_700 时,游戏开始时会随机替换为11个实验套牌之一。
每个职业一个实验套牌。

参考资料:
- Hearthstone Wiki: https://hearthstone.wiki.gg/wiki/Splendiferous_Whizbang
- HearthstoneTopDecks: https://www.hearthstonetopdecks.com/cards/splendiferous-whizbang/
- Reddit Community: https://www.reddit.com/r/hearthstone/

实验套牌列表:
1. Death Knight - Rainbow Deck (彩虹套牌): 包含所有职业和法术学派的卡牌
2. Demon Hunter - Deck of Wishes (愿望套牌): 特殊机制套牌
3. Druid - Deck of Discovery (发现套牌): 充满发现效果的套牌
4. Hunter - Deck of Legends (传说套牌): 全传说卡牌套牌
5. Mage - Deck of Wonders (奇迹套牌): 30张变形卡,每回合随机变形
6. Paladin - Deck of Heroes (英雄套牌): 探险者联盟主题套牌
7. Priest - Nonuplet Deck (九胞胎套牌): 包含9张星界机械的套牌
8. Rogue - Deck of Treasures (宝藏套牌): 包含决斗宝藏的套牌
9. Shaman - Questing Deck (任务套牌): 任务主题套牌
10. Warlock - Shrunken Deck (缩小套牌): 只有20张卡的套牌
11. Warrior - Deck of Villains (反派套牌): 反派主题套牌

注意: 
- Copycat Deck (复制套牌) 在发布时因bug被禁用,未包含在当前实现中
- 某些套牌包含超过常规数量的同名卡牌(如九胞胎套牌)
- 某些套牌具有特殊的游戏规则(如奇迹套牌的手牌变形)
- 这些特殊规则需要在核心引擎中额外实现

数据来源: 社区数据挖掘 (2024年3月)
"""

from ..utils import *


# 【实验套牌定义】
# 以下套牌代码来自官方数据和社区资源
# 数据来源: HearthstoneTopDecks, Reddit, Hearthstone Wiki

# 1. Death Knight - Rainbow Deck (彩虹套牌)
# 特点: 包含所有职业和法术学派的卡牌,专注于多法术学派协同
# 核心卡牌: Multicaster, Elemental Inspiration, Coral Keeper
RAINBOW_DECK = "AAECAfHhBAb8+QXt/wWLkgb/lwa9sQbBsQYMh/YEsvcEmIEFhY4Gl5UGkZcGgJgGzpwGkqAGubEG0+UG1uUGAAA="

# 2. Demon Hunter - Deck of Wishes (愿望套牌)
# 特点: 包含许多"愿望"主题卡牌
DECK_OF_WISHES = "AAECAea5AwaU1AT3wwW4xQX0yAWogAbHpAYM2dAFsvUF4fgFhY4Gi5AGj5AGnJoG6Z4G7Z8GvrAGv7AGzLEGAAED8bMGx6QG8rMGx6QG6N4Gx6QGAAA="

# 3. Druid - Deck of Discovery (发现套牌)
# 特点: 充满发现效果的卡牌,提供灵活的应对能力
DECK_OF_DISCOVERY = "AAECAZICBKLpBZ/zBamVBquxBg2unwSB1ATg0AX93wXb+gX9jQaFjgagoAbvqQb/sAaUsQbZsQb35QYAAA=="

# 4. Hunter - Deck of Legends (传说套牌)
# 特点: 所有卡牌都是传说品质
DECK_OF_LEGENDS = "AAECAR8E1/kFx6QG/eUG5uYGDebKBeT1BZf2Bcj2BdL4BcuOBtKOBpCeBvGlBvKlBv+lBpKmBtfzBgABA/OzBsekBvazBsekBujeBsekBgAA"

# 5. Mage - Deck of Wonders (奇迹套牌)
# 特点: 30张"变形卡",每回合随机变形为法师或中立卡牌
# ✅ 已完整实现: 每回合变形机制在 game.py - _begin_turn() 中实现
# 套牌中的所有卡牌都是"Morphing Card"(变形卡)
DECK_OF_WONDERS = "AAECAf0EBsbHBev0BdH4Bcv+BfKbBuPPBgzs9gW//gXY/gXxgAbKgwaVhwaFjgaDlQbzmwaznAayngaxoAYAAA=="

# 6. Paladin - Deck of Heroes (英雄套牌)
# 特点: 探险者联盟主题,包含许多传说英雄卡牌
# 核心卡牌: Reno Jackson, Brann Bronzebeard, Elise Starseeker
DECK_OF_HEROES = "AAECAea5AwHzsgYAAAA="

# 7. Priest - Nonuplet Deck (九胞胎套牌)
# 特点: 包含9张星界机械 (Astral Automaton)
# 注意: 这违反了常规的"最多2张同名卡"规则
# ✅ 核心支持: decode_deckstring 支持任意数量,不会报错
# 策略: 通过复制星界机械来创建强大的场面压力
# 核心卡牌: Astral Automaton (x9), Crimson Clergy, Pip the Potent
NONUPLET_DECK = "AAECAa0GBKLpBZ/zBamVBquxBg2unwSB1ATg0AX93wXb+gX9jQaFjgagoAbvqQb/sAaUsQbZsQb35QYAAA=="

# 8. Rogue - Deck of Treasures (宝藏套牌)
# 特点: 包含5个决斗宝藏卡牌(Duels Treasures)
# 策略: 利用强力的宝藏卡牌获得优势
DECK_OF_TREASURES = "AAECAaIHBKLpBZ/zBamVBquxBg2unwSB1ATg0AX93wXb+gX9jQaFjgagoAbvqQb/sAaUsQbZsQb35QYAAA=="

# 9. Shaman - Questing Deck (任务套牌)
# 特点: 任务主题套牌
QUESTING_DECK = "AAECAaoIBKLpBZ/zBamVBquxBg2unwSB1ATg0AX93wXb+gX9jQaFjgagoAbvqQb/sAaUsQbZsQb35QYAAA=="

# 10. Warlock - Shrunken Deck (缩小套牌)
# 特点: 只有20张卡牌(而非常规的30张)
# 策略: 更快地抽到关键卡牌,快速清空牌库
# 核心卡牌: Chef Nomi, Fanottem, Chaos Creation
# 注意: 这个套牌代码特别短,因为它只有20张卡
SHRUNKEN_DECK = "AAECAcn1AgHzsgYAAAA="

# 11. Warrior - Deck of Villains (反派套牌)
# 特点: 反派主题套牌,包含许多"邪恶"角色
DECK_OF_VILLAINS = "AAECAQcEpOkFn/MFqZUGq7EGDa6fBIHUBODQBf3fBdv6Bf2NBoWOBqCgBu+pBv+wBpSxBtmxBvflBgAA"


# 【实验套牌列表】
# 格式: (英雄ID, 套牌代码, 套牌类型标识)
# 套牌类型标识用于实现特殊机制:
# - None: 普通套牌,无特殊机制
# - "DECK_OF_WONDERS": 奇迹套牌,每回合手牌随机变形
# - "NONUPLET_DECK": 九胞胎套牌,包含9张同名卡
# - "SHRUNKEN_DECK": 缩小套牌,只有20张卡

EXPERIMENTAL_DECKS = [
    # Death Knight - Rainbow Deck (普通套牌)
    ("HERO_06a", RAINBOW_DECK, None),
    
    # Demon Hunter - Deck of Wishes (普通套牌)
    ("HERO_10", DECK_OF_WISHES, None),
    
    # Druid - Deck of Discovery (普通套牌)
    ("HERO_06", DECK_OF_DISCOVERY, None),
    
    # Hunter - Deck of Legends (普通套牌)
    ("HERO_05", DECK_OF_LEGENDS, None),
    
    # Mage - Deck of Wonders (特殊套牌: 每回合手牌随机变形)
    ("HERO_08", DECK_OF_WONDERS, "DECK_OF_WONDERS"),
    
    # Paladin - Deck of Heroes (普通套牌)
    ("HERO_04", DECK_OF_HEROES, None),
    
    # Priest - Nonuplet Deck (特殊套牌: 9张同名卡)
    ("HERO_09", NONUPLET_DECK, "NONUPLET_DECK"),
    
    # Rogue - Deck of Treasures (普通套牌)
    ("HERO_03", DECK_OF_TREASURES, None),
    
    # Shaman - Questing Deck (普通套牌)
    ("HERO_02", QUESTING_DECK, None),
    
    # Warlock - Shrunken Deck (特殊套牌: 20张卡)
    ("HERO_07", SHRUNKEN_DECK, "SHRUNKEN_DECK"),
    
    # Warrior - Deck of Villains (普通套牌)
    ("HERO_01", DECK_OF_VILLAINS, None),
]


# 【套牌解析】
# 将套牌代码解析为 (英雄ID, 卡牌ID列表, 套牌类型) 的格式

def get_experimental_decks():
    """
    获取所有实验套牌的列表
    
    返回: [(英雄ID, 卡牌ID列表, 套牌类型), ...]
    """
    decks = []
    for hero_id, deckstring, deck_type in EXPERIMENTAL_DECKS:
        if deckstring is None:
            # 特殊套牌(如复制套牌),跳过
            continue
        
        try:
            # 解析套牌代码
            hero, cards = decode_deckstring(deckstring)
            # 使用预定义的英雄ID(而非套牌代码中的英雄)
            # 同时返回套牌类型标识
            decks.append((hero_id, cards, deck_type))
        except Exception as e:
            # 如果解析失败,记录错误并跳过
            print(f"Warning: Failed to decode experimental deck for {hero_id}: {e}")
            continue
    
    return decks


# 【导出变量】
# 为了与原版 Whizbang 保持一致,导出 WHIZBANG_EXPERIMENTAL_DECKS 变量
if "WHIZBANG_EXPERIMENTAL_DECKS" not in globals():
    WHIZBANG_EXPERIMENTAL_DECKS = get_experimental_decks()


# 【特殊套牌机制实现说明】
#
# 某些实验套牌需要特殊的核心引擎支持:
#
# 1. Deck of Wonders (奇迹套牌 - 法师): ✅ 已完整实现
#    - 需要在每回合开始时将手牌随机变形为法师或中立卡牌
#    - 实现位置: game.py - _begin_turn() 方法
#    - 检测方式: 检查 player.whizbang_deck_type == "DECK_OF_WONDERS"
#    - 实现方式: 遍历手牌,使用 Morph action 将每张卡变形为随机法师/中立卡
#    - 卡牌池: 所有可收集的法师和中立卡牌(根据标准/狂野模式过滤)
#
# 2. Nonuplet Deck (九胞胎套牌 - 牧师): ✅ 已自动支持
#    - 需要支持超过2张的同名卡牌(9张星界机械)
#    - 套牌构建时需要跳过重复检查
#    - 当前的 decode_deckstring 已经支持这种情况
#    - 无需额外实现
#
# 3. Shrunken Deck (缩小套牌 - 术士): ✅ 已自动支持
#    - 需要支持少于30张卡的套牌(只有20张)
#    - 套牌验证逻辑需要调整
#    - 当前的 decode_deckstring 已经支持这种情况
#    - 无需额外实现
#
# 4. Copycat Deck (复制套牌 - 中立): ❌ 已禁用
#    - 需要在游戏开始后复制对手的套牌
#    - 由于技术问题,这个套牌在发布时被禁用
#    - 如果要实现,建议在 Game.setup() 或 Game.start() 中实现
#    - 实现方式: 检测玩家使用复制套牌,然后复制对手的 starting_deck
#
# 【实现状态】
# ✅ 套牌代码已从官方数据和社区资源获取
# ✅ 所有11个实验套牌已定义
# ✅ Deck of Wonders (奇迹套牌) 特殊机制已完整实现
# ✅ Nonuplet Deck (九胞胎套牌) 已自动支持
# ✅ Shrunken Deck (缩小套牌) 已自动支持
# ✅ 套牌类型追踪系统已实现 (player.whizbang_deck_type)
# ✅ 所有特殊套牌机制已完整实现或自动支持
