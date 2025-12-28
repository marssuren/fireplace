from ..utils import *


##
# Minions


class BOT_280:
    """Holomancer / 全息术士
    在你的对手使用一张随从牌后，召唤一个它的1/1的复制。"""

    # After your opponent plays a minion, summon a 1/1_copy of it.
    events = Play(OPPONENT, MINION).after(
        Summon(CONTROLLER, Buff(ExactCopy(Play.CARD), "BOT_280e"))
    )


class BOT_280e:
    atk = SET(1)
    max_health = SET(1)


class BOT_296:
    """Omega Defender / 欧米茄防御者
    嘲讽，战吼：如果你有十个法力水晶，获得+10攻击力。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If you have 10 Mana Crystals, gain +10 Attack.
    play = AT_MAX_MANA(CONTROLLER) & Buff(SELF, "BOT_296e")


BOT_296e = buff(atk=10)


class BOT_401:
    """Weaponized Piñata / 武装皮纳塔
    亡语： 随机将一张传说随从牌置入你的手牌。"""

    # <b>Deathrattle:</b> Add a random <b>Legendary</b> minion to your_hand.
    deathrattle = Give(CONTROLLER, RandomLegendaryMinion())


class BOT_447:
    """Crystallizer / 晶化师
    战吼：对你的英雄造成5点伤害。获得5点护甲值。"""

    # [x]<b>Battlecry:</b> Deal 5 damage to your hero. Gain 5 Armor.
    play = Hit(FRIENDLY_HERO, 5), GainArmor(FRIENDLY_HERO, 5)


class BOT_511:
    """Seaforium Bomber / 爆盐投弹手
    战吼：将一张“炸弹” 牌洗入你对手的牌库。当抽到“炸弹”时，便会受到5点伤害。"""

    # [x]<b>Battlecry:</b> Shuffle a Bomb into your opponent's deck. When drawn, it
    # explodes for 5 damage.
    play = Shuffle(OPPONENT, "BOT_511t")


class BOT_511t:
    play = Hit(FRIENDLY_HERO, 5)
    draw = CAST_WHEN_DRAWN


class BOT_540:
    """E.M.P. Operative / 电磁脉冲特工
    战吼： 消灭一个机械。"""

    # <b>Battlecry:</b> Destroy a Mech.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET)


class BOT_544:
    """Loose Specimen / 脱逃的样本
    战吼：造成6点伤害，随机分配到所有其他友方随从身上。"""

    # <b>Battlecry:</b> Deal 6 damage randomly split among other friendly minions.
    play = Hit(RANDOM_FRIENDLY_MINION, 1) * 6


class BOT_552:
    """Star Aligner / 群星罗列者
    战吼：如果你控制三个生命值为7的随从，对所有敌人造成7点 伤害。"""

    # [x]<b>Battlecry:</b> If you control 3 minions with 7 Health, deal 7 damage to all
    # enemies.
    play = (Count(FRIENDLY_MINIONS + (CURRENT_HEALTH == 7)) >= 3) & Hit(
        ENEMY_CHARACTERS, 7
    )


class BOT_559:
    """Augmented Elekk / 强能雷象
    每当你将一张牌洗入牌库，额外洗入一张相同的牌。"""

    # Whenever you shuffle a card into a deck, shuffle in_an extra copy.
    events = Shuffle(source=FRIENDLY - ID("BOT_559")).after(
        Shuffle(CONTROLLER, ExactCopy(Shuffle.CARD))
    )
