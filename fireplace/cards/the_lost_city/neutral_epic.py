"""
失落之城 - NEUTRAL EPIC
"""
from ..utils import *
from .kindred_helpers import check_kindred_active


# DINO_435 - 环形山实验体
class DINO_435:
    """环形山实验体 - Crater Experiment
    5费 3/4 全类型
    <b>延系：</b>召唤一个本随从的复制。
    
    Kindred: Summon a copy of this.
    
    官方说明：
    - 全类型随从（ALL种族）
    - 延系效果：如果上回合打出过任意类型的随从，则召唤一个复制
    - 全类型随从可以被任何种族触发
    """
    def play(self):
        # 检查延系是否激活（上回合打出过任意随从）
        # 使用 check_kindred_active 的特殊模式：不指定种族，只检查是否打出过随从
        if check_kindred_active(self.controller, card_type=CardType.MINION):
            # 召唤一个复制
            yield Summon(CONTROLLER, ExactCopy(SELF))


# TLC_107 - 聚积旋风
class TLC_107:
    """聚积旋风 - Gathering Whirlwind
    5费 3/6 元素
    每当本随从攻击时，先对目标造成3点伤害。<b>延系：</b>获得<b>突袭</b>。
    
    Whenever this attacks, deal 3 damage to the target first. Kindred: Gain Rush.
    
    官方说明：
    - 攻击前先造成3点伤害
    - 延系效果：如果上回合打出过元素，则获得突袭
    """
    # 延系效果：检查上回合是否打出过元素
    def play(self):
        # 检查延系是否激活（上回合打出过元素）
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.ELEMENTAL):
            # 获得突袭
            yield Buff(SELF, "TLC_107e")
    
    # 攻击前造成3点伤害
    events = Attack(SELF).on(
        lambda self, card: Hit(target, 3)
    )


class TLC_107e:
    """聚积旋风突袭增益 - Gathering Whirlwind Rush"""
    tags = {
        GameTag.RUSH: True,
    }


# TLC_245 - 远古迅猛龙
class TLC_245:
    """远古迅猛龙 - Ancient Raptor
    2费 2/1 野兽
    <b>战吼：</b>从+3攻击力，<b>圣盾</b>或"<b>亡语：</b>召唤两个1/1的植物"中选择一项并获得。
    
    Battlecry: Choose One - Gain +3 Attack; Gain Divine Shield; or Gain "Deathrattle: Summon two 1/1 Plants".
    
    官方说明：
    - 三选一效果
    - 选项1：+3攻击力
    - 选项2：圣盾
    - 选项3：亡语召唤两个1/1植物
    """
    choose = ["TLC_245a", "TLC_245b", "TLC_245c"]


class TLC_245a:
    """远古迅猛龙选项1 - +3攻击力"""
    atk = 3


class TLC_245b:
    """远古迅猛龙选项2 - 圣盾"""
    tags = {
        GameTag.DIVINE_SHIELD: True,
    }


class TLC_245c:
    """远古迅猛龙选项3 - 亡语召唤两个1/1植物"""
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    def deathrattle(self):
        # 召唤两个1/1植物
        yield Summon(CONTROLLER, "TLC_245t") * 2


# TLC_254 - 讲故事的始祖龟
class TLC_254:
    """讲故事的始祖龟 - Storytelling Tortollan
    2费 1/2
    在你的回合结束时，使每个不同类型的各一个友方随从获得+1/+1。
    
    At the end of your turn, give +1/+1 to one friendly minion of each different type.
    
    官方说明：
    - 回合结束时触发
    - 为每个不同的随从类型各选择一个随从
    - 给予+1/+1
    """
    def OWN_TURN_END(self):
        # 收集所有友方随从的种族
        minions = self.game.query(FRIENDLY_MINIONS)
        if not minions:
            return
        
        # 收集所有出现过的种族和对应的第一个随从
        races_seen = set()
        minions_to_buff = []
        
        for minion in minions:
            # 获取随从的种族列表
            if hasattr(minion, 'race'):
                minion_races = getattr(minion, 'races', [minion.race])
                for race in minion_races:
                    if race not in races_seen:
                        races_seen.add(race)
                        # 为每个种族记录第一个遇到的随从
                        minions_to_buff.append(minion)
                        break  # 每个随从只计数一次
        
        # 为每个种族的一个随从增益
        for minion in minions_to_buff:
            yield Buff(minion, "TLC_254e")
    
    events = OWN_TURN_END


class TLC_254e:
    """讲故事的始祖龟增益 - Storytelling Tortollan Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


# TLC_255 - 水晶养护工
class TLC_255:
    """水晶养护工 - Crystal Caretaker
    2费 2/2
    <b>可交易</b>
    <b>战吼：</b>获得空的法力水晶，直到双方玩家拥有的法力水晶相同。
    
    Tradeable
    Battlecry: Gain empty Mana Crystals until both players have the same amount.
    
    官方说明：
    - 可交易
    - 战吼效果：如果对手的法力水晶比你多，则获得空水晶直到相同
    """
    tags = {
        GameTag.TRADEABLE: True,
    }
    
    def play(self):
        # 计算需要获得的法力水晶数量
        mana_diff = self.controller.opponent.max_mana - self.controller.max_mana
        if mana_diff > 0:
            # 获得空的法力水晶
            yield GainEmptyMana(CONTROLLER, mana_diff)


# TLC_829 - 饥饿的魔暴龙
class TLC_829:
    """饥饿的魔暴龙 - Hungry Tyrantus
    7费 3/3 野兽
    <b>战吼：</b>消灭一个随从。<b>延系：</b>获得被消灭随从的属性值。
    
    Battlecry: Destroy a minion. Kindred: Gain its stats.
    
    官方说明：
    - 战吼消灭一个随从
    - 延系效果：如果上回合打出过野兽，则获得被消灭随从的属性值
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        target = self.target
        if target:
            # 检查延系是否激活（上回合打出过野兽）
            kindred_active = check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST)
            
            if kindred_active:
                # 记录目标的属性值
                target_atk = target.atk
                target_health = target.max_health
                
                # 消灭目标
                yield Destroy(target)
                
                # 获得属性值
                yield Buff(SELF, "TLC_829e", atk=target_atk, max_health=target_health)
            else:
                # 仅消灭目标
                yield Destroy(target)


class TLC_829e:
    """饥饿的魔暴龙属性增益 - Hungry Tyrantus Stats Buff
    
    动态buff，根据被消灭随从的属性值增加攻击力和生命值
    """
    def apply(self, target):
        # 从 buff 参数中获取属性值并保存
        self._xatk = self.atk
        self._xhealth = self.max_health
    
    # 使用 lambda 动态返回属性值
    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth
