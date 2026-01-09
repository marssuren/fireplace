from ..utils import *


##
# Minions


class BOT_216:
    """Omega Medic / 欧米茄医护兵
    战吼：如果你有十个法力水晶，为你的英雄恢复#10点生命值。"""

    # <b>Battlecry:</b> If you have 10 Mana Crystals, restore #10 Health to your hero.
    powered_up = AT_MAX_MANA(CONTROLLER)
    play = powered_up & Heal(FRIENDLY_HERO, 10)


class BOT_258:
    """Zerek, Master Cloner / 克隆大师泽里克
    亡语：如果你对本随从施放过任意法术，再次召唤本随从。"""

    # <b>Deathrattle:</b> If you've cast any spells on this minion, resummon it.
    events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "BOT_258e"))
    deathrattle = (Actived(SELF), Summon(CONTROLLER, "BOT_258"))


class BOT_258e:
    def apply(self, target):
        target.actived = True


class BOT_509:
    """Dead Ringer / 丧钟机器人
    亡语：从你的牌库中抽一张具有亡语的随从牌。"""

    # <b>Deathrattle:</b> Draw a <b>Deathrattle</b> minion from your deck.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + DEATHRATTLE))


class BOT_558:
    """Test Subject / 实验体
    亡语：将你施放在本随从身上的所有法术洗入你的牌库。"""

    # [x]<b>Deathrattle:</b> Return any spells you cast on this minion to your hand.
    events = Play(CONTROLLER, SPELL, SELF).on(StoringBuff(SELF, "BOT_558e", Play.CARD))


class BOT_558e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, Copy(STORE_CARD))


class BOT_566:
    """Reckless Experimenter / 鲁莽的实验者
    你使用的亡语随从牌的法力值消耗减少（3）点，但会在回合结束时死亡。"""

    # [x]<b>Deathrattle</b> minions you play cost (3) less, but die at the end of the turn.
    update = Refresh(FRIENDLY_HAND + DEATHRATTLE + MINION, {GameTag.COST: -3})
    events = Play(CONTROLLER, DEATHRATTLE + MINION).after(Buff(Play.CARD, "BOT_566e"))


class BOT_566e:
    events = OWN_TURN_END.on(Destroy(OWNER))


##
# Spells


class BOT_219:
    """Extra Arms / 增生手臂
    使一个随从获得+2/+2。将一张可使一个随从获得+2/+2的“更多手臂”置入你的手牌。"""

    # [x]Give a minion +2/+2. Add 'More Arms!' to your hand that gives +2/+2.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_219e"), Give(CONTROLLER, "BOT_219t")


class BOT_219t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_219te")


BOT_219e = buff(+2, +2)


BOT_219te = buff(+2, +2)


class BOT_435:
    """Cloning Device / 克隆装置
    从你对手的牌库中发现一张随从牌的复制。"""

    # <b>Discover</b> a copy of a minion in your opponent's deck.
    play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(ENEMY_DECK + MINION)) * 3))


class BOT_517:
    """Topsy Turvy / 引力翻转
    使一个随从的攻击力和生命值 互换。"""

    # Swap a minion's Attack and Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_517e")


BOT_517e = AttackHealthSwapBuff()


class BOT_529:
    """Power Word: Replicate / 真言术：仿
    选择一个友方随从，召唤一个该随从的5/5复制。"""

    # Choose a friendly minion. Summon a 5/5 copy of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, Buff(ExactCopy(TARGET), "BOT_529e"))


class BOT_529e:
    atk = SET(5)
    max_health = SET(5)


class BOT_567:
    """Zerek's Cloning Gallery / 泽里克的克隆展
    召唤你的牌库中每一个随从的1/1复制。"""

    # Summon a 1/1 copy of_each minion in your_deck.
    play = Summon(CONTROLLER, Copy(FRIENDLY_DECK + MINION)).then(
        Buff(Summon.CARD, "BOT_567e")
    )


class BOT_567e:
    atk = SET(1)
    max_health = SET(1)
