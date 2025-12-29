from ..utils import *


##
# Minions

class SCH_149:
    """Argent Braggart / 银色自大狂
    Battlecry: Set this minion's Attack and Health to the highest in the battlefield."""

    def play(self):
        # 找到战场上最高的攻击力和生命值
        all_minions = self.game.board
        if all_minions:
            max_atk = max(m.atk for m in all_minions)
            max_health = max(m.health for m in all_minions)
            # 将本随从的攻击力和生命值设置为最高值
            yield Buff(SELF, "SCH_149e", atk=max_atk, max_health=max_health)


class SCH_149e:
    """Argent Braggart Buff"""
    atk = lambda self, i: self.atk
    max_health = lambda self, i: self.max_health


class SCH_532:
    """Goody Two-Shields / 双盾优等生
    Divine Shield Spellburst: Gain Divine Shield."""

    # 圣盾（在CardDefs.xml中已定义）
    # 法术迸发：获得圣盾
    spellburst = SetAttr(SELF, GameTag.DIVINE_SHIELD, True)


class SCH_526:
    """Lord Barov / 巴罗夫领主
    Battlecry: Set the Health of all other minions to 1. Deathrattle: Deal 1 damage to all minions."""

    # 战吼：将所有其他随从的生命值变为1
    play = SetCurrentHealth(ALL_MINIONS - SELF, 1)

    # 亡语：对所有随从造成1点伤害
    deathrattle = Hit(ALL_MINIONS, 1)


class SCH_141:
    """High Abbess Alura / 高阶修士奥露拉
    Spellburst: Cast a spell from your deck (targets this if possible)."""

    def spellburst(self):
        # 从牌库中施放一张法术牌（尽可能以本随从为目标）
        spells = self.controller.deck.filter(type=CardType.SPELL)
        if spells:
            spell = random.choice(spells)
            # 尝试以本随从为目标施放法术
            yield CastSpell(spell, SELF if spell.requires_target() else None)

class SCH_139:
    """Devout Pupil / 虔诚的学徒
    Divine Shield, Taunt Costs (1) less for each spell you've cast on friendly characters this game."""

    # 圣盾、嘲讽（在CardDefs.xml中已定义）
    # 费用减免通过 Aura 实现
    cost_mod = lambda self: -Count(FRIENDLY_HERO + PLAYED_SPELL_ON_FRIENDLY_CHARACTER)


class SCH_712:
    """Judicious Junior / 踏实的大三学姐
    Lifesteal"""

    # 吸血（在CardDefs.xml中已定义）
    pass


class SCH_135:
    """Turalyon, the Tenured / 终身教授图拉扬
    Rush. Whenever this attacks a minion, set the defender's Attack and Health to 3."""

    # 突袭（在CardDefs.xml中已定义）
    # 每当本随从攻击一个随从，将目标的攻击力和生命值变为3
    events = Attack(SELF, MINION).after(
        SetAttr(Attack.DEFENDER, GameTag.ATK, 3),
        SetAttr(Attack.DEFENDER, GameTag.HEALTH, 3)
    )


##
# Spells

class SCH_247:
    """First Day of School / 新生入学
    Add 2 random 1-Cost minions to your hand."""

    # 随机将两张法力值消耗为（1）的随从牌置入你的手牌
    play = Give(CONTROLLER, RandomMinion(cost=1)) * 2


class SCH_524:
    """Shield of Honor / 荣誉护盾
    Give a damaged minion +3 Attack and Divine Shield."""

    # 使一个受伤的随从获得+3攻击力和圣盾
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    play = Buff(TARGET, "SCH_524e")


SCH_524e = buff(atk=3, divine_shield=True)


class SCH_250:
    """Wave of Apathy / 倦怠光波
    Set the Attack of all enemy minions to 1 until your next turn."""

    # 直到你的下个回合，将所有敌方随从的攻击力变为1点
    play = Buff(ENEMY_MINIONS, "SCH_250e")


class SCH_250e:
    """Wave of Apathy Buff"""
    atk = SET(1)
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class SCH_302:
    """Gift of Luminance / 流光之赐
    Give a minion Divine Shield, then summon a 1/1 copy of it."""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        yield SetAttr(TARGET, GameTag.DIVINE_SHIELD, True)
        yield Summon(CONTROLLER, ExactCopy(TARGET, atk=1, health=1))


class SCH_138:
    """Blessing of Authority / 威能祝福
    Give a minion +8/+8. It can't attack heroes this turn."""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "SCH_138e")


class SCH_138e:
    """Blessing of Authority Buff"""
    atk = 8
    max_health = 8
    tags = {GameTag.CANNOT_ATTACK_HEROES: True}
    events = TURN_END.on(Destroy(SELF))


class SCH_533:
    """Commencement / 毕业仪式
    Summon a minion from your deck. Give it Taunt and Divine Shield."""

    def play(self):
        # 从牌库中召唤一个随从
        minions = self.controller.deck.filter(type=CardType.MINION)
        if minions:
            minion = random.choice(minions)
            yield Summon(CONTROLLER, minion)
            # 使其获得嘲讽和圣盾
            yield Buff(minion, "SCH_533e")


SCH_533e = buff(taunt=True, divine_shield=True)


##
# Weapons

class SCH_523:
    """Ceremonial Maul / 仪式重槌
    Spellburst: Summon a Student with Taunt and stats equal to the spell's Cost."""

    def spellburst(self):
        # 召唤一个属性值等同于法术法力值消耗的并具有嘲讽的学生
        spell_cost = self.spellburst_spell.cost
        yield Summon(CONTROLLER, "SCH_523t", {
            GameTag.ATK: spell_cost,
            GameTag.HEALTH: spell_cost,
            GameTag.TAUNT: True
        })


class SCH_523t:
    """Devout Student / 虔诚的学生
    Student token with Taunt"""
    # Token: 属性动态设置的嘲讽学生（基础属性在CardDefs.xml中定义）
    pass
