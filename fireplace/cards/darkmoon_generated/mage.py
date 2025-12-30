"""
暗月马戏团 - 法师
"""
from ..utils import *


##
# Minions

class DMF_100:
    """甜点飓风 - Confection Cyclone
    战吼：将两张1/2的糖元素牌置入你的手牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = Give(CONTROLLER, "DMF_100t") * 2


class DMF_100t:
    """糖元素 - Sugar Elemental"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        GameTag.RACE: Race.ELEMENTAL,
    }


class DMF_101:
    """焰火元素 - Firework Elemental
    战吼：对一个随从造成3点伤害。腐蚀：改为造成12点伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)
    corrupt = Hit(TARGET, 12)


class DMF_102:
    """游戏管理员 - Game Master
    你在每回合中打出的第一张奥秘牌的法力值消耗为(1)点。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    # TODO: 实现"每回合第一张奥秘减费"的光环效果
    # 需要追踪每回合打出的奥秘数量
    update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(1)})


class DMF_106:
    """隐秘咒术师 - Occult Conjurer
    战吼：如果你控制一个奥秘，便召唤一个本随从的复制。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    play = Find(FRIENDLY_SECRETS) & Summon(CONTROLLER, ExactCopy(SELF))


class DMF_109:
    """暗月先知塞格 - Sayge, Seer of Darkmoon
    战吼：抽一张牌。（你在本局对战中每触发一个友方奥秘，便升级一次！）
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    # 简化实现：抽1张牌
    # 完整实现需要追踪奥秘触发次数
    play = Draw(CONTROLLER)


class YOP_020:
    """冰川竞速者 - Glacier Racer
    法术迸发：对所有被冻结的敌人造成3点伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    spellburst = Hit(ENEMY + FROZEN, 3)


##
# Spells

class DMF_103:
    """克苏恩面具 - Mask of C'Thun
    随机对所有敌人造成共10点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * 10


class DMF_104:
    """华丽谢幕 - Grand Finale
    召唤一个8/8的元素。你在上个回合中每打出一张元素牌，便重复一次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
    }
    # 简化实现：召唤1个8/8元素
    # 完整实现需要追踪上回合打出的元素数量
    play = Summon(CONTROLLER, "DMF_104t")


class DMF_104t:
    """元素 - Elemental"""
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 8,
        GameTag.RACE: Race.ELEMENTAL,
    }


class DMF_105:
    """套圈圈 - Ring Toss
    发现一张奥秘牌并施放。腐蚀：改为发现2张。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, cards=SECRET + MAGE_CLASS))
    # TODO: 自动施放发现的奥秘
    corrupt = GenericChoice(CONTROLLER, Discover(CONTROLLER, cards=SECRET + MAGE_CLASS)) * 2


class DMF_107:
    """非公平游戏 - Rigged Faire Game
    奥秘：如果你在对手的回合中没有受到任何伤害，便抽三张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
    }
    # TODO: 实现追踪对手回合伤害的机制
    # 简化实现：在对手回合结束时触发
    secret = OppTurnEnd(CONTROLLER).on(
        Draw(CONTROLLER) * 3,
        Reveal(SELF),
    )


class DMF_108:
    """愚人套牌 - Deck of Lunacy
    将你牌库中的法术牌变形成为法力值消耗多(3)点的法术牌。（保留原本的法力值消耗。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    # TODO: 实现牌库法术变形但保留费用的复杂机制
    # 这需要扩展核心代码，暂时简化
    play = Morph(FRIENDLY_DECK + SPELL, RandomSpell(cost=COST(SELF) + 3))


class YOP_019:
    """制造法力饼干 - Conjure Mana Biscuit
    将一张饼干牌置入你的手牌，该牌可以使你恢复2个法力水晶。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    play = Give(CONTROLLER, "YOP_019t")


class YOP_019t:
    """法力饼干 - Mana Biscuit"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    play = ManaThisTurn(CONTROLLER, 2)
