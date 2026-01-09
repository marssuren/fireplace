from ..utils import *


##
# Minions


class BOT_236:
    """Crystalsmith Kangor / 水晶工匠坎格尔
    圣盾，吸血 你的治疗效果翻倍。"""

    # <b>Divine Shield</b>, <b>Lifesteal</b> Your healing is doubled.
    update = Refresh(CONTROLLER, {GameTag.HEALING_DOUBLE: 1})


class BOT_537:
    """Mechano-Egg / 机械蛋
    亡语：召唤一个8/8的机械暴龙。"""

    # <b>Deathrattle:</b> Summon an 8/8 Robosaur.
    deathrattle = Summon(CONTROLLER, "BOT_537t")


class BOT_906:
    """Glow-Tron / 格洛顿
    磁力"""

    # <b>Magnetic</b>
    magnetic = MAGNETIC("BOT_906e")


class BOT_910:
    """Glowstone Technician / 亮石技师
    战吼：使你手牌中的所有随从牌获得+2/+2。"""

    # <b>Battlecry:</b> Give all minions in your hand +2/+2.
    play = Buff(FRIENDLY_HAND + MINION, "BOT_910e")


BOT_910e = buff(+2, +2)


class BOT_911:
    """Annoy-o-Module / 吵吵模组
    磁力 圣盾 嘲讽"""

    # <b>Magnetic</b> <b>Divine Shield</b> <b>Taunt</b>
    magnetic = MAGNETIC("BOT_911e")


class BOT_911e:
    tags = {GameTag.TAUNT: True}

    def apply(self, target):
        self.game.trigger(self, (GiveDivineShield(target),), None)


##
# Spells


class BOT_234:
    """Shrink Ray / 萎缩射线
    将所有随从的攻击力和生命值 变为1。"""

    # Set the Attack and Health of all minions to 1.
    play = Buff(ALL_MINIONS, "BOT_234e")


class BOT_234e:
    atk = SET(1)
    max_health = SET(1)


class BOT_436:
    """Prismatic Lens / 棱彩透镜
    从你的牌库中抽一张随从牌和一张法术牌，交换其法力值消耗。"""

    # Draw a minion and a spell from your deck. Swap their Costs.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    # 从牌库中抽一张随从和一张法术,然后交换它们的费用
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)),
    )


class BOT_436e:
    cost = lambda self, i: self._xcost
    events = REMOVED_IN_PLAY


class BOT_908:
    """Autodefense Matrix / 自动防御矩阵
    奥秘：当你的随从受到攻击时，使其获得圣盾。"""

    # <b>Secret:</b> When one of your minions is attacked, give it <b>Divine Shield</b>.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        Reveal(SELF), GiveDivineShield(Attack.DEFENDER)
    )


class BOT_909:
    """Crystology / 水晶学
    从你的牌库中抽两张攻击力为1的随从牌。"""

    # [x]Draw two 1-Attack minions from your deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (ATK == 1)) * 2)


class BOT_912:
    """Kangor's Endless Army / 坎格尔的无尽大军
    复活三个友方机械，它们会保留所有磁力升级。"""

    # Resurrect 3 friendly Mechs. They keep any <b>Magnetic</b> upgrades.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: 17,
    }
    play = Summon(CONTROLLER, KeepMagneticCopy(RANDOM(FRIENDLY + KILLED + MECH) * 3))
