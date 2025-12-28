from ..utils import *


##
# Minions


class ULD_195:
    """Frightened Flunky / 惊恐的仆从
    嘲讽，战吼： 发现一张具有嘲讽的随从牌。"""

    # <b>Taunt</b> <b>Battlecry:</b> <b>Discover</b> a <b>Taunt</b>_minion.
    play = DISCOVER(RandomMinion(taunt=True))


class ULD_253:
    """Tomb Warden / 陵墓守望者
    嘲讽 战吼：召唤一个本随从的复制。"""

    # <b>Taunt</b> <b>Battlecry:</b> Summon a copy of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class ULD_258:
    """Armagedillo / 硕铠鼠
    嘲讽 在你的回合结束时，使你手牌中所有嘲讽随从牌获得+2/+2。"""

    # [x]<b>Taunt</b> At the end of your turn, give all <b>Taunt</b> minions in your hand
    # +2/+2.
    events = OWN_TURN_END.on(Buff(FRIENDLY_HAND + MINION + TAUNT, "ULD_258e"))


ULD_258e = buff(+2, +2)


class ULD_709:
    """Armored Goon / 重甲暴徒
    每当你的英雄攻击时，便获得5点 护甲值。"""

    # Whenever your hero attacks, gain 5 Armor.
    events = Attack(FRIENDLY_HERO).on(GainArmor(FRIENDLY_HERO, 5))


class ULD_720:
    """Bloodsworn Mercenary / 血誓雇佣兵
    战吼：选择一个受伤的友方随从，召唤一个它的复制。"""

    # [x]<b>Battlecry</b>: Choose a damaged friendly minion. Summon a copy of it.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


##
# Spells


class ULD_256:
    """Into the Fray / 投入战斗
    使你手牌中的所有嘲讽随从牌获得+2/+2。"""

    # Give all <b>Taunt</b> minions in your hand +2/+2.
    play = Buff(FRIENDLY_HAND + MINION + TAUNT, "ULD_256e")


ULD_256e = buff(+2, +2)


class ULD_707:
    """Plague of Wrath / 愤怒之灾祸
    消灭所有受伤的随从。"""

    # Destroy all damaged minions.
    play = Destroy(ALL_MINIONS + DAMAGED)


class ULD_711:
    """Hack the System / 侵入系统
    任务：用你的英雄攻击5次。奖励：安拉斐特之核。"""

    # [x]<b>Quest:</b> Attack 5 times with your hero. <b>Reward:</b> Anraphet's Core.
    progress_total = 5
    quest = Attack(FRIENDLY_HERO).after(AddProgress(SELF, Attack.ATTACKER))
    reward = Summon(CONTROLLER, "ULD_711p3")


class ULD_711p3:
    """Anraphet's Core"""

    # [x]<b>Hero Power</b> Summon a 4/3 Golem. After your hero attacks, refresh this.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    activate = Summon(CONTROLLER, "ULD_711t")
    events = Attack(FRIENDLY_HERO).after(RefreshHeroPower(SELF))


##
# Weapons


class ULD_708:
    """Livewire Lance / 电缆长枪
    在你的英雄攻击后，将一张跟班牌置入你的 手牌。"""

    # After your Hero attacks, add a <b>Lackey</b> to your_hand.
    events = Attack(FRIENDLY_HERO).after(Give(CONTROLLER, RandomLackey()))
