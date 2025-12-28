from ..utils import *


##
# Minions


class DRG_312:
    """Shrubadier / 盆栽投手
    战吼：召唤一个2/2的树人。"""

    # <b>Battlecry:</b> Summon a 2/2_Treant.
    play = Summon(CONTROLLER, "DRG_311t")


class DRG_313:
    """Emerald Explorer / 翡翠龙探险者
    嘲讽 战吼：发现一张 龙牌。"""

    # <b>Taunt</b> <b>Battlecry:</b> <b>Discover</b> a Dragon.
    play = DISCOVER(RandomDragon())


class DRG_319:
    """Goru the Mightree / 强力巨树格鲁
    嘲讽，战吼：在本局对战的剩余时间内，你的树人拥有+1/+1。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> For the rest of the game, your Treants have +1/+1.
    play = Buff(CONTROLLER, "DRG_319e4")


class DRG_319e4:
    update = Refresh(FRIENDLY_MINIONS + TREANT, buff="DRG_319e5")


DRG_319e5 = buff(+1, +1)


class DRG_320:
    """Ysera, Unleashed / 觉醒巨龙伊瑟拉
    战吼：将七张“梦境之门”洗入你的牌库。当抽到梦境之门时，随机召唤一条龙。"""

    # [x]<b>Battlecry:</b> Shuffle 7 Dream Portals into your deck. When drawn, summon a
    # random Dragon.
    play = Shuffle(CONTROLLER, "DRG_320t") * 7


class DRG_320t:
    play = Summon(CONTROLLER, RandomDragon())
    draw = CAST_WHEN_DRAWN


##
# Spells


class DRG_051:
    """Strength in Numbers / 人多势众
    支线任务： 消耗10点法力值用于随从牌上。奖励：从你的牌库中召唤一个随从。"""

    # <b>Sidequest:</b> Spend 10 Mana on minions. <b>Reward:</b> Summon a minion from your
    # deck.
    progress_total = 10
    sidequest = SpendMana(CONTROLLER, source=MINION).after(
        AddProgress(SELF, CONTROLLER, SpendMana.AMOUNT)
    )
    reward = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))


class DRG_311:
    """Treenforcements / 树木援军
    抉择：使一个随从获得+2生命值和嘲讽；或者召唤一个2/2的树人。"""

    # [x]<b>Choose One -</b> Give a minion +2 Health and <b>Taunt</b>; or Summon a 2/2
    # Treant.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    choose = ("DRG_311a", "DRG_311b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(TARGET, "DRG_311e"),
        Summon(CONTROLLER, "DRG_311t"),
    )


class DRG_311a:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "DRG_311t")


class DRG_311b:
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "DRG_311e")


class DRG_314:
    """Aeroponics / 空气栽培
    抽两张牌。你每控制一个树人，本牌的法力值消耗便减少（2）点。"""

    # Draw 2 cards. Costs (2) less for each Treant you control.
    cost_mod = -Count(FRIENDLY_MINIONS + TREANT) * 2
    play = Draw(CONTROLLER) * 2


class DRG_315:
    """Embiggen / 森然巨化
    使你牌库中的所有随从牌获得+2/+2，且法力值消耗增加（1）点（最高不超过10点）。"""

    # Give all minions in your deck +2/+2. They cost (1) more <i>(up to 10)</i>.
    play = MultiBuff(FRIENDLY_DECK + MINION, ["DRG_315e", "DRG_315e2"])


DRG_315e = buff(+2, +2)


class DRG_315e2:
    cost = lambda self, i: i if i >= 10 else i + 1
    events = REMOVED_IN_PLAY


class DRG_317:
    """Secure the Deck / 保护甲板
    支线任务： 用你的英雄攻击两次。奖励：将三张“爪击”法术牌置入你的手牌。"""

    # <b>Sidequest:</b> Attack twice with your hero. <b>Reward:</b> Add 3 'Claw' spells to
    # your hand.
    progress_total = 2
    sidequest = Attack(FRIENDLY_HERO).after(AddProgress(SELF, FRIENDLY_HERO))
    reward = Give(CONTROLLER, "CS2_005") * 3


class DRG_318:
    """Breath of Dreams / 梦境吐息
    抽一张牌。如果你的手牌中有龙牌，便获得一个空的法力水晶。"""

    # Draw a card. If you're holding a Dragon, gain an empty Mana Crystal.
    powered_up = HOLDING_DRAGON
    play = Draw(CONTROLLER), powered_up & GainEmptyMana(CONTROLLER, 1)
