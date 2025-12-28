from ..utils import *


##
# Minions


class DRG_062:
    """Wyrmrest Purifier / 龙眠净化者
    战吼： 将你牌库中的所有中立卡牌随机变形成为你的职业的卡牌。"""

    # [x]<b>Battlecry:</b> Transform all Neutral cards in your deck into random cards from
    # your class.
    play = Morph(FRIENDLY_DECK + NEUTRAL, RandomCollectible(card_class=FRIENDLY_CLASS))


class DRG_072:
    """Skyfin / 飞天鱼人
    战吼：如果你的手牌中有龙牌，随机召唤两个鱼人。"""

    # <b>Battlecry:</b> If you're holding a Dragon, summon 2 random Murlocs.
    powered_up = HOLDING_DRAGON
    play = powered_up & Summon(CONTROLLER, RandomMurloc()) * 2


class DRG_082:
    """Kobold Stickyfinger / 黏指狗头人
    战吼： 偷取对手的武器。"""

    # <b>Battlecry:</b> Steal your opponent's weapon.
    play = Steal(ENEMY_WEAPON)


class DRG_084:
    """Tentacled Menace / 触手恐吓者
    战吼：每个玩家抽一张牌，交换其法力值消耗。"""

    # <b>Battlecry:</b> Each player draws a card. Swap their_Costs.
    play = SwapStateBuff(Draw(CONTROLLER), Draw(OPPONENT), "DRG_084e")


class DRG_084e:
    cost = lambda self, i: self._xcost
    events = REMOVED_IN_PLAY


class DRG_086:
    """Chromatic Egg / 多彩龙卵
    战吼：秘密发现一条龙作为孵化对象。 亡语：破壳而出！"""

    # [x]<b>Battlecry:</b> Secretly <b>Discover</b> a Dragon to hatch into.
    # <b>Deathrattle:</b> Hatch!
    play = Discover(CONTROLLER, RandomDragon()).then(
        StoringBuff(SELF, "DRG_086e", Discover.CARD)
    )


class DRG_086e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, Copy(STORE_CARD))


class DRG_088:
    """Dread Raven / 恐惧渡鸦
    你每控制一只其他恐惧渡鸦，便拥有+3攻击力。"""

    # Has +3 Attack for each other Dread Raven you_control.
    update = Find(FRIENDLY_MINIONS + ID("DRG_088")) & Refresh(SELF, {GameTag.ATK: 3})


class DRG_092:
    """Transmogrifier / 幻化师
    每当你抽到一张牌时，随机将其变形成为一张传说随从牌。"""

    # Whenever you draw a card, transform it into a random <b>Legendary</b> minion.
    events = Draw(CONTROLLER).on(Morph(Draw.CARD, RandomLegendaryMinion()))


class DRG_401:
    """Grizzled Wizard / 灰发巫师
    战吼：直到你的下个回合，和你的对手交换英雄技能。"""

    # <b>Battlecry:</b> Swap Hero Powers with your opponent until your next turn.
    play = (
        Swap(FRIENDLY_HERO_POWER, ENEMY_HERO_POWER),
        Buff(CONTROLLER, "DRG_401e"),
    )


class DRG_401e:
    events = OWN_TURN_BEGIN.on(
        Swap(FRIENDLY_HERO_POWER, ENEMY_HERO_POWER),
        Destroy(SELF),
    )


class DRG_403:
    """Blowtorch Saboteur / 喷灯破坏者
    战吼：你对手的下一个英雄技能的法力值消耗增加（2）点。"""

    # <b>Battlecry:</b> Your opponent's next Hero Power costs (3).
    play = Buff(ENEMY_HERO_POWER, "DRG_403e")


class DRG_403e:
    update = Refresh(ENEMY_HERO_POWER, {GameTag.COST: SET(3)})
    events = Activate(None, OWNER).on(Destroy(SELF))
