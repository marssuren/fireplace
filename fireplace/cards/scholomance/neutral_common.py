from ..utils import *


##
# Minions

class SCH_145:
    """Desk Imp / 课桌小鬼
    """
    # 0费 1/1 香草随从，无特殊效果
    pass

class SCH_311:
    """Animated Broomstick / 活化扫帚
    Rush Battlecry: Give your other minions Rush."""

    # 突袭。战吼：使你的其他随从获得突袭
    play = Buff(FRIENDLY_MINIONS - SELF, "SCH_311e")


SCH_311e = buff(rush=True)

class SCH_231:
    """Intrepid Initiate / 新生刺头
    Spellburst: Gain +2 Attack."""

    # 法术迸发：获得+2攻击力
    spellburst = Buff(SELF, "SCH_231e")


SCH_231e = buff(atk=2)
class SCH_248:
    """Pen Flinger / 甩笔侏儒
    Battlecry: Deal 1 damage to a minion. Spellburst: Return this to your hand."""

    # 战吼：对一个随从造成1点伤害
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1)

    # 法术迸发：将本随从移回你的手牌
    spellburst = Bounce(SELF)
class SCH_312:
    """Tour Guide / 巡游向导
    Battlecry: Your next Hero Power costs (0)."""

    # 战吼：你的下一个英雄技能的法力值消耗为（0）点
    play = Buff(FRIENDLY_HERO_POWER, "SCH_312e")


class SCH_312e:
    cost = SET(0)
    events = REMOVED_IN_PLAY
class SCH_350:
    """Wand Thief / 魔杖窃贼
    Combo: Discover a Mage spell."""

    # 连击：发现一张法师法术牌
    combo = Discover(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))
class SCH_283:
    """Manafeeder Panthara / 食魔影豹
    Battlecry: If you've used your Hero Power this turn, draw a card."""

    # 战吼：在本回合中，如果你使用过你的英雄技能，抽一张牌
    play = Find(FRIENDLY_HERO_POWER + EXHAUSTED) & Draw(CONTROLLER)
class SCH_708:
    """Sneaky Delinquent / 少年惯偷
    Stealth. Deathrattle: Add a 3/1 Ghost with Stealth to your hand."""

    # 潜行（在CardDefs.xml中已定义）
    # 亡语：将一张3/1并具有潜行的鬼灵置入你的手牌
    deathrattle = Give(CONTROLLER, "SCH_708t")


class SCH_708t:
    """Spectral Delinquent / 幽灵惯偷
    3/1 with Stealth"""
    # Token: 3/1 潜行鬼灵（属性在CardDefs.xml中定义）
    pass


class SCH_160:
    """Wandmaker / 魔杖工匠
    Battlecry: Add a 1-Cost spell from your class to your hand."""

    # 战吼：随机将一张你职业的法力值消耗为（1）的法术牌置入你的手牌
    play = Give(CONTROLLER, RandomSpell(cost=1, card_class=FRIENDLY_CLASS))
class SCH_232:
    """Crimson Hothead / 赤红急先锋
    Spellburst: Gain +1 Attack and Taunt."""

    # 法术迸发：获得+1攻击力和嘲讽
    spellburst = Buff(SELF, "SCH_232e")


SCH_232e = buff(atk=1, taunt=True)
class SCH_143:
    """Divine Rager / 神圣暴怒者
    Divine Shield"""

    # 圣盾（无需额外代码，CardDefs.xml中已定义）
    pass
class SCH_707:
    """Fishy Flyer / 鱼人飞骑
    Rush. Deathrattle: Add a 4/3 Ghost with Rush to your hand."""

    # 突袭（在CardDefs.xml中已定义）
    # 亡语：将一张4/3并具有突袭的鬼灵置入你的手牌
    deathrattle = Give(CONTROLLER, "SCH_707t")


class SCH_707t:
    """Spectral Flyer / 幽灵飞骑
    4/3 with Rush"""
    # Token: 4/3 突袭鬼灵（属性在CardDefs.xml中定义）
    pass


class SCH_313:
    """Wretched Tutor / 失心辅导员
    Spellburst: Deal 2 damage to all other minions."""

    # 法术迸发：对所有其他随从造成2点伤害
    spellburst = Hit(ALL_MINIONS - SELF, 2)

class SCH_605:
    """Lake Thresher / 止水湖蛇颈龙
    Also damages the minions next to whomever this attacks."""

    # 同时对攻击目标相邻的随从造成伤害
    # 这个效果需要在攻击时触发，类似于"劈斩"效果
    events = Attack(SELF).after(Hit(ADJACENT(ATTACK_TARGET), ATK(SELF)))

class SCH_710:
    """Ogremancer / 食人魔巫术师
    Whenever your opponent casts a spell, summon a 2/2 Skeleton with Taunt."""

    # 每当你的对手施放一个法术，召唤一个2/2并具有嘲讽的骷髅
    events = Play(OPPONENT, SPELL).on(Summon(CONTROLLER, "SCH_710t"))


class SCH_710t:
    """Risen Skeleton / 复活的骷髅
    2/2 with Taunt"""
    # Token: 2/2 嘲讽骷髅（属性在CardDefs.xml中定义）
    pass


class SCH_245:
    """Steward of Scrolls / 卷轴管理者
    Spell Damage +1. Battlecry: Discover a spell."""

    # 法术伤害+1（在CardDefs.xml中已定义）
    # 战吼：发现一张法术牌
    play = Discover(CONTROLLER, RandomSpell())
class SCH_230:
    """Onyx Magescribe / 黑岩法术抄写员
    Spellburst: Add 2 random spells from your class to your hand."""

    # 法术迸发：随机将两张你职业的法术牌置入你的手牌
    spellburst = Give(CONTROLLER, RandomSpell(card_class=FRIENDLY_CLASS) * 2)
class SCH_709:
    """Smug Senior / 傲慢的大四学长
    Taunt. Deathrattle: Add a 5/7 Ghost with Taunt to your hand."""

    # 嘲讽（在CardDefs.xml中已定义）
    # 亡语：将一张5/7并具有嘲讽的鬼灵置入你的手牌
    deathrattle = Give(CONTROLLER, "SCH_709t")


class SCH_709t:
    """Spectral Senior / 幽灵学长
    5/7 with Taunt"""
    # Token: 5/7 嘲讽鬼灵（属性在CardDefs.xml中定义）
    pass


class SCH_530:
    """Sorcerous Substitute / 魔法替身
    Battlecry: If you have Spell Damage, summon a copy of this."""

    # 战吼：如果你拥有法术伤害，召唤一个本随从的复制
    play = (Find(FRIENDLY_MINIONS + SPELLPOWER), Summon(CONTROLLER, ExactCopy(SELF)))

class SCH_711:
    """Plagued Protodrake / 魔疫始祖幼龙
    Deathrattle: Summon a random 7-Cost minion."""

    # 亡语：召唤一个随机的法力值消耗为（7）的随从
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=7))


##
# Spells

class SCH_270:
    """Primordial Studies / 原初研习
    Discover a Spell Damage minion. Your next one costs (1) less."""

    # 发现一个法术伤害随从。你的下一个法术伤害随从的法力值消耗减少（1）点
    # 这是一个"研习"系列卡牌，需要给予费用减免buff
    play = Discover(CONTROLLER, RandomMinion(spellpower=True)), Buff(CONTROLLER, "SCH_270e")

class SCH_623:
    """Cutting Class / 逃课
    Draw 2 cards. Costs (1) less per Attack of your weapon."""

    # 抽两张牌。本牌的法力值消耗每有你的武器的攻击力点数便减少（1）点
    # 费用减免在CardDefs.xml中通过COST_MANAGER实现
    play = Draw(CONTROLLER) * 2
