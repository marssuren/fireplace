from ..utils import *


##
# Minions


class GVG_023:
    """Goblin Auto-Barber / 地精自动理发装置
    战吼：使你的武器获得+1攻击力。"""

    play = Buff(FRIENDLY_WEAPON, "GVG_023a")


GVG_023a = buff(atk=1)


class GVG_025:
    """One-eyed Cheat / 独眼欺诈者
    每当你召唤一个海盗，便获得潜行。"""

    events = Summon(CONTROLLER, PIRATE - SELF).on(Stealth(SELF))


class GVG_027:
    """Iron Sensei / 钢铁武道家
    在你的回合结束时，使另一个友方机械获得+2/+2。"""

    events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_027e"))


GVG_027e = buff(+2, +2)


class GVG_028:
    """Trade Prince Gallywix / 加里维克斯
    每当你的对手施放一个法术，获得该法术的复制，并使其获得一张幸运币。"""

    events = Play(OPPONENT, SPELL - ID("GVG_028t")).on(
        Give(CONTROLLER, Copy(Play.CARD)), Give(OPPONENT, "GVG_028t")
    )


class GVG_028t:
    play = ManaThisTurn(CONTROLLER, 1)


class GVG_088:
    """Ogre Ninja / 食人魔忍者
    潜行，50%几率攻击错误的敌人。"""

    events = FORGETFUL


##
# Spells


class GVG_022:
    """Tinker's Sharpsword Oil / 修补匠的磨刀油
    使你的武器获得+3攻击力。连击：随机使一个友方随从获得+3攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(FRIENDLY_WEAPON, "GVG_022a")
    combo = Buff(FRIENDLY_WEAPON, "GVG_022a"), Buff(
        RANDOM_FRIENDLY_CHARACTER, "GVG_022b"
    )


GVG_022a = buff(atk=3)  # Weapon
GVG_022b = buff(atk=3)  # Minion


class GVG_047:
    """Sabotage / 暗中破坏
    随机消灭一个敌方随从，连击：并且摧毁你对手的武器。"""

    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Destroy(RANDOM_ENEMY_MINION)
    combo = Destroy(ENEMY_WEAPON | RANDOM_ENEMY_MINION)


##
# Weapons


class GVG_024:
    """Cogmaster's Wrench / 齿轮大师的扳手
    如果你控制任何机械，便拥有 +2攻击力。"""

    update = Find(FRIENDLY_MINIONS + MECH) & Refresh(SELF, {GameTag.ATK: +2})
