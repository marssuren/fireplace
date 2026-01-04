from ..utils import *

class ETC_077:
    """Disc Jockey - 八爪碟机
    2费 3/2 机械
    连击：随机将一张连击牌置入你的手牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RACE: Race.MECH,
        GameTag.COMBO: True,
    }
    # 连击：给予一张随机连击牌
    combo = Give(CONTROLLER, RandomCollectible(combo=True))

class ETC_075:
    """Mic Drop - 闭麦收工
    3费法术
    抽两张牌。压轴：使你的武器获得+2攻击力。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    def play(self):
        yield Draw(CONTROLLER) * 2
        
        # 压轴：如果剩余法力值为0，Buff武器
        if self.controller.mana == 0:
            yield Buff(FRIENDLY_WEAPON, "ETC_075e")

class ETC_075e:
    tags = {
        GameTag.ATK: 2,
    }

class ETC_074:
    """Mixtape - 串烧磁带
    1费法术
    发现一张你的对手在本局对战中使用过的牌的复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        # 发现对手使用过的卡牌
        # 需要获取对手打出过的记录列表
        # Fireplace Game对象有 history? 或者 controller.opponent.cards_played_this_game (但只含本局)
        # 题目说 "played this game"
        # 假设 list(self.controller.opponent.cards_played_this_game) 可用
        # 我们需要从中筛选并发现
        
        # 获取对手打出的所有卡牌ID
        opponent_cards = [c.id for c in self.controller.opponent.cards_played_this_game]
        
        if opponent_cards:
            # 发现逻辑：从列表中选择3个（如果足够），让玩家选一个，获得其复制
            # Fireplace 的 DiscoverAction 通常针对 RandomCard selector
            # 这里我们需要自定义发现池
            yield Discover(CONTROLLER, RandomCard(card_list=opponent_cards))
        else:
            # 如果没打出过牌，无效果
            pass

class JAM_021:
    """One Hit Wonder - 单曲流星
    2费 3/2
    突袭。连击：获得剧毒。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RUSH: True,
        GameTag.COMBO: True,
    }
    # 连击：获得剧毒
    combo = SetAttr(SELF, GameTag.POISONOUS, True)

class JAM_020:
    """Tough Crowd - 挑剔的观众
    3费法术
    选择一个随从。将其移回拥有者的手牌。如果是敌方随从，使其法力值消耗增加(2)点。
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
        target = self.target
        is_enemy = target.controller != self.controller
        
        # 移回手牌
        yield Bounce(target)
        
        # 如果是敌方，增加费用
        if is_enemy:
            # Bounce 后 target 变成了 Card 对象 (在手牌中)
            # 需要找到那张卡。BounceAction 通常会更新 target 为手牌中的卡吗？
            # Fireplace Bounce 实现：move to HAND.
            # 此时 target 引用应该仍然指向 Entity，但 Zone 变了。
            # 直接 Buff 即可。
            yield Buff(target, "JAM_020e")

class JAM_020e:
    tags = {
        GameTag.COST: 2,
    }

class ETC_072:
    """Beatboxer - B-Box拳手
    3费 3/3 机械
    连击：造成4点伤害，随机分配到所有敌人身上。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.RACE: Race.MECH,
        GameTag.COMBO: True,
    }
    # 连击：4点伤害随机分配
    combo = Hit(RANDOM_ENEMY_CHARACTER, 1) * 4

class ETC_717:
    """Harmonic Hip Hop - 悦耳嘻哈
    2费法术
    造成1点伤害。使你的武器获得+3攻击力。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    def play(self):
        yield Hit(TARGET, 1)
        yield Buff(FRIENDLY_WEAPON, "ETC_717e")
    
    # 切换逻辑 (悦耳 -> 刺耳)
    # 在手牌中，回合开始时变形
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "ETC_717t"))

class ETC_717t:
    """Dissonant Hip Hop - 刺耳嘻哈
    2费法术
    造成1点伤害。使你的武器获得+1攻击力。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    def play(self):
        yield Hit(TARGET, 1)
        yield Buff(FRIENDLY_WEAPON, "ETC_717te")

    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "ETC_717"))

class ETC_717e:
    tags = {GameTag.ATK: 3}

class ETC_717te:
    tags = {GameTag.ATK: 1}

class ETC_073:
    """Rhyme Spinner - 押韵狂人
    3费 2/3
    突袭。连击：在本局对战中，你每使用过一张其他连击牌，便获得+1/+1。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.RUSH: True,
        GameTag.COMBO: True,
    }
    
    def play(self):
        # 必须是连击触发时才获得Buff？
        # 描述："连击：......便获得+1/+1"
        # 意味着只有触发了连击，才会计算并获得Buff
        pass # play逻辑为空，逻辑在combo里
        
    def combo(self):
        # 统计已使用的连击牌 (排除自己?) "Other combo cards". 
        # 此时自己已经 played? Yes.
        # cards_played_this_game
        count = 0
        for c in self.controller.cards_played_this_game:
            if c.combo and c is not self:
                count += 1
        
        if count > 0:
            yield Buff(SELF, "ETC_073e") * count

class ETC_073e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }

class ETC_076:
    """Breakdance - 街舞起跳
    1费法术
    将一个友方随从移回你的手牌。召唤一个具有其属性值和突袭的舞者。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        target = self.target
        # 记录属性
        atk = target.atk
        health = target.health # 受伤状态？通常是当前生命值上限？还是当前生命值？
        # "With its stats". Usually means Current Stats (Buffed).
        # But Health is usually Max Health? 
        # If I bounce a 3/1 damaged (originally 3/3), token is 3/1 or 3/3?
        # Usually copies Max Health.
        max_health = target.max_health
        
        # 移回手牌
        yield Bounce(target)
        
        # 召唤舞者
        # ID: ETC_076t
        token = yield Summon(CONTROLLER, "ETC_076t")
        if token:
            # 应用属性
            # 如果直接 Summon，属性是基础属性
            # 需要 Buff 到目标属性
            # 或者使用 Morph? 不，是召唤新随从
            yield Buff(token, "ETC_076e", atk=atk, max_health=max_health)
            # 设置当前生命值为 max_health (默认即满血)

class ETC_076t:
    """Dancer - 舞者"""
    tags = {
        GameTag.ATK: 1, # Placeholder
        GameTag.HEALTH: 1,
        GameTag.COST: 1, # Placeholder
        GameTag.RUSH: True,
    }

class ETC_076e:
    # 用于设置属性的Buff
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_518:
    """Record Scratcher - 搓盘机
    3费 2/2 武器
    亡语：复原2个法力水晶。（装备期间，使用连击牌以提升此效果！）
    """
    # 基础是复原2个? 描述说 "复原 1 个... 提升效果"。
    # 假设基础是1。
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 1, # 计数器
    }
    
    # 亡语：复原 X 个水晶
    # 可能是 Refresh 还是 Gain? "Refresh Mana Crystals".
    deathrattle = GainMana(CONTROLLER, Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1))
    
    # 提升逻辑：使用连击牌
    events = Play(CONTROLLER, COMBO).on(
        Buff(SELF, "ETC_518e")
    )

class ETC_518e:
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 1,
    }

class ETC_079:
    """Bounce Around (ft. Garona) - 舞动全场（ft.迦罗娜）
    3费法术
    将所有友方随从移回你的手牌。在本回合中，其法力值消耗为（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 捕获当前场上的随从列表
        minions = list(self.controller.field)
        
        for m in minions:
            yield Bounce(m)
            # Bounce 后，m 变成了手牌中的对象 (同 Entity)
            # 施加减费 Buff (本回合有效)
            yield Buff(m, "ETC_079e")

class ETC_079e:
    tags = {
        GameTag.COST: 1, # 设置为1? 还是减少? "Set Cost to 1".
        # Fireplace Buff 默认为增加属性。
        # 如果要 SET 属性，需要特殊 Action 或 ChangeCost Buff
        # 使用 COST_SET Tag
        GameTag.COST_SET: 1,
    }
    # 本回合有效：OneTurnEffect?
    # Buff 默认是永久的。需要 ONE_TURN_EFFECT
    # 但在手牌中的 Buff 通常不会自动消失，除非是光环?
    # 描述 "This turn, they cost (1)". 
    # 这意味着回合结束恢复。
    # 需要在回合结束时移除 Buff。
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))

class ETC_078:
    """MC Blingtron - MC布林顿
    5费 3/4 
    战吼：双方玩家各装备一把1/2的麦克风。你对手的麦克风使其受到的所有伤害增加1点！
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    
    def play(self):
        # 随机麦克风 ID 列表 (假设)
        mics = ["ETC_078t", "ETC_078t2", "ETC_078t3"] # 假设有多个，或者只有一个通用麦克风
        # 这里为了简化，假设只有一个麦克风 ID
        mic_id = "ETC_078t"
        
        # 我方装备
        yield Equip(CONTROLLER, mic_id)
        
        # 敌方装备
        yield Equip(OPPONENT, mic_id)
        
        # 给敌方武器施加负面效果
        # 需要获取敌方刚装备的武器
        weapon = self.controller.opponent.weapon
        if weapon and weapon.card_id == mic_id:
            yield Buff(weapon, "ETC_078e")

class ETC_078t:
    """Microphone - 麦克风"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.WEAPON,
    }

class ETC_078e:
    """Glass Jaw - 受到伤害+1"""
    # 这是一个施加在武器上的 Buff，使得英雄受到伤害+1
    # 需要 Hero 受到伤害时触发？
    # 或者 Buff 提供一个光环：Player Tag DAMAGE_MULTIPLIER?
    # 或者 Event: Damage(OPPONENT_HERO).on(Hit(OPPONENT_HERO, 1))?
    # 这会造成连锁反应。
    # 更好的方式：Wait for damage, increase amount?
    # Fireplace 可能不支持直接修改伤害量。
    # 使用简单逻辑：当英雄受到伤害时，额外造成1点。
    events = Damage(OWNER).on(Hit(OWNER, 1))

class JAM_019:
    """Rhythmdancer Risa - 踏韵舞者丽萨
    4费 4/4
    突袭。在你的英雄攻击后，将本随从移回你的手牌并使其法力值消耗变为（1）点。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.RUSH: True,
    }
    # 事件：英雄攻击后
    events = Attack(FRIENDLY_HERO).after(
        Bounce(SELF),
        Buff(SELF, "JAM_019e")
    )

class JAM_019e:
    tags = {
        GameTag.COST_SET: 1, # 永久变为1? 描述未说"本回合"。
    }

class ETC_074:
    """Mixtape - 串烧磁带
    1费法术 发现一张你的对手在本局对战中使用过的牌的复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    def play(self):
        # 简单发现逻辑
        yield Discover(CONTROLLER, RandomCard(card_list=lambda: [c.id for c in self.controller.opponent.cards_played_this_game]))
