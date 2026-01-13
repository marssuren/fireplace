"""
深暗领域 - PRIEST
"""
from ..utils import *


# COMMON

class GDB_452:
    """阿斯卡拉之盾 - Shield of Askara
    6费 4/8 牧师随从 - 德莱尼
    嘲讽，圣盾，吸血
    
    Taunt, Divine Shield, Lifesteal
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DIVINE_SHIELD: True,
        GameTag.LIFESTEAL: True,
    }
    race = Race.DRAENEI


class GDB_460:
    """神圣之星 - Divine Star
    2费 牧师法术（神圣）
    对一个随从造成3点伤害。随机使你手牌中的一张随从牌获得+3生命值。
    
    Deal 3 damage to a minion. Give a random minion in your hand +3 Health.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 对目标造成3点伤害
        self.hit(self.target, 3)
        
        # 随机使手牌中的一张随从牌获得+3生命值
        minions_in_hand = self.controller.hand.filter(type=CardType.MINION)
        if minions_in_hand:
            target_minion = random.choice(minions_in_hand)
            target_minion.buff(self.controller, "GDB_460e")


class GDB_460e:
    """神圣之星增益 - Divine Star Buff
    +3生命值
    """
    tags = {
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_457:
    """光速 - Lightspeed
    2费 牧师法术（神圣）
    使一个随从获得+1/+2和突袭。本回合可重复使用。
    
    Give a minion +1/+2 and Rush. Repeatable this turn.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 使目标获得+1/+2和突袭
        self.target.buff(self.controller, "GDB_457e")
        
        # 本回合可重复使用 - 返回手牌
        Give(self.controller, self.id).run()


class GDB_457e:
    """光速增益 - Lightspeed Buff
    +1/+2和突袭
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_764:
    """机械哨兵 - Sentry
    2费 2/2 牧师随从 - 机械
    吸血
    亡语：在本局对战中，你的星灵随从的法力值消耗减少（1）点。
    
    Lifesteal
    Deathrattle: Your Protoss minions cost (1) less this game.
    """
    tags = {
        GameTag.LIFESTEAL: True,
        GameTag.DEATHRATTLE: True,
    }
    race = Race.MECHANICAL
    
    def deathrattle(self):
        # 在本局对战中，星灵随从减费（1）点
        Buff(self.controller, "SC_764e").run()


class SC_764e:
    """星灵减费光环 - Protoss Cost Reduction
    你的星灵随从的法力值消耗减少（1）点
    """
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + PROTOSS, {GameTag.COST: -1})


# RARE

class GDB_439:
    """星轨晕环 - Orbital Halo
    2费 牧师法术（神圣）
    使一个随从获得+2/+1和圣盾。如果你在本回合中打出过与本牌相邻的牌，则法力值消耗为（0）点。
    
    Give a minion +2/+1 and Divine Shield. Costs (0) if you played an adjacent card this turn.
    
    参考实现: space/paladin.py - GDB_462 (在轨卫星)
    使用 cards_played_this_turn_with_position 追踪手牌位置
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def cost_func(self, value):
        """动态费用计算
        
        检查本回合是否打出过与本牌相邻的牌
        如果是，则费用变为0
        """
        if self._played_adjacent_card():
            return 0
        return value
    
    def play(self):
        # 使目标获得+2/+1和圣盾
        self.target.buff(self.controller, "GDB_439e")
    
    def _played_adjacent_card(self):
        """检查本回合是否打出过与本牌相邻的牌
        
        相邻指的是在手牌中位置相邻（位置差为1）
        参考 space/paladin.py - GDB_462 的实现
        """
        # 只在手牌中时检查
        if self.zone != Zone.HAND:
            return False
        
        # 获取本牌当前在手牌中的位置
        my_position = self.zone_position
        
        # 检查本回合打出的其他牌是否与本牌相邻
        for card, position in self.controller.cards_played_this_turn_with_position:
            if card != self and abs(position - my_position) == 1:
                return True
        
        return False



class GDB_439e:
    """星轨晕环增益 - Orbital Halo Buff
    +2/+1和圣盾
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.DIVINE_SHIELD: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_441:
    """德莱尼学者 - Anchorite
    3费 2/4 牧师随从 - 德莱尼
    每当另一个随从被过量治疗时，使其获得等量的额外生命值。
    
    Whenever another minion is Overhealed, give it that much extra Health.
    """
    race = Race.DRAENEI
    
    # 监听过量治疗事件
    events = [
        Overheal(FRIENDLY_MINIONS - SELF).on(
            lambda self, target, amount: target.buff(target.controller, "GDB_441e", atk=0, health=amount)
        )
    ]


class GDB_441e:
    """德莱尼学者增益 - Anchorite Buff
    额外生命值
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_454:
    """狂热的医者 - Overzealous Healer
    1费 3/3 牧师随从 - 德莱尼
    亡语：为敌方英雄恢复6点生命值。
    法术迸发：沉默本随从。
    
    Deathrattle: Restore 6 Health to the enemy hero.
    Spellburst: Silence this minion.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
        GameTag.SPELLBURST: True,
    }
    race = Race.DRAENEI
    
    # 法术迸发：沉默本随从
    events = OWN_SPELL_PLAY.on(
        lambda self, player: Silence(self).run(),
        SetTags(SELF, {GameTag.SPELLBURST: False})
    )
    
    def deathrattle(self):
        # 为敌方英雄恢复6点生命值
        Heal(self.controller.opponent.hero, 6).run()


class SC_757:
    """幻像 - Hallucination
    3费 牧师法术
    召唤一个友方星灵随从的复制。该复制受到双倍伤害。
    
    Summon a copy of a friendly Protoss minion. It takes double damage.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.PROTOSS,
    }
    
    def play(self):
        # 召唤目标的复制
        copy = self.target.copy()
        Summon(self.controller, copy).run()
        
        # 使复制受到双倍伤害
        copy.buff(self.controller, "SC_757e")


class SC_757e:
    """幻像增益 - Hallucination Buff
    受到双倍伤害
    """
    tags = {
        GameTag.INCOMING_DAMAGE_MULTIPLIER: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# EPIC

class GDB_440:
    """迷惑生物图查 - Mystified To'cha
    4费 4/2 牧师随从
    战吼：如果双方英雄的生命值总和恰好为42点，则将你的英雄生命值设为42点。
    
    Battlecry: If the combined Health of both heroes is exactly 42, set your hero's Health to 42.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 计算双方英雄的生命值总和
        total_health = self.controller.hero.health + self.controller.opponent.hero.health
        
        # 如果总和恰好为42，则将己方英雄生命值设为42
        if total_health == 42:
            # 设置生命值为42
            self.controller.hero.set_current_health(42)


class GDB_464:
    """引力失效 - Gravity Lapse
    0费 牧师法术
    将所有随从的攻击力和生命值设为两者中较低的数值。
    
    Set EVERY minion's Attack and Health to the lower of the two.
    """
    def play(self):
        # 对所有随从应用引力失效效果
        for minion in self.game.board:
            lower_value = min(minion.atk, minion.health)
            # 计算需要调整的数值
            atk_diff = lower_value - minion.atk
            health_diff = lower_value - minion.max_health
            # 使用buff设置攻击力和生命值
            if atk_diff != 0 or health_diff != 0:
                minion.buff(self.controller, "GDB_464e", atk=atk_diff, health=health_diff)


class GDB_464e:
    """引力失效增益 - Gravity Lapse Buff
    设置攻击力和生命值
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_762:
    """母舰 - Mothership
    12费 10/10 牧师随从 - 机械
    嘲讽
    战吼和亡语：随机获取两张星灵随从牌。
    
    Taunt
    Battlecry and Deathrattle: Get two random Protoss minions.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.BATTLECRY: True,
        GameTag.DEATHRATTLE: True,
    }
    race = Race.MECHANICAL
    
    def play(self):
        # 定义获取星灵随从的辅助函数
        def get_protoss_minions():
            """随机获取两张星灵随从牌"""
            # 获取所有星灵随从
            protoss_minions = self.game.cards.filter(
                type=CardType.MINION,
                race=Race.PROTOSS,
                collectible=True
            )
            
            # 随机选择两张
            for _ in range(2):
                if protoss_minions:
                    card = random.choice(protoss_minions)
                    Give(self.controller, card).run()
        
        # 随机获取两张星灵随从牌
        get_protoss_minions()
    
    def deathrattle(self):
        # 定义获取星灵随从的辅助函数（deathrattle 也需要）
        def get_protoss_minions():
            """随机获取两张星灵随从牌"""
            # 获取所有星灵随从
            protoss_minions = self.game.cards.filter(
                type=CardType.MINION,
                race=Race.PROTOSS,
                collectible=True
            )
            
            # 随机选择两张
            for _ in range(2):
                if protoss_minions:
                    card = random.choice(protoss_minions)
                    Give(self.controller, card).run()
        
        # 随机获取两张星灵随从牌
        get_protoss_minions()


# LEGENDARY

class GDB_442:
    """克乌雷，圣光领域 - K'ure, the Light Beyond
    3费 3/3 牧师随从
    法术迸发：召唤一个随机的法力值消耗为（3）的随从。
    （神圣法术不会移除此法术迸发。）
    
    Spellburst: Summon a random 3-Cost minion.
    (Holy spells don't remove this Spellburst.)
    """
    tags = {
        GameTag.SPELLBURST: True,
        GameTag.ELITE: True,
    }
    
    def _trigger_spellburst(self, player):
        """法术迸发触发逻辑"""
        # 召唤一个随机的3费随从
        Summon(self.controller, RandomCollectible(
            type=CardType.MINION,
            cost=3
        )).run()
        
        # 如果不是神圣法术，则移除法术迸发
        if not hasattr(source, 'spell_school') or source.spell_school != SpellSchool.HOLY:
            self.tags[GameTag.SPELLBURST] = False
    
    # 法术迸发：召唤一个随机的3费随从
    # 神圣法术不会移除此法术迸发
    events = OWN_SPELL_PLAY.on(
        lambda self, player, played_card, target=None: self._trigger_spellburst(played_card)
    )


class GDB_455:
    """阿斯卡拉 - Askara
    4费 4/4 牧师随从 - 德莱尼
    战吼：你使用的下一个德莱尼会召唤一个自身的复制。
    
    Battlecry: The next Draenei you play summons a copy of itself.
    """
    tags = {
        GameTag.BATTLECRY: True,
        GameTag.ELITE: True,
    }
    race = Race.DRAENEI
    
    def play(self):
        # 给控制者添加buff，使下一个德莱尼召唤复制
        Buff(self.controller, "GDB_455e").run()


class GDB_455e:
    """阿斯卡拉增益 - Askara Buff
    你使用的下一个德莱尼会召唤一个自身的复制
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    # 监听德莱尼打出事件
    # 使用MINION选择器并在lambda中过滤德莱尼种族
    events = Play(CONTROLLER, MINION).after(
        lambda self, player, played_card, target=None: [
            # 检查是否是德莱尼
            Summon(self.owner.controller, card.copy()).run() if card.race == Race.DRAENEI else None,
            # 移除此buff（无论是否是德莱尼都移除）
            Destroy(self).run() if card.race == Race.DRAENEI else None
        ]
    )

