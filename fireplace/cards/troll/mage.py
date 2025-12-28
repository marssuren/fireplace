from ..utils import *


##
# Minions


class TRL_311:
    """Arcanosaur / 奥术暴龙
    战吼：如果你在上个回合使用过元素牌，则对所有其他随从造成3点伤害。"""

    # <b>Battlecry:</b> If you played an_Elemental last turn, deal_3_damage_to_all other
    # minions.
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    play = powered_up & Hit(ALL_MINIONS - SELF, 3)


class TRL_315:
    """Pyromaniac / 火焰狂人
    每当你的英雄技能消灭一个随从，抽 一张牌。"""

    # Whenever your Hero Power_kills a minion, draw a card.
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
        Dead(Activate.TARGET) & Draw(CONTROLLER)
    )


class TRL_316(ThresholdUtils):
    """Jan'alai, the Dragonhawk"""

    # [x]<b>Battlecry:</b> If your Hero Power dealt 8 damage this game, summon Ragnaros the
    # Firelord.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = ThresholdUtils.powered_up & Summon(CONTROLLER, "TRL_316t")


class TRL_316t:
    """Ragnaros the Firelord"""

    # Can't attack. At the end of your turn, deal 8 damage to a random enemy.
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 8))


class TRL_318:
    """Hex Lord Malacrass / 妖术领主玛拉卡斯
    战吼：将你的起始手牌的复制置入手牌（不包括这张牌）。"""

    # <b>Battlecry</b>: Add a copy of your opening hand to your hand <i>(except this
    # card)</i>.
    play = Give(CONTROLLER, Copy(STARTING_HAND - SELF))


class TRL_319:
    """Spirit of the Dragonhawk / 龙鹰之灵
    潜行一回合。你的英雄技能会以选中的随从及其相邻随从作为 目标。"""

    # [x]<b>Stealth</b> for 1 turn. Your Hero Power also targets adjacent minions.
    events = OWN_TURN_BEGIN.on(Unstealth(SELF))
    update = Refresh(CONTROLLER, buff="TRL_319e")


class TRL_319e:
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).on(
        PlayHeroPower(FRIENDLY_HERO_POWER, ADJACENT(Activate.TARGET))
    )


class TRL_390:
    """Daring Fire-Eater / 大胆的吞火者
    战吼：在本回合中，你的下一个英雄技能会额外造成2点伤害。"""

    # <b>Battlecry:</b> Your next Hero Power this turn deals 2_more damage.
    play = Buff(CONTROLLER, "TRL_390e")


class TRL_390e:
    update = Refresh(CONTROLLER, {GameTag.HEROPOWER_DAMAGE: 2})
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(Destroy(SELF))


##
# Spells


class TRL_310:
    """Elemental Evocation / 元素唤醒
    在本回合中，你使用的下一张元素牌的法力值消耗减少（2）点。"""

    # The next Elemental you_play this turn costs (2) less.
    play = Buff(CONTROLLER, "TRL_310e")


class TRL_310e:
    update = Refresh(FRIENDLY_HAND + ELEMENTAL, {GameTag.COST: -2})
    events = Play(CONTROLLER, ELEMENTAL).on(Destroy(SELF))


class TRL_313:
    """Scorch / 灼烧
    对一个随从造成$4点伤害。如果你在上个回合使用过元素牌，则法力值消耗变为（1）点。"""

    # [x]Deal $4 damage to a minion. Costs (1) if you played an Elemental last turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    cost_mod = ELEMENTAL_PLAYED_LAST_TURN & -1
    play = Hit(TARGET, 4)


class TRL_317:
    """Blast Wave / 冲击波
    对所有随从造成$2点伤害。超杀：随机将一张法师法术牌置入你的手牌。"""

    # Deal $2 damage to_all minions. <b>Overkill</b>: Add a random Mage spell to your hand.
    play = Hit(ALL_MINIONS, 2)
    overkill = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))


class TRL_400:
    """Splitting Image / 裂魂残像
    奥秘：当你的随从受到攻击时，召唤一个该随从的复制。"""

    # <b>Secret:</b> When one of your minions is attacked, summon a copy of it.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, ExactCopy(Attack.DEFENDER)))
    )
