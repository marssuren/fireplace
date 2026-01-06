"""
威兹班的工坊 - DEATHKNIGHT
"""
from ..utils import *


# COMMON

class MIS_006:
    """玩具盗窃恶鬼 - Toysnatching Geist
    [x]Gigantify Battlecry: Discover an Undead. Reduce its Cost by this minion's Attack.
    """
    # 3/2/1 Gigantify 战吼：发现一张亡灵牌。使其法力值消耗减少（等同于本随从的攻击力）
    def play(self):
        # Discover 一张亡灵牌
        card = yield DISCOVER(RandomCollectible(race=Race.UNDEAD))
        if card:
            # 减少费用，减少量 = 本随从的攻击力
            yield Buff(card[0], "MIS_006e")


class MIS_006e:
    """费用减少 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 费用减少量等于施法者的攻击力
    # 这个 buff 需要在创建时记录攻击力值
    # 由于 Gigantify 机制，攻击力可能不同
    cost_mod = lambda self, i: -self.source.atk if hasattr(self, 'source') else 0


class TOY_821:
    """毛绒暴暴狗 - Rambunctious Stuffy
    Rush After you cast a Frost spell, gain Reborn.
    """
    # 3/4/2 突袭。在你施放一张冰霜法术后，获得复生
    # 双种族：UNDEAD + BEAST
    rush = True
    events = Play(CONTROLLER, SPELL + FROST).after(GiveReborn(SELF))


class TOY_824:
    """黑棘针线师 - Darkthorn Quilter
    [x]At the end of your turn, deal this minion's Attack damage randomly split among enemies.
    """
    # 4/2/4 在你的回合结束时，随机对敌方角色造成等同于本随从攻击力的伤害（分摊）
    # 双种族：UNDEAD + QUILBOAR
    events = OWN_TURN_END.on(
        Hit(RANDOM_ENEMY_CHARACTER, ATK(SELF)) * ATK(SELF)
    )


class TOY_827:
    """蹒跚的僵尸坦克 - Shambling Zombietank
    [x]Taunt Battlecry: Spend 5 Corpses to summon a copy of this.
    """
    # 2/3/2 嘲讽 战吼：消耗5具尸体以召唤一个本随从的复制
    # 双种族：UNDEAD + MECHANICAL
    taunt = True
    
    def play(self):
        if self.controller.corpses >= 5:
            yield SpendCorpses(CONTROLLER, 5)
            yield Summon(CONTROLLER, ExactCopy(SELF))


# RARE

class MIS_100:
    """屈辱头盔 - Helm of Humiliation
    Give a minion -5/-5. Give a minion in your hand +5/+5.
    """
    # 2费法术 使一个随从获得-5/-5。使你手牌中的一个随从获得+5/+5
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        yield Buff(TARGET, "MIS_100e")
        # 给手牌中的一个随从+5/+5
        hand_minion = yield RandomTarget(FRIENDLY_HAND + MINION)
        if hand_minion:
            yield Buff(hand_minion, "MIS_100e2")


class MIS_100e:
    """-5/-5 Debuff"""
    tags = {
        GameTag.ATK: -5,
        GameTag.HEALTH: -5,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class MIS_100e2:
    """+5/+5 Buff"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class MIS_101:
    """海绵斧 - Foamrender
    Whenever your hero attacks, spend 3 Corpses to gain +1 Durability.
    """
    # 3/3/2 武器 每当你的英雄攻击时，消耗3具尸体以获得+1耐久度
    events = Attack(FRIENDLY_HERO).after(
        Find(Attr(CONTROLLER, "corpses") >= 3) & (
            SpendCorpses(CONTROLLER, 3),
            Buff(SELF, "MIS_101e")
        )
    )


class MIS_101e:
    """+1 耐久度"""
    tags = {
        GameTag.DURABILITY: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_825:
    """小型法术尖晶石 - Lesser Spinel Spellstone
    Give Undead in your hand +1/+1. <i>(Gain 5 Corpses to upgrade.)</i>
    """
    # 1费法术 使你手牌中的亡灵获得+1/+1（获得5具尸体后升级）
    play = Buff(FRIENDLY_HAND + UNDEAD, "TOY_825e")
    
    class Hand:
        # 在手牌中时，监听获得尸体事件
        # 当累计获得5具尸体时，升级为 TOY_825t（不是 t2！）
        events = GainCorpses(CONTROLLER, 5).after(Morph(SELF, "TOY_825t"))


class TOY_825t:
    """法术尖晶石 - Spinel Spellstone (Upgraded)
    Give Undead in your hand +2/+2. <i>(Gain 5 Corpses to upgrade.)</i>
    """
    # 升级版本：+2/+2
    play = Buff(FRIENDLY_HAND + UNDEAD, "TOY_825e2")
    
    class Hand:
        # 继续监听，再获得5具尸体时升级为最终版本 TOY_825t2
        events = GainCorpses(CONTROLLER, 5).after(Morph(SELF, "TOY_825t2"))


class TOY_825t2:
    """大型法术尖晶石 - Greater Spinel Spellstone
    Give Undead in your hand +3/+3.
    """
    # 最终版本：+3/+3
    play = Buff(FRIENDLY_HAND + UNDEAD, "TOY_825e3")


class TOY_825e:
    """+1/+1 Buff"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_825e2:
    """+2/+2 Buff"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_825e3:
    """+3/+3 Buff"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_826:
    """绝望线缕 - Threads of Despair
    Give all minions "Deathrattle: Deal 1 damage to all minions."
    """
    # 3费法术 使所有随从获得"亡语：对所有随从造成1点伤害"
    play = Buff(ALL_MINIONS, "TOY_826e")


class TOY_826e:
    """亡语：对所有随从造成1点伤害"""
    deathrattle = Hit(ALL_MINIONS, 1)


class TOY_828:
    """业余傀儡师 - Amateur Puppeteer
    [x]Miniaturize, Taunt Deathrattle: Give Undead in your hand +2/+2.
    """
    # 5/2/6 Miniaturize 嘲讽 亡语：使你手牌中的亡灵获得+2/+2
    # Miniaturize 机制由核心引擎自动处理（card.py 的 _set_zone 方法）
    taunt = True
    deathrattle = Buff(FRIENDLY_HAND + UNDEAD, "TOY_828e")


class TOY_828e:
    """+2/+2 Buff"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# EPIC

class TOY_822:
    """蛛丝缝纫 - Silk Stitching
    Choose a friendly minion. Discover a spell that costs (4) or less for it to cast when it dies.
    """
    # 2费法术 选择一个友方随从。发现一张法力值消耗不高于(4)的法术，使其在死亡时施放
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # Discover 一张费用<=4的法术
        cards = yield DISCOVER(RandomCollectible(card_type=CardType.SPELL, cost=range(0, 5)))
        if cards and self.target:
            # 给目标随从添加亡语：施放这张法术
            # 将法术 ID 存储在 buff 中
            spell_id = cards[0].id
            yield Buff(TARGET, "TOY_822e", spell_id=spell_id)


class TOY_822e:
    """亡语：施放发现的法术"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, spell_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id
    
    @property
    def deathrattle(self):
        """动态生成亡语效果：施放存储的法术"""
        if hasattr(self, 'spell_id') and self.spell_id:
            # 施放存储的法术
            # 不指定目标，让法术根据自身的要求选择目标
            # 如果法术需要目标，引擎会自动选择随机有效目标
            return CastSpell(self.spell_id)
        return None


class TOY_823:
    """彩虹裁缝 - Rainbow Seamstress
    [x]Battlecry: If your deck started with a Blood, Frost, or Unholy card, gain Lifesteal, Reborn, or Rush respectively.
    """
    # 3/3/3 战吼：如果你的套牌中有鲜血/冰霜/邪恶符文牌，分别获得吸血/复生/突袭
    def play(self):
        # 检查起始套牌中的符文类型
        starting_deck = self.controller.starting_deck
        
        has_blood = any(
            card.data.tags.get(GameTag.RUNE_BLOOD, 0) > 0 
            for card in starting_deck
        )
        has_frost = any(
            card.data.tags.get(GameTag.RUNE_FROST, 0) > 0 
            for card in starting_deck
        )
        has_unholy = any(
            card.data.tags.get(GameTag.RUNE_UNHOLY, 0) > 0 
            for card in starting_deck
        )
        
        if has_blood:
            yield GiveLifesteal(SELF)
        if has_frost:
            yield GiveReborn(SELF)
        if has_unholy:
            yield GiveRush(SELF)


# LEGENDARY

class TOY_829:
    """无头骑士 - The Headless Horseman
    [x]Battlecry: Destroy the enemy minion with the most <i>Attack!</i> Shuffle my Head into your deck, you must get it <i>back!</i>
    """
    # 6费英雄牌 30生命值 5护甲
    # 英雄技能: TOY_829hp3 (跃马攻击)
    # 
    # 官方数据显示：
    # - TOY_829: 可收集的英雄牌 (30生命, 5护甲, 英雄技能 hp3)
    # - TOY_829t: 无头骑士的头颅 (Cast When Drawn 法术)
    # - TOY_829t2: 找回头颅后的英雄 (30生命, 0护甲, 英雄技能 hp)
    #
    # 注意：TOY_829 本身就是 HERO 类型，不像加拉克苏斯需要 Summon 另一个英雄
    # fireplace 引擎会自动处理 HERO 类型卡牌的打出和替换
    
    def play(self):
        # 战吼效果：消灭攻击力最高的敌方随从
        highest_atk_enemy = ENEMY_MINIONS.eval(self.game, self)
        if highest_atk_enemy:
            max_atk = max(m.atk for m in highest_atk_enemy)
            targets = [m for m in highest_atk_enemy if m.atk == max_atk]
            if targets:
                yield Destroy(targets[0])
        
        # 将头颅洗入牌库
        yield Shuffle(CONTROLLER, "TOY_829t")


class TOY_830:
    """玩具医生斯缔修 - Dr. Stitchensew
    [x]Battlecry: Discover a 5, 3, and 1-Cost minion to stitch to this. Deathrattle: Summon the 5-Cost minion.
    """
    # 6/6/4 战吼：发现一张5费、3费和1费随从缝合到本随从上。亡语：召唤该5费随从
    # 
    # 官方机制："套娃效果"（Nesting Doll Effect）
    # - TOY_830 死亡 → 召唤 5费随从（带亡语）
    # - 5费随从死亡 → 召唤 3费随从（带亡语）
    # - 3费随从死亡 → 召唤 1费随从
    # 
    # 参考：Rattlegore (SCH_621), Nesting Golem (TOY_893)
    
    def play(self):
        # Discover 5费随从
        card_5 = yield DISCOVER(RandomCollectible(card_type=CardType.MINION, cost=5))
        # Discover 3费随从
        card_3 = yield DISCOVER(RandomCollectible(card_type=CardType.MINION, cost=3))
        # Discover 1费随从
        card_1 = yield DISCOVER(RandomCollectible(card_type=CardType.MINION, cost=1))
        
        # 存储发现的随从ID，用于构建亡语链
        minion_5_id = card_5[0].id if card_5 else None
        minion_3_id = card_3[0].id if card_3 else None
        minion_1_id = card_1[0].id if card_1 else None
        
        # 给自己添加亡语：召唤5费随从（带有召唤3费的亡语）
        if minion_5_id:
            yield Buff(SELF, "TOY_830e", 
                      minion_5_id=minion_5_id, 
                      minion_3_id=minion_3_id, 
                      minion_1_id=minion_1_id)


class TOY_830e:
    """缝合亡语 - 第一层（TOY_830 的亡语）"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, minion_5_id=None, minion_3_id=None, minion_1_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.minion_5_id = minion_5_id
        self.minion_3_id = minion_3_id
        self.minion_1_id = minion_1_id
    
    @property
    def deathrattle(self):
        """动态生成亡语效果：召唤5费随从，并给它添加召唤3费的亡语"""
        if hasattr(self, 'minion_5_id') and self.minion_5_id:
            # 召唤5费随从，然后给它添加亡语
            return Summon(CONTROLLER, self.minion_5_id).then(
                # 如果有3费随从，给召唤的5费随从添加亡语
                Find(self.minion_3_id) & Buff(
                    Summon.CARD, 
                    "TOY_830e2", 
                    minion_3_id=self.minion_3_id, 
                    minion_1_id=self.minion_1_id
                ) if self.minion_3_id else None
            )
        return None


class TOY_830e2:
    """缝合亡语 - 第二层（5费随从的亡语）"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, minion_3_id=None, minion_1_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.minion_3_id = minion_3_id
        self.minion_1_id = minion_1_id
    
    @property
    def deathrattle(self):
        """动态生成亡语效果：召唤3费随从，并给它添加召唤1费的亡语"""
        if hasattr(self, 'minion_3_id') and self.minion_3_id:
            # 召唤3费随从，然后给它添加亡语
            return Summon(CONTROLLER, self.minion_3_id).then(
                # 如果有1费随从，给召唤的3费随从添加亡语
                Find(self.minion_1_id) & Buff(
                    Summon.CARD, 
                    "TOY_830e3", 
                    minion_1_id=self.minion_1_id
                ) if self.minion_1_id else None
            )
        return None


class TOY_830e3:
    """缝合亡语 - 第三层（3费随从的亡语）"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, minion_1_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.minion_1_id = minion_1_id
    
    @property
    def deathrattle(self):
        """动态生成亡语效果：召唤1费随从（最后一层，不再添加亡语）"""
        if hasattr(self, 'minion_1_id') and self.minion_1_id:
            return Summon(CONTROLLER, self.minion_1_id)
        return None


