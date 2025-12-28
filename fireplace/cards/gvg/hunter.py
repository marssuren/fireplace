from ..utils import *


##
# Minions


class GVG_046:
    """King of Beasts / 百兽之王
    嘲讽 你每控制一只其他野兽，便拥有+1攻击力。"""

    play = Buff(SELF, "GVG_046e") * Count(FRIENDLY_MINIONS + BEAST)


GVG_046e = buff(atk=1)


class GVG_048:
    """Metaltooth Leaper / 金刚刃牙兽
    战吼：使你的其他机械获得+2攻击力。"""

    play = Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_048e")


GVG_048e = buff(atk=2)


class GVG_049:
    """Gahz'rilla / 加兹瑞拉
    每当本随从受到伤害，其攻击力翻倍。"""

    events = SELF_DAMAGE.on(Buff(SELF, "GVG_049e"))


class GVG_049e:
    atk = lambda self, i: i * 2


class GVG_087:
    """Steamwheedle Sniper / 热砂港狙击手
    你的英雄技能能够以随从为目标。"""

    update = Refresh(CONTROLLER, {GameTag.STEADY_SHOT_CAN_TARGET: True})


##
# Spells


class GVG_017:
    """Call Pet / 召唤宠物
    抽一张牌。如果该牌是野兽牌，则其法力值消耗 减少（4）点。"""

    play = Draw(CONTROLLER).then(Find(BEAST + Draw.CARD) & Buff(Draw.CARD, "GVG_017e"))


@custom_card
class GVG_017e:
    events = REMOVED_IN_PLAY
    tags = {
        GameTag.CARDNAME: "Call Pet Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -4,
    }


class GVG_026:
    """Feign Death / 假死
    触发所有友方随从的亡语。"""

    play = Deathrattle(FRIENDLY_MINIONS)


class GVG_073:
    """Cobra Shot / 眼镜蛇射击
    对一个随从和敌方英雄造成$3点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET | ENEMY_HERO, 3)


##
# Weapons


class GVG_043:
    """Glaivezooka / 重型刃弩
    战吼：随机使一个友方随从获得+1攻击力。"""

    play = Buff(RANDOM_FRIENDLY_MINION, "GVG_043e")


GVG_043e = buff(atk=1)
