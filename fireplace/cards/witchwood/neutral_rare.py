from ..utils import *


##
# Minions


class GIL_125:
    """Mad Hatter / 疯帽客
    战吼：随机向其他随从丢出三顶帽子。每顶帽子可使随从获得+1/+1。"""

    # [x]<b>Battlecry:</b> Randomly toss 3 hats to other minions. Each hat gives +1/+1.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 11,
    }
    play = Buff(RANDOM_OTHER_MINION, "GIL_125e") * 3


GIL_125e = buff(+1, +1)


class GIL_202:
    """Gilnean Royal Guard / 吉尔尼斯皇家卫兵
    圣盾，突袭 如果这张牌在你的手牌中，每个回合使其攻击力和生命值互换。"""

    # [x]<b>Divine Shield</b>, <b>Rush</b> Each turn this is in your hand, swap its Attack
    # and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_202t", "GIL_200e")))


class GIL_202t:
    """Gilnean Royal Guard"""

    # [x]<b>Stealth</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_202", "GIL_200e")))


class GIL_584:
    """Witchwood Piper / 女巫森林吹笛人
    战吼：从你的牌库中抽一张法力值消耗最低的随从牌。"""

    # [x]<b>Battlecry:</b> Draw the lowest Cost minion from your deck.
    play = ForceDraw(LOWEST_COST(FRIENDLY_DECK + MINION))


class GIL_601:
    """Scaleworm / 巨鳞蠕虫
    战吼：如果你的手牌中有龙牌，便获得+1攻击力和突袭。"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain +1 Attack and <b>Rush</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "GIL_601e")


GIL_601e = buff(atk=1, rush=True)


class GIL_622:
    """Lifedrinker / 吸血蚊
    战吼：对敌方英雄造成3点伤害。为你的英雄恢复#3点生命值。"""

    # [x]<b>Battlecry:</b> Deal 3 damage to the enemy hero. Restore 3 Health to your hero.
    play = Hit(ENEMY_HERO, 3), Heal(FRIENDLY_HERO, 3)


class GIL_623:
    """Witchwood Grizzly / 女巫森林灰熊
    嘲讽。战吼： 你的对手每有一张手牌，本随从便失去1点生命值。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Lose 1 Health for each card in your opponent's
    # hand.
    play = Buff(SELF, "GIL_623e") * Count(ENEMY_HERO)


GIL_623e = buff(health=-1)


class GIL_624:
    """Night Prowler / 暗夜徘徊者
    战吼：如果它是战场上唯一的一个随从，获得+3/+3。"""

    # <b>Battlecry:</b> If this is the only minion on the battlefield, gain +3/+3.
    play = Find(ALL_MINIONS - SELF) | Buff(SELF, "GIL_624e")


GIL_624e = buff(+3, +3)


class GIL_648:
    """Chief Inspector / 总督察
    战吼：摧毁所有敌方奥秘。"""

    # <b>Battlecry:</b> Destroy all enemy <b>Secrets</b>.
    play = Destroy(ENEMY_SECRETS)
