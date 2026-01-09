from ..utils import *


##
# Minions


class ICC_062:
    """Mountainfire Armor / 熔甲卫士
    亡语：如果此时是你对手的回合，则获得 6点护甲值。"""

    deathrattle = (CurrentPlayer(OPPONENT), GainArmor(FRIENDLY_HERO, 6))


class ICC_238:
    """Animated Berserker / 活化狂战士
    在你使用一张随从牌后，对其造成1点 伤害。"""

    events = Play(CONTROLLER, MINION).after(Hit(Play.CARD, 1))


class ICC_405:
    """Rotface / 腐面
    在本随从受到伤害并存活下来后，随机召唤一个传说随从。"""

    events = SELF_DAMAGE.on(Summon(CONTROLLER, RandomLegendaryMinion()))


class ICC_408:
    """Val'kyr Soulclaimer / 瓦格里摄魂者
    在本随从受到伤害并存活下来后，召唤一个2/2的食尸鬼。"""

    events = SELF_DAMAGE.on(Summon(CONTROLLER, "ICC_900t"))


class ICC_450:
    """Death Revenant / 死亡幽魂
    战吼：每有一个受伤的随从，便获得+1/+1。"""

    play = Buff(SELF, "ICC_450e") * Count(ALL_MINIONS + DAMAGED)


ICC_450e = buff(+1, +1)


##
# Spells


class ICC_091:
    """Dead Man's Hand / 亡者之牌
    复制你的手牌并洗入你的牌库。"""

    play = Shuffle(CONTROLLER, ExactCopy(FRIENDLY_HAND))


class ICC_281:
    """Forge of Souls / 灵魂洪炉
    从你的牌库中抽两张武器牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON)) * 2


class ICC_837:
    """Bring It On! / 放马过来
    获得10点护甲值。使你对手的手牌中所有随从牌的法力值消耗减少（2）点。"""

    play = GainArmor(FRIENDLY_HERO, 10), Buff(ENEMY_HAND + MINION, "ICC_837e")


class ICC_837e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -2}


##
# Weapons


class ICC_064:
    """Blood Razor / 血刃剃刀
    [x]战吼，亡语： 对所有随从造成 1点伤害。"""

    play = Hit(ALL_MINIONS, 1)
    deathrattle = Hit(ALL_MINIONS, 1)


##
# Heros


class ICC_834:
    """Scourgelord Garrosh / 天灾领主加尔鲁什
    战吼：装备一把4/3的影之哀伤，影之哀伤同时对其攻击目标相邻的随从造成伤害。"""

    play = Summon(CONTROLLER, "ICC_834w")


class ICC_834h:
    activate = Hit(ALL_MINIONS, 1)


class ICC_834w:
    events = Attack(FRIENDLY_HERO).on(
        Hit(ADJACENT(Attack.DEFENDER), ATK(FRIENDLY_HERO))
    )
