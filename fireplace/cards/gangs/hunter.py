from ..utils import *


##
# Minions


class CFM_315:
    """Alleycat / 雄斑虎
    战吼：召唤一个1/1的雌斑虎。"""

    play = Summon(CONTROLLER, "CFM_315t")


class CFM_316:
    """Rat Pack / 瘟疫鼠群
    亡语：召唤若干个1/1的老鼠，数量等同于本随从的攻击力。"""

    deathrattle = Summon(CONTROLLER, "CFM_316") * ATK(SELF)


class CFM_333:
    """Knuckles / 金手指纳克斯
    在纳克斯攻击一名随从后，还会命中敌方英雄。"""

    events = Attack(SELF, ALL_MINIONS).after(Hit(ENEMY_HERO, ATK(SELF)))


class CFM_335:
    """Dispatch Kodo / 驮运科多兽
    战吼：造成等同于本随从攻击力的伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, ATK(SELF))


class CFM_336:
    """Shaky Zipgunner / 豺狼人土枪手
    亡语：随机使你手牌中的一张随从牌获得+2/+2。"""

    deathrattle = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_336e")


CFM_336e = buff(+2, +2)


class CFM_338:
    """Trogg Beastrager / 穴居人驯兽师
    战吼：随机使你手牌中的一张野兽牌获得+1/+1。"""

    play = Buff(RANDOM(FRIENDLY_HAND + BEAST), "CFM_338e")


CFM_338e = buff(+1, +1)


##
# Spells


class CFM_026:
    """Hidden Cache / 军备宝箱
    奥秘：在你的对手使用一张随从牌后，随机使你手牌中的一张随从牌获得+2/+2。"""

    secret = Play(OPPONENT, MINION).after(
        Reveal(SELF), Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_026e")
    )


CFM_026e = buff(+2, +2)


class CFM_334:
    """Smuggler's Crate / 走私货物
    随机使你手牌中的一张野兽牌获得+2/+2。"""

    play = Buff(RANDOM(FRIENDLY_HAND + BEAST), "CFM_334e")


CFM_334e = buff(+2, +2)


##
# Weapons


class CFM_337:
    """Piranha Launcher / 食人鱼喷枪
    在你的英雄攻击后，召唤一个1/1的食人鱼。"""

    events = Attack(FRIENDLY_HERO, MINION).after(Summon(CONTROLLER, "CFM_337t"))
