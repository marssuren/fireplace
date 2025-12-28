from ..utils import *


##
# Minions


class BOT_424:
    """Mecha'thun / 机械克苏恩
    亡语： 如果你的牌库、手牌和战场没有任何牌，消灭敌方英雄。"""

    # [x]<b>Deathrattle:</b> If you have no cards in your deck, hand, and battlefield,
    # destroy the enemy hero.
    deathrattle = Find(FRIENDLY_DECK | FRIENDLY_HAND | FRIENDLY_MINIONS) | Destroy(
        ENEMY_HERO
    )


class BOT_548:
    """Zilliax / 奇利亚斯
    磁力，圣盾，嘲讽，吸血，突袭"""

    # <b>Magnetic</b> <b><b>Divine Shield</b>, <b>Taunt</b>, Lifesteal, Rush</b>
    magnetic = MAGNETIC("BOT_548e")


class BOT_548e:
    tags = {GameTag.TAUNT: True, GameTag.LIFESTEAL: True, GameTag.RUSH: True}

    def apply(self, target):
        self.game.trigger(self, (GiveDivineShield(target),), None)


class BOT_555:
    """Harbinger Celestia / 星界使者塞雷西亚
    潜行 在你的对手使用一张随从牌后，变成它的复制。"""

    # [x]<b>Stealth</b> After your opponent plays a minion, become a copy of it.
    events = Play(OPPONENT, MINION).after(Morph(SELF, ExactCopy(Play.CARD)))


class BOT_573:
    """Subject 9 / 实验体9号
    战吼： 从你的牌库中抽五张不同的奥秘牌。"""

    # <b>Battlecry:</b> Draw 5 different <b>Secrets</b> from your deck.
    play = ForceDraw(RANDOM(DeDuplicate(FRIENDLY_DECK + SECRET)) * 5)


class BOT_700:
    """SN1P-SN4P / 大铡蟹
    磁力，回响，亡语：召唤两个1/1的微型机器人。"""

    # <b>Magnetic</b>, <b>Echo</b> <b>Deathrattle:</b> Summon two 1/1 Microbots.
    magnetic = MAGNETIC("BOT_700e")
    deathrattle = Summon(CONTROLLER, "BOT_312t") * 2


class BOT_700e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "BOT_312t") * 2
