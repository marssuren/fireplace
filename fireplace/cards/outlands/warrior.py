from ..utils import *


##
# Minions


class BT_120:
    """Warmaul Challenger / 战槌挑战者
    战吼： 选择一个敌方随从。与其战斗至死！"""

    # <b>Battlecry:</b> Choose an enemy minion. Battle it to the death!
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        yield Attack(SELF, TARGET)
        for _ in range(29):
            if not Dead(SELF | TARGET).check(self):
                yield Attack(SELF, TARGET)
            else:
                break


class BT_121:
    """Imprisoned Gan'arg / 被禁锢的甘尔葛
    休眠2回合。 唤醒时，装备一把3/2的斧子。"""

    # <b>Dormant</b> for 2 turns. When this awakens, equip a 3/2 Axe.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Summon(CONTROLLER, "CS2_106")


class BT_123:
    """Kargath Bladefist / 卡加斯·刃拳
    突袭 亡语：将“终极卡加斯”洗入你的牌库。"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Shuffle 'Kargath Prime' into your
    # deck.
    deathrattle = Shuffle(CONTROLLER, "BT_123t")


class BT_123t:
    """Kargath Prime"""

    # <b>Rush</b>. Whenever this attacks and kills a minion, gain 10 Armor.
    events = Attack(SELF, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & GainArmor(FRIENDLY_HERO, 10)
    )


class BT_138:
    """Bloodboil Brute / 沸血蛮兵
    突袭 每有一个受伤的随从，本牌的法力值消耗便减少（1）点。"""

    # <b>Rush</b> Costs (1) less for each damaged minion.
    cost_mod = -Count(DAMAGED_CHARACTERS)


class BT_140:
    """Bonechewer Raider / 噬骨骑兵
    战吼：如果有受伤的随从，便获得+1/+1和突袭。"""

    # <b>Battlecry:</b> If there is a damaged minion, gain +1/+1 and
    # <b>Rush</b>.
    powered_up = Find(ALL_MINIONS + DAMAGED)
    play = powered_up & Buff(SELF, "BT_140e")


BT_140e = buff(+1, +1, rush=True)


class BT_249:
    """Scrap Golem / 废铁魔像
    嘲讽。亡语：获得等同于本随从攻击力的护甲值。"""

    # <b>Taunt</b>. <b>Deathrattle</b>: Gain Armor equal to this minion's
    # Attack.
    deathrattle = GainArmor(FRIENDLY_HERO, ATK(SELF))


##
# Spells


class BT_117:
    """Bladestorm / 剑刃风暴
    对所有随从造成$1点伤害。重复此效果，直到某个随从 死亡。"""

    # Deal $1 damage to all minions. Repeat until one dies.
    def play(self):
        yield Hit(ALL_MINIONS, 1)
        for _ in range(29):
            if not Dead(ALL_MINIONS).check(self):
                yield Hit(ALL_MINIONS, 1)
            else:
                break


class BT_124:
    """Corsair Cache / 海盗藏品
    抽一张武器牌。使其获得+1/+1。"""

    # Draw a weapon. Give it +1 Durability.
    play = ForceDraw(RANDOM(FRIENDLY_HAND + WEAPON)).then(
        Buff(ForceDraw.TARGET, "BT_124e")
    )


BT_124e = buff(health=1)


class BT_233:
    """Sword and Board / 剑盾猛攻
    对一个随从造成$2点伤害。获得2点护甲值。"""

    # Deal $2 damage to a minion. Gain 2 Armor.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), GainArmor(FRIENDLY_HERO, 2)


##
# Weapons


class BT_781:
    """Bulwark of Azzinoth / 埃辛诺斯壁垒
    每当你的英雄即将受到伤害，改为埃辛诺斯壁垒失去1点耐久度。"""

    # [x]Whenever your hero would take damage, this loses _1 Durability
    # instead.
    events = Predamage(FRIENDLY_HERO).on(Predamage(FRIENDLY_HERO, 0), Hit(SELF, 1))
