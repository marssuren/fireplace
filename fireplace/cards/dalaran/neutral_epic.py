from ..utils import *


##
# Minions


class DAL_087:
    """Hench-Clan Hag / 荆棘帮巫婆
    战吼：召唤两个具有全部随从类型的1/1的融合怪。"""

    # <b>Battlecry:</b> Summon two 1/1 Amalgams with all minion types.
    play = SummonBothSides(CONTROLLER, "DAL_087t") * 2


class DAL_538:
    """Unseen Saboteur / 隐秘破坏者
    战吼： 随机使你的对手从手牌中施放一个法术（目标随机而定）。"""

    # <b>Battlecry:</b> Your opponent casts a random spell from their hand <i>(targets
    # chosen randomly)</i>.
    play = CastSpell(RANDOM(ENEMY_HAND + SPELL))


class DAL_548:
    """Azerite Elemental / 艾泽里特元素
    在你的回合开始时，获得法术伤害+2。"""

    # At the start of your turn, gain <b>Spell Damage +2</b>.
    events = OWN_TURN_BEGIN.on(Buff(SELF, "DAL_548e"))


DAL_548e = buff(spellpower=2)


class DAL_553:
    """Big Bad Archmage / 恶狼大法师
    在你的回合结束时，随机召唤一个法力值消耗为（6）的随从。"""

    # At the end of your turn, summon a random 6-Cost minion.
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomMinion(cost=6)))


class DAL_565:
    """Portal Overfiend / 传送门大恶魔
    战吼：将三张传送门洗入你的牌库。当抽到传送门时，召唤一个2/2并具有突袭的恶魔。"""

    # [x]<b>Battlecry:</b> Shuffle 3 Portals into your deck. When drawn, summon a 2/2 Demon
    # with <b>Rush</b>.
    play = Shuffle(CONTROLLER, "DAL_582t") * 3


class DAL_592:
    """Batterhead / 莽头食人魔
    突袭 在本随从攻击并消灭一个随从后，可再次攻击。"""

    # <b>Rush</b>. After this attacks and kills a minion, it may_attack again.
    events = Attack(SELF, ALL_MINIONS).after(Dead(Attack.DEFENDER) & ExtraAttack(SELF))


class DAL_742:
    """Whirlwind Tempest / 暴走旋风
    你的风怒随从拥有超级风怒。"""

    # Your minions with <b>Windfury</b> have <b>Mega-Windfury</b>.
    update = Refresh(FRIENDLY_MINIONS + WINDFURY, {GameTag.MEGA_WINDFURY: True})


class DAL_773:
    """Magic Carpet / 魔法飞毯
    在你使用一张法力值消耗为（1）的随从牌后，使其获得+1攻击力和突袭。"""

    # After you play a 1-Cost minion, give it +1 Attack and <b>Rush</b>.
    events = Play(CONTROLLER, MINION + (COST == 1)).after(Buff(Play.CARD, "DAL_773e"))


DAL_773e = buff(atk=1, rush=True)
