from ..utils import *


##
# Minions


class OG_042:
    """Y'Shaarj, Rage Unbound / 亚煞极
    在你的回合结束时，将一个随从从你的牌库置入战场。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)))


class OG_122:
    """Mukla, Tyrant of the Vale / 山谷之王穆克拉
    战吼：将两根香蕉置入你的手牌。"""

    play = Give(CONTROLLER, "EX1_014t") * 2


class OG_317:
    """Deathwing, Dragonlord / 黑龙领主死亡之翼
    亡语：将你手牌中所有的龙牌置入战场。"""

    deathrattle = Summon(CONTROLLER, FRIENDLY_HAND + DRAGON)


class OG_318:
    """Hogger, Doom of Elwynn / 艾尔文灾星霍格
    每当本随从受到伤害，召唤一个2/2并具有嘲讽的豺狼人。"""

    events = SELF_DAMAGE.on(Summon(CONTROLLER, "OG_318t"))


class OG_338:
    """Nat, the Darkfisher / 阴暗渔夫纳特
    你的对手在回合开始时，有50%的几率额外抽一张牌。"""

    events = BeginTurn(OPPONENT).on(COINFLIP & Draw(OPPONENT))


class OG_123:
    """Shifter Zerus / 百变泽鲁斯
    如果这张牌在你的手牌中，每个回合都会随机变成一张随从牌。"""

    class Hand:
        events = OWN_TURN_BEGIN.on(
            Morph(SELF, RandomMinion()).then(Buff(Morph.CARD, "OG_123e"))
        )


class OG_123e:
    class Hand:
        events = OWN_TURN_BEGIN.on(
            Morph(OWNER, RandomMinion()).then(Buff(Morph.CARD, "OG_123e"))
        )

    events = REMOVED_IN_PLAY


class OG_300:
    """The Boogeymonster / 波戈蒙斯塔
    每当波戈蒙斯塔攻击并消灭一个随从，便获得+2/+2。"""

    events = Attack(SELF, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & Buff(SELF, "OG_300e")
    )


OG_300e = buff(+2, +2)


class OG_133:
    """N'Zoth, the Corruptor / 恩佐斯
    战吼：召唤所有你在本局对战中死亡的，并具有亡语的随从。"""

    play = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + MINION + DEATHRATTLE))


class OG_134:
    """Yogg-Saron, Hope's End / 尤格-萨隆
    战吼： 在本局对战中，你每施放过一个法术，便随机施放一个法术（目标随机而定）。"""

    def play(self):
        times = TIMES_SPELL_PLAYED_THIS_GAME.evaluate(self)
        times = min(times, 30)
        for _ in range(times):
            yield CastSpell(RandomSpell())
            yield Deaths()
            if self.dead or self.silenced or self.zone != Zone.PLAY:
                break


class OG_280:
    """C'Thun / 克苏恩
    战吼： 造成等同于本随从攻击力的伤害，随机分配到所有敌人身上。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * ATK(SELF)


class OG_131:
    """Twin Emperor Vek'lor / 维克洛尔大帝
    嘲讽，战吼：如果你的克苏恩至少有10点攻击力，则召唤另一名双子皇帝。"""

    play = CHECK_CTHUN & Summon(CONTROLLER, "OG_319")
