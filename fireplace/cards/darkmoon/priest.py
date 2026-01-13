"""
暗月马戏团 - 牧师
"""
from ..utils import *


##
# Minions

class DMF_053:
    """幸运灵魂 - Fortune Teller
    战吼：如果你在本回合中抽过至少3张牌，便发现一张法术牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    # 使用 fireplace 已有的 cards_drawn_this_turn 计数器
    # 检查本回合是否抽过至少3张牌
    play = Find(Attr(CONTROLLER, "cards_drawn_this_turn") >= 3) & GenericChoice(
        CONTROLLER, Discover(CONTROLLER, cards=RandomCollectible(card_class=CardClass.PRIEST, card_type=CardType.SPELL))
    )


class DMF_056:
    """纳鲁之光 - Nazmani Bloodweaver
    战吼：如果你在本回合中受到过伤害，便发现一张法术牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    # 使用 fireplace 已有的 damaged_this_turn 计数器
    # 检查英雄本回合是否受到过伤害
    play = Find(Attr(FRIENDLY_HERO, "damaged_this_turn") > 0) & GenericChoice(
        CONTROLLER, Discover(CONTROLLER, cards=RandomCollectible(card_class=CardClass.PRIEST, card_type=CardType.SPELL))
    )


class DMF_116:
    """血色魔术师 - Blood of G'huun
    嘲讽。战吼：抽一张牌。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 9,
        GameTag.TAUNT: True,
    }
    play = Draw(CONTROLLER)


class DMF_120:
    """亚煞拉惧塑像 - Idol of Y'Shaarj
    战吼：选择一个友方随从。每当你抽一张牌，便召唤一个该随从的复制。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 8,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    # 给玩家添加buff，并将目标随从信息传递给buff
    def play(self):
        if self.target:
            # 创建buff并存储目标随从信息
            buff = self.controller.card("DMF_120e", source=self)
            buff.stored_minion_id = self.target.id  # 存储目标随从的ID
            yield Buff(CONTROLLER, buff)


class DMF_120e:
    """亚煞拉惧塑像buff
    每当抽牌时，召唤存储的随从的复制。
    """
    def apply(self, target):
        # 确保有存储的随从ID
        if not hasattr(self, 'stored_minion_id'):
            self.stored_minion_id = None
    
    # 监听抽牌事件，召唤存储的随从的复制
    events = Draw(CONTROLLER).after(
        lambda self, player: (
            Summon(CONTROLLER, self.stored_minion_id) 
            if hasattr(self, 'stored_minion_id') and self.stored_minion_id 
            else None
        )
    )


class DMF_121:
    """无名者 - The Nameless One
    战吼：选择一个随从。变成它的一个4/4复制，然后使其沉默。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    # 变成目标的复制（保持4/4），然后沉默目标
    def play(self):
        if self.target:
            # 变成目标的复制
            yield Morph(SELF, ExactCopy(self.target))
            # 设置为4/4（覆盖复制的攻击力和生命值）
            yield Buff(SELF, "DMF_121e")
            # 沉默目标
            yield Silence(self.target)


class DMF_121e:
    """设置为4/4"""
    tags = {
        GameTag.ATK: SET(4),
        GameTag.HEALTH: SET(4),
    }


class DMF_184:
    """光明战马 - Lightsteed
    战吼：如果你在本回合中恢复过生命值，便获得+2/+2。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    # 检查本回合是否有友方角色恢复过生命值
    # 包括英雄和所有友方随从
    play = Find(
        (Attr(FRIENDLY_HERO, "healed_this_turn") > 0) | 
        Find(FRIENDLY_MINIONS + (Attr(SELF, "healed_this_turn") > 0))
    ) & Buff(SELF, "DMF_184e")


class DMF_184e:
    """+2/+2"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


##
# Spells

class DMF_054:
    """洞察 - Insight
    抽一张牌。如果它的法力值消耗为(3)或更少，则再抽一张。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    # 抽一张牌，如果费用≤3则再抽一张
    # 使用 Draw.CARD 引用抽到的卡牌（即使被烧毁也能检查）
    # 如果抽到疲劳（Draw.CARD 为 None），则不会触发第二次抽牌
    play = Draw(CONTROLLER).then(
        Find(Draw.CARD) & Find(COST(Draw.CARD) <= 3) & Draw(CONTROLLER)
    )


class DMF_055:
    """吉兆精魂 - Auspicious Spirits
    召唤一个随机的法力值消耗为(4)的随从。腐蚀：改为(8)。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    play = Summon(CONTROLLER, RandomMinion(cost=4))
    corrupt = Summon(CONTROLLER, RandomMinion(cost=8))


class DMF_186:
    """掌纹预言 - Palm Reading
    发现一张法术牌。你手牌中的法术牌在本回合中法力值消耗减少(1)点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = (
        Discover(CONTROLLER, RandomCollectible(card_class=CardClass.PRIEST, card_type=CardType.SPELL)),
        Buff(CONTROLLER, "DMF_186e"),
    )


class DMF_186e:
    """手牌法术减费"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = OWN_TURN_END.on(Destroy(SELF))


class DMF_187:
    """塞泰克隐纱织者 - Sethekk Veilweaver
    造成2点伤害。如果目标是一个随从，则将一张随机牌置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = (
        Hit(TARGET, 2),
        Find(TARGET + MINION) & Give(CONTROLLER, RandomCollectible()),
    )
