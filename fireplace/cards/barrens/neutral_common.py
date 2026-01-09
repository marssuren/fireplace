"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_020:
    """Razormane Raider - 钢鬃掠夺者
    Frenzy: Attack a random enemy.
    暴怒：攻击一个随机敌人。
    """
    frenzy = Attack(SELF, RANDOM_ENEMY_CHARACTER)


class BAR_021:
    """Gold Road Grunt - 黄金之路步兵
    Taunt. Frenzy: Gain Armor equal to the damage taken.
    嘲讽。暴怒：获得等同于受到伤害数值的护甲值。
    """
    frenzy = GainArmor(FRIENDLY_HERO, EventValue())


class BAR_022:
    """Peon - 苦工
    Frenzy: Add a random spell from your class to your hand.
    暴怒：将一张你职业的随机法术牌置入你的手牌。
    """
    frenzy = Give(CONTROLLER, RandomSpell(card_class=CONTROLLER_CLASS))


class BAR_024:
    """Oasis Thrasher - 绿洲长尾鳄
    Frenzy: Deal 3 damage to the enemy hero.
    暴怒：对敌方英雄造成3点伤害。
    """
    frenzy = Hit(ENEMY_HERO, 3)


class BAR_025:
    """Sunwell Initiate - 太阳之井新兵
    Frenzy: Gain Divine Shield.
    暴怒：获得圣盾。
    """
    frenzy = GiveDivineShield(SELF)


class BAR_026:
    """Death's Head Cultist - 亡首教徒
    Taunt. Deathrattle: Restore 4 Health to your hero.
    嘲讽。亡语：为你的英雄恢复4点生命值。
    """
    deathrattle = Heal(FRIENDLY_HERO, 4)


class BAR_027:
    """Darkspear Berserker - 暗矛狂战士
    Deathrattle: Deal 5 damage to your hero.
    亡语：对你的英雄造成5点伤害。
    """
    deathrattle = Hit(FRIENDLY_HERO, 5)


class BAR_060:
    """Hog Rancher - 放猪牧人
    Battlecry: Summon a 2/1 Hog with Rush.
    战吼：召唤一个2/1并具有突袭的野猪。
    """
    play = Summon(CONTROLLER, "BAR_060t")


class BAR_061:
    """Ratchet Privateer - 棘齿城私掠者
    Battlecry: Give your weapon +1 Attack.
    战吼：使你的武器获得+1攻击力。
    """
    play = Buff(FRIENDLY_WEAPON, "BAR_061e")


class BAR_061e:
    tags = {
        GameTag.ATK: 1,
    }


class BAR_062:
    """Lushwater Murcenary - 甜水鱼人佣兵
    Battlecry: If you control a Murloc, gain +1/+1.
    战吼：如果你控制一个鱼人，获得+1/+1。
    """
    play = (Find(FRIENDLY_MINIONS + MURLOC), Buff(SELF, "BAR_062e"))


class BAR_062e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_063:
    """Lushwater Scout - 甜水鱼人斥候
    After you summon a Murloc, give it +1 Attack and Rush.
    在你召唤一个鱼人后，使其获得+1攻击力和突袭。
    """
    events = Summon(CONTROLLER, MURLOC).after(
        Buff(Summon.CARD, "BAR_063e"),
        SetTag(Summon.CARD, {GameTag.RUSH: True}),
    )


class BAR_063e:
    tags = {
        GameTag.ATK: 1,
    }


class BAR_064:
    """Talented Arcanist - 精明的奥术师
    Battlecry: Your next spell this turn has Spell Damage +2.
    战吼：你在本回合中的下一个法术获得法术伤害+2。
    """
    play = Buff(FRIENDLY_HERO, "BAR_064e")


class BAR_064e:
    tags = {
        GameTag.SPELLPOWER: 2,
    }
    events = (
        Play(CONTROLLER, SPELL).after(Destroy(SELF)),
        OWN_TURN_END.on(Destroy(SELF)),
    )


class BAR_065:
    """Venomous Scorpid - 剧毒魔蝎
    Poisonous. Battlecry: Discover a spell.
    剧毒。战吼：发现一张法术牌。
    """
    play = DISCOVER(RandomSpell())


class BAR_069:
    """Injured Marauder - 受伤的掠夺者
    Taunt. Battlecry: Deal 6 damage to this minion.
    嘲讽。战吼：对该随从造成6点伤害。
    """
    play = Hit(SELF, 6)


class BAR_070:
    """Gruntled Patron - 满意的奴隶主
    Frenzy: Summon another Gruntled Patron.
    暴怒：召唤另一个满意的奴隶主。
    """
    frenzy = Summon(CONTROLLER, "BAR_070")


class BAR_074:
    """Far Watch Post - 前沿哨所
    Can't attack. After your opponent draws a card, it costs (1) more (up to 10).
    无法攻击。在你的对手抽一张牌后，使其法力值消耗增加（1）点（最多为10点）。
    """
    def _on_opponent_draw(self, source, cards):
        """对手抽牌后，增加费用"""
        if cards:
            for card in cards:
                if card:
                    yield Buff(card, "BAR_074e")
    
    events = Draw(OPPONENT).after(_on_opponent_draw)


class BAR_074e:
    max_cost = 10
    tags = {
        GameTag.COST: +1,
    }


class BAR_082:
    """Barrens Trapper - 贫瘠之地诱捕者
    Your Deathrattle cards cost (1) less.
    你的亡语牌的法力值消耗减少（1）点。
    """
    update = Refresh(FRIENDLY_HAND + DEATHRATTLE, {GameTag.COST: -1})


class BAR_743:
    """Toad of the Wilds - 狂野蟾蜍
    Taunt. Battlecry: If you're holding a Nature spell, gain +2 Health.
    嘲讽。战吼：如果你的手牌中有自然法术，获得+2生命值。
    """
    play = (Find(FRIENDLY_HAND + SPELL + NATURE), Buff(SELF, "BAR_743e"))


class BAR_743e:
    tags = {
        GameTag.HEALTH: 2,
    }


class BAR_854:
    """Kindling Elemental - 火光元素
    Battlecry: The next Elemental you play costs (1) less.
    战吼：你打出的下一张元素牌的法力值消耗减少（1）点。
    """
    play = Buff(FRIENDLY_HERO, "BAR_854e")


class BAR_854e:
    update = Refresh(FRIENDLY_HAND + ELEMENTAL, {GameTag.COST: -1})
    events = Play(CONTROLLER, ELEMENTAL).after(Destroy(SELF))


class BAR_890:
    """Crossroads Gossiper - 十字路口大嘴巴
    After a friendly Secret is revealed, gain +2/+2.
    在一个友方奥秘被揭示后，获得+2/+2。
    """
    events = Reveal(FRIENDLY + SECRET).on(Buff(SELF, "BAR_890e"))


class BAR_890e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class WC_027:
    """Devouring Ectoplasm - 吞噬软浆怪
    Deathrattle: Summon a 2/2 Adventurer with a random bonus effect.
    亡语：召唤一个2/2并具有随机奖励效果的冒险者。
    """
    deathrattle = Summon(CONTROLLER, RandomID("WC_027t", "WC_027t2", "WC_027t3", "WC_027t4"))


class WC_028:
    """Meeting Stone - 集合石
    At the end of your turn, add a 2/2 Adventurer with a random bonus effect to your hand.
    在你的回合结束时，将一个2/2并具有随机奖励效果的冒险者置入你的手牌。
    """
    events = OWN_TURN_END.on(
        Give(CONTROLLER, RandomID("WC_028t", "WC_028t2", "WC_028t3", "WC_028t4"))
    )


class WC_029:
    """Selfless Sidekick - 无私的同伴
    Battlecry: Equip a random weapon from your deck.
    战吼：从你的牌库中装备一把随机武器。
    """
    play = Equip(RANDOM(FRIENDLY_DECK + WEAPON))


