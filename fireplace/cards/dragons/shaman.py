from ..utils import *


##
# Minions


class DRG_096:
    """Bandersmosh / 班德斯莫什
    如果这张牌在你的手牌中，每个回合都会随机变成一张传说随从牌的5/5的复制。"""

    # [x]Each turn this is in your hand, transform it into a 5/5 copy of a random
    # <b>Legendary</b> minion.
    class Hand:
        events = OWN_TURN_BEGIN.on(
            Morph(SELF, RandomLegendaryMinion()).then(Buff(Morph.CARD, "DRG_096e"))
        )


class DRG_096e:
    class Hand:
        events = OWN_TURN_BEGIN.on(
            Morph(OWNER, RandomLegendaryMinion()).then(Buff(Morph.CARD, "DRG_096e"))
        )

    events = REMOVED_IN_PLAY


class DRG_096e2:
    atk = SET(5)
    max_health = SET(5)


class DRG_216:
    """Surging Tempest / 电涌风暴
    当你有过载的法力水晶时，拥有+1 攻击力。"""

    # Has +1 Attack while you_have <b>Overloaded</b> Mana Crystals.
    update = OVERLOADED(CONTROLLER) & Refresh(SELF, {GameTag.ATK: 1})


class DRG_218:
    """Corrupt Elementalist / 堕落的元素师
    战吼：祈求迦拉克隆两次。"""

    # <b>Battlecry:</b> <b>Invoke</b> Galakrond twice.
    play = INVOKE, INVOKE


class DRG_223:
    """Cumulo-Maximus / 遮天雨云
    战吼：如果你有过载的法力水晶，造成5点伤害。"""

    # <b>Battlecry:</b> If you have <b>Overloaded</b> Mana Crystals, deal 5 damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_HAS_OVERLOADED_MANA: 0}
    powered_up = OVERLOADED(CONTROLLER)
    play = powered_up & Hit(TARGET, 5)


class DRG_224:
    """Nithogg / 尼索格
    战吼：召唤两个0/3的龙卵。下个回合它们将孵化为4/4并具有突袭的幼龙。"""

    # [x]<b>Battlecry:</b> Summon two 0/3 Eggs. Next turn they hatch into 4/4 Drakes with
    # <b>Rush</b>.
    play = SummonBothSides(CONTROLLER, "DRG_224t") * 2


class DRG_224t:
    events = OWN_TURN_BEGIN.on(Morph(SELF, "DRG_224t2"))


##
# Spells


class DRG_215:
    """Storm's Wrath / 风暴狂怒
    使你的所有随从获得+1/+1。 过载：（1）"""

    # Give your minions +1/+1. <b>Overload:</b> (1)
    play = Buff(FRIENDLY_MINIONS, "DRG_215e")


DRG_215e = buff(+1, +1)


class DRG_217:
    """Dragon's Pack / 巨龙的兽群
    召唤两只2/3并具有嘲讽的幽灵狼。如果你已经祈求过两次，则使它们获得+3/+3。"""

    # Summon two 2/3 Spirit Wolves with <b>Taunt</b>. If you've <b>Invoked</b> twice, give
    # them +2/+2.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    powered_up = INVOKED_TWICE
    play = powered_up & (
        Summon(CONTROLLER, "DRG_217t").then(Buff(Summon.CARD, "DRG_217e")) * 2
    ) | (Summon(CONTROLLER, "DRG_217t") * 2)


DRG_217e = buff(+2, +2)


class DRG_219:
    """Lightning Breath / 闪电吐息
    对一个随从造成$4点伤害。如果你的手牌中有龙牌，则同样对其相邻随从造成伤害。"""

    # [x]Deal $4 damage to a minion. If you're holding a Dragon, also damage its neighbors.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0,
    }
    powered_up = HOLDING_DRAGON
    play = Hit(TARGET, 4), powered_up & Hit(TARGET_ADJACENT, 4)


class DRG_248:
    """Invocation of Frost / 霜之祈咒
    冻结一个敌人。祈求迦拉克隆。"""

    # <b>Freeze</b> an enemy. <b>Invoke</b> Galakrond.
    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Freeze(TARGET), INVOKE


##
# Heros


class DRG_620(GalakrondUtils):
    """Galakrond, the Tempest"""

    # [x]<b>Battlecry:</b> Summon two 2/2 Storms with <b>Rush</b>. <i>(@)</i>
    progress_total = 2
    play = Summon(CONTROLLER, "DRG_620t4") * 2
    reward = Find(SELF + FRIENDLY_HERO) | Morph(SELF, "DRG_620t2")


class DRG_620t2(GalakrondUtils):
    """Galakrond, the Apocalypse"""

    # [x]<b>Battlecry:</b> Summon two 4/4 Storms with <b>Rush</b>. <i>(@)</i>
    progress_total = 2
    play = Summon(CONTROLLER, "DRG_620t5") * 2
    reward = Find(SELF + FRIENDLY_HERO) | Morph(SELF, "DRG_620t3")


class DRG_620t3:
    """Galakrond, Azeroth's End"""

    # [x]<b>Battlecry:</b> Summon two 8/8 Storms with <b>Rush</b>. Equip a 5/2 Claw.
    play = (Summon(CONTROLLER, "DRG_620t6") * 2, Summon(CONTROLLER, "DRG_238ht"))


class DRG_238p4:
    """Galakrond's Fury"""

    # <b>Hero Power</b> Summon a 2/1 Elemental with <b>Rush</b>.
    activate = Summon(CONTROLLER, "DRG_238t14t3")
