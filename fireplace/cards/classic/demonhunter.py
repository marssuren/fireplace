from ..utils import *


##
# Minions


class BT_142:
    """Shadowhoof Slayer / 影蹄杀手
    战吼：在本回合中，使你的英雄获得+1攻击力。"""

    # <b>Battlecry:</b> Give your hero +1_Attack this turn.
    play = Buff(CONTROLLER, "BT_142e")


BT_142e = buff(atk=1)


class BT_323:
    """Sightless Watcher / 盲眼监视者
    战吼：检视你牌库中的三张牌。选择一张置于牌库顶。"""

    # <b>Battlecry:</b> Look at 3 cards in your deck. Choose one to put on top.
    play = Choice(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK)) * 3).then(
        PutOnTop(CONTROLLER, Choice.CARD)
    )


class BT_352:
    """Satyr Overseer / 萨特监工
    在你的英雄攻击后，召唤一个2/2的萨特。"""

    # After your hero attacks, summon a 2/2 Satyr.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "BT_352t"))


class BT_495:
    """Glaivebound Adept / 刃缚精锐
    战吼：在本回合中，如果你的英雄进行过攻击，则造成4点 伤害。"""

    # <b>Battlecry:</b> If your hero attacked this turn, deal 4 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_HERO_ATTACKED_THIS_TURN: 0,
    }
    powered_up = NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) > 0
    play = Hit(TARGET, 4)


##
# Spells


class BT_035:
    """Chaos Strike / 混乱打击
    在本回合中，使你的英雄获得+2攻击力。抽一张牌。"""

    # Give your hero +2_Attack this turn. Draw a card.
    play = Buff(FRIENDLY_HERO, "BT_035e"), Draw(CONTROLLER)


BT_035e = buff(atk=2)


class BT_036:
    """Coordinated Strike / 协同打击
    召唤三个1/1并具有突袭的伊利达雷。"""

    # Summon three 1/1_Illidari with <b>Rush</b>.
    play = Summon(CONTROLLER, "BT_036t") * 3


class BT_235:
    """Chaos Nova / 混乱新星
    对所有随从造成$4点伤害。"""

    # Deal $4 damage to all_minions.
    play = Hit(ALL_MINIONS, 4)


class BT_512:
    """Inner Demon / 心中的恶魔
    在本回合中，使你的英雄获得+8攻击力。"""

    # Give your hero +8_Attack this turn.
    play = Buff(FRIENDLY_HERO, "BT_512e")


BT_512e = buff(atk=8)


class BT_740:
    """Soul Cleave / 灵魂裂劈
    吸血 随机对两个敌方随从造成$2点伤害。"""

    # <b>Lifesteal</b> Deal $2 damage to two random enemy minions.
    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION * 2, 2)
