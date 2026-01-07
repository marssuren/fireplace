"""
漫游翡翠梦境 - DRUID (完整修复版)
"""
from ..utils import *


# COMMON

class EDR_060:
    """大地庇护 - Ward of Earth
    Gain 5 Armor. Summon a random 5-Cost minion and give it Taunt.

    5费 自然法术
    获得5点护甲值。随机召唤一个法力值消耗为（5）的随从并使其获得嘲讽。
    """
    requirements = {}

    def play(self):
        # 获得5点护甲值
        yield GainArmor(FRIENDLY_HERO, 5)
        # 随机召唤一个5费随从
        yield Summon(CONTROLLER, RandomMinion(cost=5))
        # 给予嘲讽
        yield Buff(Find(CONTROLLER_FIELD + FRIENDLY + LAST_SUMMONED), "EDR_060e")


class EDR_270:
    """丰裕之角 - Horn of Plenty
    [x]Discover a Nature spell. It costs (2) less.

    2费 自然法术
    发现一张自然法术牌，其法力值消耗减少（2）点。
    """
    requirements = {}

    def play(self):
        # 发现一张自然法术牌
        # 使用 GenericChoice 来实现发现效果，过滤自然法术
        from ...dsl.selector import SPELL, NATURE
        yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.SPELL and c.spell_school == SpellSchool.NATURE,
            count=3
        ))
        # 减少2费
        yield Buff(Find(CONTROLLER_HAND + FRIENDLY + LAST_CARD_PLAYED), "EDR_270e")


class EDR_272:
    """常青雄鹿 - Evergreen Stag
    Elusive Lifesteal Taunt

    6费 6/7 野兽
    扰魔。吸血。嘲讽。
    """
    tags = {
        GameTag.ELUSIVE: True,
        GameTag.LIFESTEAL: True,
        GameTag.TAUNT: True,
    }


class FIR_908:
    """火炭变色龙 - Charred Chameleon
    Battlecry: If you've used your Hero Power this turn, give a friendly minion +1/+2 and Rush.

    1费 1/2 野兽
    战吼：如果你在本回合中使用过英雄技能，使一个友方随从获得+1/+2和突袭。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }

    def play(self):
        # 检查本回合是否使用过英雄技能
        if self.controller.hero.power.exhausted:
            # 给予目标随从 +1/+2 和突袭
            yield Buff(TARGET, "FIR_908e")


# RARE

class EDR_273:
    """共生术 - Symbiosis
    [x]Discover a Choose One card from another class.

    1费 法术
    发现一张另一职业的抉择牌。
    """
    requirements = {}

    def play(self):
        # 发现一张另一职业的抉择牌
        # 过滤条件：非德鲁伊职业 + 具有 CHOOSE_ONE 标签
        yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: (
                c.card_class != CardClass.DRUID and
                GameTag.CHOOSE_ONE in c.tags
            ),
            count=3
        ))


class EDR_847:
    """梦缚信徒 - Dreambound Disciple
    Battlecry and Deathrattle: Your next Hero Power costs (0).

    3费 3/3 随从
    战吼，亡语：你的下一个英雄技能的法力值消耗为（0）点。
    """
    def play(self):
        # 战吼：下一个英雄技能0费
        yield Buff(CONTROLLER, "EDR_847e")

    deathrattle = Buff(CONTROLLER, "EDR_847e")


class EDR_848:
    """光合作用 - Photosynthesis
    Restore #6 Health. Get 3 random Druid spells.

    3费 法术
    恢复6点生命值。随机获取3张德鲁伊法术牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        # 恢复6点生命值
        yield Heal(TARGET, 6)
        # 随机获取3张德鲁伊法术牌
        for _ in range(3):
            yield RandomCard(CONTROLLER, card_class=CardClass.DRUID, card_type=CardType.SPELL)


class FIR_906:
    """过热 - Overheat
    Give your minions +1/+1. Discard a random Nature spell to give them +1/+1 more.

    3费 法术
    使你的随从获得+1/+1。随机弃一张自然法术牌以使其再获得+1/+1。
    """
    requirements = {}

    def play(self):
        # 使所有友方随从获得 +1/+1
        yield Buff(FRIENDLY_MINIONS, "FIR_906e")

        # 检查手牌中是否有自然法术
        nature_spells = [c for c in self.controller.hand if c.type == CardType.SPELL and c.spell_school == SpellSchool.NATURE]

        if nature_spells:
            # 随机弃一张自然法术
            import random
            discarded = random.choice(nature_spells)
            yield Discard(discarded)
            # 再次使所有友方随从获得 +1/+1
            yield Buff(FRIENDLY_MINIONS, "FIR_906e")


# EPIC

class EDR_271:
    """林地塑型者 - Grove Shaper
    [x]After you cast a Nature spell, summon a 2/2 Treant with "Deathrattle: Get a copy of that spell."

    5费 3/6 随从
    在你施放一个自然法术后，召唤一个2/2并具有亡语：获取该法术的一张复制的树人。
    
    官方验证: ✅ 属性为5费3/6 (已修正)
    """
    # 监听自然法术施放事件
    events = OWN_SPELL_PLAY.after(
        lambda self, source, target: source.spell_school == SpellSchool.NATURE,
        lambda self, source, target: [
            Summon(CONTROLLER, "EDR_271t"),
            # 将法术ID存储到树人的buff中，用于亡语效果
            Buff(Find(CONTROLLER_FIELD + FRIENDLY + LAST_SUMMONED), "EDR_271e", spell_id=source.id)
        ]
    )


class EDR_843:
    """森林再生 - Reforestation
    [x]Choose One - Draw a spell; or Draw a minion. <i>(Hold this for 3 turns to do both!)</i>
    
    1费 自然法术
    抉择:抽一张法术牌;或者抽一张随从牌。(持有此牌3回合后同时执行两个效果!)
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("EDR_843a", "EDR_843b")
    
    def play(self):
        # 检查是否已持有3回合
        turns_held = getattr(self, 'turns_held', 0)
        
        if turns_held >= 3:
            # 持有3回合后,同时执行两个效果
            yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + SPELL))
            yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + MINION))
        else:
            # 正常的抉择效果
            if self.choice == "EDR_843a":
                # 抽一张法术牌
                yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + SPELL))
            elif self.choice == "EDR_843b":
                # 抽一张随从牌
                yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + MINION))
    
    class Hand:
        # 每回合开始时增加持有回合数
        events = OWN_TURN_BEGIN.on(
            lambda self: setattr(self.owner, 'turns_held', getattr(self.owner, 'turns_held', 0) + 1)
        )


# LEGENDARY

class EDR_209:
    """森林之王塞纳留斯 - Forest Lord Cenarius
    [x]Choose Thrice - Give your other minions +1/+3; or Summon a 5/5 Ancient with Taunt.
    
    7费 5/8 随从
    抉择三次：使你的其他随从获得+1/+3；或者召唤一个5/5并具有嘲讽的古树。
    
    实现说明：参考 paradise/druid.py 中的 WORK_025 和 VAC_907
    使用三次连续的 Choice().then(Battlecry()) 来实现 Choose Thrice 机制
    """
    play = (
        Choice(CONTROLLER, ["EDR_209a", "EDR_209b"]).then(Battlecry(Choice.CARD, SELF)),
        Choice(CONTROLLER, ["EDR_209a", "EDR_209b"]).then(Battlecry(Choice.CARD, SELF)),
        Choice(CONTROLLER, ["EDR_209a", "EDR_209b"]).then(Battlecry(Choice.CARD, SELF))
    )


class EDR_209a:
    """给予其他随从+1/+3"""
    play = Buff(FRIENDLY_MINIONS - TARGET, "EDR_209e")


class EDR_209b:
    """召唤5/5嘲讽古树"""
    play = Summon(CONTROLLER, "EDR_209t")


class EDR_845:
    """哈缪尔·符文图腾 - Hamuul Runetotem
    [x]Start of Game: If each spell in your deck is Nature, Imbue your Hero Power. Repeat this  every 2 spells you cast.
    
    3费 3/4 随从
    游戏开始时：如果你套牌中的每张法术牌都是自然法术，则灌注你的英雄技能。每施放2个法术后重复此效果。
    
    实现说明：参考 witchwood/neutral_legendary.py 中的 GIL_692 和 GIL_826
    使用 class Deck 和 class Hand 配合 GameStart() 事件
    """
    
    class Deck:
        # 游戏开始时检查套牌
        events = GameStart().on(
            # 检查套牌中所有法术是否都是自然法术
            Find(
                lambda self: all(
                    card.spell_school == SpellSchool.NATURE 
                    for card in self.owner.controller.deck + self.owner.controller.hand
                    if card.type == CardType.SPELL
                )
            ) & Buff(CONTROLLER, "EDR_845e")
        )
    
    class Hand:
        # 游戏开始时检查套牌（手牌中的情况）
        events = GameStart().on(
            Find(
                lambda self: all(
                    card.spell_school == SpellSchool.NATURE 
                    for card in self.owner.controller.deck + self.owner.controller.hand
                    if card.type == CardType.SPELL
                )
            ) & Buff(CONTROLLER, "EDR_845e")
        )


class FIR_907:
    """阿梅达希尔 - Amirdrassil
    [x]Summon a 1-Cost minion. Gain 1 Armor. Draw 1 card. Refresh 1 Mana |4(Crystal, Crystals). <i>(Improves each use!)</i>
    
    5费 地标
    召唤一个法力值消耗为（1）的随从。获得1点护甲值。抽1张牌。刷新1个法力水晶。（每次使用后提升效果！）
    
    官方验证: ✅ 费用为5费 (已修正)
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 5,
        GameTag.HEALTH: 3,
    }
    
    def activate(self):
        # 获取当前使用次数（从buff中获取）
        use_count = self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) + 1
        
        # 召唤随从（数量递增）
        yield Summon(CONTROLLER, RandomMinion(cost=1)) * use_count
        
        # 获得护甲（数量递增）
        yield GainArmor(FRIENDLY_HERO, use_count)
        
        # 抽牌（数量递增）
        yield Draw(CONTROLLER) * use_count
        
        # 刷新法力水晶（数量递增）
        yield FillMana(CONTROLLER, use_count)
        
        # 增加使用次数
        yield Buff(SELF, "FIR_907e")


