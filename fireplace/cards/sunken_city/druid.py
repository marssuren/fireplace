from ..utils import *
from ...actions import Action


class TryDrawDredged(Action):
    """尝试抽取探底后的牌(如果法力值足够)"""
    def do(self, source, target=None):
        controller = source.controller
        if not controller.deck:
            return
            
        top_card = controller.deck[0]
        
        # 检查费用
        if controller.mana >= top_card.cost:
            controller.game.queue_actions(source, [Draw(controller, top_card)])


class TSC_654:
    """Aquatic Form - 水栖形态
    0费法术 探底。如果你有足够的法力值使用选中的牌，则抽取该牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    # 模拟探底：从牌库底3张中发现一张置于牌库顶
    # 然后检查法力值是否足够使用牌库顶的牌，如果足够则抽牌
    # Dredge 动作会将选中的牌置于牌库顶
    play = Dredge(CONTROLLER).then(
        # 检查是否可以抽牌
        # 此时选中的牌已在牌库顶 (deck[0])
        # 如果 当前法力值 >= 牌的费用，则抽牌
        # 注意：Dredge 是 Choice，后续动作通过 .then 链式调用
        # 这里需要自定义动作来检查和抽牌
        TryDrawDredged()
    )


class TID_001:
    """Moonbeam - 月光射线
    1费法术 对一个敌人造成$2点伤害。如果你拥有法术伤害，此效果翻倍。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        # 基础伤害 2
        damage = 2
        # 如果有法术伤害（SpellPower > 0），基础伤害翻倍为 4
        # Fireplace 会自动在 Hit 动作中叠加 SpellPower, 所以我们只调整基础值
        if self.controller.spellpower > 0:
            damage = 4
        yield Hit(TARGET, damage)


class TSC_653:
    """Bottomfeeder - 底层掠食鱼
    1费 1/3 野兽
    亡语：将一张"底层掠食鱼"置于你的牌库底部，并使其获得+2/+2。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.BEAST,
    }
    
    def deathrattle(self):
        """创建复制，Buff，然后放入牌库底部"""
        # 创建一个新的底层掠食鱼
        yield ShuffleIntoDeck(CONTROLLER, "TSC_653", position='bottom')
        # 给牌库底部的卡牌添加buff
        if self.controller.deck:
            bottom_card = self.controller.deck[-1]
            if bottom_card.id == "TSC_653":
                yield Buff(bottom_card, "TSC_653e")


class TSC_653e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class TSC_657:
    """Dozing Kelpkeeper - 嗜睡的藻农
    1费 0/2
    休眠2回合。当唤醒时，获得+4/+4和突袭。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        GameTag.DORMANT: 2, 
    }
    # 唤醒时获得 Buff
    # 在 Fireplace 中，休眠唤醒通常触发 Awaken 事件吗？
    # 或者 Minion 自身逻辑处理。
    # 我们使用 Link 机制或者监听自身唤醒。
    # 标准做法：events = Awaken(SELF).on(...)
    events = Awaken(SELF).on(Buff(SELF, "TSC_657e"))


class TSC_657e:
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.RUSH: True,
    }


class TSC_927:
    """Azsharan Gardens - 艾萨拉的花园
    1费法术 使你手牌中的所有随从牌获得+1/+1。将一张"沉没的花园"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Buff(FRIENDLY_HAND + MINION, "TSC_927e"), ShuffleIntoDeck(CONTROLLER, "TSC_927t", position='bottom')


class TSC_927e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class TSC_927t:
    """Sunken Gardens - 沉没的花园
    1费法术 使你手牌、牌库和战场上的所有随从牌获得+1/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = (
        Buff(FRIENDLY_HAND + MINION, "TSC_927e"),
        Buff(FRIENDLY_DECK + MINION, "TSC_927e"),
        Buff(FRIENDLY_MINIONS, "TSC_927e")
    )


class TID_000:
    """Spirit of the Tides - 潮汐之灵
    2费 2/2
    在你的回合结束时，如果你有未使用的法力水晶，获得+1/+2。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    # 检查未使用的法力水晶 (Current Mana > 0)
    events = OWN_TURN_END.on(
        (MANA(CONTROLLER) > 0) & Buff(SELF, "TID_000e")
    )


class TID_000e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class TID_002:
    """Herald of Nature - 自然使徒
    3费 3/3
    战吼：如果你在本回合中施放过自然法术，使你的其他随从获得+1/+2。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    def play(self):
        """如果本回合施放过自然法术，使其他随从获得+1/+2"""
        # 检查本回合是否施放过自然法术
        # 注意：cards_played_this_turn 是整数，应使用 cards_played_this_turn_with_position
        cards_this_turn = getattr(self.controller, 'cards_played_this_turn_with_position', [])
        nature_cast_this_turn = any(
            card.type == CardType.SPELL and getattr(card, 'spell_school', None) == SpellSchool.NATURE
            for card, _ in cards_this_turn
        )
        
        if nature_cast_this_turn:
            yield Buff(FRIENDLY_MINIONS - SELF, "TID_002e")


class TID_002e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class TSC_651:
    """Seaweed Strike - 海草卷击
    3费法术 对一个随从造成$4点伤害。如果你在本回合中打出过娜迦牌，你的下一个法术法力值消耗减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        """造成4点伤害,如果本回合打出过娜迦,下一个法术减1费"""
        yield Hit(TARGET, 4)
        
        # 检查本回合是否打出过娜迦
        # 注意：cards_played_this_turn 是整数，应使用 cards_played_this_turn_with_position
        naga_played_this_turn = False
        cards_this_turn = getattr(self.controller, 'cards_played_this_turn_with_position', [])
        for card, _ in cards_this_turn:
            try:
                if card.type == CardType.MINION:
                    races = getattr(card, 'races', None)
                    if races and hasattr(races, '__iter__') and Race.NAGA in races:
                        naga_played_this_turn = True
                        break
            except Exception:
                continue
        
        if naga_played_this_turn:
            yield Buff(CONTROLLER, "TSC_651e")


class TSC_651e:
    """Next Spell Costs (1) Less - 下一个法术减少(1)费"""
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    # 光环效果：手牌中法术消耗 -1
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    # 打出法术后销毁此 Buff
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class TSC_650:
    """Flipper Friends - 划水好友
    5费法术 召唤两个 3/3 并具有突袭的水獭。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    play = Summon(CONTROLLER, "TSC_650t") * 2


class TSC_650t:
    """Otter (3/3 Rush)"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3, # Guess cost
        GameTag.RUSH: True,
        GameTag.CARDRACE: Race.BEAST,
    }


class TSC_656:
    """Miracle Growth - 奇迹生长
    8费法术 抽三张牌。召唤一个属性值等同于你手牌数量的植物，并具有嘲讽。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
    }
    def play(self):
        yield Draw(CONTROLLER) * 3
        # Summon plant with stats
        hand_size = len(self.controller.hand)
        yield Summon(CONTROLLER, "TSC_652t", {
            GameTag.ATK: hand_size, 
            GameTag.HEALTH: hand_size
        })


class TSC_652t:
    """Kelp (Plant)"""
    tags = {
        GameTag.COST: 1,
        GameTag.TAUNT: True,
        GameTag.CARDRACE: Race.ELEMENTAL # Usually Plant is elemental or treant? It says "Plant". No race implied or Treant? 
        # Check race later.
    }


class TSC_026:
    """Colaque - 科拉克
    7费 6/5 野兽
    巨型+1。战吼：当你控制科拉克的壳时，获得免疫。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
        GameTag.CARDRACE: Race.BEAST,
        GameTag.COLOSSAL: 1,
    }
    colossal_appendages = ["TSC_026t"]
    
    # 战吼：如果控制壳，获得免疫
    play = Find(FRIENDLY + MINION + ID("TSC_026t")) & Buff(SELF, "TSC_026e")
    
    # 注意：如果壳死了，免疫应该消失? 
    # 原文："Gain Immune while you control Colaque's Shell."
    # 这应该是一个 Link Aura，不仅仅是战吼。
    # 但是战吼只有一次。
    # 修正：这是一个由于战吼获得的 Buff，这个 Buff 每一帧检查是否控制壳?
    # 或者 Effect: "Immune while..." 是光环？
    # 只有战吼赋予了这个能力？ 不，如果是 "Battlecry: Gain Immune..."，那是一次性的。
    # 如果是 "Immune while..."，那是被动光环。
    # 官方文本："Colossal +1. Battlecry: Gain Immune while you control Colaque's Shell."
    # 意思是战吼触发一个永久 Buff，该 Buff 有条件（控制壳）。
    pass


class TSC_026t:
    """Colaque's Shell"""
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 8,
        GameTag.COST: 5,
        GameTag.TAUNT: True,
        GameTag.CARDRACE: Race.BEAST,
    }


class TSC_026e:
    """Colaque Immune Buff - 科拉克免疫增益"""
    # 条件免疫：只有当控制壳(TSC_026t)时才免疫
    # 使用 Find + Refresh 实现条件光环
    update = Find(FRIENDLY_MINIONS + ID("TSC_026t")) & Refresh(OWNER, {GameTag.IMMUNE: True})


class TSC_658:
    """Hedra the Heretic - 异端纳迦海德拉
    7费 4/5
    战吼：你每在本局对战中施放过一个法术，召唤一个法力值消耗等同于该法术的随机随从。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
        GameTag.CARDRACE: Race.NAGA,
    }
    
    def play(self):
        # 遍历本局对战施放的法术
        if hasattr(self.controller, 'spells_played_this_game'):
            for card in self.controller.spells_played_this_game:
                cost = card.cost
                yield Summon(CONTROLLER, RandomMinion(cost=cost))


class TSC_652:
    """Green-Thumb Gardener - 妙手园丁
    6费 5/5
    战吼：你每有一张手牌是法术牌，复原一个法力水晶。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    
    def play(self):
        spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        count = len(spells)
        if count > 0:
            yield ManaThisTurn(CONTROLLER, count)
