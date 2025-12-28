from ..utils import *


##
# Minions


class BT_008:
    """Rustsworn Initiate / 锈誓新兵
    亡语：召唤一个1/1并具有法术伤害+1的小鬼施法者。"""

    # <b>Deathrattle:</b> Summon a 1/1 Impcaster with <b>Spell Damage +1</b>.
    deathrattle = Summon(CONTROLLER, "BT_008t")


class BT_010:
    """Felfin Navigator / 邪鳍导航员
    战吼：使你的其他鱼人获得+1/+1。"""

    # <b>Battlecry:</b> Give your other Murlocs +1/+1.
    play = Buff(FRIENDLY_MINIONS + MURLOC - SELF, "BT_010e")


BT_010e = buff(+1, +1)


class BT_156:
    """Imprisoned Vilefiend / 被禁锢的邪犬
    休眠2回合。 突袭"""

    # <b>Dormant</b> for 2 turns. <b>Rush</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2


class BT_159:
    """Terrorguard Escapee / 逃脱的恐惧卫士
    战吼：为你的对手召唤三个1/1的女猎手。"""

    # <b>Battlecry:</b> Summon three 1/1 Huntresses for your_opponent.
    play = Summon(OPPONENT, "BT_159t")


class BT_160:
    """Rustsworn Cultist / 锈誓信徒
    战吼：使你的其他随从获得“亡语：召唤一个1/1的恶魔。”"""

    # [x]<b>Battlecry:</b> Give your other minions "<b>Deathrattle:</b> Summon
    # a 1/1 Demon."
    play = Buff(FRIENDLY_MINIONS - SELF, "BT_160e")


class BT_160e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "BT_160t")


class BT_714:
    """Frozen Shadoweaver / 冰霜织影者
    战吼： 冻结一个敌人。"""

    # <b>Battlecry:</b> <b>Freeze</b> an_enemy.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Freeze(TARGET)


class BT_715:
    """Bonechewer Brawler / 噬骨殴斗者
    嘲讽 每当本随从受到伤害，便获得+2攻击力。"""

    # [x]<b>Taunt</b> Whenever this minion takes _damage, gain +2 Attack.
    events = SELF_DAMAGE.on(Buff(SELF, "BT_715e"))


BT_715e = buff(atk=2)


class BT_716:
    """Bonechewer Vanguard / 噬骨先锋
    嘲讽 每当本随从受到伤害，便获得+2攻击力。"""

    # [x]<b>Taunt</b> Whenever this minion takes damage, gain +2 Attack.
    events = SELF_DAMAGE.on(Buff(SELF, "BT_716e"))


BT_715e = buff(atk=2)


class BT_717:
    """Burrowing Scorpid / 潜地蝎
    战吼：造成2点伤害。如果消灭了目标，则获得潜行。"""

    # [x]<b>Battlecry:</b> Deal 2 damage. If that kills the target, gain
    # <b>Stealth</b>.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 2), Dead(TARGET) & Stealth(SELF)


class BT_720:
    """Ruststeed Raider / 锈骑劫匪
    嘲讽，突袭， 战吼：在本回合获得+4攻击力。"""

    # <b>Taunt</b>, <b>Rush</b> <b>Battlecry:</b> Gain +4 Attack this turn.
    play = Buff(SELF, "BT_720e")


BT_720e = buff(atk=4)


class BT_722:
    """Guardian Augmerchant / 防护改装师
    战吼：对一个随从造成1点伤害，并使其获得圣盾。"""

    # <b>Battlecry:</b> Deal 1 damage to a minion and give it <b>Divine
    # Shield</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), GiveDivineShield(TARGET)


class BT_723:
    """Rocket Augmerchant / 火箭改装师
    战吼：对一个随从造成1点伤害，并使其获得突袭。"""

    # <b>Battlecry:</b> Deal 1 damage to a minion and give it <b>Rush</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), GiveRush(TARGET)


class BT_724:
    """Ethereal Augmerchant / 虚灵改装师
    战吼：对一个随从造成1点伤害，并使其获得法术伤害+1。"""

    # <b>Battlecry:</b> Deal 1 damage to a minion and give it <b>Spell Damage
    # +1</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Buff(TARGET, "BT_724e")


BT_724e = buff(spellpower=1)


class BT_726:
    """Dragonmaw Sky Stalker / 龙喉巡天者
    亡语：召唤一个3/4的龙骑士。"""

    # <b>Deathrattle:</b> Summon a 3/4 Dragonrider.
    deathrattle = Summon(CONTROLLER, "BT_726t")


class BT_727:
    """Soulbound Ashtongue / 魂缚灰舌
    每当本随从受到伤害，对你的英雄造成等量的伤害。"""

    # Whenever this minion takes damage, also deal that amount to your hero.
    events = SELF_DAMAGE.on(Hit(FRIENDLY_HERO, Damage.AMOUNT))


class BT_728:
    """Disguised Wanderer / 变装游荡者
    亡语：召唤一个9/1的审判官。"""

    # <b>Deathrattle:</b> Summon a 9/1 Inquisitor.
    deathrattle = Summon(CONTROLLER, "BT_728t")


class BT_730:
    """Overconfident Orc / 狂傲的兽人
    嘲讽 当有所有生命值时，本随从拥有+2攻击力。"""

    # <b>Taunt</b> While at full Health, this has +2 Attack.
    update = Find(DAMAGED + SELF) | Refresh(SELF, {GameTag.ATK: +2})


class BT_732:
    """Scavenging Shivarra / 食腐破坏魔
    战吼：造成6点伤害，随机分配到所有其他随从身上。"""

    # <b>Battlecry:</b> Deal 6 damage randomly split among all_other minions.
    play = Hit(RANDOM_OTHER_MINION, 1) * 6


class BT_734:
    """Supreme Abyssal / 渊狱至尊
    无法攻击英雄。"""

    # Can't attack heroes.
    tags = {GameTag.CANNOT_ATTACK_HEROES: True}
