from ..utils import *
from ... import enums


# Helper Action to Give Abyssal Curse
class GiveAbyssalCurse(Action):
    def __init__(self, source_selector, target_selector):
        self.source_selector = source_selector
        self.target_selector = target_selector
    
    def trigger(self, source):
        # 评估目标玩家
        if hasattr(self.target_selector, 'evaluate'):
            target_player = self.target_selector.evaluate(source)
        elif hasattr(self.target_selector, 'eval'):
            results = self.target_selector.eval(source.game, source)
            target_player = results[0] if results else source.controller.opponent
        else:
            target_player = self.target_selector
        
        self.do(source, target_player)
        return []
    
    def do(self, source, target_player):
        controller = source.controller
        # 使用语义化标签 ABYSSAL_CURSE_LEVEL 替代通用 TAG_SCRIPT_DATA_NUM_1
        current_level = getattr(controller, 'abyssal_curse_level', 0) + 1
        controller.abyssal_curse_level = current_level
        
        curse_card = controller.card("TSC_950t")
        curse_card.tags[enums.ABYSSAL_CURSE_LEVEL] = current_level
        
        source.game.queue_actions(source, [Give(target_player, curse_card)])


class TSC_925:
    """Rock Bottom - 岩石海底
    1费法术 召唤一个1/3的虚空行者。探底。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Summon(CONTROLLER, "CS2_065"), Dredge(CONTROLLER)


class TSC_614:
    """Voidgill - 虚鳃鱼人
    2费 3/2 鱼人
    亡语：使你手牌中的所有鱼人牌获得+1/+1。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.MURLOC,
    }
    deathrattle = Buff(FRIENDLY_HAND + MURLOC, "TSC_614e")


class TSC_614e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class TSC_957:
    """Chum Bucket - 鱼饵桶
    2费法术 使你手牌中的所有鱼人牌获得+2/+2。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = Buff(FRIENDLY_HAND + MURLOC, "TSC_957e")


class TSC_957e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class TID_717:
    """Shadow Suffusion - 暗影灌注
    3费法术 使一个随从获得亡语：对所有敌人造成3点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "TID_717e")


class TID_717e:
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Hit(ENEMY_CHARACTERS, 3)


class TSC_753:
    """Bloodscent Vilefin - 血腥恶鳍鱼人
    3费 3/4 鱼人
    战吼：探底。如果选中的牌是鱼人牌，将其法力值消耗改为生命值消耗。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.MURLOC,
    }
    
    def play(self):
        yield Dredge(CONTROLLER)
        if self.controller.deck:
            top_card = self.controller.deck[0]
            if top_card.type == CardType.MINION and Race.MURLOC in top_card.races:
                yield Buff(top_card, "TSC_753e")


class TSC_753e:
    """Costs Health Instead of Mana"""
    tags = {
        GameTag.CARD_COSTS_HEALTH: True,
    }


class TSC_955:
    """Sira'kess Cultist - 希拉柯丝教徒
    3费 2/3 纳迦
    战吼：塞给你的对手一张深渊诅咒。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.NAGA,
    }
    play = GiveAbyssalCurse(SELF, OPPONENT)


class TSC_956:
    """Dragged Below - 拖入深渊
    3费法术 造成$4点伤害。塞给你的对手一张深渊诅咒。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4), GiveAbyssalCurse(SELF, OPPONENT)


class TID_718:
    """Immolate - 献祭
    4费法术 焚烧对手手牌中的所有卡牌。3回合后，被焚烧的卡牌会被弃掉。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    play = Buff(ENEMY_HAND, "TID_718e")


class TID_718e:
    """Immolate Effect"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3, # Counter
    }
    events = BeginTurn(OWNER).on(
        (
            SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_NUM_1: Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1) - 1}),
            (Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1) <= 0) & Discard(OWNER)
        )
    )


class TID_719:
    """Commander Ulthok - 指挥官乌尔索克
    5费 7/7 恶魔
    战吼：对你的英雄造成5点伤害。你的牌消耗生命值，而非法力值。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 7,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.DEMON,
    }
    play = Hit(FRIENDLY_HERO, 5)
    auras = [Buff(SELF, "TID_719e_Real")] 


class TID_719e_Real:
    update = Refresh(FRIENDLY_HAND, {GameTag.CARD_COSTS_HEALTH: True})


class TSC_959:
    """Za'qul - 扎库尔
    5费 6/5
    你的深渊诅咒为你恢复生命值，而不是造成伤害。战吼：塞给你的对手一张深渊诅咒。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    play = GiveAbyssalCurse(SELF, OPPONENT)
    
    # 监听诅咒造成的伤害并补偿治疗
    events = Damage(ENEMY_HERO, ID("TSC_950t")).on(
        Heal(FRIENDLY_HERO, Damage.AMOUNT)
    )


class TSC_924:
    """Abyssal Wave - 深渊波流
    6费法术 对所有随从造成$4点伤害。塞给你的对手一张深渊诅咒。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
    }
    play = Hit(ALL_MINIONS, 4), GiveAbyssalCurse(SELF, OPPONENT)


class TSC_962:
    """Gigafin - 老巨鳍
    8费 7/4 鱼人
    巨型+1。战吼：吞食所有敌方随从。亡语：吐出它们。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 4,
        GameTag.COST: 8,
        GameTag.CARDRACE: Race.MURLOC,
        GameTag.COLOSSAL: 1,
    }
    colossal_appendages = ["TSC_962t"]
    
    def play(self):
        buff = yield Buff(SELF, "TSC_962e")
        if buff:
            targets = list(self.controller.opponent.field)
            for minion in targets:
                 yield Setaside(minion)
                 buff.devoured.append(minion)


class TSC_962e:
    """Gigafin Stomach"""
    def __init__(self):
        self.devoured = []
        
    deathrattle = Summon(OPPONENT, lambda self: self.devoured)


class TSC_962t:
    """Gigafin's Maw - 老巨鳍之口
    4费 4/7 鱼人
    嘲讽
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 7,
        GameTag.COST: 4,
        GameTag.CARDRACE: Race.MURLOC,
        GameTag.TAUNT: True,
    }


class TSC_039:
    """Azsharan Scavenger - 艾萨拉的拾荒者
    2费 2/3 鱼人
    战吼：将一张"沉没的拾荒者"置于你的牌库底部。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.MURLOC,
    }
    play = ShuffleIntoDeck(CONTROLLER, "TSC_039t", position='bottom')


class TSC_039t:
    """Sunken Scavenger - 沉没的拾荒者
    2费 2/3 鱼人
    战吼：使你的所有鱼人牌获得+1/+1。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.MURLOC,
    }
    # "Give your murlocs +1/+1" usually implies everywhere?
    # Or just board/hand?
    # Text said "Permanently". Usually implies "Wherever they are".
    # Buff(FRIENDLY_MINIONS + FRIENDLY_HAND + FRIENDLY_DECK + MURLOC, ...)
    # For safety/common power level, assume Board/Hand/Deck.
    play = Buff(FRIENDLY_MINIONS + FRIENDLY_HAND + FRIENDLY_DECK + MURLOC, "TSC_039te")


class TSC_039te:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class TSC_950t:
    """Abyssal Curse - 深渊诅咒
    2费法术
    在你的回合开始时，受到X点伤害。你每受到一次诅咒伤害，该数值增加1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 0, # Damage amount set at creation
    }
    class Hand:
        events = OWN_TURN_BEGIN.on(
            Hit(FRIENDLY_HERO, Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1))
        )
