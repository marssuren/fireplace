from ..utils import *


##
# Minions


class OG_303:
    """Cult Sorcerer / 异教女巫
    法术伤害+1 在你施放一个法术后，使你的克苏恩获得+1/+1（无论它在哪里）。"""

    events = OWN_SPELL_PLAY.after(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


class OG_083:
    """Twilight Flamecaller / 暮光烈焰召唤者
    战吼：对所有敌方随从造成1点伤害。"""

    play = Hit(ENEMY_MINIONS, 1)


class OG_085:
    """Demented Frostcaller / 癫狂的唤冰者
    在你施放一个法术后，随机冻结 一个敌人。"""

    events = OWN_SPELL_PLAY.after(Freeze(RANDOM(ENEMY_CHARACTERS - DEAD - FROZEN)))


class OG_120:
    """Anomalus / 阿诺玛鲁斯
    亡语：对所有随从造成8点伤害。"""

    deathrattle = Hit(ALL_MINIONS, 8)


class OG_207:
    """Faceless Summoner / 无面召唤者
    战吼：随机召唤一个法力值消耗为（3）的随从。"""

    play = Summon(CONTROLLER, RandomMinion(cost=3))


class OG_087:
    """Servant of Yogg-Saron / 尤格-萨隆的仆从
    战吼：随机施放一个法力值消耗大于或等于（5）点的法术（目标随机而定）。"""

    play = CastSpell(RandomSpell(id="DS1_184"))


##
# Spells


class OG_081:
    """Shatter / 冰爆
    消灭一个被冻结的随从。"""

    requirements = {
        PlayReq.REQ_FROZEN_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET)


class OG_090:
    """Cabalist's Tome / 秘法宝典
    随机获取3张法师法术牌。"""

    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 3


class OG_086:
    """Forbidden Flame / 禁忌烈焰
    消耗你所有的法力值，对一个随从造成等同于所消耗法力值数量的伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
        Hit(TARGET, SpendMana.AMOUNT)
    )
