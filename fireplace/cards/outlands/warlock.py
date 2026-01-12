from ..utils import *


##
# Minions


class BT_196:
    """Keli'dan the Breaker / 击碎者克里丹
    战吼：消灭一个随从。如果在本回合被抽到，则改为消灭除本随从外的所有随从。"""

    # [x]<b>Battlecry:</b> Destroy a minion. If drawn this turn, instead
    # destroy all minions except this one.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_NOT_DRAWN_THIS_TURN: 0,
    }
    powered_up = Find(SELF + DRAWN_THIS_TURN)
    play = powered_up & Destroy(ALL_MINIONS - SELF) | Destroy(TARGET)


class BT_301:
    """Nightshade Matron / 夜影主母
    突袭，战吼： 弃掉你手牌中法力值消耗最高的牌。"""

    # <b>Rush</b> <b>Battlecry:</b> Discard your highest Cost card.
    play = Discard(HIGHEST_COST(FRIENDLY_HAND))


class BT_304:
    """Enhanced Dreadlord / 改进型恐惧魔王
    嘲讽，亡语：召唤一个5/5并具有吸血的恐惧魔王。"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 5/5 Dreadlord with
    # <b>Lifesteal</b>.
    deathrattle = Summon(CONTROLLER, "BT_304t")


class BT_305:
    """Imprisoned Scrap Imp / 被禁锢的拾荒小鬼
    休眠2回合。唤醒时，使你手牌中的所有随从牌获得+2/+2。"""

    # <b>Dormant</b> for 2 turns. When this awakens, give all minions in your
    # hand +2/+2.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Buff(FRIENDLY_HAND, "BT_305e")


BT_305e = buff(+2, +2)


class BT_307:
    """Darkglare / 黑眼
    战吼：如果你的英雄在本回合受到过伤害，复原3个法力水晶。"""

    # After your hero takes damage, refresh 2 Mana_Crystals.
    events = Damage(FRIENDLY_HERO).on(FillMana(CONTROLLER, 2))


class BT_309:
    """Kanrethad Ebonlocke / 坎雷萨德·埃伯洛克
    你的恶魔牌法力值消耗减少（1）点。亡语：将“终极坎雷萨德”洗入你的牌库。"""

    # [x]Your Demons cost (1) less. <b>Deathrattle:</b> Shuffle 'Kanrethad
    # Prime' into your deck.
    update = Refresh(FRIENDLY_HAND + DEMON, {GameTag.COST: -1})
    deathrattle = Shuffle(CONTROLLER, "BT_309t")


class BT_309t:
    """Kanrethad Prime"""

    # <b>Battlecry:</b> Summon 3 friendly Demons that died_this game.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + DEMON) * 3))


##
# Spells


class BT_199:
    """Unstable Felbolt / 不稳定的邪能箭
    对一个敌方随从和一个随机友方随从造成$3点伤害。"""

    # Deal $3 damage to an enemy minion and a random friendly one.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Hit(TARGET, 3), Hit(RANDOM_FRIENDLY_MINION, 3)


class BT_300:
    """Hand of Gul'dan / 古尔丹之手
    当你使用或弃掉这张牌时，抽三张牌。"""

    # When you play or discard this, draw 3 cards.
    play = discard = Draw(CONTROLLER) * 3


class BT_302:
    """The Dark Portal / 黑暗之门
    抽一张随从牌。如果你拥有至少八张手牌，则使其法力值消耗减少（5）点。"""

    # Draw a minion. If you have at least 8 cards in hand, it costs (5) less.
    powered_up = Count(FRIENDLY_HAND - SELF) >= 7
    play = powered_up & (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
            Buff(ForceDraw.TARGET, "BT_302e")
        )
    ) | (ForceDraw(RANDOM(FRIENDLY_DECK + MINION)))


class BT_302e:
    tags = {GameTag.COST: -5}
    events = REMOVED_IN_PLAY


class BT_306:
    """Shadow Council / 暗影议会
    随机将你的手牌替换成恶魔牌，并使它们获得+2/+2。"""

    # Replace your hand with random Demons. Give them +2/+2.
    def play(self):
        hand_cards = list(self.controller.hand)
        for card in hand_cards:
            morphed = yield Morph(card, RandomDemon())
            if morphed:
                yield Buff(morphed, "BT_306e")


BT_306e = buff(+2, +2)
