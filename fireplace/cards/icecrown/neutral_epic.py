from ..utils import *


##
# Minions


class ICC_025:
    """Rattling Rascal / 骷髅捣蛋鬼
    战吼：召唤一个5/5的骷髅。 亡语：为你的对手召唤一个5/5的骷髅。"""

    play = Summon(CONTROLLER, "ICC_025t")
    deathrattle = Summon(OPPONENT, "ICC_025t")


class ICC_096:
    """Furnacefire Colossus / 熔火巨像
    战吼：弃掉你手牌中所有的武器牌，并获得这些武器的属性值。"""

    play = Discard(IN_HAND + WEAPON).then(
        Buff(
            SELF,
            "ICC_096e",
            atk=ATK(Discard.TARGET),
            max_health=CURRENT_DURABILITY(Discard.TARGET),
        )
    )


class ICC_098:
    """Tomb Lurker / 墓穴潜伏者
    战吼：随机将一个在本局对战中死亡并具有亡语的随从置入你的手牌。"""

    play = Give(CONTROLLER, Copy(RANDOM(KILLED + MINION + DEATHRATTLE)))


class ICC_701:
    """Skulking Geist / 游荡恶鬼
    战吼：摧毁双方手牌中和牌库中所有法力值消耗为（1）的 法术牌。"""

    play = Destroy((IN_DECK | IN_HAND) + (COST == 1) + SPELL)


class ICC_706:
    """Nerubian Unraveler / 蛛魔拆解者
    法术的法力值消耗增加（2）点。"""

    update = Refresh(IN_HAND + SPELL, {GameTag.COST: +2})


class ICC_810:
    """Deathaxe Punisher / 亡斧惩罚者
    战吼：随机使你手牌中一个具有吸血的随从获得+2/+2。"""

    play = Buff(RANDOM(FRIENDLY_HAND + LIFESTEAL + MINION), "ICC_810e")


ICC_810e = buff(+2, +2)


class ICC_812:
    """Meat Wagon / 绞肉车
    亡语：从你的牌库中召唤一个攻击力小于本随从攻击力的随从。"""

    deathrattle = Summon(
        CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (ATK <= ATK(SELF)))
    )


class ICC_901:
    """Drakkari Enchanter / 达卡莱附魔师
    你的回合结束效果会触发两次。"""

    update = Refresh(CONTROLLER, {enums.EXTRA_END_TURN_EFFECT: True})


class ICC_912:
    """Corpsetaker / 夺尸者
    战吼： 如果你的牌库里有嘲讽随从牌，则获得嘲讽。依此法检定是否可获得圣盾，吸血和风怒。"""

    play = (
        Find(FRIENDLY_DECK + MINION + TAUNT) & Taunt(SELF),
        Find(FRIENDLY_DECK + MINION + DIVINE_SHIELD) & GiveDivineShield(SELF),
        Find(FRIENDLY_DECK + MINION + LIFESTEAL) & GiveLifesteal(SELF),
        Find(FRIENDLY_DECK + MINION + WINDFURY) & GiveWindfury(SELF),
    )
