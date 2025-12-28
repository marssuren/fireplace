from ..utils import *


##
# Minions


class ULD_158:
    """Sandstorm Elemental / 沙暴元素
    战吼：对所有敌方随从造成1点伤害。 过载：（1）"""

    # <b>Battlecry:</b> Deal 1 damage to all enemy minions. <b>Overload:</b> (1)
    play = Hit(ENEMY_MINIONS, 1)


class ULD_169:
    """Mogu Fleshshaper / 魔古血肉塑造者
    突袭 战场上每有一个随从，本牌的法力值消耗便减少（1）点。"""

    # [x]<b>Rush</b>. Costs (1) less for each minion on the battlefield.
    cost_mod = -Count(ALL_MINIONS)


class ULD_170:
    """Weaponized Wasp / 武装胡蜂
    战吼：如果你控制一个跟班，造成3点 伤害。"""

    # <b>Battlecry:</b> If you control a <b>Lackey</b>, deal 3_damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_FRIENDLY_LACKEY: 0,
    }
    play = Hit(TARGET, 3)


class ULD_173:
    """Vessina / 维西纳
    当你过载时，你的其他随从拥有+2攻击力。"""

    # While you're <b>Overloaded</b>, your other minions have +2 Attack.
    update = OVERLOADED(CONTROLLER) & Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: 2})


class ULD_276:
    """EVIL Totem / 怪盗图腾
    在你的回合结束时，将一张跟班牌置入你的手牌。"""

    # At the end of your turn, add a <b>Lackey</b> to your hand.
    events = OWN_TURN_END.on(Give(CONTROLLER, RandomLackey()))


##
# Spells


class ULD_171:
    """Totemic Surge / 图腾潮涌
    使你的图腾获得+2攻击力。"""

    # Give your Totems +2_Attack.
    play = Buff(FRIENDLY_MINIONS + TOTEM, "ULD_171e")


ULD_171e = buff(atk=2)


class ULD_172:
    """Plague of Murlocs / 鱼人之灾祸
    随机将所有随从变形成为鱼人。"""

    # Transform all minions into random Murlocs.
    play = Morph(ALL_MINIONS, RandomMurloc())


class ULD_181:
    """Earthquake / 地震术
    对所有随从造成$5点伤害，再对所有随从造成$2点伤害。"""

    # Deal $5 damage to all minions, then deal $2 damage to all minions.
    play = Hit(ALL_MINIONS, 5), Hit(ALL_MINIONS, 2)


class ULD_291:
    """Corrupt the Waters / 腐化水源
    任务：使用6张战吼牌。奖励：维尔纳尔之心。"""

    # [x]<b>Quest:</b> Play 6 <b>Battlecry</b> cards. <b>Reward:</b> Heart of Vir'naal.
    progress_total = 6
    quest = Play(CONTROLLER, BATTLECRY).after(AddProgress(SELF, Play.CARD))
    reward = Summon(CONTROLLER, "ULD_291p")


class ULD_291p:
    """Heart of Vir'naal"""

    # <b>Hero Power</b> Your <b>Battlecries</b> trigger twice this turn.
    activate = Buff(CONTROLLER, "ULD_291pe")


class ULD_291pe:
    tags = {enums.EXTRA_BATTLECRIES: True}


##
# Weapons


class ULD_413:
    """Splitting Axe / 分裂战斧
    战吼：召唤你的图腾的复制。"""

    # <b>Battlecry:</b> Summon copies of your Totems.
    play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + TOTEM))
