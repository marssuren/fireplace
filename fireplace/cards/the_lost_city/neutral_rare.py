"""
失落之城 - NEUTRAL RARE
"""
from ..utils import *


# DINO_411 - 神圣布蛋者
class DINO_411:
    """神圣布蛋者 - Sacred Egg Placer
    2费 1/2
    <b>战吼：</b>抽一张攻击力为0的随从牌。
    
    Battlecry: Draw a minion with 0 Attack.
    
    官方说明：
    - 从牌库中抽一张攻击力为0的随从牌
    - 如果牌库中没有攻击力为0的随从，则不抽牌
    """
    def play(self):
        # 抽一张攻击力为0的随从牌
        yield DrawCard(CONTROLLER, MINION + (ATK == 0))


# TLC_246 - 远古翼手龙
class TLC_246:
    """远古翼手龙 - Ancient Pterrordax
    4费 4/4 野兽
    <b>战吼：</b>从<b>扰魔</b>，<b>风怒</b>或直到下回合<b>潜行</b>中选择一项获得。
    
    Battlecry: Choose One - Gain Elusive; Gain Windfury; or Gain Stealth until next turn.
    
    官方说明：
    - 三选一效果
    - 选项1：扰魔（Elusive）
    - 选项2：风怒（Windfury）
    - 选项3：潜行直到下回合（Stealth until next turn）
    """
    choose = ["TLC_246a", "TLC_246b", "TLC_246c"]


class TLC_246a:
    """远古翼手龙选项1 - 扰魔"""
    tags = {
        GameTag.ELUSIVE: True,
    }


class TLC_246b:
    """远古翼手龙选项2 - 风怒"""
    tags = {
        GameTag.WINDFURY: True,
    }


class TLC_246c:
    """远古翼手龙选项3 - 潜行直到下回合"""
    tags = {
        GameTag.STEALTH: True,
    }
    
    # 下回合开始时移除潜行
    events = OWN_TURN_BEGIN.on(
        lambda self: SetTag(SELF, {GameTag.STEALTH: False})
    )


# TLC_251 - 蛮鱼挑战者
class TLC_251:
    """蛮鱼挑战者 - Murloc Challenger
    3费 3/2 鱼人
    <b>战吼：</b>你的下一个<b>延系</b>效果会触发两次。
    
    Battlecry: Your next Kindred effect triggers twice.
    
    官方说明：
    - 给玩家添加一个buff，使下一个延系效果触发两次
    - 这需要在核心引擎中添加支持（Player.kindred_double_trigger）
    """
    def play(self):
        # 给玩家添加延系双倍触发标记
        # 这需要在 Player 类中添加 kindred_double_trigger 属性
        # 并在 kindred_helpers.py 中检查此属性
        self.controller.kindred_double_trigger = True


# TLC_252 - 蚀解软泥怪
class TLC_252:
    """蚀解软泥怪 - Dissolving Ooze
    3费 3/3
    <b>战吼：</b>消灭一个友方随从，将一张骸骨置入你的手牌。骸骨可以使一个随从获得被消灭随从的攻击力和生命值。
    
    Battlecry: Destroy a friendly minion. Add a Bone to your hand that gives a minion its stats.
    
    官方说明：
    - 消灭一个友方随从
    - 获得一张骸骨法术牌
    - 骸骨可以给目标随从增加被消灭随从的攻击力和生命值
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        if TARGET:
            # 记录目标的属性值
            target_atk = TARGET.atk
            target_health = TARGET.max_health
            
            # 消灭目标
            yield Destroy(TARGET)
            
            # 创建一张骸骨法术牌，并记录属性值
            bone_card = yield Give(CONTROLLER, "TLC_252t")
            if bone_card:
                # 给骸骨牌添加属性值标记
                yield Buff(bone_card[0], "TLC_252e", atk=target_atk, max_health=target_health)


class TLC_252e:
    """蚀解软泥怪属性标记 - Dissolving Ooze Stats Marker
    
    用于在骸骨法术牌上存储被消灭随从的属性值
    """
    def apply(self, target):
        # 保存属性值到buff中
        self._stored_atk = self.atk
        self._stored_health = self.max_health


# TLC_465 - 绞缠血藤
class TLC_465:
    """绞缠血藤 - Entangling Bloodvine
    3费 3/2
    <b>亡语：</b>使一个随机友方随从获得一项随机<b>额外效果</b>以及此<b>亡语</b>。
    
    Deathrattle: Give a random friendly minion a random Keyword and this Deathrattle.
    
    官方说明：
    - 亡语效果：随机选择一个友方随从
    - 给予一项随机关键词（额外效果）
    - 同时给予此亡语效果（递归）
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    def deathrattle(self):
        # 随机选择一个友方随从
        targets = self.game.query(FRIENDLY_MINIONS)
        if targets:
            target = random.choice(targets)
            
            # 给予随机关键词
            # 可能的关键词：嘲讽、圣盾、风怒、吸血、突袭、剧毒等
            keywords = [
                "TLC_465e1",  # 嘲讽
                "TLC_465e2",  # 圣盾
                "TLC_465e3",  # 风怒
                "TLC_465e4",  # 吸血
                "TLC_465e5",  # 突袭
                "TLC_465e6",  # 剧毒
            ]
            
            # 随机选择一个关键词
            keyword_buff = random.choice(keywords)
            yield Buff(target, keyword_buff)
            
            # 给予此亡语效果
            yield Buff(target, "TLC_465e_deathrattle")


class TLC_465e1:
    """绞缠血藤关键词1 - 嘲讽"""
    tags = {
        GameTag.TAUNT: True,
    }


class TLC_465e2:
    """绞缠血藤关键词2 - 圣盾"""
    tags = {
        GameTag.DIVINE_SHIELD: True,
    }


class TLC_465e3:
    """绞缠血藤关键词3 - 风怒"""
    tags = {
        GameTag.WINDFURY: True,
    }


class TLC_465e4:
    """绞缠血藤关键词4 - 吸血"""
    tags = {
        GameTag.LIFESTEAL: True,
    }


class TLC_465e5:
    """绞缠血藤关键词5 - 突袭"""
    tags = {
        GameTag.RUSH: True,
    }


class TLC_465e6:
    """绞缠血藤关键词6 - 剧毒"""
    tags = {
        GameTag.POISONOUS: True,
    }


class TLC_465e_deathrattle:
    """绞缠血藤亡语传递 - Entangling Bloodvine Deathrattle Transfer
    
    将亡语效果传递给目标随从
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    def deathrattle(self):
        # 递归调用相同的亡语效果
        # 随机选择一个友方随从
        targets = self.game.query(FRIENDLY_MINIONS)
        if targets:
            target = random.choice(targets)
            
            # 给予随机关键词
            keywords = [
                "TLC_465e1",  # 嘲讽
                "TLC_465e2",  # 圣盾
                "TLC_465e3",  # 风怒
                "TLC_465e4",  # 吸血
                "TLC_465e5",  # 突袭
                "TLC_465e6",  # 剧毒
            ]
            
            # 随机选择一个关键词
            keyword_buff = random.choice(keywords)
            yield Buff(target, keyword_buff)
            
            # 给予此亡语效果（递归）
            yield Buff(target, "TLC_465e_deathrattle")


# TLC_888 - 云端翔龙
class TLC_888:
    """云端翔龙 - Skyward Wyvern
    3费 3/3 元素/龙
    <b>战吼：</b>获取你手牌中另一张元素牌或龙牌的一张复制。
    
    Battlecry: Add a copy of another Elemental or Dragon in your hand to your hand.
    
    官方说明：
    - 从手牌中随机选择一张元素或龙牌（不包括自己）
    - 获得该牌的一张复制
    """
    def play(self):
        # 查找手牌中的其他元素或龙牌
        candidates = [
            card for card in self.controller.hand
            if card != self and (
                (hasattr(card, 'race') and (card.race == Race.ELEMENTAL or card.race == Race.DRAGON)) or
                (hasattr(card, 'races') and (Race.ELEMENTAL in card.races or Race.DRAGON in card.races))
            )
        ]
        
        if candidates:
            # 随机选择一张
            target_card = random.choice(candidates)
            # 获得复制
            yield Give(CONTROLLER, Copy(target_card))

