# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 恶魔猎手
"""

from ..utils import *


class TID_703:
    """Topple the Idol - 推倒神像
    4费法术 探底。展示该牌并对所有随从造成等同于其法力值消耗的伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    
    def play(self):
        """
        探底，展示该牌并对所有随从造成等同于其费用的伤害
        """
        # 探底
        yield Dredge(CONTROLLER)
        
        # 获取牌库顶的牌
        if self.controller.deck:
            top_card = self.controller.deck[0]
            # 展示并造成伤害
            yield Reveal(top_card)
            yield Hit(ALL_MINIONS, top_card.cost)


class TID_704:
    """Fossil Fanatic - 化石狂热者
    2费 2/2 在你的英雄攻击后，抽一张邪能法术牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    events = Attack(FRIENDLY_HERO).after(ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL + FEL))


class TID_706:
    """Herald of Chaos - 混乱使徒
    3费 3/4 吸血 战吼：如果你在持有本牌期间施放过邪能法术，获得突袭。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.LIFESTEAL: True,
    }
    
    # 在手牌中时监听邪能法术施放
    # 当施放邪能法术时，给自己添加标记
    events = Play(CONTROLLER, SPELL + FEL).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TID_706_tracker")
    )
    
    def play(self):
        """
        如果持有期间施放过邪能法术，获得突袭
        """
        # 检查是否有追踪标记
        has_tracker = any(
            buff.id == "TID_706_tracker"
            for buff in self.buffs
        )
        
        if has_tracker:
            yield SetAttr(SELF, GameTag.RUSH, True)


class TID_706_tracker:
    """Herald of Chaos Tracker - 追踪标记"""
    # 这个buff只是一个标记，表示在手牌中时施放过邪能法术
    pass


class TSC_006:
    """Multi-Strike - 多重打击
    2费法术 在本回合中，使你的英雄获得+2攻击力。本回合可以额外攻击一个敌方随从。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = (
        Buff(FRIENDLY_HERO, "TSC_006e"),
        SetAttr(FRIENDLY_HERO, GameTag.EXTRA_ATTACKS_THIS_TURN, 1),
    )


class TSC_006e:
    """+2攻击力"""
    tags = {
        GameTag.ATK: 2,
    }
    events = TURN_END.on(Destroy(SELF))


class TSC_057:
    """Azsharan Defector - 艾萨拉叛逃者
    4费 5/3 突袭 亡语：将一张"沉没的叛逃者"置于你的牌库底部。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.RUSH: True,
    }
    deathrattle = ShuffleIntoDeck(CONTROLLER, "TSC_057t")


class TSC_057t:
    """Sunken Defector - 沉没的叛逃者
    4费 5/3 突袭 亡语：召唤两个本随从的复制。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.RUSH: True,
    }
    deathrattle = Summon(CONTROLLER, "TSC_057t") * 2


class TSC_058:
    """Predation - 捕食
    2费法术 造成$2点伤害。如果你在持有本牌期间打出过娜迦牌，本牌的法力值消耗为(0)点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    # 在手牌中时监听娜迦打出
    events = Play(CONTROLLER, MINION + NAGA).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TSC_058_tracker")
    )
    
    play = Hit(TARGET, 2)
    
    # 如果有追踪标记，费用为0
    def cost_mod(self):
        has_tracker = any(
            buff.id == "TSC_058_tracker"
            for buff in self.buffs
        )
        return -2 if has_tracker else 0


class TSC_058_tracker:
    """Predation Tracker - 追踪标记"""
    pass


class TSC_217:
    """Wayward Sage - 迷途贤者
    2费 2/2 流放：使你手牌中最左边和最右边的牌的法力值消耗减少(1)点。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    def outcast(self):
        """
        流放效果：减少手牌两端的费用
        """
        hand = self.controller.hand
        if len(hand) >= 2:
            # 最左边的牌
            yield Buff(hand[0], "TSC_217e")
            # 最右边的牌
            yield Buff(hand[-1], "TSC_217e")


class TSC_217e:
    """-1费用"""
    tags = {
        GameTag.COST: -1,
    }


class TSC_218:
    """Lady S'theno - 斯忒诺女士
    3费 1/4 在攻击时免疫。在你施放法术后，攻击生命值最低的敌人。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    # 攻击时免疫
    events = [
        Attack(SELF).on(SetAttr(SELF, GameTag.IMMUNE, True)),
        Attack(SELF).after(SetAttr(SELF, GameTag.IMMUNE, False)),
        # 施放法术后攻击生命值最低的敌人
        Play(CONTROLLER, SPELL).after(
            Attack(SELF, ENEMY_CHARACTERS + LOWEST_HEALTH)
        ),
    ]


class TSC_219:
    """Xhilag of the Abyss - 渊狱魔犬希拉格
    7费 3/6 巨型+4 在你的回合开始时，希拉格之茎的伤害+1。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
    }
    # 巨型+4：召唤4个附属部件
    colossal_appendages = ["TSC_219t"] * 4
    # 回合开始时，给所有茎添加伤害增加标记
    events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_MINIONS + ID("TSC_219t"), "TSC_219e"))


class TSC_219t:
    """Xhilag's Stalk - 希拉格之茎
    1费 0/2 在你的回合结束时，对一个随机敌人造成1点伤害。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
    }
    
    def trigger_end_of_turn_damage(self):
        """
        回合结束时造成伤害，伤害值 = 1 + 伤害增加buff的数量
        """
        # 统计TSC_219e buff的数量
        damage_bonus = sum(
            1 for buff in self.buffs
            if buff.id == "TSC_219e"
        )
        
        # 基础伤害1点 + 额外伤害
        total_damage = 1 + damage_bonus
        
        yield Hit(RANDOM_ENEMY_CHARACTER, total_damage)
    
    # 回合结束时触发
    events = OWN_TURN_END.on(trigger_end_of_turn_damage)


class TSC_219e:
    """+1伤害增加标记"""
    # 这个buff只是一个计数标记
    # 每个回合开始时添加一个，用于增加伤害
    # 不增加攻击力，只增加技能伤害
    pass


class TSC_608:
    """Abyssal Depths - 深渊深处
    3费法术 抽出你牌库中法力值消耗最低的两张随从牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        """
        抽出牌库中费用最低的两张随从牌
        """
        # 获取牌库中的所有随从
        minions_in_deck = [card for card in self.controller.deck if card.type == CardType.MINION]
        
        if minions_in_deck:
            # 按费用排序
            minions_in_deck.sort(key=lambda c: c.cost)
            # 抽出最低费用的两张
            for i in range(min(2, len(minions_in_deck))):
                yield ForceDraw(CONTROLLER, minions_in_deck[i])


class TSC_609:
    """Coilskar Commander - 盘蛇指挥官
    6费 3/7 嘲讽 战吼：如果你在持有本牌期间施放过三个法术，召唤两个本随从的复制。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 7,
        GameTag.COST: 6,
        GameTag.TAUNT: True,
    }
    
    # 在手牌中时监听法术施放，每次添加一个计数标记
    events = Play(CONTROLLER, SPELL).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TSC_609_tracker")
    )
    
    def play(self):
        """
        如果持有期间施放过3个法术，召唤两个复制
        """
        # 统计追踪标记的数量
        tracker_count = sum(
            1 for buff in self.buffs
            if buff.id == "TSC_609_tracker"
        )
        
        if tracker_count >= 3:
            yield Summon(CONTROLLER, ExactCopy(SELF)) * 2


class TSC_609_tracker:
    """Coilskar Commander Tracker - 法术计数标记"""
    # 每施放一个法术就添加一个这样的buff
    pass


class TSC_610:
    """Glaiveshark - 刃鲨
    4费 4/3 战吼：如果你的英雄在本回合攻击过，对所有敌人造成2点伤害。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    
    def play(self):
        """
        如果英雄本回合攻击过，对所有敌人造成2点伤害
        """
        # 检查英雄是否攻击过
        if self.controller.hero.num_attacks > 0:
            yield Hit(ENEMY_CHARACTERS, 2)


class TSC_915:
    """Bone Glaive - 骨刃
    5费 5/0武器 战吼：探底。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 5,
        GameTag.DURABILITY: 0,
        GameTag.COST: 5,
    }
    play = Dredge(CONTROLLER)
