from ..utils import *


##
# Minions


class GIL_634:
    """Bellringer Sentry / 警钟哨卫
    战吼，亡语：将一个奥秘从你的牌库中置入战场。"""

    # <b>Battlecry and Deathrattle:</b> Put a <b>Secret</b> from your deck into the
    # battlefield.
    play = deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class GIL_635:
    """Cathedral Gargoyle / 教堂石像兽
    战吼：如果你的手牌中有龙牌，则获得嘲讽和圣盾。"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain <b>Taunt</b> and <b>Divine
    # Shield</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & (Taunt(SELF), GiveDivineShield(SELF))


class GIL_685:
    """Paragon of Light / 圣光楷模
    如果本随从的攻击力大于或等于3，便拥有嘲讽和吸血。"""

    # While this minion has 3 or more Attack, it has <b>Taunt</b> and <b>Lifesteal</b>.
    update = Find(SELF + (ATK >= 3)) & Refresh(
        SELF,
        {
            GameTag.TAUNT: True,
            GameTag.LIFESTEAL: True,
        },
    )


class GIL_694:
    """Prince Liam / 利亚姆王子
    战吼：将你牌库中所有法力值消耗为（1）的牌变为传说随从牌。"""

    # [x]<b>Battlecry:</b> Transform all 1-Cost cards in your deck _into <b>Legendary</b>
    # minions.
    play = Morph(FRIENDLY_DECK + (COST == 1), RandomLegendaryMinion())


class GIL_817:
    """The Glass Knight / 玻璃骑士
    圣盾 每当有角色获得你的治疗时，获得圣盾。"""

    # [x]<b>Divine Shield</b> Whenever you restore Health, gain <b>Divine Shield</b>.
    events = Heal(source=FRIENDLY).on(GiveDivineShield(SELF))


##
# Spells


class GIL_145:
    """Sound the Bells! / 敲响警钟
    回响 使一个随从获得+1/+2。"""

    # <b>Echo</b> Give a minion +1/+2.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "GIL_145e")


GIL_145e = buff(+1, +2)


class GIL_203:
    """Rebuke / 责难
    下个回合敌方法术的法力值消耗增加（5）点。"""

    # Enemy spells cost (5) more next turn.
    play = Buff(OPPONENT, "GIL_203e")


class GIL_203e:
    update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +5})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class GIL_903:
    """Hidden Wisdom / 隐秘的智慧
    奥秘：当你的对手在一回合中使用三张牌后，抽两张牌。"""

    # [x]<b>Secret:</b> After your opponent plays three cards in a turn, draw 2 cards.
    secret = Play(OPPONENT).after(
        (Attr(CONTROLLER, GameTag.NUM_CARDS_PLAYED_THIS_TURN) >= 3)
        & (Reveal(SELF), Draw(CONTROLLER) * 2)
    )


##
# Weapons


class GIL_596:
    """Silver Sword / 银剑
    在你的英雄攻击后，你的所有随从获得+1/+1。"""

    # After your hero attacks, give your minions +1/+1.
    events = events = Attack(FRIENDLY_HERO).after(Buff(FRIENDLY_MINIONS, "GIL_596e"))


GIL_596e = buff(+1, +1)
