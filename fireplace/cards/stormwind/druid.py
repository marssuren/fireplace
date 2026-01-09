# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 德鲁伊
"""

from ..utils import *


class DED_001:
    """暗礁德鲁伊 / Druid of the Reef
    抉择 - 变形成为一个3/1并具有突袭的鲨鱼；或者一个1/3并具有嘲讽的乌龟。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    choose = ["DED_001a", "DED_001b"]


class DED_001a:
    """鲨鱼形态"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
        GameTag.RUSH: True,
    }


class DED_001b:
    """乌龟形态"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.TAUNT: True,
    }


class DED_002:
    """月光指引 / Moonlit Guidance
    发现你的牌库中一张牌的复制。如果你在本回合中打出该牌，则抽出原版。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        发现牌库中的一张牌，打出后抽出原版
        
        实现逻辑:
        1. 发现牌库中的一张牌（自动创建复制）
        2. 给玩家添加追踪 buff 来监听该牌被打出
        """
        # 发现牌库中的一张牌
        discovered = yield Discover(CONTROLLER, FRIENDLY_DECK)
        
        if discovered:
            # 记录发现的卡牌ID
            card_id = discovered[0].id
            # 给控制者添加追踪 buff
            yield Buff(CONTROLLER, "DED_002e", discovered_card_id=card_id)


class DED_002e:
    """月光指引追踪器"""
    def apply(self, target):
        """记录发现的卡牌ID"""
        if hasattr(self, 'discovered_card_id'):
            target.moonlit_guidance_card_id = self.discovered_card_id
    
    # 监听打出卡牌
    events = [
        Play(CONTROLLER).on(
            lambda self: (
                ForceDraw(CONTROLLER, FRIENDLY_DECK + ID(getattr(self.controller, 'moonlit_guidance_card_id', None)))
                if hasattr(self.controller, 'moonlit_guidance_card_id') and Play.CARD.id == self.controller.moonlit_guidance_card_id
                else None,
                Destroy(SELF) if hasattr(self.controller, 'moonlit_guidance_card_id') and Play.CARD.id == self.controller.moonlit_guidance_card_id else None
            )
        ),
        # 回合结束时移除追踪器（只在本回合有效）
        OWN_TURN_END.on(Destroy(SELF))
    ]



class DED_003:
    """应急木工 / Jerry Rig Carpenter
    战吼：抽一张抉择法术牌并将其拆分。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    def play(self):
        """
        抽一张抉择法术并将其拆分
        
        拆分的含义：
        - 抽一张抉择法术（例如：播种施肥）
        - 将它的两个选项都作为独立卡牌加入手牌
        - 移除原版抉择法术
        
        这样玩家可以直接使用两个选项，而不需要选择
        """
        # 从牌库中找到一张抉择法术
        choose_one_spells = [c for c in self.controller.deck 
                            if c.type == CardType.SPELL and hasattr(c, 'choose') and c.choose]
        
        if choose_one_spells:
            # 抽第一张抉择法术
            card = choose_one_spells[0]
            yield Draw(CONTROLLER, card)
            
            # 拆分：将两个选项都加入手牌
            if hasattr(card, 'choose') and card.choose:
                option1_id = card.choose[0]
                option2_id = card.choose[1] if len(card.choose) > 1 else card.choose[0]
                
                yield Give(CONTROLLER, option1_id)
                yield Give(CONTROLLER, option2_id)
                
                # 移除原版抉择法术
                yield Discard(card)




class SW_419:
    """艾露恩神谕者 / Oracle of Elune
    在你打出一个法力值消耗小于或等于（2）点的随从后，召唤一个该随从的复制。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    
    events = Play(CONTROLLER, MINION + (COST <= 2)).after(
        Summon(CONTROLLER, ExactCopy(Play.CARD))
    )


class SW_422:
    """播种施肥 / Sow the Soil
    抉择 - 使你的随从获得+1攻击力；或者召唤一个2/2的树人。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    choose = ["SW_422a", "SW_422b"]


class SW_422a:
    """使你的随从获得+1攻击力"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Buff(FRIENDLY_MINIONS, "SW_422e")


class SW_422e:
    """播种施肥增益"""
    atk = 1


class SW_422b:
    """召唤一个2/2的树人"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Summon(CONTROLLER, "SW_422t")


class SW_422t:
    """树人"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
    }


class SW_428:
    """游园迷梦 / Lost in the Park
    任务线：使你的英雄获得4点攻击力。奖励：获得5点护甲值。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段都需要英雄获得4点攻击力
    questline_requirements = [4, 4, 4]
    
    def play(self):
        """打出任务线"""
        from ..enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_428e")
    
    def questline_reward_1(self):
        """阶段1奖励：获得5点护甲值"""
        return [GainArmor(FRIENDLY_HERO, 5)]
    
    def questline_reward_2(self):
        """阶段2奖励：获得5点护甲值"""
        return [GainArmor(FRIENDLY_HERO, 5)]
    
    def questline_reward_3(self):
        """阶段3奖励：获得5点护甲值"""
        return [GainArmor(FRIENDLY_HERO, 5)]


class SW_428e:
    """游园迷梦追踪器"""
    # 标记为监听英雄攻击力事件
    hero_attack_gained = True
    
    def hero_attack_gained(self, event_args):
        """
        当英雄获得攻击力时触发
        
        增加任务线进度
        """
        attack = event_args.get('attack', 0)
        if attack > 0:
            # 找到任务线
            questlines = [q for q in self.controller.secrets if q.id == "SW_428"]
            if questlines:
                from ..actions import QuestlineProgress
                yield QuestlineProgress(questlines[0], attack)


class SW_429:
    """紧壳商品 / Best in Shell
    可交易 召唤两个2/7并具有嘲讽的乌龟。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Summon(CONTROLLER, "SW_429t") * 2


class SW_429t:
    """乌龟"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 7,
        GameTag.COST: 5,
        GameTag.TAUNT: True,
    }


class SW_431:
    """花园猎豹 / Park Panther
    突袭。每当本随从攻击时，在本回合中使你的英雄获得+3攻击力。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.RUSH: True,
    }
    
    events = Attack(SELF).on(
        Buff(FRIENDLY_HERO, "SW_431e")
    )


class SW_431e:
    """花园猎豹英雄攻击力"""
    tags = {
        GameTag.ATK: 3,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }


class SW_432:
    """科多兽坐骑 / Kodo Mount
    使一个随从获得+4/+2和突袭。当其死亡时，召唤一只科多兽。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    play = Buff(TARGET, "SW_432e")


class SW_432e:
    """科多兽坐骑增益"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
    }
    deathrattle = Summon(CONTROLLER, "SW_432t")


class SW_432t:
    """科多兽"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }


class SW_436:
    """柳魔锐爪兽 / Wickerclaw
    在你的英雄获得攻击力后，本随从获得+2攻击力。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    
    # 标记为监听英雄攻击力事件
    hero_attack_gained = True
    
    def hero_attack_gained(self, event_args):
        """
        当英雄获得攻击力时触发
        
        本随从获得+2攻击力
        """
        attack = event_args.get('attack', 0)
        if attack > 0:
            yield Buff(SELF, "SW_436e")


class SW_436e:
    """柳魔锐爪兽增益"""
    atk = 2


class SW_437:
    """堆肥 / Composting
    使你的随从获得"亡语：抽一张牌"。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    play = Buff(FRIENDLY_MINIONS, "SW_437e")


class SW_437e:
    """堆肥亡语"""
    deathrattle = Draw(CONTROLLER)


class SW_439:
    """活泼的松鼠 / Vibrant Squirrel
    亡语：将4个橡果洗入你的牌库。当抽到时，召唤一个2/1的松鼠。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    
    deathrattle = Shuffle(CONTROLLER, "SW_439t") * 4


class SW_439t:
    """橡果"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    # 抽到时触发
    draw = Summon(CONTROLLER, "SW_439t2")


class SW_439t2:
    """松鼠"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


class SW_447:
    """沙德拉斯·月树 / Sheldras Moontree
    战吼：你抽到的接下来3张法术牌会在抽到时施放。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,  # 修正：7 → 5
        GameTag.COST: 8,    # 修正：7 → 8
    }
    
    play = Buff(CONTROLLER, "SW_447e")


class SW_447e:
    """沙德拉斯·月树效果"""
    def apply(self, target):
        """初始化计数器"""
        if not hasattr(target, 'sheldras_spells_remaining'):
            target.sheldras_spells_remaining = 3
    
    # 抽到法术时施放
    events = Draw(CONTROLLER, SPELL).on(
        lambda self: [
            CastSpell(CONTROLLER, Draw.CARD),
            setattr(self.controller, 'sheldras_spells_remaining', 
                   self.controller.sheldras_spells_remaining - 1),
            Destroy(SELF) if self.controller.sheldras_spells_remaining <= 0 else None
        ]
    )
