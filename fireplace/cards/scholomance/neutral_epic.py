from ..utils import *


##
# Minions

class SCH_199:
    """Transfer Student / 转校生
    This has different effects based on which game board you're on."""

    # 转校生：根据游戏棋盘的不同具有不同的效果
    # 这张卡已经在fireplace中实现过了，这里保持pass即可
    pass

class SCH_714:
    """Educated Elekk / 博学的雷象
    Whenever a spell is played, this minion remembers it. Deathrattle: Shuffle the spells into your deck."""

    # 每当一个法术被施放，本随从记住它。亡语：将这些法术洗入你的牌库
    # 使用自定义 buff 来累积存储多张法术
    events = Play(ALL_PLAYERS, SPELL).on(Buff(SELF, "SCH_714e", spell_to_store=Play.CARD))


class SCH_714e:
    """Buff that stores a spell card"""
    tags = {GameTag.DEATHRATTLE: True}

    def apply(self, target):
        # 初始化存储列表（如果不存在）
        if not hasattr(target, 'stored_spells'):
            target.stored_spells = []
        # 将法术添加到列表中
        if hasattr(self, 'spell_to_store'):
            target.stored_spells.append(self.spell_to_store)

    deathrattle = lambda self: [
        Shuffle(self.controller, Copy(spell))
        for spell in getattr(self, 'stored_spells', [])
    ]

class SCH_157:
    """Enchanted Cauldron / 魔法大锅
    Spellburst: Cast a random spell of the same Cost."""

    # 法术迸发：施放一个随机的法力值消耗相同的法术
    spellburst = CastSpell(RandomSpell(cost=COST(SPELLBURST_SPELL)))

class SCH_522:
    """Steeldancer / 钢铁舞者
    Battlecry: Summon a random minion with Cost equal to your weapon's Attack."""

    # 战吼：召唤一个随机的法力值消耗等于你的武器的攻击力的随从
    play = (Find(FRIENDLY_WEAPON), Summon(CONTROLLER, RandomMinion(cost=ATK(FRIENDLY_WEAPON))))


##
# Spells

class SCH_235:
    """Devolving Missiles / 退化飞弹
    Shoot three missiles at random enemy minions that transform them into ones that cost (1) less."""

    # 向随机的敌方随从发射三枚飞弹，使其变形成为法力值消耗减少（1）点的随从
    play = Morph(RANDOM(ENEMY_MINIONS) * 3, RandomMinion(cost=COST(MORPH_TARGET) - 1))

class SCH_352:
    """Potion of Illusion / 幻象药水
    Add 1/1 copies of your minions to your hand. They cost (1)."""

    # 将你的随从的1/1复制置入你的手牌。这些复制的法力值消耗为（1）点
    play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS, atk=1, health=1, cost=1))
