"""
暗月马戏团 - 圣骑士
"""
from ..utils import *


##
# Minions

class DMF_064:
    """旋转木马 - Carousel Gryphon
    圣盾。腐蚀：获得+3/+3和嘲讽。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.DIVINE_SHIELD: True,
    }
    corrupt = Buff(SELF, "DMF_064e")


class DMF_064e:
    """+3/+3和嘲讽"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.TAUNT: True,
    }


class DMF_194:
    """赤鳞驯龙者 - Redscale Dragontamer
    亡语：抽一张龙牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    deathrattle = ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + DRAGON)


class DMF_235:
    """气球商人 - Balloon Merchant
    战吼：使你的白银之手新兵获得+1攻击力和圣盾。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 1,
        GameTag.COST: 4,
    }
    play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "DMF_235e")  # Silver Hand Recruit


class DMF_235e:
    """+1攻击力和圣盾"""
    tags = {
        GameTag.ATK: 1,
        GameTag.DIVINE_SHIELD: True,
    }


class DMF_237:
    """狂欢报幕员 - Carnival Barker
    每当你召唤一个生命值为1的随从，便使其获得+1/+2。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    events = Summon(CONTROLLER, MINION + (HEALTH == 1)).after(
        Buff(EVENT_TARGET, "DMF_237e")
    )


class DMF_237e:
    """+1/+2"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class DMF_240:
    """救赎者洛萨克森 - Lothraxion the Redeemed
    战吼：在本局对战的剩余时间内，在你召唤一个白银之手新兵后，使其获得圣盾。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    play = Buff(CONTROLLER, "DMF_240e")


class DMF_240e:
    """洛萨克森的祝福"""
    events = Summon(CONTROLLER, ID("CS2_101t")).after(  # Silver Hand Recruit
        Buff(EVENT_TARGET, "DMF_240e2")
    )


class DMF_240e2:
    """圣盾"""
    tags = {
        GameTag.DIVINE_SHIELD: True,
    }


class DMF_241:
    """大主教伊瑞尔 - High Exarch Yrel
    战吼：如果你的牌库中没有中立牌，便获得突袭、吸血、嘲讽和圣盾。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 5,
        GameTag.COST: 8,
    }
    play = Find(~(FRIENDLY_DECK + NEUTRAL)) & Buff(SELF, "DMF_241e")


class DMF_241e:
    """纯粹祝福"""
    tags = {
        GameTag.RUSH: True,
        GameTag.LIFESTEAL: True,
        GameTag.TAUNT: True,
        GameTag.DIVINE_SHIELD: True,
    }


class YOP_010:
    """被禁锢的星骓 - Imprisoned Celestial
    休眠2回合。法术迸发：使你的所有随从获得圣盾。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
    }
    spellburst = Buff(FRIENDLY_MINIONS, "YOP_010e")


class YOP_010e:
    """圣盾"""
    tags = {
        GameTag.DIVINE_SHIELD: True,
    }


##
# Spells

class DMF_195:
    """零食大冲关 - Snack Run
    发现一张法术牌。为你的英雄恢复等同于该牌法力值消耗的生命值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    
    # 使用标准的 Discover().then() 模式
    # 参考 KAR_057 (象牙骑士) 的实现
    play = Discover(CONTROLLER, RandomSpell()).then(
        Give(CONTROLLER, Discover.CARD), 
        Heal(FRIENDLY_HERO, COST(Discover.CARD))
    )


class DMF_236:
    """古神在上 - Oh My Yogg!
    奥秘：当你的对手施放一个法术时，改为施放一个法力值消耗相同的随机法术。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SECRET: True,
    }
    # 拦截对手法术并替换成相同费用的随机法术
    secret = Play(OPPONENT, SPELL).on(
        Reveal(SELF),
        Counter(Play.CARD),  # 取消对手的法术
        CastSpell(RandomSpell(cost=COST(Play.CARD)))  # 施放相同费用的随机法术
    )


class DMF_244:
    """游园日 - Day at the Faire
    召唤三个白银之手新兵。腐蚀：改为召唤五个。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Summon(CONTROLLER, "CS2_101t") * 3  # Silver Hand Recruit
    corrupt = Summon(CONTROLLER, "CS2_101t") * 5


##
# Weapons

class DMF_238:
    """纳鲁之锤 - Hammer of the Naaru
    战吼：召唤一个6/6并具有嘲讽的神圣元素。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 3,
        GameTag.COST: 6,
    }
    play = Summon(CONTROLLER, "DMF_238t")


class DMF_238t:
    """神圣元素 - Holy Elemental"""
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6,
        GameTag.COST: 6,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.TAUNT: True,
    }


class YOP_011:
    """审判圣契 - Libram of Judgment
    腐蚀：获得吸血。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 5,
        GameTag.DURABILITY: 3,
        GameTag.COST: 7,
    }
    corrupt = Buff(SELF, "YOP_011e")


class YOP_011e:
    """吸血"""
    tags = {
        GameTag.LIFESTEAL: True,
    }
