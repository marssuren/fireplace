from ..utils import *


##
# Minions


class TRL_010:
    """Half-Time Scavenger / 中场拾荒者
    潜行 超杀：获得3点 护甲值。"""

    # <b>Stealth</b> <b>Overkill</b>: Gain 3 Armor.
    overkill = GainArmor(FRIENDLY_HERO, 3)


class TRL_015:
    """Ticket Scalper / 黑心票贩
    超杀：抽两张牌。"""

    # <b>Overkill</b>: Draw 2 cards.
    overkill = Draw(CONTROLLER) * 2


class TRL_020:
    """Sightless Ranger / 盲眼游侠
    突袭 超杀：召唤两个1/1的蝙蝠。"""

    # <b>Rush</b> <b>Overkill</b>: Summon two 1/1_Bats.
    overkill = SummonBothSides(CONTROLLER, "TRL_020t") * 2


class TRL_151:
    """Former Champ / 退役冠军
    战吼：召唤一个5/5的赛场新秀。"""

    # <b>Battlecry:</b> Summon a 5/5_Hotshot.
    play = Summon(CONTROLLER, "TRL_151t")


class TRL_312:
    """Spellzerker / 狂暴咒术师
    受伤时拥有 法术伤害+2。"""

    # Has <b>Spell Damage +2</b> while damaged.
    enrage = Refresh(SELF, buff="TRL_312e")


TRL_312e = buff(spellpower=2)


class TRL_363:
    """Saronite Taskmaster / 萨隆铁矿监工
    亡语：为你的对手召唤一个0/3并具有嘲讽的自由的矿工。"""

    # <b>Deathrattle:</b> Summon a 0/3 Free Agent with <b>Taunt</b> for_your opponent.
    deathrattle = Summon(OPPONENT, "TRL_363t")


class TRL_406:
    """Dozing Marksman / 嗜睡的神枪手
    受伤时拥有 +4攻击力。"""

    # Has +4 Attack while damaged.
    enrage = Refresh(SELF, buff="TRL_406e")


TRL_406e = buff(atk=+4)


class TRL_503:
    """Scarab Egg / 甲虫卵
    亡语：召唤三只1/1的甲虫。"""

    # <b>Deathrattle:</b> Summon three 1/1 Scarabs.
    deathrattle = Summon(CONTROLLER, "TRL_503t") * 3


class TRL_505:
    """Helpless Hatchling / 无助的幼雏
    亡语：使你手牌中的一张野兽牌法力值消耗减少（1）点。"""

    # <b>Deathrattle:</b> Reduce the Cost of a Beast in your hand by (1).
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "TRL_505e")


class TRL_505e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class TRL_506:
    """Gurubashi Chicken / 古拉巴什小鸡
    超杀： 获得+5攻击力。"""

    # <b>Overkill:</b> Gain +5 Attack.
    overkill = Buff(SELF, "TRL_506e")


TRL_506e = buff(atk=5)


class TRL_507:
    """Sharkfin Fan / 鲨鳍后援
    在你的英雄攻击后，召唤一个1/1的海盗。"""

    # After your hero attacks, summon a 1/1 Pirate.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "TRL_507t"))


class TRL_508:
    """Regeneratin' Thug / 再生暴徒
    在你的回合开始时，为本随从恢复 #2点生命值。"""

    # At the start of your turn, restore #2 Health to this_minion.
    events = OWN_TURN_BEGIN.on(Heal(SELF, 2))


class TRL_509:
    """Banana Buffoon / 香蕉小丑
    战吼：将两根香蕉 置入你的手牌。"""

    # <b>Battlecry:</b> Add 2 Bananas to your hand.
    play = Give(CONTROLLER, "TRL_509t") * 2


class TRL_509t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "TRL_509te")


TRL_509te = buff(+1, +1)


class TRL_512:
    """Cheaty Anklebiter / 调皮的噬踝者
    吸血 战吼：造成1点伤害。"""

    # <b>Lifesteal</b> <b>Battlecry:</b> Deal 1 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 1)


class TRL_515:
    """Rabble Bouncer / 场馆保镖
    嘲讽 每有一个敌方随从，本牌的法力值消耗便减少（1）点。"""

    # <b>Taunt</b> Costs (1) less for each enemy minion.
    cost_mod = -Count(ENEMY_MINIONS)


class TRL_517:
    """Arena Fanatic / 赛场狂热者
    战吼：使你手牌中的所有随从牌获得+1/+1。"""

    # <b>Battlecry:</b> Give all minions in your hand +1/+1.
    play = Buff(FRIENDLY_HAND + MINION, "TRL_517e2")


TRL_517e2 = buff(+1, +1)


class TRL_525:
    """Arena Treasure Chest / 竞技场财宝箱
    亡语：抽两张牌。"""

    # <b>Deathrattle:</b> Draw 2 cards.
    deathrattle = Draw(CONTROLLER) * 2


class TRL_526:
    """Dragonmaw Scorcher / 龙喉喷火者
    战吼：对所有其他随从造成1点伤害。"""

    # <b>Battlecry:</b> Deal 1 damage to all other minions.
    play = Hit(ALL_MINIONS - SELF, 1)


class TRL_531:
    """Rumbletusk Shaker / 暴牙震颤者
    亡语：召唤一个3/2的暴牙破坏者。"""

    # <b>Deathrattle:</b> Summon a 3/2 Rumbletusk Breaker.
    deathrattle = Summon(CONTROLLER, "TRL_531t")


class TRL_546:
    """Ornery Tortoise / 暴躁的巨龟
    战吼：对你的英雄造成5点伤害。"""

    # <b>Battlecry:</b> Deal 5 damage to your hero.
    play = Hit(FRIENDLY_HERO, 5)
