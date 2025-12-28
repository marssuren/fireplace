from ..utils import *


##
# Minions


class LOOT_069:
    """Sewer Crawler / 下水道爬行者
    战吼：召唤一个2/3的巨鼠。"""

    # <b>Battlecry:</b> Summon a 2/3_Giant Rat.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "LOOT_069t")


class LOOT_122:
    """Corrosive Sludge / 腐蚀淤泥
    战吼： 摧毁对手的武器。"""

    # <b>Battlecry:</b> Destroy your opponent's weapon.
    play = Destroy(ENEMY_WEAPON)


class LOOT_131:
    """Green Jelly / 绿色凝胶怪
    在你的回合结束时，召唤一个1/2并具有嘲讽的软泥怪。"""

    # At the end of your turn, summon a 1/2 Ooze with_<b>Taunt</b>.
    events = OWN_TURN_END.on(Summon(CONTROLLER, "LOOT_131t1"))


class LOOT_132:
    """Dragonslayer / 屠龙者
    战吼：对一条龙造成6点伤害。"""

    # <b>Battlecry:</b> Deal 6 damage to a Dragon.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 24,
    }
    play = Hit(TARGET, 6)


class LOOT_134:
    """Toothy Chest / 利齿宝箱
    在你的回合开始时，将本随从的攻击力 变为4。"""

    # At the start of your turn, set this minion's Attack to 4.
    events = OWN_TURN_BEGIN.on(Buff(SELF, "LOOT_134e"))


class LOOT_134e:
    atk = SET(4)


class LOOT_136:
    """Sneaky Devil / 鬼祟恶魔
    潜行 你的其他随从拥有+1攻击力。"""

    # <b>Stealth</b> Your other minions have +1 Attack.
    update = Refresh(FRIENDLY_MINIONS - SELF, buff="LOOT_136e")


LOOT_136e = buff(atk=1)


class LOOT_144:
    """Hoarding Dragon / 藏宝巨龙
    亡语：使你的对手获得两张幸运币。"""

    # <b>Deathrattle:</b> Give your opponent two Coins.
    deathrattle = Give(OPPONENT, THE_COIN) * 2


class LOOT_152:
    """Boisterous Bard / 喧哗的诗人
    战吼：使你的其他随从获得+1生命值。"""

    # <b>Battlecry:</b> Give your other minions +1 Health.
    play = Buff(FRIENDLY_MINIONS - SELF, "LOOT_152e")


LOOT_152e = buff(health=1)


class LOOT_153:
    """Violet Wurm / 紫色岩虫
    亡语：召唤七只1/1的肉虫。"""

    # <b>Deathrattle:</b> Summon seven 1/1 Grubs.
    deathrattle = Summon(CONTROLLER, "LOOT_153t1") * 7


class LOOT_167:
    """Fungalmancer / 菌菇术士
    战吼：使相邻的随从获得+2/+2。"""

    # <b>Battlecry:</b> Give adjacent minions +2/+2.
    play = Buff(SELF_ADJACENT, "LOOT_167e")


LOOT_167e = buff(+2, +2)


class LOOT_184:
    """Silver Vanguard / 白银先锋
    亡语： 招募一个法力值消耗为（8）的随从。"""

    # <b>Deathrattle:</b> <b>Recruit</b> an 8-Cost minion.
    deathrattle = Recruit(COST == 8)


class LOOT_233:
    """Cursed Disciple / 被诅咒的门徒
    亡语：召唤一个5/1的亡魂。"""

    # <b>Deathrattle:</b> Summon a 5/1 Revenant.
    deathrattle = Summon(CONTROLLER, "LOOT_233t")


class LOOT_291:
    """Shroom Brewer / 蘑菇酿酒师
    战吼： 恢复#4点生命值。"""

    # <b>Battlecry:</b> Restore 4_Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Heal(TARGET, 4)


class LOOT_347:
    """Kobold Apprentice / 狗头人学徒
    战吼：造成3点伤害，随机分配到所有敌人身上。"""

    # <b>Battlecry:</b> Deal 3 damage randomly split among all_enemies.
    play = Hit(RANDOM_ENEMY_MINION, 1) * 3


class LOOT_375:
    """Guild Recruiter / 公会招募员
    战吼：招募一个法力值消耗小于或等于（4）点的随从。"""

    # <b>Battlecry:</b> <b>Recruit</b> a minion that costs (4) or less.
    play = Recruit(COST <= 4)


class LOOT_388:
    """Fungal Enchanter / 菌菇附魔师
    战吼：为所有友方角色恢复#2点生命值。"""

    # <b>Battlecry:</b> Restore 2 Health to all friendly characters.
    play = Heal(FRIENDLY_CHARACTERS, 2)


class LOOT_413:
    """Plated Beetle / 硬壳甲虫
    亡语： 获得3点护甲值。"""

    # <b>Deathrattle:</b> Gain 3 Armor.
    deathrattle = GainArmor(FRIENDLY_HERO, 3)
