"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_015:
    """Jury Duty - 陪审义务
    [x]Summon two
Silver Hand Recruits.
Give your Silver Hand
Recruits +1/+1.
    召唤两个白银之手新兵。使你的白银之手新兵获得+1/+1。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 召唤两个白银之手新兵
        yield Summon(CONTROLLER, "CS2_101t") * 2
        # 给所有白银之手新兵+1/+1
        yield Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "MAW_015e")


class MAW_015e:
    """Jury Duty Buff - 陪审义务增益"""
    atk = 1
    max_health = 1


class MAW_016:
    """Order in the Court - 法庭秩序
    [x]Reorder your deck from
 highest Cost to lowest
Cost. Draw a card.
    将你的牌库按照法力值消耗从高到低重新排序。抽一张牌。
    """
    def play(self):
        # 将牌库按费用从高到低排序
        if self.controller.deck:
            # 使用 Python 的 sort，按费用降序
            self.controller.deck.sort(key=lambda card: card.cost, reverse=True)
        
        # 抽一张牌
        yield Draw(CONTROLLER)


class MAW_017:
    """Class Action Lawyer - 集体诉讼律师
    [x]<b>Battlecry:</b> If your deck
has no Neutral cards, set
 a minion's stats to 1/1.
    <b>战吼：</b>如果你的牌库中没有中立卡牌，将一个随从的属性变为1/1。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 检查牌库中是否有中立卡
        from hearthstone.enums import CardClass
        has_neutral = any(card.card_class == CardClass.NEUTRAL for card in self.controller.deck)
        
        # 如果没有中立卡且有目标
        if not has_neutral and TARGET:
            # 将目标的属性设为1/1
            yield Buff(TARGET, "MAW_017e")


class MAW_017e:
    """Class Action Lawyer Debuff - 集体诉讼律师减益"""
    def apply(self, target):
        target.atk = 1
        target.max_health = 1


class REV_842:
    """Promotion - 晋升
    [x]Give a Silver Hand
Recruit +3/+3
and <b>Taunt</b>.
    使一个白银之手新兵获得+3/+3和<b>嘲讽</b>。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    # 原版只能对白银之手新兵使用，但fireplace没有内置的卡牌ID限制
    # 这里检查目标是否是白银之手新兵
    def play(self):
        # 检查目标是否是白银之手新兵
        if self.target and self.target.card_id == "CS2_101t":
            # 给目标+3/+3和嘲讽
            yield Buff(TARGET, "REV_842e")


class REV_842e:
    """Promotion Buff - 晋升增益"""
    atk = 3
    max_health = 3
    tags = {GameTag.TAUNT: True}


class REV_947:
    """Muckborn Servant - 污泥仆从
    <b>Taunt</b>
<b>Battlecry:</b> <b>Discover</b> a Paladin card.
    <b>嘲讽，战吼：</b>从圣骑士卡牌中<b>发现</b>一张。
    """
    tags = {GameTag.TAUNT: True}
    
    def play(self):
        # 从圣骑士卡牌中发现一张
        from hearthstone.enums import CardClass
        yield Discover(CONTROLLER, RandomCollectible(card_class=CardClass.PALADIN))


class REV_948:
    """Service Bell - 服务呼叫铃
    <b>Discover</b> a Class card from your deck and draw all copies of it.
    从你的牌库中<b>发现</b>一张职业卡牌，并抽出它的所有复制。
    """
    def play(self):
        # 从牌库中发现一张职业卡（非中立）
        from hearthstone.enums import CardClass
        
        # 使用标准的 Discover 从牌库中发现
        # Discover 会自动处理选项生成和选择
        card = yield Discover(CONTROLLER, FRIENDLY_DECK - NEUTRAL)
        
        if card:
            # 找出牌库中所有同名卡牌（包括刚发现的这张）
            cards_to_draw = [c for c in list(self.controller.deck) if c.card_id == card.card_id]
            
            # 使用 Draw action 抽出所有同名卡牌
            # 这会触发所有抽牌相关的逻辑和事件
            for deck_card in cards_to_draw:
                if deck_card.zone == Zone.DECK:
                    yield Draw(CONTROLLER, deck_card)


class REV_950:
    """Divine Toll - 圣洁鸣钟
    [x]Shoot 5 rays at random
minions. They give friendly
minions +2/+2, and deal $2
damage to enemy minions.
    向随机随从射出5道光线。它们使友方随从获得+2/+2，并对敌方随从造成$2点伤害。
    """
    def play(self):
        # 射出5道光线
        for i in range(5):
            # 每次重新评估存活的随从
            all_minions = [m for m in FRIENDLY_MINIONS.eval(self.game, self) if not m.dead]
            all_minions.extend([m for m in ENEMY_MINIONS.eval(self.game, self) if not m.dead])
            
            if not all_minions:
                break
            
            target = self.game.random.choice(all_minions)
            
            # 如果是友方随从，+2/+2
            if target.controller == self.controller:
                yield Buff(target, "REV_950e")
            # 如果是敌方随从，造成2点伤害
            else:
                yield Hit(target, 2)


class REV_950e:
    """Divine Toll Buff - 圣洁鸣钟增益"""
    atk = 2
    max_health = 2


class REV_951:
    """The Countess - 女伯爵
    [x]<b>Battlecry:</b> If your deck 
has no Neutral cards, add 
3 <b>Legendary </b>Invitations 
to your hand.
    <b>战吼：</b>如果你的牌库中没有中立卡牌，将3张<b>传说</b>邀请函置入你的手牌。
    """
    def play(self):
        # 检查牌库中是否有中立卡
        from hearthstone.enums import CardClass
        has_neutral = any(card.card_class == CardClass.NEUTRAL for card in self.controller.deck)
        
        # 如果没有中立卡
        if not has_neutral:
            # 添加3张传说邀请函
            # 邀请函是随机的传说圣骑士卡牌
            from hearthstone.enums import Rarity
            for i in range(3):
                yield Give(CONTROLLER, RandomCollectible(
                    card_class=CardClass.PALADIN,
                    rarity=Rarity.LEGENDARY
                ))


class REV_952:
    """Sinful Sous Chef - 罪恶的副厨师长
    <b>Deathrattle:</b> Add 2
Silver Hand Recruits
to your hand.
    <b>亡语：</b>将2个白银之手新兵置入你的手牌。
    """
    deathrattle = Give(CONTROLLER, "CS2_101t") * 2


class REV_955:
    """Stewart the Steward - 执事者斯图尔特
    [x]<b>Deathrattle:</b> Give the next
Silver Hand Recruit you
summon +3/+3 and
this <b>Deathrattle</b>.
    <b>亡语：</b>使你召唤的下一个白银之手新兵获得+3/+3和此<b>亡语</b>。
    """
    def deathrattle(self):
        # 给控制者添加一个buff，下次召唤白银之手新兵时触发
        yield Buff(FRIENDLY_HERO, "REV_955e")


class REV_955e:
    """Stewart the Steward Effect - 执事者斯图尔特效果"""
    # 监听召唤事件，参考 EX1_366 (公正之剑)
    # Summon 事件的 after 会传入 Summon.CARD
    events = Summon(CONTROLLER, MINION).after(
        # 检查召唤的是否是白银之手新兵
        Find(Summon.CARD + ID("CS2_101t")) & (
            Buff(Summon.CARD, "REV_955e2"),
            Destroy(SELF)
        )
    )


class REV_955e2:
    """Stewart the Steward Buff - 执事者斯图尔特增益"""
    atk = 3
    max_health = 3
    # 亡语：递归触发相同效果
    def deathrattle(self):
        yield Buff(FRIENDLY_HERO, "REV_955e")


class REV_958:
    """Buffet Biggun - 餐会巨仆
    [x]<b>Battlecry:</b> Summon two Silver 
Hand Recruits. <b>Infuse (3):</b> 
Give them +2 Attack 
and <b>Divine Shield</b>.
    <b>战吼：</b>召唤两个白银之手新兵。<b>注能(3)：</b>使它们获得+2攻击力和<b>圣盾</b>。
    """
    infuse = 3
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 召唤两个白银之手新兵
        recruits = yield Summon(CONTROLLER, "CS2_101t") * 2
        
        # 如果已注能，给它们+2攻击和圣盾
        if self.infused and recruits:
            for recruit in recruits:
                if recruit:
                    yield Buff(recruit, "REV_958e")


class REV_958e:
    """Buffet Biggun Buff - 餐会巨仆增益"""
    atk = 2
    tags = {GameTag.DIVINE_SHIELD: True}


class REV_961:
    """Elitist Snob - 势利精英
    [x]<b>Battlecry:</b> For each Paladin
card in your hand, randomly 
gain <b>Divine Shield</b>, <b>Lifesteal</b>, 
<b>Rush</b>, or <b>Taunt</b>.
    <b>战吼：</b>你的手牌中每有一张圣骑士卡牌，随机获得<b>圣盾</b>、<b>吸血</b>、<b>突袭</b>或<b>嘲讽</b>。
    """
    def play(self):
        # 计算手牌中圣骑士卡牌的数量
        from hearthstone.enums import CardClass
        paladin_cards = [c for c in self.controller.hand 
                        if c != self and c.card_class == CardClass.PALADIN]
        
        count = len(paladin_cards)
        
        # 随机获得能力
        buffs = ["REV_961e1", "REV_961e2", "REV_961e3", "REV_961e4"]
        
        for i in range(count):
            # 随机选择一个buff
            buff_id = self.game.random.choice(buffs)
            yield Buff(SELF, buff_id)


class REV_961e1:
    """Elitist Snob - Divine Shield"""
    tags = {GameTag.DIVINE_SHIELD: True}


class REV_961e2:
    """Elitist Snob - Lifesteal"""
    tags = {GameTag.LIFESTEAL: True}


class REV_961e3:
    """Elitist Snob - Rush"""
    tags = {GameTag.RUSH: True}


class REV_961e4:
    """Elitist Snob - Taunt"""
    tags = {GameTag.TAUNT: True}


class REV_983:
    """Great Hall - 大厅
    Set a minion's Attack and Health to 3.
    将一个随从的攻击力和生命值变为3点。
    """
    # LOCATION 卡牌
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    activate = Buff(TARGET, "REV_983e")


class REV_983e:
    """Great Hall Effect - 大厅效果"""
    def apply(self, target):
        target.atk = 3
        target.max_health = 3


