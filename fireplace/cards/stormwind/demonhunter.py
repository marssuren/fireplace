# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 恶魔猎手
"""

from ..utils import *


class DED_506:
    """贪婪需求 / Need for Greed
    可交易 抽三张牌。如果在本回合被抽到，则法力值消耗为（3）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Draw(CONTROLLER) * 3
    
    @property
    def cost_mod(self):
        """
        如果在本回合被抽到，则法力值消耗为（3）点
        
        使用 turn_drawn 属性（由 Draw action 自动设置）
        如果 turn_drawn == 当前回合，则减少2费（5 -> 3）
        """
        if hasattr(self, 'turn_drawn') and self.turn_drawn == self.game.turn:
            return -2  # 从5费减到3费
        return 0



class DED_507:
    """桅台观察员 / Crow's Nest Lookout
    战吼：对最左边和最右边的敌方随从造成2点伤害。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    def play(self):
        """对最左边和最右边的敌方随从造成2点伤害"""
        enemy_minions = self.game.opponent.field
        if enemy_minions:
            # 最左边的随从
            leftmost = enemy_minions[0]
            yield Hit(leftmost, 2)
            
            # 最右边的随从（如果不是同一个）
            if len(enemy_minions) > 1:
                rightmost = enemy_minions[-1]
                yield Hit(rightmost, 2)


class DED_508:
    """试炼场 / Proving Grounds
    从你的牌库中召唤两个随从。使其互相攻击！"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
    }
    
    def play(self):
        """从牌库召唤两个随从并使其互相攻击"""
        # 从牌库中随机选择两个随从
        deck_minions = [c for c in self.controller.deck if c.type == CardType.MINION]
        
        if len(deck_minions) >= 2:
            # 随机选择两个
            minion1 = self.game.random_choice(deck_minions)
            deck_minions.remove(minion1)
            minion2 = self.game.random_choice(deck_minions)
            
            # 召唤它们
            yield Summon(CONTROLLER, minion1)
            yield Summon(CONTROLLER, minion2)
            
            # 使其互相攻击
            if minion1.zone == Zone.PLAY and minion2.zone == Zone.PLAY:
                yield Attack(minion1, minion2)


class SW_037:
    """怒缚蛮兵 / Irebound Brute
    嘲讽 在本回合中每抽一张牌，本牌的法力值消耗便减少（1）点。"""
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 7,
        GameTag.COST: 7,
        GameTag.TAUNT: True,
    }
    
    @property
    def cost_mod(self):
        """每抽一张牌减少1费"""
        return -self.controller.cards_drawn_this_turn


class SW_039:
    """一决胜负 / Final Showdown
    任务线：在一回合中抽四张牌。奖励：使抽到的牌法力值消耗减少（1）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段都需要在一回合中抽4张牌
    questline_requirements = [4, 4, 4]
    
    def play(self):
        """
        打出任务线，初始化阶段和进度
        """
        from ...enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        # 初始化任务线
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        
        # 将任务线放到奥秘区
        self.zone = Zone.SECRET
        
        # 添加追踪器
        yield Buff(CONTROLLER, "SW_039e")
    
    # 阶段1奖励
    def questline_reward_1(self):
        """阶段1完成：使抽到的牌法力值消耗减少（1）点"""
        return [Buff(CONTROLLER, "SW_039_reward")]
    
    # 阶段2奖励
    def questline_reward_2(self):
        """阶段2完成：使抽到的牌法力值消耗减少（1）点（累计-2）"""
        return [Buff(CONTROLLER, "SW_039_reward")]
    
    # 阶段3奖励（最终奖励）
    def questline_reward_3(self):
        """阶段3完成：使抽到的牌法力值消耗减少（1）点（累计-3）"""
        return [Buff(CONTROLLER, "SW_039_reward")]


class SW_039e:
    """一决胜负追踪器"""
    # 在回合开始时重置本回合抽牌计数
    events = [
        OWN_TURN_BEGIN.on(
            Buff(CONTROLLER, "SW_039_turn_tracker")
        ),
        # 每次抽牌时检查进度
        Draw(CONTROLLER).on(
            Find(FRIENDLY_SECRETS + ID("SW_039")) & 
            QuestlineProgress(FRIENDLY_SECRETS + ID("SW_039"), 1)
        ),
    ]


class SW_039_turn_tracker:
    """回合追踪器 - 在回合结束时重置任务线进度"""
    def apply(self, target):
        """在回合结束时重置任务线进度"""
        # 找到任务线
        questlines = [q for q in target.controller.secrets if q.id == "SW_039"]
        if questlines:
            from ...enums import QUESTLINE_PROGRESS
            questlines[0].tags[QUESTLINE_PROGRESS] = 0
    
    events = OWN_TURN_END.on(Destroy(SELF))



class SW_039_reward:
    """一决胜负奖励 - 使抽到的牌法力值消耗减少（1）点"""
    # 每次抽牌时减费
    events = Draw(CONTROLLER).on(
        Buff(Draw.CARD, "SW_039_cost_reduction")
    )


class SW_039_cost_reduction:
    """抽到的牌减费"""
    cost = -1


class SW_040:
    """邪能弹幕 / Fel Barrage
    对生命值最低的敌人造成$2点伤害两次。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    def play(self):
        """对生命值最低的敌人造成2点伤害两次"""
        for _ in range(2):
            enemies = self.game.opponent.characters
            if enemies:
                # 找到生命值最低的敌人
                lowest_health_enemy = min(enemies, key=lambda x: x.health)
                yield Hit(lowest_health_enemy, 2)


class SW_041:
    """敏捷咒符 / Sigil of Alacrity
    在你的下个回合开始时，抽一张牌，并使其法力值消耗减少（1）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    play = Buff(CONTROLLER, "SW_041e")


class SW_041e:
    """敏捷咒符效果"""
    events = OWN_TURN_BEGIN.on(
        (Draw(CONTROLLER), Buff(Draw.CARD, "SW_041e2"), Destroy(SELF))
    )


class SW_041e2:
    """敏捷咒符减费"""
    cost = -1


class SW_042:
    """固执的商贩 / Persistent Peddler
    可交易 亡语：从你的牌库中召唤一个固执的商贩。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    
    # 可交易在 CardDefs.xml 中定义
    deathrattle = Summon(CONTROLLER, FRIENDLY_DECK + ID("SW_042"))


class SW_043:
    """邪能吞食者 / Felgorger
    战吼：抽一张邪能法术牌，使其法力值消耗减少（2）点。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    
    def play(self):
        """抽一张邪能法术牌并减费"""
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL + FEL)
        
        if drawn:
            yield Buff(drawn[0], "SW_043e")


class SW_043e:
    """邪能吞食者减费"""
    cost = -2


class SW_044:
    """杰斯·织暗 / Jace Darkweaver
    战吼：施放你在本局对战中施放过的所有邪能法术（优先以敌人为目标）。"""
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 5,
        GameTag.COST: 8,
    }
    
    def play(self):
        """重新施放所有邪能法术"""
        # 找到本局游戏中施放过的所有邪能法术
        fel_spells = [
            card for card in self.controller.cards_played_this_game
            if card.type == CardType.SPELL and card.spell_school == SpellSchool.FEL
        ]
        
        # 重新施放它们
        for spell in fel_spells:
            # 使用 CastSpellTargetsEnemiesIfPossible 优先以敌人为目标
            yield CastSpellTargetsEnemiesIfPossible(CONTROLLER, Copy(spell))


class SW_451:
    """魔变鱼人 / Metamorfin
    嘲讽 战吼：如果你在本回合施放过邪能法术，则获得+2/+2。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.TAUNT: True,
    }
    
    def play(self):
        """如果本回合施放过邪能法术，获得+2/+2"""
        # 检查本回合是否施放过邪能法术
        fel_cast_this_turn = any(
            card.type == CardType.SPELL and card.spell_school == SpellSchool.FEL
            for card in self.controller.cards_played_this_turn
        )
        
        if fel_cast_this_turn:
            yield Buff(SELF, "SW_451e")


class SW_451e:
    """魔变鱼人增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class SW_452:
    """混乱吸取 / Chaos Leech
    吸血。对一个随从造成$3点伤害。流放：改为造成$5点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.LIFESTEAL: True,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        """造成3点伤害，流放时造成5点"""
        damage = 5 if self.play_outcast else 3
        yield Hit(TARGET, damage)


class SW_454:
    """雄狮之怒 / Lion's Frenzy
    攻击力等同于你在本回合中抽到的牌的数量。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        """造成等于本回合抽牌数的伤害"""
        damage = self.controller.cards_drawn_this_turn
        if damage > 0:
            yield Hit(TARGET, damage)
