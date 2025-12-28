from ..utils import *


class CS2_181:
    """Injured Blademaster / 负伤剑圣
    战吼：对自身造成4点伤害。"""

    play = Hit(SELF, 4)


class EX1_001:
    """Lightwarden / 圣光护卫者
    每当一个角色获得治疗，便获得 +2攻击力。"""

    events = Heal().on(Buff(SELF, "EX1_001e"))


EX1_001e = buff(atk=2)


class EX1_004:
    """Young Priestess / 年轻的女祭司
    在你的回合结束时，随机使另一个友方随从获得+1生命值。"""

    events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "EX1_004e"))


EX1_004e = buff(health=1)


class EX1_006:
    """Alarm-o-Bot / 报警机器人
    在你的回合开始时，随机将你的手牌中的一张随从牌与本随从 交换。"""

    events = OWN_TURN_BEGIN.on(Swap(SELF, RANDOM(FRIENDLY_HAND + MINION)))


class EX1_009:
    """Angry Chicken / 愤怒的小鸡
    受伤时拥有+5攻 击力。"""

    enrage = Refresh(SELF, buff="EX1_009e")


EX1_009e = buff(atk=5)


class EX1_043:
    """Twilight Drake / 暮光幼龙
    战吼： 你每有一张手牌，便获得+1生命值。"""

    play = Buff(SELF, "EX1_043e") * Count(FRIENDLY_HAND)


EX1_043e = buff(health=1)


class EX1_044:
    """Questing Adventurer / 任务达人
    每当你使用一张牌时，便获得+1/+1。"""

    events = OWN_CARD_PLAY.on(Buff(SELF, "EX1_044e"))


EX1_044e = buff(+1, +1)


class EX1_050:
    """Coldlight Oracle / 寒光智者
    战吼：每个玩家抽两张牌。"""

    play = Draw(ALL_PLAYERS) * 2


class EX1_055:
    """Mana Addict / 魔瘾者
    在本回合中，每当你施放一个法术，便获得+2攻击力。"""

    events = OWN_SPELL_PLAY.on(Buff(SELF, "EX1_055o"))


EX1_055o = buff(atk=2)


class EX1_058:
    """Sunfury Protector / 日怒保卫者
    战吼：使相邻的随从获得嘲讽。"""

    play = Taunt(SELF_ADJACENT)


class EX1_059:
    """Crazed Alchemist / 疯狂的炼金师
    战吼： 使一个随从的攻击力和生命值互换。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Buff(TARGET, "EX1_059e")


EX1_059e = AttackHealthSwapBuff()


class EX1_076:
    """Pint-Sized Summoner / 小个子召唤师
    你每个回合使用的第一张随从牌的法力值消耗减少（1）点。"""

    update = (Attr(CONTROLLER, GameTag.NUM_MINIONS_PLAYED_THIS_TURN) == 0) & Refresh(
        FRIENDLY_HAND + MINION, {GameTag.COST: -1}
    )


class EX1_080:
    """Secretkeeper / 奥秘守护者
    每当有一张奥秘牌被使用时，便获得+1/+1。"""

    events = OWN_SECRET_PLAY.on(Buff(SELF, "EX1_080o"))


EX1_080o = buff(+1, +1)


class EX1_085:
    """Mind Control Tech / 精神控制技师
    战吼：如果你的对手有4个或者更多随从，夺取其中一个的控制权。"""

    play = (Count(ENEMY_MINIONS) >= 4) & Steal(RANDOM_ENEMY_MINION)


class EX1_089:
    """Arcane Golem / 奥术傀儡
    冲锋，战吼：使你的对手获得一个法力水晶。"""

    play = GainMana(OPPONENT, 1)


class EX1_093:
    """Defender of Argus / 阿古斯防御者
    战吼：使相邻的随从获得+1/+1和嘲讽。"""

    play = Buff(SELF_ADJACENT, "EX1_093e")


EX1_093e = buff(+1, +1, taunt=True)


class EX1_095:
    """Gadgetzan Auctioneer / 加基森拍卖师
    每当你施放一个法术，抽一张牌。"""

    events = OWN_SPELL_PLAY.on(Draw(CONTROLLER))


class EX1_097:
    """Abomination / 憎恶
    嘲讽，亡语：对所有角色造成2点伤害。"""

    deathrattle = Hit(ALL_CHARACTERS, 2)


class EX1_103:
    """Coldlight Seer / 寒光先知
    战吼：使你的其他鱼人获得+2生命值。"""

    play = Buff(FRIENDLY_MINIONS + MURLOC - SELF, "EX1_103e")


EX1_103e = buff(health=2)


class EX1_284:
    """Azure Drake / 碧蓝幼龙
    法术伤害+1，战吼：抽一张牌。"""

    play = Draw(CONTROLLER)


class EX1_509:
    """Murloc Tidecaller / 鱼人招潮者
    每当你召唤一个鱼人，便获得 +1攻击力。"""

    events = Summon(ALL_PLAYERS, MURLOC).on(Buff(SELF, "EX1_509e"))


EX1_509e = buff(atk=1)


class EX1_584:
    """Ancient Mage / 年迈的法师
    战吼：使相邻的随从获得法术伤害+1。"""

    play = Buff(SELF_ADJACENT, "EX1_584e")


class EX1_597:
    """Imp Master / 小鬼召唤师
    在你的回合结束时，对本随从造成1点伤害，并召唤一个1/1的 小鬼。"""

    events = OWN_TURN_END.on(Hit(SELF, 1), Summon(CONTROLLER, "EX1_598"))


class EX1_616:
    """Mana Wraith / 法力怨魂
    所有随从的法力值消耗增加（1）点。"""

    update = Refresh(IN_HAND + MINION, {GameTag.COST: +1})


class NEW1_019:
    """Knife Juggler / 飞刀杂耍者
    在你召唤一个随从后，随机对一个敌人造成1点伤害。"""

    events = Summon(CONTROLLER, MINION - SELF).after(Hit(RANDOM_ENEMY_CHARACTER, 1))


class NEW1_020:
    """Wild Pyromancer / 狂野炎术师
    在你施放一个法术后，对所有随从造成1点伤害。"""

    events = OWN_SPELL_PLAY.after(Hit(ALL_MINIONS, 1))


class NEW1_025:
    """Bloodsail Corsair / 血帆海盗
    战吼：使对手的武器失去1点耐久度。"""

    play = Hit(ENEMY_WEAPON, 1)


class NEW1_026:
    """Violet Teacher / 紫罗兰教师
    每当你施放一个法术，召唤一个1/1的紫罗兰学徒。"""

    events = OWN_SPELL_PLAY.on(Summon(CONTROLLER, "NEW1_026t"))


class NEW1_037:
    """Master Swordsmith / 铸剑师
    在你的回合结束时，随机使另一个友方随从获得+1攻击力。"""

    events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "NEW1_037e"))


NEW1_037e = buff(atk=1)


class NEW1_041:
    """Stampeding Kodo / 狂奔科多兽
    战吼：随机消灭一个攻击力小于或等于2的敌方随从。"""

    play = Destroy(RANDOM(ENEMY_MINIONS - DEAD + (ATK <= 2)))


class EX1_186:
    """SI:7 Infiltrator / 军情七处渗透者
    战吼：随机摧毁一个敌方奥秘。"""

    # <b>Battlecry:</b> Destroy a random enemy <b>Secret</b>.
    play = Destroy(RANDOM(ENEMY_SECRETS))


class EX1_187:
    """Arcane Devourer / 奥术吞噬者
    每当你施放一个法术，便获得+2/+2。"""

    # Whenever you cast a spell, gain +2/+2.
    events = OWN_SPELL_PLAY.on(Buff(SELF, "EX1_187e"))


EX1_187e = buff(+2, +2)
