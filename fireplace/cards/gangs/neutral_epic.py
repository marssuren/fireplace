from ..utils import *


##
# Minions


class CFM_025:
    """Wind-up Burglebot / 发条强盗机器人
    每当本随从攻击随从并存活下来时，抽一张牌。"""

    events = Attack(SELF, ALL_MINIONS).after(Dead(SELF) | Draw(CONTROLLER))


class CFM_064:
    """Blubber Baron / 黑金大亨
    每当你召唤一个具有战吼的随从时，便使这张牌（在你手牌中时）获得+1/+1。"""

    class Hand:
        events = Play(CONTROLLER, BATTLECRY + MINION).on(Buff(SELF, "CFM_064e"))


CFM_064e = buff(+1, +1)


class CFM_095:
    """Weasel Tunneler / 鼬鼠挖掘工
    亡语：将本随从洗入你对手的牌库。"""

    deathrattle = Shuffle(OPPONENT, SELF)


class CFM_328:
    """Fight Promoter / 竞技推广员
    战吼：如果你控制一个生命值大于或等于6的随从，抽两张牌。"""

    play = Find(FRIENDLY_MINIONS + (CURRENT_HEALTH >= 6)) & Draw(CONTROLLER) * 2


class CFM_609:
    """Fel Orc Soulfiend / 邪兽人噬魂魔
    在你的回合开始时，对本随从造成2点 伤害。"""

    events = OWN_TURN_BEGIN.on(Hit(SELF, 2))


class CFM_669:
    """Burgly Bully / 穴居人强盗
    每当你的对手施放一个法术，将一张幸运币置入你的手牌。"""

    events = Play(OPPONENT, SPELL).on(Give(CONTROLLER, "GAME_005"))


class CFM_790:
    """Dirty Rat / 卑劣的脏鼠
    嘲讽，战吼：使你的对手随机从手牌中召唤一个随从。"""

    play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION))


class CFM_810:
    """Leatherclad Hogleader / 野猪骑士蕾瑟兰
    战吼：如果你的对手拥有6张或者更多手牌，便获得冲锋。"""

    play = (Count(ENEMY_HAND) >= 6) & GiveCharge(SELF)


class CFM_855:
    """Defias Cleaner / 迪菲亚清道夫
    战吼：沉默一个具有亡语的随从。"""

    requirements = {
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Silence(TARGET)
