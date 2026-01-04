from ..utils import *


##
# Minions

class SCH_310:
    """Lab Partner / 研究搭档
    Spell Damage +1 / 法术伤害+1"""

    # 1费 1/3 法术伤害+1
    # 法术伤害通过 CardDefs.xml 中的 spellDamage 属性定义
    pass


class SCH_241:
    """Firebrand / 火印随从
    Spellburst: Deal 4 damage randomly split among all enemy minions.
    法术迸发：造成4点伤害，随机分配到所有敌方随从上。"""

    # 3费 3/4 法术迸发：造成4点伤害，随机分配到所有敌方随从上
    spellburst = Hit(RANDOM_ENEMY_MINION, 1) * 4


class SCH_243:
    """Wyrm Weaver / 龙织编织师
    Spellburst: Summon two 1/3 Mana Wyrms.
    法术迸发：召唤两个1/3的法力浮龙。"""

    # 4费 3/5 法术迸发：召唤两个1/3的法力浮龙
    # NEW1_012 是法力浮龙的卡牌ID
    spellburst = Summon(CONTROLLER, "NEW1_012") * 2


class SCH_400:
    """Mozaki, Master Duelist / 决斗大师莫扎奇
    After you cast a spell, gain Spell Damage +1.
    在你施放一个法术后，获得法术伤害+1。"""

    # 5费 3/8 传说 在你施放一个法术后，获得法术伤害+1
    events = CastSpell(CONTROLLER).after(Buff(SELF, "SCH_400e"))


SCH_400e = buff(spellpower=1)


##
# Spells

class SCH_353:
    """Cram Session / 临阵刷夜
    Draw $1 cards (improved by Spell Damage).
    抽1张牌（受法术伤害加成影响）。"""

    # 2费 抽1张牌（受法术伤害加成影响）
    # 抽牌数 = 1 + 法术伤害
    play = Draw(CONTROLLER) * (1 + CURRENT_SPELLPOWER(FRIENDLY_HERO))


class SCH_348:
    """Combustion / 燃烧
    Deal $4 damage to a minion. Any excess damages both neighbors.
    对一个随从造成4点伤害。超出的伤害会分配到相邻的随从上。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        target = self.target
        # 对目标造成4点伤害
        target_health_before = target.health
        yield Hit(target, 4)

        # 计算超出的伤害（如果目标被消灭）
        if target.dead:
            excess_damage = 4 - target_health_before
            if excess_damage > 0:
                # 获取相邻的随从
                adjacent = target.adjacent_minions
                if adjacent:
                    # 将超出伤害分配到相邻随从
                    for minion in adjacent:
                        yield Hit(minion, excess_damage)
