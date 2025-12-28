from ..utils import *


##
# Minions


class LOOT_111:
    """Scorp-o-matic / 机械异种蝎
    战吼： 消灭一个攻击力小于或等于1的随从。"""

    # <b>Battlecry:</b> Destroy a minion with 1 or less Attack.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_MAX_ATTACK: 1,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Destroy(TARGET)


class LOOT_118:
    """Ebon Dragonsmith / 黑色龙兽铁匠
    战吼：随机使你手牌中的一张武器牌的 法力值消耗减少（2）点。"""

    # <b>Battlecry:</b> Reduce the Cost of a random weapon in your hand by (2).
    play = Buff(RANDOM(FRIENDLY_HAND + MINION), "LOOT_118e")


class LOOT_118e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -2}


class LOOT_124:
    """Lone Champion / 孤胆英雄
    战吼：如果你没有控制其他随从，则获得嘲讽和圣盾。"""

    # <b>Battlecry:</b> If you control no other minions, gain <b>Taunt</b> and <b>Divine
    # Shield</b>.
    play = Find(FRIENDLY_MINIONS - SELF) | Buff(SELF, "LOOT_124e"), GiveDivineShield(
        SELF
    )


LOOT_124e = buff(taunt=True)


class LOOT_150:
    """Furbolg Mossbinder / 缚苔熊怪
    战吼：将一个友方随从变形成为一个6/6的元素。"""

    # <b>Battlecry:</b> Transform a friendly minion into a 6/6_Elemental.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Morph(TARGET, "LOOT_150t1")


class LOOT_154:
    """Gravelsnout Knight / 砂齿骑兵
    战吼：为你的对手随机召唤一个法力值消耗为（1）的随从。"""

    # <b>Battlecry:</b> Summon a random 1-Cost minion for_your opponent.
    play = Summon(OPPONENT, RandomMinion(cost=1))


class LOOT_218:
    """Feral Gibberer / 凶猛的聒噪怪
    在本随从攻击一方英雄后，将一张它的复制置入你的手牌。"""

    # After this minion attacks a hero, add a copy of it to_your hand.
    events = Attack(SELF, ENEMY_HERO).after(Give(CONTROLLER, Copy(SELF)))


class LOOT_382:
    """Kobold Monk / 狗头人武僧
    你的英雄拥有扰魔。"""

    # Your hero can't be targeted by spells or Hero_Powers.
    update = Refresh(
        FRIENDLY_HERO,
        {
            GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
            GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
        },
    )


class LOOT_383:
    """Hungry Ettin / 饥饿的双头怪
    嘲讽，战吼： 为你的对手随机召唤一个法力值消耗为（2）的随从。"""

    # <b>Taunt</b> <b>Battlecry:</b> Summon a random 2-Cost minion for your opponent.
    play = Summon(OPPONENT, RandomMinion(cost=2))


class LOOT_394:
    """Shrieking Shroom / 闪光的蘑菇
    在你的回合结束时，随机召唤一个法力值消耗为（1）的随从。"""

    # At the end of your turn, summon a random 1-Cost minion.
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomMinion(cost=1)))
