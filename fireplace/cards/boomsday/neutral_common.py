from ..utils import *


##
# Minions


class BOT_020:
    """Skaterbot / 滑板机器人
    磁力 突袭"""

    # <b>Magnetic</b> <b>Rush</b>
    magnetic = MAGNETIC("BOT_020e")


BOT_020e = buff(rush=True)


class BOT_021:
    """Bronze Gatekeeper / 青铜门卫
    磁力 嘲讽"""

    # <b>Magnetic</b> <b>Taunt</b>
    magnetic = MAGNETIC("BOT_021e")


BOT_021e = buff(taunt=True)


class BOT_031:
    """Goblin Bomb / 地精炸弹
    亡语：对敌方英雄造成2点伤害。"""

    # [x]<b>Deathrattle:</b> Deal 2 damage to the enemy hero.
    deathrattle = Hit(ENEMY_HERO, 2)


class BOT_079:
    """Faithful Lumi / 可靠的灯泡
    战吼：使一个友方机械获得+1/+1。"""

    # <b>Battlecry:</b> Give a friendly Mech +1/+1.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_079e")


BOT_079e = buff(+1, +1)


class BOT_083:
    """Toxicologist / 毒物学家
    战吼：使你的武器获得+1攻击力。"""

    # <b>Battlecry:</b> Give your weapon +1 Attack.
    play = Buff(FRIENDLY_WEAPON, "BOT_083e")


BOT_083e = buff(atk=1)


class BOT_267:
    """Piloted Reaper / 载人毁灭机
    亡语：随机从你的手牌中召唤一个法力值消耗小于或等于（2）点的随从。"""

    # <b>Deathrattle:</b> Summon a random minion from your hand that costs (2) or less.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + (COST <= 2)))


class BOT_308:
    """Spring Rocket / 弹簧火箭犬
    战吼：造成2点伤害。"""

    # <b>Battlecry:</b> Deal 2 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 2)


class BOT_413:
    """Brainstormer / 脑力激荡者
    战吼：你手牌中每有一张法术牌，便获得+1生命值。"""

    # [x]<b>Battlecry:</b> Gain +1 Health for each spell in your hand.
    play = Buff(SELF, "BOT_413e") * Count(FRIENDLY_HAND + SPELL)


BOT_413e = buff(health=1)


class BOT_431:
    """Whirliglider / 旋翼滑翔者
    战吼：召唤一个0/2的地精炸弹。"""

    # <b>Battlecry:</b> Summon a 0/2_Goblin Bomb.
    play = Summon(CONTROLLER, "BOT_031")


class BOT_445:
    """Mecharoo / 机械袋鼠
    亡语：召唤一个1/1的机械袋鼠宝宝。"""

    # <b>Deathrattle:</b> Summon a 1/1 Jo-E Bot.
    deathrattle = Summon(CONTROLLER, "BOT_445t")


class BOT_448:
    """Damaged Stegotron / 受损的机械剑龙
    嘲讽。战吼：对本随从造成6点伤害。"""

    # <b>Taunt</b> <b>Battlecry:</b> Deal 6 damage to this minion.
    play = Hit(SELF, 6)


class BOT_532:
    """Explodinator / 投弹机器人
    战吼：召唤两个0/2的地精炸弹。"""

    # <b>Battlecry:</b> Summon two 0/2 Goblin Bombs.
    play = SummonBothSides(CONTROLLER, "BOT_031") * 2


class BOT_535:
    """Microtech Controller / 微机操控者
    战吼：召唤两个1/1的微型机器人。"""

    # <b>Battlecry:</b> Summon two 1/1 Microbots.
    play = SummonBothSides(CONTROLLER, "BOT_312t") * 2


class BOT_550:
    """Electrowright / 电能工匠
    战吼： 如果你的手牌中有法力值消耗大于或等于（5）点的法术牌，便获得+1/+1。"""

    # <b>Battlecry:</b> If you're holding a spell that costs (5) or more, gain +1/+1.
    play = Find(FRIENDLY_HAND + SPELL + (COST >= 5)) & Buff(SELF, "BOT_550e")


BOT_550e = buff(+1, +1)


class BOT_562:
    """Coppertail Imposter / 铜尾仿冒鼠
    战吼：获得潜行直到你的下个回合。"""

    # <b>Battlecry:</b> Gain <b>Stealth</b> until your next turn.
    play = Stealth(SELF), Buff(SELF, "BOT_562e")


class BOT_562e:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class BOT_563:
    """Wargear / 战争机兵
    磁力"""

    # <b>Magnetic</b>
    magnetic = MAGNETIC("BOT_563e")


class BOT_606:
    """Kaboom Bot / 爆爆机器人
    亡语：随机对一个敌方随从造成4点伤害。"""

    # <b>Deathrattle:</b> Deal 4_damage to a random enemy minion.
    deathrattle = Hit(RANDOM_ENEMY_MINION, 4)
