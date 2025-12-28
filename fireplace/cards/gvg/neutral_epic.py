from ..utils import *


##
# Minions


class GVG_016:
    """Fel Reaver / 魔能机甲
    每当你的对手使用一张卡牌时，便移除你的牌库顶的三张牌。"""

    events = Play(OPPONENT).on(Mill(CONTROLLER) * 3)


class GVG_092:
    """Gnomish Experimenter / 侏儒实验技师
    战吼： 抽一张牌，如果该牌是随从牌，则将其变形成为一只小鸡。"""

    play = Draw(CONTROLLER).then(
        Find(MINION + Draw.CARD) & Morph(Draw.CARD, "GVG_092t")
    )


class GVG_104:
    """Hobgoblin / 大胖
    每当你使用一张攻击力为1的随从牌，便使其获得+2/+2。"""

    events = Play(CONTROLLER, MINION + (ATK == 1)).on(Buff(Play.CARD, "GVG_104a"))


GVG_104a = buff(+2, +2)


class GVG_105:
    """Piloted Sky Golem / 载人飞天魔像
    亡语：随机召唤一个法力值消耗为（4）的随从。"""

    deathrattle = Summon(CONTROLLER, RandomMinion(cost=4))


class GVG_106:
    """Junkbot / 回收机器人
    每当一个友方机械死亡，便获得+2/+2。"""

    events = Death(FRIENDLY + MECH).on(Buff(SELF, "GVG_106e"))


GVG_106e = buff(+2, +2)


class GVG_107:
    """Enhance-o Mechano / 强化机器人
    战吼：随机使你的其他随从分别获得风怒，嘲讽，或者圣盾效果中的一种。"""

    def play(self):
        for target in (FRIENDLY_MINIONS - SELF).eval(self.game, self):
            tag = self.game.random.choice(
                (GameTag.WINDFURY, GameTag.TAUNT, GameTag.DIVINE_SHIELD)
            )
            yield SetTags(target, (tag,))


class GVG_108:
    """Recombobulator / 侏儒变形师
    战吼： 将一个友方随从随机变形成为一个法力值消耗相同的随从。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Morph(TARGET, RandomMinion(cost=COST(TARGET)))


class GVG_121:
    """Clockwork Giant / 发条巨人
    你的对手每有一张手牌，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Count(ENEMY_HAND)


class GVG_122:
    """Wee Spellstopper / 小个子扰咒师
    相邻的随从拥有扰魔。"""

    update = Refresh(
        SELF_ADJACENT,
        {
            GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
            GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
        },
    )
