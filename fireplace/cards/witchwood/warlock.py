from ..utils import *


##
# Minions


class GIL_508:
    """Duskbat / 夜行蝙蝠
    战吼：如果你的英雄在本回合受到过伤害，召唤两只1/1的 蝙蝠。"""

    # <b>Battlecry:</b> If your hero took damage this turn, summon two 1/1 Bats.
    powered_up = DAMAGED_THIS_TURN(FRIENDLY_HERO) >= 0
    play = powered_up & SummonBothSides(CONTROLLER, "GIL_508t") * 2


class GIL_515:
    """Ratcatcher / 捕鼠人
    突袭，战吼：消灭一个友方随从，并获得其攻击力和生命值。"""

    # <b>Rush</b> <b>Battlecry:</b> Destroy a friendly minion and gain its Attack and
    # Health.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = (
        Buff(SELF, "GIL_515e", atk=ATK(TARGET), max_health=CURRENT_HEALTH(TARGET)),
        Destroy(TARGET),
    )


class GIL_565:
    """Deathweb Spider / 逝网蜘蛛
    战吼：如果你的英雄在本回合受到过伤害，获得吸血。"""

    # <b>Battlecry:</b> If your hero took damage this turn, gain <b>Lifesteal</b>.
    powered_up = DAMAGED_THIS_TURN(FRIENDLY_HERO) >= 0
    play = powered_up & GiveLifesteal(SELF)


class GIL_608:
    """Witchwood Imp / 女巫森林小鬼
    潜行，亡语：随机使一个友方随从获得+2生命值。"""

    # [x]<b>Stealth</b> <b>Deathrattle:</b> Give a random friendly minion +2 Health.
    deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "GIL_608e")


GIL_608e = buff(health=2)


class GIL_618:
    """Glinda Crowskin / 格林达·鸦羽
    你手牌中的所有随从牌拥有回响。"""

    # Minions in your hand have_<b>Echo</b>.
    update = Refresh(FRIENDLY_HAND + MINION, {GameTag.ECHO: True})


class GIL_693:
    """Blood Witch / 鲜血女巫
    在你的回合开始时，对你的英雄造成 1点伤害。"""

    # At the start of your turn, deal 1 damage to your_hero.
    events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class GIL_825:
    """Lord Godfrey / 高弗雷勋爵
    战吼：对所有其他随从造成2点伤害。如果有随从死亡，则重复此战吼效果。"""

    # [x]<b>Battlecry:</b> Deal 2 damage to all other minions. If any die, repeat this
    # <b>Battlecry</b>.
    def play(self):
        yield Hit(ALL_MINIONS - SELF, 2)
        for _ in range(13):
            if Dead(ALL_MINIONS).check(self):
                yield Deaths()
                yield Hit(ALL_MINIONS - SELF, 2)
            else:
                break


##
# Spells


class GIL_191:
    """Fiendish Circle / 恶魔法阵
    召唤四个1/1的小鬼。"""

    # [x]Summon four 1/1 Imps.
    play = Summon(CONTROLLER, "GIL_191t") * 4


class GIL_543:
    """Dark Possession / 黑暗附体
    对一个友方角色造成$2点伤害。发现一张恶魔牌。"""

    # Deal $2 damage to a friendly character. <b>Discover</b> a Demon.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Hit(TARGET, 2), DISCOVER(RandomDemon())


class GIL_665:
    """Curse of Weakness / 虚弱诅咒
    回响 直到你的下个回合，使所有敌方随从获得-2攻击力。"""

    # <b>Echo</b> Give all enemy minions -2_Attack until your next_turn.
    play = Buff(ENEMY_MINIONS, "GIL_665e")


class GIL_665e:
    tags = {GameTag.ATK: -2}
    events = OWN_TURN_BEGIN.on(Destroy(SELF))
