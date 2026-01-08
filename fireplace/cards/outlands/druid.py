from ..utils import *


##
# Minions


class BT_127:
    """Imprisoned Satyr / 被禁锢的萨特
    休眠2回合。唤醒时，使你手牌中的随机一张随从牌的法力值消耗减少（5）点。"""

    # [x]<b>Dormant</b> for 2 turns. When this awakens, reduce the Cost of a
    # random minion in your hand by (5).
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Buff(RANDOM(FRIENDLY_HAND + MINION), "BT_127e")


class BT_127e:
    tags = {GameTag.COST: -5}
    events = REMOVED_IN_PLAY


class BT_131:
    """Ysiel Windsinger / 伊谢尔·风歌
    你的法术的法力值消耗为（1）点。"""

    # Your spells cost (1).
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(1)})


class BT_133:
    """Marsh Hydra / 沼泽多头蛇
    突袭 在本随从攻击后，随机将一张法力值消耗为（8）的随从牌置入你的手牌。"""

    # [x]<b>Rush</b> After this attacks, add a random 8-Cost minion to your
    # hand.
    events = Attack(SELF).after(Give(CONTROLLER, RandomMinion(cost=8)))


class BT_136:
    """Archspore Msshi'fn / 孢子首领姆希菲
    嘲讽 亡语：将“终极姆希菲”洗入你的牌库。"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Shuffle 'Msshi'fn Prime' into your
    # deck.
    deathrattle = Shuffle(CONTROLLER, "BT_136t")


class BT_136t:
    """Msshi'fn Prime"""

    # <b>Taunt</b> <b>Choose One -</b> Summon a 9/9 Fungal Giant with
    # <b>Taunt</b>; or <b>Rush</b>.
    choose = ("BT_136ta", "BT_136tb")
    play = ChooseBoth(CONTROLLER) & Summon(CONTROLLER, "BT_136tt3")


class BT_136ta:
    play = Summon(CONTROLLER, "BT_136tt1")


class BT_136tb:
    play = Summon(CONTROLLER, "BT_136tt2")


##
# Spells


class BT_128:
    """Fungal Fortunes / 真菌宝藏
    抽三张牌。 弃掉抽到的所有随从牌。"""

    # Draw 3 cards. Discard any minions drawn.
    play = Draw(CONTROLLER).then(Find(Draw.CARD + MINION) & Discard(Draw.CARD)) * 3


class BT_129:
    """Germination / 萌芽分裂
    召唤一个友方随从的复制。使复制获得嘲讽。"""

    # Summon a copy of a friendly minion. Give the copy <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET)).then(Taunt(Summon.CARD))


class BT_130:
    """Overgrowth / 过度生长
    获得两个空的法力水晶。"""

    # Gain two empty Mana_Crystals.
    play = AT_MAX_MANA(CONTROLLER) & Give(CONTROLLER, "CS2_013t") | GainEmptyMana(
        CONTROLLER, 2
    )


class BT_132:
    """Ironbark / 铁木树皮
    使一个随从获得+1/+3和嘲讽。如果你拥有至少七个法力水晶，则法力值消耗为（0）点。"""

    # Give a minion +1/+3 and <b>Taunt</b>. Costs (0) if you have at least 7
    # Mana Crystals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BT_132e")

    class Hand:
        update = (MANA(CONTROLLER) >= 7) & Refresh(SELF, {GameTag.COST: SET(0)})


BT_132e = buff(atk=1, health=3, taunt=True)


class BT_134:
    """Bogbeam / 沼泽射线
    对一个随从造成$3点伤害。如果你拥有至少七个法力水晶，则法力值消耗为（0）点。"""

    # Deal $3 damage to_a minion. Costs (0) if you have at least 7 Mana
    # Crystals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)

    class Hand:
        update = (MANA(CONTROLLER) >= 7) & Refresh(SELF, {GameTag.COST: SET(0)})


class BT_135:
    """Glowfly Swarm / 萤火成群
    你的手牌中每有一张法术牌，召唤一只2/2的萤火虫。"""

    # Summon a 2/2 Glowfly for each spell in your_hand.
    play = Summon(CONTROLLER, "BT_135t") * Count(FRIENDLY_HAND + SPELL)
