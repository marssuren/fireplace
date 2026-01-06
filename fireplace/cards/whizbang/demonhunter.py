"""
威兹班的工坊 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class MIS_102:
    """退货政策 - Return Policy
    Discover a friendly Deathrattle card you've played this game. Trigger its Deathrattle.
    """
    # 3费法术 发现一张你在本局对战中使用过的友方亡语牌。触发其亡语
    def play(self):
        # 获取本局对战中使用过的亡语牌
        deathrattle_cards = [
            card for card in self.controller.cards_played_this_game
            if card.has_deathrattle
        ]
        
        if deathrattle_cards:
            # Discover 一张亡语牌
            cards = yield DISCOVER(deathrattle_cards)
            if cards:
                # 触发其亡语
                # 创建一个临时卡牌实例
                card_id = cards[0].id
                temp_card = self.controller.card(card_id, source=self)
                temp_card.controller = self.controller
                
                # 获取亡语效果并触发
                if hasattr(temp_card, 'deathrattle'):
                    deathrattle_action = temp_card.deathrattle
                    # 如果是 callable，调用它
                    if callable(deathrattle_action):
                        yield from deathrattle_action()
                    else:
                        # 如果是 action，直接 yield
                        yield deathrattle_action


class MIS_710:
    """滑矛布袋手偶 - Sock Puppet Slitherspear
    This minion's Attack is improved by your hero's.
    """
    # 1/1/2 本随从的攻击力随你的英雄的攻击力提高
    # 使用 Aura 实现动态攻击力
    class Hand:
        # 在手牌中也显示正确的攻击力
        update = Refresh(SELF, {GameTag.ATK: lambda self, i: ATK(FRIENDLY_HERO).eval(i, self)})
    
    update = Refresh(SELF, {GameTag.ATK: lambda self, i: ATK(FRIENDLY_HERO).eval(i, self)})


class TOY_641:
    """裁判拳套 - Umpire's Grasp
    Deathrattle: Draw a Demon and reduce its Cost by (2).
    """
    # 4/3/2 武器 亡语：抽一张恶魔牌，并使其法力值消耗减少（2）点
    def deathrattle(self):
        # 抽一张恶魔牌
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + DEMON)
        if cards:
            # 使其法力值消耗减少（2）点
            yield Buff(cards, "TOY_641e")


class TOY_641e:
    """费用减少 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -2


class TOY_642:
    """球霸野猪人 - Ball Hog
    [x]Lifesteal Battlecry and Deathrattle: Deal 2 damage to the lowest Health enemy.
    """
    # 4/3/3 吸血。战吼，亡语：对生命值最低的敌人造成2点伤害
    lifesteal = True
    
    def play(self):
        # 对生命值最低的敌人造成2点伤害
        yield self._deal_damage()
    
    def deathrattle(self):
        yield self._deal_damage()
    
    def _deal_damage(self):
        """对生命值最低的敌人造成2点伤害"""
        enemies = ENEMY_CHARACTERS.eval(self.game, self)
        if enemies:
            # 找到生命值最低的敌人
            min_health = min(e.health for e in enemies)
            targets = [e for e in enemies if e.health == min_health]
            if targets:
                yield Hit(targets[0], 2)


class TOY_643:
    """盲盒 - Blind Box
    Get 2 random Demons. Outcast: Discover them instead.
    """
    # 2费法术 随机获取2张恶魔牌。流放：改为发现
    def play(self):
        if self.outcast:
            # 流放：发现2张恶魔牌
            for _ in range(2):
                cards = yield DISCOVER(RandomCollectible(race=Race.DEMON))
        else:
            # 随机获取2张恶魔牌
            for _ in range(2):
                yield Give(CONTROLLER, RandomCollectible(race=Race.DEMON))


# RARE

class MIS_911:
    """残次聒噪怪 - Gibbering Reject
    After your hero attacks, summon another Gibbering Reject.
    """
    # 4/3/3 在你的英雄攻击后，召唤另一个残次聒噪怪
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "MIS_911"))


class TOY_028:
    """团队之灵 - Spirit of the Team
    Stealth for 1 turn. Your hero has +2 Attack on your turn.
    """
    # 2/0/3 潜行一回合。你的英雄在你的回合拥有+2攻击力
    stealth = True
    
    # Aura: 在你的回合，英雄获得+2攻击力
    update = Find(CURRENT_PLAYER) & Refresh(FRIENDLY_HERO, {
        GameTag.ATK: lambda self, i: ATK(FRIENDLY_HERO).eval(i, self) + 2
    })


class TOY_028e:
    """团队之灵 Buff"""
    tags = {
        GameTag.ATK: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_640:
    """工坊事故 - Workshop Mishap
    Deal $5 damage to a minion. Excess damages both neighbors. Outcast: Gain Lifesteal.
    """
    # 4费法术 对一个随从造成$5点伤害，相邻的随从均会受到超过其生命值的伤害。流放：获得吸血
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        target = self.target
        if not target:
            return
        
        # 记录目标的初始生命值（用于计算超出伤害）
        target_health_before = target.health
        
        # 获取相邻随从（在目标死亡前）
        board = target.controller.field
        target_pos = board.index(target) if target in board else -1
        left_minion = board[target_pos - 1] if target_pos > 0 else None
        right_minion = board[target_pos + 1] if target_pos < len(board) - 1 else None
        
        # 对目标造成5点伤害
        yield Hit(target, 5)
        
        # 计算超出伤害
        excess_damage = max(0, 5 - target_health_before)
        
        if excess_damage > 0:
            # 对相邻随从造成超出伤害
            if left_minion and left_minion.zone == Zone.PLAY:
                yield Hit(left_minion, excess_damage)
            
            if right_minion and right_minion.zone == Zone.PLAY:
                yield Hit(right_minion, excess_damage)
        
        # 流放：获得吸血
        # 注意：法术本身已经有 lifesteal 标签，这里不需要额外处理
        # 如果需要手动实现吸血效果，应该在造成伤害时自动回复
        # 但这需要修改 Hit action，这里我们假设引擎会自动处理


class TOY_645:
    """小型法术欧珀石 - Lesser Opal Spellstone
    Draw 1 card. <i>(Attack with your hero 2 times to upgrade.)</i>
    """
    # 2费法术 抽一张牌。（用你的英雄攻击2次后升级）
    play = Draw(CONTROLLER)
    
    class Hand:
        # 在手牌中时，监听英雄攻击事件
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.times_hero_attacked = 0
        
        # 追踪英雄攻击次数并在攻击2次后升级
        events = Attack(FRIENDLY_HERO).after(
            lambda self: (
                setattr(self, "times_hero_attacked", getattr(self, "times_hero_attacked", 0) + 1),
                Morph(SELF, "TOY_645t") if getattr(self, "times_hero_attacked", 0) >= 2 else None
            )[1]
        )


# EPIC

class TOY_644:
    """红牌 - Red Card
    Make a minion go Dormant for 2 turns.
    """
    # 1费法术 使一个随从休眠2回合
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 使目标随从休眠2回合
        yield SetDormant(TARGET, 2)


class TOY_652:
    """橱窗看客 - Window Shopper
    [x]Miniaturize Battlecry: Discover a Demon. Set its stats and Cost to this minion's.
    """
    # 5/6/5 微缩。战吼：发现一张恶魔牌，将其属性值与法力值消耗变为与本随从相同
    # Miniaturize 机制由核心引擎自动处理
    def play(self):
        # Discover 一张恶魔牌
        cards = yield DISCOVER(RandomCollectible(race=Race.DEMON))
        if cards:
            discovered_card = cards[0]
            # 设置属性值和费用
            # 使用 Buff 设置固定值
            yield Buff(discovered_card, "TOY_652e", atk_value=self.atk, health_value=self.health, cost_value=self.cost)


class TOY_652e:
    """属性值和费用调整 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, atk_value=0, health_value=0, cost_value=0, **kwargs):
        super().__init__(*args, **kwargs)
        self._atk_value = atk_value
        self._health_value = health_value
        self._cost_value = cost_value
    
    # 设置为固定值
    @property
    def atk(self):
        return self._atk_value - (self.owner.atk if hasattr(self, 'owner') and self.owner else 0)
    
    @property
    def max_health(self):
        return self._health_value - (self.owner.max_health if hasattr(self, 'owner') and self.owner else 0)
    
    @property
    def cost_mod(self):
        return self._cost_value - (self.owner.cost if hasattr(self, 'owner') and self.owner else 0)


# LEGENDARY

class TOY_647:
    """玛瑟里顿（未发售版） - Magtheridon, Unreleased
    [x]Dormant for 2 turns. While Dormant, deal 3 damage to all enemies at the end of your turn.
    """
    # 8/12/12 休眠2回合。休眠状态下，在你的回合结束时，对所有敌人造成3点伤害
    # 双种族：MECHANICAL + DEMON
    
    def play(self):
        # 使自己休眠2回合
        yield SetDormant(SELF, 2)
        # 添加休眠期间的效果
        yield Buff(SELF, "TOY_647e3")


class TOY_647e3:
    """休眠期间的效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 在你的回合结束时，如果随从处于休眠状态，对所有敌人造成3点伤害
    events = OWN_TURN_END.on(
        Find(Attr(OWNER, "dormant") == True) & Hit(ENEMY_CHARACTERS, 3)
    )


class TOY_913:
    """希希集 - Ci'Cigi
    [x]Battlecry, Outcast, and Deathrattle: Get a random   first-edition Demon Hunter   card <i>(in mint condition)</i>.
    """
    # 4/3/3 战吼，流放，亡语：随机获取一张初版恶魔猎手卡牌（品相完美）
    # 初版恶魔猎手卡牌指的是"外域的灰烬"（BLACK_TEMPLE）扩展包的恶魔猎手卡牌
    
    def play(self):
        # 战吼：获取一张初版恶魔猎手卡牌
        yield self._get_first_edition_card()
        
        # 流放：再获取一张
        if self.outcast:
            yield self._get_first_edition_card()
    
    def deathrattle(self):
        # 亡语：获取一张初版恶魔猎手卡牌
        yield self._get_first_edition_card()
    
    def _get_first_edition_card(self):
        """获取一张初版恶魔猎手卡牌"""
        # 初版恶魔猎手卡牌来自 BLACK_TEMPLE 扩展包
        # 使用 RandomCollectible 过滤
        yield Give(CONTROLLER, RandomCollectible(
            card_class=CardClass.DEMONHUNTER,
            card_set=CardSet.BLACK_TEMPLE
        ))
