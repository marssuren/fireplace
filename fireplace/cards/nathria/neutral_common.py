"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_004:
    """Soul Seeker - 搜魂者
    <b>Battlecry:</b> Swap this with a random minion from your opponent's deck.
    <b>战吼：</b>与对手牌库中的一个随机随从交换。
    """
    play = (
        # 从对手牌库中随机选择一个随从并移到己方手牌
        Give(CONTROLLER, RANDOM(ENEMY_DECK + MINION)),
        # 将自己洗入对手牌库
        Shuffle(OPPONENT, SELF)
    )


class REV_012:
    """Bog Beast - 沼泽兽
    [x]<b><b>Taunt</b></b>
<b>Deathrattle:</b> Summon a 2/4
Muckmare with <b>Taunt</b>.
    <b>嘲讽，亡语：</b>召唤一个2/4并具有<b>嘲讽</b>的淤泥梦魇。
    """
    tags = {GameTag.TAUNT: True}
    deathrattle = Summon(CONTROLLER, "REV_012t")


class REV_012t:
    """Muckmare - 淤泥梦魇"""
    tags = {GameTag.TAUNT: True}


class REV_013:
    """Stoneborn Accuser - 石裔指控者
    [x]<b>Infuse (5):</b> Gain
"<b>Battlecry:</b> Deal 5
damage."
    <b>注能(5)：</b>获得"<b>战吼：</b>造成5点伤害"。
    """
    # Infuse 机制已在核心实现（card.py:394-413, actions.py:391-414）
    # 当友方随从死亡时，手牌中的 Infuse 卡牌获得充能
    # 达到阈值后，可通过 self.infused 属性检查是否已注能
    infuse = 5  # 注能阈值
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    
    def play(self):
        if self.infused:
            # 注能后：获得战吼效果
            yield Buff(SELF, "REV_013e")


class REV_013e:
    """Infused - 已注能"""
    tags = {GameTag.BATTLECRY: True}
    play = Hit(TARGET, 5)


class REV_014:
    """Red Herring - 红鲱鱼
    [x]<b>Taunt</b>
Your non-Red Herring
minions have <b>Stealth</b>.
    <b>嘲讽</b>，你的其他随从具有<b>潜行</b>。
    """
    tags = {GameTag.TAUNT: True}
    # 给所有其他友方随从添加潜行
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.STEALTH: True})


class REV_015:
    """Masked Reveler - 假面狂欢者
    [x]<b>Rush</b>
<b>Deathrattle:</b> Summon
a 2/2 copy of another
minion in your deck.
    <b>突袭，亡语：</b>召唤一个你牌库中其他随从的2/2复制。
    """
    tags = {GameTag.RUSH: True}
    
    def deathrattle(self):
        # 从牌库中随机选择一个随从（排除自己）
        minion = yield RANDOM(FRIENDLY_DECK + MINION - ID("REV_015"))
        if minion:
            # 召唤一个2/2的复制
            copy = yield Summon(CONTROLLER, ExactCopy(minion))
            if copy:
                # 使用 SetTag 设置为2/2
                copy.tags[GameTag.ATK] = 2
                copy.tags[GameTag.HEALTH] = 2
                copy.damage = 0  # 重置伤害


class REV_020:
    """Dinner Performer - 晚宴表演者
    [x]<b>Battlecry:</b> Summon a
random minion from
your deck that you
can afford to play.
    <b>战吼：</b>从你的牌库中召唤一个你能打得起的随机随从。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 获取牌库中费用 <= 当前可用法力的随从
        affordable_minions = [card for card in self.controller.deck 
                             if card.type == CardType.MINION and card.cost <= self.controller.mana]
        if affordable_minions:
            # 随机选择一个并召唤
            minion = self.game.random.choice(affordable_minions)
            yield Summon(CONTROLLER, minion)


class REV_251:
    """Sinrunner - 罪奔者
    <b>Deathrattle:</b> Destroy a random enemy minion.
    <b>亡语：</b>消灭一个随机敌方随从。
    """
    deathrattle = Destroy(RANDOM_ENEMY_MINION)


class REV_308:
    """Maze Guide - 迷宫向导
    <b>Battlecry</b>: Summon a random 2-Cost minion.
    <b>战吼：</b>召唤一个随机的2费随从。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, RandomMinion(cost=2))


class REV_338:
    """Dredger Staff - 泥仆员工
    [x]<b>Battlecry:</b> Give minions 
in your hand +1 Health.
    <b>战吼：</b>使你手牌中的所有随从获得+1生命值。
    """
    play = Buff(FRIENDLY_HAND + MINION, "REV_338e")


class REV_338e:
    """Dredger Staff Buff - 泥仆员工增益"""
    tags = {
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class REV_351:
    """Roosting Gargoyle - 栖巢石像鬼
    <b>Battlecry:</b> Give a friendly Beast +2 Attack.
    <b>战吼：</b>使一个友方野兽获得+2攻击力。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Buff(TARGET, "REV_351e")


class REV_351e:
    """Roosting Gargoyle Buff - 栖巢石像鬼增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }


class REV_375:
    """Stoneborn General - 石裔干将
    [x]<b>Rush</b> 
  <b>Deathrattle:</b> Summon an 
   8/8 Gravewing with <b>Rush</b>. 
    <b>突袭，亡语：</b>召唤一个8/8并具有<b>突袭</b>的墓翼。
    """
    tags = {GameTag.RUSH: True}
    deathrattle = Summon(CONTROLLER, "REV_375t")


class REV_375t:
    """Gravewing - 墓翼
    8/8 亡灵，突袭
    """
    tags = {GameTag.RUSH: True}


class REV_378:
    """Forensic Duster - 涂粉取证师
    [x]<b>Battlecry:</b> Your 
opponent's minions 
cost (1) more next turn.
    <b>战吼:</b>在对手的下个回合中，其随从的法力值消耗增加(1)点。
    """
    play = Buff(OPPONENT, "REV_378e")


class REV_378e:
    """Forensic Duster Effect - 涂粉取证师效果"""
    # 对手的随从+1费
    update = Refresh(ENEMY_HAND + MINION, buff="REV_378e2")
    # 对手回合开始时移除
    events = BeginTurn(OPPONENT).on(Destroy(SELF))


class REV_378e2:
    """Forensic Duster Cost Increase - 涂粉取证师费用增加"""
    tags = {
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class REV_837:
    """Muck Plumber - 淤泥水管工
    ALL minions cost (2) more.
    所有随从的法力值消耗增加(2)点。
    """
    # 光环效果：所有随从+2费
    update = Refresh(ALL_MINIONS, buff="REV_837e")


class REV_837e:
    """Muck Plumber Aura - 淤泥水管工光环"""
    tags = {
        GameTag.COST: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class REV_839:
    """Sinstone Totem - 罪碑图腾
    At the end of your turn, gain +1 Health.
    在你的回合结束时，获得+1生命值。
    """
    events = OWN_TURN_END.on(Buff(SELF, "REV_839e"))


class REV_839e:
    """Sinstone Totem Buff - 罪碑图腾增益"""
    tags = {
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class REV_841:
    """Anonymous Informant - 匿名线人
    <b>Battlecry:</b> The next <b>Secret</b> you play costs (0).
    <b>战吼：</b>你打出的下一个<b>奥秘</b>的法力值消耗为（0）点。
    """
    play = Buff(FRIENDLY_HERO, "REV_841e")


class REV_841e:
    """Anonymous Informant Effect - 匿名线人效果"""
    # 下一个奥秘0费
    events = Play(CONTROLLER, SECRET).after(lambda self, player, played_card, target=None: Destroy(SELF))
    
    class Hand:
        # 在手牌中时，给奥秘减费
        update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(0)})


class REV_845:
    """Volatile Skeleton - 不稳定的骷髅
    <b>Deathrattle:</b> Deal 2 damage to a random enemy.
    <b>亡语：</b>对一个随机敌人造成2点伤害。
    """
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 2)


class REV_900:
    """Scuttlebutt Ghoul - 谣言食尸鬼
    [x]<b>Taunt</b>
<b>Battlecry:</b> If you control
a <b>Secret</b>, summon a
copy of this.
    <b>嘲讽，战吼:</b>如果你控制一个<b>奥秘</b>，召唤一个本随从的复制。
    """
    tags = {GameTag.TAUNT: True}
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 检查是否控制奥秘
        if len(self.controller.secrets) > 0:
            # 召唤自己的复制
            yield Summon(CONTROLLER, ExactCopy(SELF))


class REV_916:
    """Creepy Painting - 诡异的画像
    After another minion dies, become a copy of it.
    在另一个随从死亡后，变成它的复制。
    """
    def _transform_on_death(self, card):
        # 只在其他随从死亡时触发（不是自己）
        if card != self and card.type == CardType.MINION:
            # 变成死亡随从的复制
            yield Morph(SELF, ExactCopy(card))
    
    events = Death(ALL_MINIONS - SELF).on(_transform_on_death)


class REV_945:
    """Sketchy Stranger - 模糊的陌生人
    <b>Battlecry:</b> <b>Discover</b> a <b>Secret</b> from another class.
    <b>战吼:</b>从其他职业的<b>奥秘</b>中<b>发现</b>一张。
    """
    def play(self):
        # 发现一个其他职业的奥秘
        # 官方机制：从所有其他职业的奥秘中发现（展示3个选项）
        from hearthstone.enums import CardClass
        
        # 获取所有有奥秘的职业（Hunter, Mage, Paladin, Rogue）
        secret_classes = [CardClass.HUNTER, CardClass.MAGE, CardClass.PALADIN, CardClass.ROGUE]
        
        # 排除自己的职业
        other_classes = [c for c in secret_classes if c != self.controller.hero.card_class]
        
        # 从其他职业的奥秘中发现
        if other_classes:
            # 使用 Discover，它会自动从指定职业的奥秘中选择3个选项
            # 通过传入多个职业，Discover 会从所有这些职业的奥秘池中随机选择
            yield Discover(CONTROLLER, RandomSpell(card_class=other_classes, secret=True))


class REV_956:
    """Priest of the Deceased - 亡者牧师
    <b>Taunt</b>
<b>Infuse (3):</b> Gain +2/+2.
    <b>嘲讽，注能（3）：</b>获得+2/+2。
    """
    tags = {GameTag.TAUNT: True}
    infuse = 3
    
    def play(self):
        if self.infused:
            yield Buff(SELF, "REV_956e")


class REV_956e:
    """Priest of the Deceased Buff - 亡者牧师增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class REV_957:
    """Murlocula - 鱼人吸血鬼
    <b>Lifesteal</b>
<b>Infuse (4):</b> This costs (0).
    <b>吸血，注能（4）：</b>本牌的法力值消耗变为（0）点。
    """
    tags = {GameTag.LIFESTEAL: True}
    infuse = 4
    
    def play(self):
        # 如果已注能，给自己添加一个永久的减费buff
        if self.infused:
            # 注意：这个buff需要在打出前就生效，所以我们在这里不做任何事
            # 实际的减费通过 Hand 类的 update 实现
            pass
    
    class Hand:
        # 在手牌中时，如果已注能则费用变为0
        cost_mod = lambda self, i: -self.cost if self.infused else 0
