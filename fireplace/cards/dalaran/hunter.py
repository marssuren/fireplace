from ..utils import *


##
# Minions


class DAL_372:
    """Arcane Fletcher / 奥术弓箭手
    每当你使用一张法力值消耗为（1）的随从牌，从你的牌库中抽一张法术牌。"""

    # [x]Whenever you play a 1-Cost minion, draw a spell from your deck.
    events = Play(CONTROLLER, MINION + (COST == 1)).on(
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))
    )


class DAL_376:
    """Oblivitron / 湮灭战车
    亡语：从你的手牌中召唤一个机械，并触发其亡语。"""

    # [x]<b>Deathrattle:</b> Summon a Mech from your hand and trigger its
    # <b>Deathrattle</b>.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MECH)).then(
        Deathrattle(Summon.CARD)
    )


class DAL_379:
    """Vereesa Windrunner / 温蕾萨·风行者
    战吼：装备索利达尔，群星之怒。"""

    # <b>Battlecry:</b> Equip Thori'dal, the Stars' Fury.
    play = Summon(CONTROLLER, "DAL_379t")


class DAL_379t:
    events = Attack(FRIENDLY_HERO).after(Buff(CONTROLLER, "DAL_379e"))


DAL_379e = buff(spellpower=2)


class DAL_587:
    """Shimmerfly / 闪光蝴蝶
    亡语： 随机将一张猎人法术牌置入你的手牌。"""

    # <b>Deathrattle:</b> Add a random Hunter spell to your hand.
    deathrattle = Give(CONTROLLER, RandomSpell(card_class=CardClass.HUNTER))


class DAL_604:
    """Ursatron / 机械巨熊
    亡语：从你的牌库中抽一张机械牌。"""

    # <b>Deathrattle:</b> Draw a Mech from your deck.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MECH))


##
# Spells


class DAL_371:
    """Marked Shot / 标记射击
    对一个随从造成$4点伤害。发现一张法术牌。"""

    # Deal $4 damage to_a_minion. <b>Discover</b>_a_spell.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), DISCOVER(RandomSpell())


class DAL_373:
    """Rapid Fire / 急速射击
    双生法术 造成$2点伤害。"""

    # <b>Twinspell</b> Deal $1 damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 1)


class DAL_373ts(DAL_373):
    pass


class DAL_377:
    """Nine Lives / 九命兽魂
    发现一个在本局对战中死亡的友方亡语随从，并触发其 亡语。"""

    # <b>Discover</b> a friendly <b>Deathrattle</b> minion that died this game. Also
    # trigger its <b>Deathrattle</b>.
    requirements = {
        PlayReq.REQ_FRIENDLY_DEATHRATTLE_MINION_DIED_THIS_GAME: 0,
    }
    play = GenericChoice(
        CONTROLLER,
        Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + DEATHRATTLE + MINION)) * 3),
    ).then(Give(CONTROLLER, GenericChoice.CARD), Deathrattle(GenericChoice.CARD))


class DAL_378:
    """Unleash the Beast / 猛兽出笼
    双生法术 召唤一只5/5并具有突袭的双足飞龙。"""

    # <b>Twinspell</b> Summon a 5/5 Wyvern with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "DAL_378t1")


class DAL_378ts(DAL_378):
    pass


class DAL_589:
    """Hunting Party / 狩猎盛宴
    复制你手牌中的所有野兽牌。"""

    # Copy all Beasts in your_hand.
    play = Give(CONTROLLER, ExactCopy(FRIENDLY_HAND + BEAST))
