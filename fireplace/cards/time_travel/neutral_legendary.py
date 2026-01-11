"""
穿越时间流 - 中立 - LEGENDARY
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# ========================================
# TIME_024 - 无限巨龙姆诺兹多
# ========================================

class TIME_024:
    """无限巨龙姆诺兹多 - Murozond, Unbounded
    9费 8/8 龙
    战吼：在你的下个回合开始时，将本随从的攻击力变为无穷大！
    
    Battlecry: At the start of your next turn, set this minion's Attack to INFINITY!
    
    实现说明：
    - 在下个回合开始时，将攻击力设置为999（游戏中的"无穷大"）
    - 参考 badlands 中的超高攻击力实现
    """
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 给自己添加buff，在下个回合开始时触发
            yield Buff(SELF, "TIME_024e")
        
        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_024e:
    """无限巨龙姆诺兹多 - 无限攻击力buff
    
    在下个回合开始时，将攻击力设置为999
    """
    # 监听己方回合开始事件
    events = OWN_TURN_BEGIN.on(
        lambda self, source: [
            # 将攻击力设置为999（游戏中的"无穷大"）
            SetAtk(OWNER, 999),
            # 移除这个buff（只触发一次）
            Destroy(SELF)
        ]
    )


# ========================================
# TIME_038 - 钟表先生克劳沃斯
# ========================================

class TIME_038:
    """钟表先生克劳沃斯 - Mister Clocksworth
    8费 3/3 机械
    回溯，回溯，回溯
    战吼：随机召唤2个传说随从。
    
    Rewind, Rewind, Rewind
    Battlecry: Summon 2 random Legendary minions.
    
    实现说明：
    - 拥有3次回溯机会（通过tags标记）
    - 战吼召唤2个随机传说随从
    - 参考 rewind_helpers.py 的回溯机制
    - REWIND相关标签在 fireplace.enums 中定义
    """
    # 标记卡牌具有3次回溯能力
    # 使用 fireplace.enums 中定义的 REWIND 相关标签
    tags = {
        GameTag.REWIND: True,  # 官方标签
    }
    
    def play(self):
        # 创建回溯点
        # 每次打出都会创建一个新的回溯点
        # 玩家可以选择回溯最多3次
        
        # 召唤2个随机传说随从
        yield Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))
        yield Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))



        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

# ========================================
# TIME_063 - 时光之主诺兹多姆
# ========================================

class TIME_063:
    """时光之主诺兹多姆 - Timelord Nozdormu
    3费 8/8 龙
    休眠5回合。突袭。在你使用一张最新扩展包的牌后，提前1回合唤醒。
    
    Dormant for 5 turns. Rush. 
    After you play a card from the newest expansion, awaken 1 turn sooner.
    
    实现说明：
    - 初始休眠5回合
    - 拥有突袭
    - 每次打出最新扩展包的牌，减少1回合休眠时间
    - 参考 demonhunter.py 的休眠机制
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.DORMANT: 5,  # 初始休眠5回合
    }
    
    def play(self):
        # 给控制者添加追踪buff
        yield Buff(CONTROLLER, "TIME_063e")


class TIME_063e:
    """时光之主诺兹多姆 - 追踪buff
    
    监听打出最新扩展包的牌，减少休眠时间
    """
    # 监听打出卡牌事件
    events = Play(CONTROLLER).after(
        lambda self, source, card, target: (
            self._reduce_dormant() 
            if hasattr(card, 'card_set') and card.card_set == CardSet.TIME_TRAVEL 
            else []
        )
    )
    
    def _reduce_dormant(self):
        """减少诺兹多姆的休眠时间"""
        actions = []
        
        # 找到场上的诺兹多姆
        for minion in self.controller.field:
            if minion.id == "TIME_063":
                # 检查是否处于休眠状态
                # 使用 tags.get 来安全获取 DORMANT 值
                current_dormant = minion.tags.get(GameTag.DORMANT, 0)
                
                # 只有当前处于休眠状态时才减少时间
                if current_dormant > 0:
                    # 减少1回合休眠时间
                    new_dormant = current_dormant - 1
                    actions.append(SetTags(minion, {GameTag.DORMANT: new_dormant}))
                    
                    # 如果休眠时间降到0，唤醒（SetTag会自动处理）
                    # 不需要额外的SetTag(0)调用
                    
                    # 如果已经唤醒，移除追踪buff
                    if new_dormant <= 0:
                        actions.append(Destroy(SELF))
                # 只处理第一个找到的诺兹多姆
                break
        
        return actions



# ========================================
# TIME_064 - 时空领主戴欧斯
# ========================================

class TIME_064:
    """时空领主戴欧斯 - Chrono-Lord Deios
    7费 4/8
    你的战吼，亡语，英雄技能和回合结束效果会触发两次。
    
    Your Battlecries, Deathrattles, Hero Power, and end of turn effects trigger twice.
    
    实现说明：
    - 使用 EXTRA_BATTLECRIES 和 EXTRA_DEATHRATTLES 标签
    - TODO: 英雄技能和回合结束效果双倍触发需要额外实现
    - 参考 naxxramas/collectible.py 的双倍触发实现
    """
    # 使用 Aura 实现光环效果
    # 给控制者添加双倍触发效果
    # 注意：目前只实现了战吼和亡语的双倍触发
    # 英雄技能和回合结束效果的双倍触发需要通过其他机制实现
    update = Refresh(CONTROLLER, {
        GameTag.EXTRA_BATTLECRIES: True,
        GameTag.EXTRA_DEATHRATTLES: True,
    })


# ========================================
# TIME_103 - 克罗米
# ========================================

class TIME_103:
    """克罗米 - Chromie
    6费 4/6
    亡语:抽取你在本局对战中使用过的每张牌的另一张复制。
    
    Deathrattle: Draw another copy of cards you've played this game.
    
    实现说明：
    - 追踪本局对战中打出的所有牌
    - 亡语时抽取这些牌的复制
    - 参考 player.py 的 cards_played_this_game 追踪
    """
    @property
    def deathrattle(self):
        """亡语：抽取打出过的牌的复制"""
        actions = []
        
        # 获取本局对战中打出的所有牌
        # cards_played_this_game 是一个 CardList，包含卡牌对象
        if hasattr(self.controller, 'cards_played_this_game'):
            cards_played = self.controller.cards_played_this_game
            
            # 为每张打出的牌生成一张复制并加入手牌
            # 注意：Give action 会自动处理手牌上限（10张）
            # 如果手牌已满，多余的牌会被烧掉（这是炉石的正常机制）
            for card in cards_played:
                # 使用 Give 将卡牌的复制加入手牌
                # card.id 是卡牌的ID字符串
                # Give action 内部会检查手牌空间
                actions.append(Give(CONTROLLER, card.id))
        
        return actions


