from ..utils import *


##
# Minions


class GIL_128:
    """Emeriss / 艾莫莉丝
    战吼：使你手牌中所有随从牌的攻击力和生命值翻倍。"""

    # <b>Battlecry:</b> Double the Attack and Health of all minions in_your hand.
    play = Buff(FRIENDLY_HAND + MINION, "GIL_128e")


class GIL_128e:
    def apply(self, target):
        self._xatk = target.atk * 2
        self._xhealth = target.health * 2

    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


class GIL_200:
    """Duskhaven Hunter / 暮湾镇猎手
    潜行 如果这张牌在你的手牌中，每个回合使其攻击力和生命值互换。"""

    # [x]<b>Stealth</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_200t", "GIL_200e")))


class GIL_200t:
    """Duskhaven Hunter"""

    # [x]<b>Stealth</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_200", "GIL_200e")))


class GIL_200e:
    def apply(self, target):
        self._xatk = self.source.health
        self._xhealth = self.source.atk

    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


class GIL_607:
    """Toxmonger / 毒药贩子
    每当你使用一张法力值消耗为（1）的随从牌，使其获得剧毒。"""

    # [x]Whenever you play a 1-Cost minion, give it <b>Poisonous</b>.
    events = Play(CONTROLLER, MINION + (COST == 1)).on(GivePoisonous(Play.CARD))


class GIL_650:
    """Houndmaster Shaw / 驯犬大师肖尔
    你的其他随从拥有突袭。"""

    # Your other minions have <b>Rush</b>.
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.RUSH: True})


class GIL_905:
    """Carrion Drake / 食腐幼龙
    战吼：如果在本回合中有一个随从死亡，获得剧毒。"""

    # <b>Battlecry:</b> If a minion died this turn, gain <b>Poisonous</b>.
    play = (Find(KILLED_THIS_TURN), GivePoisonous(SELF))


##
# Spells


class GIL_518:
    """Wing Blast / 飞翼冲击
    对一个随从造成$4点伤害。如果在本回合中有一个随从死亡，该牌的法力值消耗为（1）点。"""

    # Deal $4 damage to a minion. If a minion died this turn, this costs (1).
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4)

    class Hand:
        update = Find(KILLED_THIS_TURN) & Refresh(SELF, {GameTag.COST: SET(1)})


class GIL_577:
    """Rat Trap / 捕鼠陷阱
    奥秘：当你的对手在一回合中使用三张牌后，召唤一只6/6的老鼠。"""

    # [x]<b>Secret:</b> After your opponent plays three cards in a turn, summon a 6/6 Rat.
    secret = Play(OPPONENT).after(
        (Attr(OPPONENT, GameTag.NUM_CARDS_PLAYED_THIS_TURN) >= 3)
        & (FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "GIL_577t")))
    )


class GIL_828:
    """Dire Frenzy / 凶猛狂暴
    使一个野兽获得+3/+3。将它的三张复制洗入你的牌库，且这些复制都具有+3/+3。"""

    # Give a Beast +3/+3. Shuffle 3 copies into your deck with +3/+3.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Buff(TARGET, "GIL_828e").then(Shuffle(CONTROLLER, ExactCopy(TARGET)) * 3)


GLI_828e = buff(+3, +3)
