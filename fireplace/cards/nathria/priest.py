"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_021:
    """Clear Conscience - 问心无愧
    Give a friendly minion +2/+3 and "<b>Elusive</b> on your opponent's turn."
    使一个友方随从获得+2/+3，并在你的对手回合中获得"<b>无法成为法术或英雄技能的目标</b>"。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    play = Buff(TARGET, "MAW_021e")


class MAW_021e:
    """Clear Conscience Buff - 问心无愧增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
    }
    
    # 在对手回合中获得 Elusive（无法被法术或英雄技能指定）
    def _update_elusive(self, player):
        # 如果是对手回合，添加 CANT_BE_TARGETED_BY_SPELLS
        if source.controller.game.current_player != source.controller:
            source.tags[GameTag.CANT_BE_TARGETED_BY_SPELLS] = True
            source.tags[GameTag.CANT_BE_TARGETED_BY_HERO_POWERS] = True
        else:
            source.tags[GameTag.CANT_BE_TARGETED_BY_SPELLS] = False
            source.tags[GameTag.CANT_BE_TARGETED_BY_HERO_POWERS] = False
    
    events = [
        TURN_BEGIN.on(_update_elusive),
        TURN_END.on(_update_elusive),
    ]


class MAW_022:
    """Incriminating Psychic - 控罪心灵密探
    [x]<b>Taunt</b>
 <b>Deathrattle:</b> Copy two
 random cards from your
opponent's hand.
    <b>嘲讽，亡语：</b>从你的对手手牌中随机复制两张牌。
    """
    tags = {GameTag.TAUNT: True}
    
    def deathrattle(self):
        # 从对手手牌中随机复制两张
        if self.controller.opponent.hand:
            cards = self.game.random.sample(
                list(self.controller.opponent.hand),
                min(2, len(self.controller.opponent.hand))
            )
            for card in cards:
                yield Give(CONTROLLER, Copy(card))


class MAW_023:
    """Theft Accusation - 盗窃指控
    [x]Choose a minion.
Destroy it after you play
a card copied from
the opponent.
    选择一个随从。在你打出一张从对手处复制的卡牌后，消灭它。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 给目标添加标记
        yield Buff(TARGET, "MAW_023e")


class MAW_023e:
    """Theft Accusation Mark - 盗窃指控标记"""
    # 监听玩家打出从对手复制的卡牌
    def _check_and_destroy(self, player, played_card, target=None):
        # Play.after 事件参数：(player, played_card, target)
        if played_card is None:
            return
        
        if not hasattr(played_card, 'tags'):
            return
        
        # 检查卡牌是否是从对手复制的
        from ... import enums
        if played_card.tags.get(enums.COPIED_FROM_OPPONENT, False):
            # 消灭被标记的随从
            yield Destroy(OWNER)
    
    events = Play(CONTROLLER).after(_check_and_destroy)


class REV_002:
    """Suspicious Usher - 可疑的侍应
    [x]<b>Battlecry:</b> <b>Discover</b> a
<b>Legendary</b> minion. If your
opponent guesses your
  choice, they get a copy.
    <b>战吼：</b>从传说随从中<b>发现</b>一张。如果你的对手猜中了你的选择，他们会获得一张复制。
    """
    def play(self):
        # 使用 DiscoverWithPendingGuess 实现对手猜测机制
        # 参考 REV_000 (可疑的炼金师)
        from hearthstone.enums import Rarity
        yield DiscoverWithPendingGuess(
            CONTROLLER,
            RandomCollectible(card_class=CardClass.NEUTRAL, rarity=Rarity.LEGENDARY, type=CardType.MINION)
        )


class REV_011:
    """The Harvester of Envy - 妒妒收割者
    After you play a card copied from the opponent, steal the original.
    在你打出一张从对手处复制的卡牌后，偷取原版卡牌。
    """
    def _steal_original(self, player, played_card, target=None):
        # Play.after 事件参数：(player, played_card, target)
        # self 是触发事件的实体（REV_011 随从）
        if played_card is None:
            return
        
        if not hasattr(played_card, 'tags'):
            return
        
        from ... import enums
        if played_card.tags.get(enums.COPIED_FROM_OPPONENT, False):
            # 尝试从对手手牌/牌库中偷取同名卡
            # 优先从手牌
            for opponent_card in player.opponent.hand:
                if opponent_card.card_id == played_card.card_id:
                    yield Steal(opponent_card, CONTROLLER)
                    return
            
            # 如果手牌没有，从牌库偷取
            for opponent_card in player.opponent.deck:
                if opponent_card.card_id == played_card.card_id:
                    yield Steal(opponent_card, CONTROLLER)
                    return
    
    events = Play(CONTROLLER).after(_steal_original)


class REV_246:
    """Mysterious Visitor - 神秘访客
    <b>Battlecry:</b> Reduce the Cost of cards copied from your opponent by (3).
    <b>战吼：</b>使从你的对手处复制的卡牌的法力值消耗减少（3）点。
    """
    def play(self):
        # 给所有从对手复制的卡牌减费
        from ... import enums
        for card in self.controller.hand:
            # 检查是否是从对手复制的
            if card.tags.get(enums.COPIED_FROM_OPPONENT, False):
                yield Buff(card, "REV_246e")


class REV_246e:
    """Mysterious Visitor Buff - 神秘访客减费"""
    tags = {GameTag.COST: -3}


class REV_247:
    """Partner in Crime - 共犯
    [x]<b>Battlecry:</b> Summon a 
copy of this minion at 
the end of your turn.
    <b>战吼：</b>在你的回合结束时，召唤一个该随从的复制。
    """
    def play(self):
        # 给自己添加一个buff，回合结束时召唤自己的复制
        yield Buff(SELF, "REV_247e")


class REV_247e:
    """Partner in Crime Effect - 共犯效果"""
    # 回合结束时召唤拥有者的完整复制（包含所有buff）
    # 但需要移除复制身上的 REV_247e buff 以避免无限循环
    def _summon_copy_and_cleanup(self, player):
        if source.controller.game.current_player == self.controller:
            # 召唤拥有者的完整复制（包含所有buff）
            copy_minion = yield Summon(CONTROLLER, ExactCopy(OWNER))
            
            # 从复制身上移除 REV_247e buff，避免无限循环
            if copy_minion:
                for buff in list(copy_minion.buffs):
                    if buff.id == "REV_247e":
                        yield Destroy(buff)
            
            # 移除原随从身上的此buff（一次性效果）
            yield Destroy(SELF)
    
    events = OWN_TURN_END.on(_summon_copy_and_cleanup)


class REV_248:
    """Boon of the Ascended - 晋升者之赐
    Give a minion +2 Health. Summon a Kyrian with its stats and <b>Taunt</b>.
    使一个随从获得+2生命值。召唤一个具有其属性和<b>嘲讽</b>的凯瑞安。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        target = self.target
        if target:
            # 先记录目标的原始属性（在buff之前）
            original_atk = target.atk
            original_health = target.health
            
            # 给目标+2生命值
            yield Buff(target, "REV_248e")
            
            # 召唤一个凯瑞安，具有目标的原始属性和嘲讽
            kyrian = yield Summon(CONTROLLER, "REV_248t")
            
            if kyrian:
                # 设置凯瑞安的属性为目标的原始属性
                kyrian.atk = original_atk
                kyrian.max_health = original_health


class REV_248e:
    """Boon of the Ascended Buff - 晋升者之赐增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.HEALTH: 2,
    }


class REV_248t:
    """Kyrian - 凯瑞安"""
    # Token: 具有嘲讽的凯瑞安（属性动态设置）
    tags = {GameTag.TAUNT: True}


class REV_249:
    """The Light! It Burns! - 炽燃圣光
    [x]Deal damage to a minion
 equal to its Attack.
    对一个随从造成等同于其攻击力的伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    play = Hit(TARGET, ATK(TARGET))


class REV_250:
    """Pelagos - 裴拉戈斯
    [x]After you cast a spell 
on a friendly minion, set 
its Attack and Health to 
the higher of the two.
    在你对一个友方随从施放法术后，将其攻击力和生命值设为两者中较高的那个。
    """
    # 使用自定义函数处理，因为需要检查目标并计算值
    def _equalize_stats(self, player, played_card, spell_target=None):
        # Play.after 事件参数：(player, played_card, target)
        if played_card is None:
            return
        
        if not hasattr(played_card, 'target'):
            return
        
        # 需要检查该卡牌是否有目标，以及目标是否是友方随从
        if played_card.target and hasattr(played_card.target, 'type'):
            target = played_card.target
            if target.type == CardType.MINION and target.controller == player:
                # 获取较高的属性值
                higher_value = max(target.atk, target.health)
                # 设置攻击力和生命值
                yield Buff(target, "REV_250e", atk_value=higher_value, health_value=higher_value)
    
    events = Play(CONTROLLER, SPELL).after(_equalize_stats)


class REV_250e:
    """Pelagos Buff - 裴拉戈斯增益"""
    def __init__(self, *args, atk_value=0, health_value=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk_value = atk_value
        self.health_value = health_value
    
    def apply(self, target):
        target.atk = self.atk_value
        target.max_health = self.health_value


class REV_252:
    """Clean the Scene - 净场
    Destroy all minions with 3 or less Attack. <b>Infuse (3):</b> 6 or less.
    消灭所有攻击力小于或等于3点的随从。<b>注能(3)：</b>改为6点。
    """
    infuse = 3
    
    def play(self):
        # 根据是否注能，选择不同的攻击力阈值
        threshold = 6 if self.infused else 3
        
        # 消灭所有攻击力小于等于阈值的随从
        yield Destroy(ALL_MINIONS + (ATK <= threshold))


class REV_253:
    """Identity Theft - 盗用身份
    <b>Discover</b> a copy of a card from your opponent's hand and deck.
    从你的对手的手牌和牌库中<b>发现</b>一张卡牌的复制。
    """
    def play(self):
        # 收集对手的手牌和牌库
        opponent_cards = list(self.controller.opponent.hand) + list(self.controller.opponent.deck)
        
        if opponent_cards:
            # 使用 GenericChoice 从对手卡牌中选择
            # 这里不能用 Discover 因为 Discover 是生成新卡，而这里需要从实际卡牌中选择
            options = self.game.random.sample(opponent_cards, min(3, len(opponent_cards)))
            choice = yield GenericChoice(CONTROLLER, options)
            
            if choice:
                # 给予复制
                yield Give(CONTROLLER, Copy(choice[0]))


class REV_290:
    """Cathedral of Atonement - 赎罪教堂
    Give a minion +2/+1 and draw a card.
    使一个随从获得+2/+1并抽一张牌。
    """
    # LOCATION 地标
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    activate = Buff(TARGET, "REV_290e"), Draw(CONTROLLER)


class REV_290e:
    """Cathedral of Atonement Buff - 赎罪教堂增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }


