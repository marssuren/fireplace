"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_018:
    """Perjury - 伪证
    [x]<b>Secret:</b> When your
turn starts, <b>Discover</b>
and cast a <b>Secret</b> from
another class.
    <b>奥秘：</b>在你的回合开始时，从其他职业的<b>奥秘</b>中<b>发现</b>一张并施放。
    """
    secret = True
    
    def _trigger(self):
        # 从其他职业的奥秘中发现一张并施放
        # 使用 RandomCollectible 配合 secret=True 和 exclude_class
        card = yield Discover(CONTROLLER, RandomCollectible(secret=True, exclude_class=CardClass.ROGUE))
        if card:
            yield CastSpell(card)
        yield Reveal(SELF)
    
    events = OWN_TURN_BEGIN.on(_trigger)


class MAW_019:
    """Murder Accusation - 谋杀指控
    Choose a minion. Destroy it after another enemy minion dies.
    选择一个随从。在另一个敌方随从死亡后，消灭它。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 给目标添加标记
        yield Buff(TARGET, "MAW_019e")


class MAW_019e:
    """Murder Accusation Mark - 谋杀指控标记"""
    # 监听敌方随从死亡
    def _check_and_destroy(self, source, entity):
        # 如果死亡的是敌方随从（不是被标记的自己）
        if entity != OWNER:
            # 消灭被标记的随从
            yield Destroy(OWNER)
    
    events = Death(ENEMY_MINIONS).on(_check_and_destroy)


class MAW_020:
    """Scribbling Stenographer - 潦草的书记员
    <b>Rush</b>. Costs (1) less for each card you've played this turn.
    <b>突袭</b>。你在本回合中每打出一张牌，其法力值消耗便减少（1）点。
    """
    tags = {GameTag.RUSH: True}
    
    class Hand:
        def cost_mod(self, source, game):
            # 本回合打出的卡牌数量
            cards_played = source.controller.cards_played_this_turn
            return -cards_played


class REV_750:
    """Sinstone Graveyard - 罪碑坟场
    [x]Summon a 1/1 Ghost.
<i>(Has +1/+1 for each other
card you played this turn!)</i>
    召唤一个1/1的幽灵。<i>（你在本回合中每打出一张其他卡牌，其便获得+1/+1！）</i>
    """
    # LOCATION 地标
    def activate(self):
        # 召唤幽灵
        ghost = yield Summon(CONTROLLER, "REV_750t")
        
        # 根据本回合打出的其他卡牌数量给予buff
        # 减1是因为不包括地标自己的激活
        if ghost:
            cards_played = max(0, self.controller.cards_played_this_turn - 1)
            if cards_played > 0:
                yield Buff(ghost, "REV_750e", atk_bonus=cards_played, health_bonus=cards_played)


class REV_750t:
    """Ghost - 幽灵"""
    # Token: 1/1 幽灵
    pass


class REV_750e:
    """Sinstone Graveyard Buff - 罪碑坟场增益"""
    def __init__(self, *args, atk_bonus=0, health_bonus=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk = atk_bonus
        self.max_health = health_bonus


class REV_825:
    """Double Cross - 双面生意
    <b>Secret:</b> When your opponent spends all their Mana, draw two cards.
    <b>奥秘：</b>当你的对手用光所有法力值时，抽两张牌。
    """
    # 监听对手使用法力
    # 当对手法力变为0时触发
    secret = SpendMana(OPPONENT).on(
        # 检查对手是否用光所有法力
        Find(OPPONENT + (MANA == 0)) & (
            Reveal(SELF),
            Draw(CONTROLLER) * 2
        )
    )


class REV_826:
    """Private Eye - 私家眼线
    [x]<b>Battlecry:</b> Cast a <b>Secret</b>
from your deck.
 <b>Combo:</b> Cast 2 instead.
    <b>战吼：</b>从你的牌库中施放一张<b>奥秘</b>。<b>连击：</b>改为施放2张。
    """
    def play(self):
        # 根据是否连击，施放不同数量的奥秘
        count = 2 if self.controller.combo else 1
        
        for i in range(count):
            # 从牌库中找奥秘
            secrets = list(FRIENDLY_DECK + SECRET).eval(self.game, self)
            if secrets:
                # 随机选择一张并施放
                secret = self.game.random.choice(secrets)
                yield CastSpell(secret)


class REV_827:
    """Sticky Situation - 缠人处境
    <b>Secret:</b> After your opponent casts a spell, summon a 3/4 Spider with <b>Stealth</b>.
    <b>奥秘：</b>在你的对手施放一个法术后，召唤一个3/4并具有<b>潜行</b>的蜘蛛。
    """
    secret = Play(OPPONENT, SPELL).after(
        FULL_BOARD | (
            Reveal(SELF),
            Summon(CONTROLLER, "REV_827t")
        )
    )


class REV_827t:
    """Spider - 蜘蛛"""
    # Token: 3/4 潜行蜘蛛
    tags = {GameTag.STEALTH: True}


class REV_828:
    """Kidnap - 绑架
    <b>Secret:</b> After your opponent plays a minion, stuff it in a 0/4 Sack.
    <b>奥秘：</b>在你的对手打出一个随从后，将其塞进一个0/4的麻袋中。
    """
    secret = Play(OPPONENT, MINION).after(
        FULL_BOARD | (
            Reveal(SELF),
            # 将对手的随从变形为麻袋
            Morph(Play.CARD, "REV_828t")
        )
    )


class REV_828t:
    """Sack - 麻袋"""
    # Token: 0/4 麻袋
    # 亡语：召唤原来的随从
    def deathrattle(self):
        # 恢复原来的随从
        # Morph 会设置 morphed_from 属性
        if hasattr(self, 'morphed_from') and self.morphed_from:
            # 召唤原随从的复制
            yield Summon(CONTROLLER, ExactCopy(self.morphed_from))


class REV_829:
    """Halkias - 哈尔吉亚斯
    [x]<b>Stealth</b>. <b>Deathrattle:</b> Store
Halkias's soul inside of a
friendly <b>Secret</b>. It resummons
Halkias when triggered.
    <b>潜行，亡语：</b>将哈尔吉亚斯的灵魂储存在一个友方<b>奥秘</b>中。当其被触发时，重新召唤哈尔吉亚斯。
    """
    tags = {GameTag.STEALTH: True}
    
    def deathrattle(self):
        # 找一个友方奥秘
        secrets = list(self.controller.secrets)
        if secrets:
            # 随机选择一个奥秘
            secret = self.game.random.choice(secrets)
            # 给奥秘添加buff，当其被揭示时召唤哈尔吉亚斯
            yield Buff(secret, "REV_829e")


class REV_829e:
    """Halkias's Soul - 哈尔吉亚斯的灵魂"""
    # 当奥秘被揭示时，召唤哈尔吉亚斯
    events = Reveal(OWNER).on(Summon(CONTROLLER, "REV_829"))


class REV_938:
    """Door of Shadows - 暗影之门
    [x]Draw a spell. <b>Infuse (2):</b>
Add a <b>Temporary</b> copy
of it to your hand.
    抽一张法术牌。<b>注能(2)：</b>将一张该牌的<b>临时</b>复制置入你的手牌。
    """
    infuse = 2
    
    def play(self):
        # 抽一张法术
        card = yield Draw(CONTROLLER, FRIENDLY_DECK + SPELL)
        
        # 如果已注能，添加一张临时复制
        if self.infused and card:
            # 创建临时复制（回合结束时消失）
            temp_copy = yield Give(CONTROLLER, Copy(card))
            if temp_copy:
                # 添加临时标记
                yield Buff(temp_copy, "REV_938e")


class REV_938e:
    """Temporary - 临时"""
    # 回合结束时移除
    events = TURN_END.on(Destroy(OWNER))


class REV_939:
    """Serrated Bone Spike - 锯齿骨刺
    [x]Deal $3 damage to a 
minion. If it dies, your 
next card this turn 
costs (2) less.
    对一个随从造成$3点伤害。如果其死亡，你在本回合中打出的下一张牌的法力值消耗减少（2）点。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)
        
        # 检查目标是否死亡
        if TARGET.dead or TARGET.to_be_destroyed:
            # 使用通用的"下一张卡减费"机制
            from fireplace.dsl.next_card_cost import NextCardCostReduction
            yield Buff(FRIENDLY_HERO, NextCardCostReduction(amount=2))


class REV_940:
    """Necrolord Draka - 通灵领主德拉卡
    [x]<b>Battlecry:</b> Equip a 1/3
Dagger. <i>(+1 Attack for
each other card you played
this turn, up to 10!)</i>
    <b>战吼：</b>装备一把1/3的匕首。<i>（你在本回合中每打出一张其他卡牌，其便获得+1攻击力，最多10点！）</i>
    """
    def play(self):
        # 装备匕首
        weapon = yield Summon(CONTROLLER, "REV_940t")
        
        # 根据本回合打出的其他卡牌数量增加攻击力
        # 减1是因为不包括德拉卡自己
        if weapon:
            cards_played = max(0, self.controller.cards_played_this_turn - 1)
            # 最多10点
            bonus = min(cards_played, 10)
            if bonus > 0:
                yield Buff(weapon, "REV_940e", atk_bonus=bonus)


class REV_940t:
    """Dagger - 匕首"""
    # Token: 1/3 武器
    pass


class REV_940e:
    """Necrolord Draka Buff - 通灵领主德拉卡增益"""
    def __init__(self, *args, atk_bonus=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk = atk_bonus


class REV_959:
    """Ghastly Gravedigger - 恐怖的掘墓者
    [x]<b>Battlecry:</b> If you control a
<b>Secret</b>, choose a card in
your opponent's hand to
 shuffle into their deck.
    <b>战吼：</b>如果你控制一个<b>奥秘</b>，选择对手手牌中的一张牌，将其洗回其牌库。
    """
    # requirements 在 play 方法中检查
    
    def play(self):
        # 检查是否控制奥秘
        if self.controller.secrets:
            # 从对手手牌中选择一张
            if self.controller.opponent.hand:
                # AI从对手手牌中选择
                choice = yield GenericChoice(CONTROLLER, list(self.controller.opponent.hand))
                
                if choice:
                    # 将选中的卡洗回牌库
                    yield Shuffle(OPPONENT, choice[0])


