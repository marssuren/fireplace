"""
威兹班的工坊 - 中立 - RARE
"""
from ..utils import *


class MIS_314:
    """积木魔像 - Building-Block Golem
    Rush Deathrattle: Summon three random 1-Cost minions.
    """
    # 5费 6/3 突袭。亡语：随机召唤三个法力值消耗为（1）的随从
    # 官方数据：突袭 + 亡语机制
    rush = True
    
    def deathrattle(self):
        # 召唤3个随机1费随从
        for _ in range(3):
            yield Summon(CONTROLLER, RandomCollectible(card_type=CardType.MINION, cost=1))


class TOY_312:
    """恋旧的侏儒 - Nostalgic Gnome
    Miniaturize Rush. After this minion deals exact lethal damage on your turn, draw a card.
    """
    # 4费 4/4 微缩。突袭。在本随从在你的回合中造成恰好致命伤害后，抽一张牌
    # 官方数据：Miniaturize 机制由核心引擎自动处理，生成 1费 1/1 的 TOY_312t
    # 
    # 【完整实现】"exact lethal" 意味着攻击伤害恰好等于目标剩余生命值
    # 官方解释：如果敌方随从有3点生命，本随从需要造成恰好3点伤害才能触发抽牌
    # 如果本随从攻击力大于目标生命值（例如5攻打3血），则不触发
    # 
    # 实现方式：
    # 1. 在攻击前记录目标的当前生命值
    # 2. 在攻击后检查：目标死亡 且 本随从攻击力 == 目标原生命值
    rush = True
    
    # 使用 Attack 事件的 on 触发器（攻击前）记录目标生命值
    # 然后在 after 触发器（攻击后）检查是否恰好致命
    def OWN_ATTACK_TRIGGER(self, source, target):
        """攻击前：记录目标生命值"""
        if target and hasattr(target, 'health'):
            # 记录目标当前生命值
            self._last_target_health = target.health
            self._last_target = target
        return []
    
    def OWN_ATTACK_AFTER_TRIGGER(self, source, target):
        """攻击后：检查是否造成恰好致命伤害"""
        # 检查是否在自己的回合
        if not self.controller.current_player:
            return []
        
        # 检查是否有记录的目标
        if not hasattr(self, '_last_target') or not hasattr(self, '_last_target_health'):
            return []
        
        # 检查目标是否死亡
        if target and target.zone == Zone.GRAVEYARD:
            # 检查是否恰好致命：攻击力 == 目标原生命值
            if source.atk == self._last_target_health:
                # 触发抽牌
                return [Draw(CONTROLLER)]
        
        return []
    
    events = [
        Attack(SELF).on(OWN_ATTACK_TRIGGER),
        Attack(SELF).after(OWN_ATTACK_AFTER_TRIGGER)
    ]


class TOY_509:
    """发条演奏家 - Wind-Up Musician
    Tradeable Battlecry: Deal 1 damage to all enemy minions. <i>(Trade to upgrade!)</i>
    """
    # 6费 5/5 可交易。战吼：对所有敌方随从造成1点伤害。（交易后升级！）
    # 官方数据：Tradeable 机制，交易后升级
    # 
    # 【交易升级机制】每次交易后，伤害增加1点
    # - 基础版本：造成 1 点伤害
    # - 交易 1 次后：造成 2 点伤害
    # - 交易 2 次后：造成 3 点伤害
    # - 以此类推
    # 
    # 实现方式：使用卡牌自定义属性 times_traded 追踪交易次数
    # 参考：druid.py 中的 TOY_802 (发条树苗)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化交易次数计数器
        if not hasattr(self, 'times_traded'):
            self.times_traded = 0
    
    def play(self):
        # 伤害 = 1 + 交易次数
        damage = 1 + getattr(self, 'times_traded', 0)
        # 对所有敌方随从造成伤害
        yield Hit(ENEMY_MINIONS, damage)
    
    # 监听交易事件（卡牌从手牌返回牌库）
    events = ZoneChange(SELF, Zone.HAND, Zone.DECK).after(
        lambda self: setattr(self, 'times_traded', getattr(self, 'times_traded', 0) + 1)
    )


class TOY_520:
    """秘迹观测者 - Observer of Mysteries
    Battlecry: Cast 2 random Secrets. At the start of your turn, destroy them.
    """
    # 3费 2/2 恶魔 战吼：随机施放2个奥秘。在你的回合开始时，摧毁这些奥秘
    # 官方数据：战吼机制，施放随机奥秘
    # 
    # 【完整实现】追踪由本随从施放的奥秘，只摧毁这些奥秘
    # 官方描述："destroy them" 指代施放的2个奥秘，不是所有奥秘
    # 
    # 实现方式：
    # 1. 使用自定义属性 `_cast_secrets` 存储施放的奥秘引用
    # 2. 参考 hunter.py 中的 MIS_914 实现，直接创建奥秘卡牌并设置 zone
    # 3. 在回合开始时，只摧毁存储的奥秘
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化施放的奥秘列表
        self._cast_secrets = []
    
    def play(self):
        # 施放2个随机奥秘
        # 从玩家职业的可收集奥秘中随机选择
        for _ in range(2):
            # 随机选择一个职业奥秘
            secret_pool = RandomCollectible(
                card_class=self.controller.hero.card_class,
                card_type=CardType.SPELL,
                game_tag={GameTag.SECRET: True}
            )
            secrets = secret_pool.eval(self.game, self)
            
            if secrets:
                # 创建奥秘卡牌并直接放入奥秘区域
                # 参考 hunter.py 中的 MIS_914 实现
                secret_id = secrets[0].id
                secret = self.controller.card(secret_id, source=self)
                secret.zone = Zone.SECRET
                
                # 记录施放的奥秘引用
                self._cast_secrets.append(secret)
    
    def OWN_TURN_BEGIN_TRIGGER(self, player):
        """在回合开始时，摧毁施放的奥秘"""
        # 摧毁所有记录的奥秘
        actions = []
        for secret in self._cast_secrets:
            # 检查奥秘是否还在场上（可能已被触发）
            if secret.zone == Zone.SECRET:
                actions.append(Destroy(secret))
        
        # 清空列表
        self._cast_secrets = []
        
        return actions
    
    events = OWN_TURN_BEGIN.on(OWN_TURN_BEGIN_TRIGGER)


class TOY_895:
    """折纸仙鹤 - Origami Crane
    Taunt Battlecry: Swap Health with another minion.
    """
    # 4费 4/1 野兽 嘲讽。战吼：与另一个随从交换生命值
    # 官方数据：嘲讽 + 战吼机制
    taunt = True
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        target = self.target
        if target:
            # 交换生命值
            self_health = self.health
            target_health = target.health
            # 使用 Buff 设置生命值
            yield Buff(SELF, "TOY_895e", health=target_health - self_health)
            yield Buff(target, "TOY_895e", health=self_health - target_health)


class TOY_895e:
    """折纸 - 生命值交换"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


class TOY_897:
    """软软多头蛇 - Floppy Hydra
    Deathrattle: Shuffle a copy of this into your deck with permanently doubled Attack and Health.
    """
    # 3费 2/4 野兽 亡语：将一张本随从的复制洗入你的牌库，并使其攻击力与生命值永久翻倍
    # 官方数据：亡语机制，永久翻倍属性
    # 
    # 【实现说明】使用卡牌级别计数器追踪翻倍次数
    # 每次亡语触发，翻倍次数+1，属性值 = 基础值 * 2^level
    
    def deathrattle(self):
        # 获取当前卡牌级别（翻倍次数）
        level = getattr(self, 'card_level', 0)
        # 计算新的属性值（基础值 2/4，每次翻倍）
        new_atk = 2 * (2 ** (level + 1))
        new_health = 4 * (2 ** (level + 1))
        
        # 创建一个新的复制并洗入牌库
        card = yield Shuffle(CONTROLLER, self.id)
        if card:
            # 设置新的卡牌级别
            setattr(card, 'card_level', level + 1)
            # 添加永久属性 Buff
            yield Buff(card, "TOY_897e", atk=new_atk - 2, health=new_health - 4)


class TOY_897e:
    """软软翻倍 - 永久属性增强"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


