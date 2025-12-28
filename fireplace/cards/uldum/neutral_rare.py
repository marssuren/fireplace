from ..utils import *


##
# Minions


class ULD_157:
    """Questing Explorer / 奋进的探险者
    战吼：如果你控制一个任务，抽一张牌。"""

    # <b>Battlecry:</b> If you control a <b>Quest</b>, draw a card.
    play = Find(FRIENDLY_QUEST) & Draw(CONTROLLER)


class ULD_180:
    """Sunstruck Henchman / 中暑的匪徒
    在你的回合开始时，本随从有50%的几率陷入沉睡。"""

    # At the start of your turn, this has a 50% chance to_fall asleep.
    events = OWN_TURN_BEGIN.on(
        COINFLIP & SetTags(SELF, {GameTag.NUM_TURNS_IN_PLAY: -1})
    )


class ULD_196:
    """Neferset Ritualist / 尼斐塞特仪祭师
    战吼：为相邻的随从恢复所有生命值。"""

    # <b>Battlecry:</b> Restore adjacent minions to full_Health.
    play = FullHeal(SELF_ADJACENT)


class ULD_197:
    """Quicksand Elemental / 流沙元素
    战吼：在本回合中，使所有敌方随从获得-2攻击力。"""

    # <b>Battlecry:</b> Give all enemy minions -2 Attack this_turn.
    play = Buff(ENEMY_MINIONS, "ULD_197e")


ULD_197e = buff(atk=-2)


class ULD_198:
    """Conjured Mirage / 魔法幻象
    嘲讽 在你的回合开始时，将本随从洗入你的 牌库。"""

    # <b>Taunt</b> At the start of your turn, shuffle this minion into your deck.
    events = OWN_TURN_BEGIN.on(Shuffle(CONTROLLER, SELF))


class ULD_208:
    """Khartut Defender / 卡塔图防御者
    嘲讽，复生。亡语：为你的英雄恢复#3点生命值。"""

    # [x]<b>Taunt</b>, <b>Reborn</b> <b>Deathrattle:</b> Restore #3 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 3)


class ULD_214:
    """Generous Mummy / 慷慨的木乃伊
    复生 你对手的卡牌法力值消耗减少（1）点。"""

    # <b>Reborn</b> Your opponent's cards cost (1) less.
    update = Refresh(ENEMY_HAND, {GameTag.COST: -1})


class ULD_215:
    """Wrapped Golem / 被缚的魔像
    复生 在你的回合结束时，召唤一只1/1并具有嘲讽的甲虫。"""

    # [x]<b>Reborn</b> At the end of your turn, summon a 1/1 Scarab with <b>Taunt</b>.
    events = OWN_TURN_END.on(Summon(CONTROLLER, "ULD_215t"))


class ULD_250:
    """Infested Goblin / 招虫的地精
    嘲讽，亡语：将两张1/1并具有嘲讽的“甲虫”置入你的手牌。"""

    # <b>Taunt</b> <b>Deathrattle:</b> Add two 1/1 Scarabs with <b>Taunt</b> to your hand.
    deathrattle = Give(CONTROLLER, "ULD_215t") * 2
