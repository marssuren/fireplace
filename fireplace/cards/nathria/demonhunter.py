"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_008:
    """Sightless Magistrate - 盲眼法官
    <b>Battlecry:</b> Both players draw until they have 5 cards.
    战吼：双方玩家抽若干数量的牌，直到拥有5张手牌。
    """
    # 战吼：双方玩家抽牌直到拥有5张手牌
    def play(self):
        # 己方玩家抽牌至5张
        while len(self.controller.hand) < 5 and len(self.controller.deck) > 0:
            yield Draw(CONTROLLER)

        # 对手玩家抽牌至5张
        while len(self.controller.opponent.hand) < 5 and len(self.controller.opponent.deck) > 0:
            yield Draw(OPPONENT)


class MAW_012:
    """All Fel Breaks Loose - 邪能之乱
    [x]Summon a friendly Demon that died this game.
    <b>Infuse (3):</b> Summon three instead.
    召唤一个在本局对战中死亡的友方恶魔。
    注能（3）：改为召唤三个。
    """
    # 注能机制：当3个友方随从死亡时充能升级
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    infuse = 3  # 需要3个友方随从死亡

    def play(self):
        # 检查是否已注能
        if self.infused:
            # 注能后：召唤三个死亡的友方恶魔
            for _ in range(3):
                yield Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + DEMON))
        else:
            # 未注能：召唤一个死亡的友方恶魔
            yield Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + DEMON))


class MAW_014:
    """Prosecutor Mel'tranix - 公诉人梅尔特拉尼克斯
    [x]<b>Battlecry:</b> Your opponent can only play their left-
    and right-most cards on their next turn.
    战吼：你的对手在其下回合中只能使用最左边和最右边的牌。
    """
    # 战吼：给对手添加一个buff，限制其下回合只能打出最左和最右的牌
    play = Buff(OPPONENT, "MAW_014e")


class MAW_014e:
    """Prosecutor Mel'tranix Effect - 公诉人效果
    限制玩家只能打出最左边和最右边的牌
    """
    # 在对手的回合开始时，禁用中间的手牌
    events = BeginTurn(OPPONENT).on(
        # 给除了最左和最右之外的所有手牌添加"不能打出"标记
        Buff(ENEMY_HAND - (ENEMY_HAND[0] | ENEMY_HAND[-1]), "MAW_014e2")
    ), EndTurn(OPPONENT).on(Destroy(SELF))


class MAW_014e2:
    """Cannot be played this turn"""
    tags = {GameTag.CANT_PLAY: True}
    events = TURN_END.on(Destroy(SELF))


class REV_506:
    """Sinful Brand - 罪孽烙印
    [x]Brand an enemy minion. Whenever it takes damage, deal 1 damage to the enemy hero.
    标记一个敌方随从。每当该随从受到伤害，对敌方英雄造成1点伤害。
    """
    # 给目标随从添加buff，每当受到伤害时对敌方英雄造成1点伤害
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "REV_506e")


class REV_506e:
    """Sinful Brand Effect - 罪孽烙印效果"""
    # 每当该随从受到伤害时，对敌方英雄造成1点伤害
    events = Damage(OWNER).on(Hit(ENEMY_HERO, 1))


class REV_507:
    """Dispose of Evidence - 处理证据
    Give your hero +3 Attack this turn. Choose a card in your hand to shuffle into your deck.
    在本回合中，使你的英雄获得+3攻击力。选择一张你的手牌洗入你的牌库。
    """
    # 给英雄+3攻击力（本回合），然后选择一张手牌洗入牌库
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0}

    def play(self):
        # 给英雄+3攻击力（本回合结束时移除）
        yield Buff(FRIENDLY_HERO, "REV_507e")
        # 将目标手牌洗入牌库
        yield Shuffle(CONTROLLER, TARGET)


class REV_507e:
    """Dispose of Evidence Buff - 处理证据增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }
    events = TURN_END.on(Destroy(SELF))


class REV_508:
    """Relic of Dimensions - 次元圣物
    [x]Draw two cards and reduce their Cost by (1). Improve your future Relics.
    抽两张牌并使其法力值消耗降低（1）点。提升你此后的圣物效果。
    """
    # 圣物标签
    tags = {enums.RELIC: True}

    # 抽两张牌并减费，然后提升圣物等级
    def play(self):
        # 获取当前圣物等级（通过计算 REV_RELIC_COUNTER 的层数）
        relic_level = 1
        for buff in self.controller.hero.buffs:
            if buff.id == "REV_RELIC_COUNTER":
                relic_level += 1

        # 抽两张牌
        drawn_cards = []
        for _ in range(2):
            card = yield Draw(CONTROLLER)
            if card:
                drawn_cards.append(card)

        # 给抽到的牌减费（减费量 = 圣物等级）
        for card in drawn_cards:
            yield Buff(card, "REV_508e", cost=-relic_level)

        # 提升圣物等级
        yield Buff(FRIENDLY_HERO, "REV_RELIC_COUNTER")


class REV_508e:
    """Relic of Dimensions Buff - 次元圣物减费"""
    # 动态减费，由 Buff 调用时传入 cost 参数
    pass


class REV_509:
    """Magnifying Glaive - 放大战刃
    [x]After your hero attacks, draw until you have 3 cards.
    在你的英雄攻击后，抽牌，直到你拥有三张牌。
    """
    # 英雄攻击后，抽牌直到拥有3张手牌
    events = Attack(FRIENDLY_HERO).after(
        lambda self, source, target: [Draw(CONTROLLER) for _ in range(max(0, 3 - len(self.controller.hand)))]
    )


class REV_510:
    """Kryxis the Voracious - 贪食的克里克西斯
    [x]<b>Battlecry</b>: Discard your hand. <b>Deathrattle:</b> Draw 3 cards.
    战吼：弃掉你的手牌。亡语：抽三张牌。
    """
    # 战吼：弃掉所有手牌
    play = Discard(FRIENDLY_HAND)
    # 亡语：抽三张牌
    deathrattle = Draw(CONTROLLER) * 3


class REV_511:
    """Bibliomite - 案卷书虫
    [x]<b>Battlecry</b>: Choose a card in your hand to shuffle into your deck.
    战吼：选择一张你的手牌洗入你的牌库。
    """
    # 战吼：选择一张手牌洗入牌库
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0}
    play = Shuffle(CONTROLLER, TARGET)


class REV_834:
    """Relic of Extinction - 灭绝圣物
    Deal $1 damage to a random enemy minion, twice. Improve your future Relics.
    随机对一个敌方随从造成$1点伤害，触发两次。提升你此后的圣物效果。
    """
    # 圣物标签
    tags = {enums.RELIC: True}

    # 随机对敌方随从造成伤害，然后提升圣物等级
    def play(self):
        # 获取当前圣物等级（通过计算 REV_RELIC_COUNTER 的层数）
        relic_level = 1
        for buff in self.controller.hero.buffs:
            if buff.id == "REV_RELIC_COUNTER":
                relic_level += 1

        # 造成两次伤害（伤害量 = 圣物等级）
        yield Hit(RANDOM_ENEMY_MINION, relic_level)
        yield Hit(RANDOM_ENEMY_MINION, relic_level)

        # 提升圣物等级
        yield Buff(FRIENDLY_HERO, "REV_RELIC_COUNTER")


class REV_937:
    """Artificer Xy'mox - 圣物匠赛·墨克斯
    [x]<b>Battlecry:</b> <b>Discover</b> and cast a Relic. <b>Infuse (5):</b> Cast all three instead.
    战吼：发现并施放一个圣物。注能（5）：改为施放全部三个。
    """
    # 注能机制：需要5个友方随从死亡
    infuse = 5

    def play(self):
        # 定义三个圣物卡牌ID
        relic_ids = ["REV_508", "REV_834", "REV_943"]

        if self.infused:
            # 注能后：施放全部三个圣物
            for relic_id in relic_ids:
                yield CastSpell(relic_id)
        else:
            # 未注能：发现一个圣物并施放
            # 创建三个圣物卡牌供选择
            cards = [self.controller.card(card_id) for card_id in relic_ids]
            discovered = yield GenericChoice(CONTROLLER, cards)
            
            # 施放选中的圣物
            if discovered:
                yield CastSpell(discovered[0].id)


class REV_942:
    """Relic Vault - 圣物仓库
    The next Relic you play this turn casts twice.
    在本回合中你使用的下一个圣物将施放两次。
    """
    # Location 地标：使下一个圣物施放两次
    # 给控制者添加一个buff，使下一个圣物施放两次
    play = Buff(FRIENDLY_HERO, "REV_942e")


class REV_942e:
    """Relic Vault Effect - 圣物仓库效果
    下一个圣物施放两次
    """
    # 当施放圣物时，再次施放一次
    # 使用 enums.RELIC 标签来判断是否为圣物
    events = Play(CONTROLLER, SPELL).after(
        lambda self, source, card: (
            CastSpell(card.id) if card.tags.get(enums.RELIC, False) else None,
            Destroy(SELF) if card.tags.get(enums.RELIC, False) else None
        )
    ), TURN_END.on(Destroy(SELF))


class REV_943:
    """Relic of Phantasms - 幻灭心能圣物
    Summon two 1/1 Spirits. Improve your future Relics.
    召唤两个1/1的灵魂。提升你此后的圣物效果。
    """
    # 圣物标签
    tags = {enums.RELIC: True}

    # 召唤灵魂，然后提升圣物等级
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 获取当前圣物等级（通过计算 REV_RELIC_COUNTER 的层数）
        relic_level = 1
        for buff in self.controller.hero.buffs:
            if buff.id == "REV_RELIC_COUNTER":
                relic_level += 1

        # 召唤灵魂（数量 = 圣物等级 + 1）
        num_spirits = relic_level + 1
        for _ in range(num_spirits):
            yield Summon(CONTROLLER, "REV_943t")

        # 提升圣物等级
        yield Buff(FRIENDLY_HERO, "REV_RELIC_COUNTER")


class REV_943t:
    """Spirit - 灵魂
    1/1 token"""
    # Token: 1/1 灵魂（属性在CardDefs.xml中定义）
    pass


class REV_RELIC_COUNTER:
    """Relic Counter - 圣物计数器
    追踪圣物升级等级，每施放一个圣物增加1层
    """
    # 圣物计数器：累积型buff，不会被移除
    # 每层代表一次圣物升级，影响后续圣物的效果强度
    # - REV_508（次元圣物）：减费量 = 层数 + 1
    # - REV_834（灭绝圣物）：伤害量 = 层数 + 1
    # - REV_943（幻灭心能圣物）：召唤数量 = 层数 + 2
    max_stacks = 10  # 最多叠加10层


