from ..utils import *


##
# Minions


class DAL_077:
    """Toxfin / 毒鳍鱼人
    战吼：使一个友方鱼人获得剧毒。"""

    # <b>Battlecry:</b> Give a friendly Murloc <b>Poisonous</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 14,
    }
    play = GivePoisonous(TARGET)


class DAL_078:
    """Traveling Healer / 旅行医者
    圣盾，战吼：恢复#3点生命值。"""

    # [x]<b>Divine Shield</b> <b>Battlecry:</b> Restore #3 Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Heal(TARGET, 3)


class DAL_086:
    """Sunreaver Spy / 夺日者间谍
    战吼：如果你控制一个奥秘，便获得+1/+1。"""

    # <b>Battlecry:</b> If you control a <b>Secret</b>, gain +1/+1.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Buff(SELF, "DAL_086e")


DAL_086e = buff(+1, +1)


class DAL_088:
    """Safeguard / 机械保险箱
    嘲讽，亡语：召唤一个0/5并具有嘲讽的保险柜。"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 0/5 Vault Safe with <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "DAL_088t2")


class DAL_089:
    """Spellbook Binder / 魔法订书匠
    战吼：如果你拥有法术伤害，抽一张牌。"""

    # <b>Battlecry:</b> If you have <b>Spell Damage</b>, draw a card.
    powered_up = Find(FRIENDLY + SPELLPOWER)
    play = powered_up & Draw(CONTROLLER)


class DAL_095:
    """Violet Spellsword / 紫罗兰魔剑士
    战吼：你手牌中每有一张法术牌，便获得+1攻击力。"""

    # [x]<b>Battlecry:</b> Gain +1 Attack for each spell in your hand.
    play = Buff(SELF, "DAL_095e") * Count(FRIENDLY_HAND + SPELL)


DAL_095e = buff(atk=1)


class DAL_400:
    """EVIL Cable Rat / 怪盗布缆鼠
    战吼：将一张跟班牌置入你的手牌。"""

    # <b>Battlecry:</b> Add a <b>Lackey</b> to_your hand.
    play = Give(CONTROLLER, RandomLackey())


class DAL_544:
    """Potion Vendor / 药水商人
    战吼：为所有友方角色恢复#2点生命值。"""

    # <b>Battlecry:</b> Restore #2 Health to all friendly characters.
    play = Heal(FRIENDLY_CHARACTERS, 2)


class DAL_551:
    """Proud Defender / 骄傲的防御者
    嘲讽 如果你没有其他随从，则拥有+2攻 击力。"""

    # <b>Taunt</b> Has +2 Attack while you [x]have no other minions.
    update = Find(FRIENDLY_MINIONS - SELF) | Refresh(SELF, {GameTag.ATK: +2})


class DAL_560:
    """Heroic Innkeeper / 霸气的旅店老板娘
    嘲讽，战吼：每有一个其他友方随从，便获得+2/+2。"""

    # <b>Taunt.</b> <b>Battlecry:</b> Gain +2/+2 for each other friendly minion.
    play = Buff(SELF, "DAL_560e2") * Count(FRIENDLY_MINIONS - SELF)


DAL_560e2 = buff(+2, +2)


class DAL_566:
    """Eccentric Scribe / 古怪的铭文师
    亡语：召唤四个1/1的复仇卷轴。"""

    # <b>Deathrattle:</b> Summon four 1/1 Vengeful Scrolls.
    deathrattle = Summon(CONTROLLER, "DAL_566t") * 4


class DAL_735:
    """Dalaran Librarian / 达拉然图书管理员
    战吼： 沉默相邻的随从。"""

    # <b>Battlecry:</b> <b>Silence</b> adjacent minions.
    play = Silence(SELF_ADJACENT)


class DAL_743:
    """Hench-Clan Hogsteed / 荆棘帮斗猪
    突袭，亡语：召唤一个1/1的鱼人。"""

    # <b>Rush</b> <b>Deathrattle:</b> Summon a 1/1 Murloc.
    deathrattle = Summon(CONTROLLER, "DAL_743t")


class DAL_744:
    """Faceless Rager / 无面暴怒者
    战吼：复制一个友方随从的生命值。"""

    # <b>Battlecry:</b> Copy a friendly minion's Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = CopyStateBuff(TARGET, "DAL_744e")


class DAL_744e:
    max_health = lambda self, _: self._xhealth


class DAL_747:
    """Flight Master / 飞行管理员
    战吼：为每个玩家召唤一只2/2的狮鹫。"""

    # <b>Battlecry:</b> Summon a 2/2 Gryphon for each player.
    play = Summon(ALL_PLAYERS, "DAL_747t")


class DAL_771:
    """Soldier of Fortune / 散财军士
    每当本随从攻击时，使你的对手获得一张幸运币。"""

    # Whenever this minion attacks, give your opponent a Coin.
    events = Attack(SELF).on(Give(OPPONENT, THE_COIN))
