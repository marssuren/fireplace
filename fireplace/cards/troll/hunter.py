from ..utils import *


##
# Minions


class TRL_348:
    """Springpaw / 魔泉山猫
    突袭，战吼：将一张1/1并具有突袭的山猫置入你的手牌。"""

    # [x]<b>Rush</b> <b>Battlecry:</b> Add a 1/1 Lynx with <b>Rush</b> to your hand.
    play = Give(CONTROLLER, "TRL_348t")


class TRL_349:
    """Bloodscalp Strategist / 血顶战略家
    战吼：如果你装备着武器，发现一张 法术牌。"""

    # <b>Battlecry:</b> If you have a weapon equipped, <b>Discover</b> a spell.
    play = Find(FRIENDLY_WEAPON) & DISCOVER(RandomSpell())


class TRL_900:
    """Halazzi, the Lynx / 哈尔拉兹，山猫之神
    战吼：用1/1并具有 突袭的山猫填满你的手牌。"""

    # <b>Battlecry:</b> Fill your hand with 1/1 Lynxes that have_<b>Rush</b>.
    play = Give(CONTROLLER, "TRL_348t") * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class TRL_901:
    """Spirit of the Lynx / 山猫之灵
    潜行一回合。每当你召唤一个野兽时，使其获得+1/+1。"""

    # [x]<b>Stealth</b> for 1 turn. Whenever you summon a Beast, give it +1/+1.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Summon(CONTROLLER, BEAST).on(Buff(Summon.CARD, "TRL_901e")),
    )


TRL_901e = buff(+1, +1)


##
# Spells


class TRL_119:
    """The Beast Within / 野兽之心
    使一个友方野兽获得+1/+1，使其随机攻击一个敌方随从。"""

    # Give a friendly Beast +1/+1, then it attacks a random enemy minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "TRL_119e").then(Attack(TARGET, RANDOM_ENEMY_MINION))


TRL_119e = buff(+1, +1)


class TRL_339:
    """Master's Call / 主人的召唤
    从你的牌库中发现一张随从牌。如果三张牌都是野兽，改为抽取全部三张牌。"""

    # <b>Discover</b> a minion in your deck. If all 3 are Beasts, draw them all.
    def play(self):
        entities = (RANDOM(DeDuplicate(FRIENDLY_DECK + MINION)) * 3).eval(
            self.game, self
        )
        if all(Race.BEAST in entity.races for entity in entities):
            yield Give(CONTROLLER, entities)
        else:
            yield GenericChoice(CONTROLLER, entities)


class TRL_347:
    """Baited Arrow / 诱饵射击
    造成$3点伤害。超杀：召唤一个5/5的魔暴龙。"""

    # Deal $3 damage. <b>Overkill:</b> Summon a 5/5 Devilsaur.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3)
    overkill = Summon(CONTROLLER, "TRL_347t")


class TRL_566:
    """Revenge of the Wild / 荒野的复仇
    召唤在 本回合中死亡的友方野兽。"""

    # Summon your Beasts that died this turn.
    requirements = {
        PlayReq.REQ_FRIENDLY_MINION_OF_RACE_DIED_THIS_TURN: 20,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, Copy(FRIENDLY + BEAST + KILLED_THIS_TURN))


##
# Weapons


class TRL_111:
    """Headhunter's Hatchet / 猎头者之斧
    战吼：如果你控制一个野兽，便获得+1耐久度。"""

    # [x]<b>Battlecry:</b> If you control a Beast, gain +1 Durability.
    play = Find(FRIENDLY_MINIONS + BEAST) & Buff(SELF, "TRL_111e1")


TRL_111e1 = buff(health=1)


##
# Heros


class TRL_065:
    """Zul'jin / 祖尔金
    战吼： 施放你在本局对战中使用过的所有法术（目标随机而定）。"""

    # [x]<b>Battlecry:</b> Cast all spells you've played this game <i>(targets chosen
    # randomly)</i>.
    play = CastSpell(Copy(CARDS_PLAYED_THIS_GAME + SPELL))


class TRL_065h:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Hit(TARGET, 2)
