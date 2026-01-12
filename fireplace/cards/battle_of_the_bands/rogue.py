from ..utils import *

class ETC_077:
    """Disc Jockey - 八爪碟机
    2费 3/2 机械
    连击：随机将一张连击牌置入你的手牌。
    """
    race = Race.MECHANICAL
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        
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
        # 发现对手在本局对战中使用过的卡牌
        # 使用 Player.cards_played_this_game 追踪系统
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
    combo = GivePoisonous(SELF)

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
        # Bounce 后 target 引用仍然有效，可以直接 Buff
        # 参考：OG_080c (Bloodthistle Toxin) 使用相同模式
        if is_enemy:
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
    race = Race.MECHANICAL
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        
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
        events = OWN_TURN_BEGIN.on(Morph(SELF, "ETC_717t"))

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
        events = OWN_TURN_BEGIN.on(Morph(SELF, "ETC_717"))

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
            # 检查是否有 COMBO 标签
            if c.tags.get(GameTag.COMBO, False) and c is not self:
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
        # 记录目标的当前属性（包含增益和受伤状态）
        # 参考：nathria/priest.py REV_248 - "with its stats" 使用当前属性
        # - atk: 当前攻击力（包含增益）
        # - health: 当前生命值（如果受伤，复制品也保持相同生命值）
        atk = target.atk
        health = target.health

        # 移回手牌
        yield Bounce(target)

        # 召唤舞者，具有目标的属性和突袭
        token = yield Summon(CONTROLLER, "ETC_076t")
        if token:
            # 设置舞者的属性为目标的当前属性
            token.atk = atk
            token.max_health = health  # 使用当前生命值作为最大生命值

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
    亡语：复原1个法力水晶。（装备期间，使用连击牌以提升此效果！）

    官方数据确认：基础复原1个法力水晶，每打出连击牌+1
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 1, # 计数器：复原的法力水晶数量
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
    """本回合费用为1

    实现方式：
    - 使用 COST_SET 设置费用为1（而不是增加）
    - 使用 OwnTurnEnd 事件在回合结束时销毁此 Buff

    参考：
    - VAC_524e2 (paradise/mage.py) - 使用 COST_SET 设置费用
    - DMF_111e (darkmoon/warlock.py) - 使用 OwnTurnEnd 实现本回合有效
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: SET(1),
    }
    events = OWN_TURN_END.on(Destroy(SELF))

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
        # 官方数据确认:只有一个通用的麦克风武器 (1/2)
        mic_id = "ETC_078t"

        # 我方装备
        yield Equip(CONTROLLER, mic_id)

        # 敌方装备
        yield Equip(OPPONENT, mic_id)
        
        # 给敌方武器施加负面效果
        # 需要获取敌方刚装备的武器
        weapon = self.controller.opponent.weapon
        if weapon and weapon.id == mic_id:
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
    """Glass Jaw - 玻璃下巴
    使装备此武器的英雄的对手受到的所有伤害增加1点

    实现方式：
    - 这是一个施加在对手武器上的 Buff
    - 监听武器拥有者（OWNER）受到伤害的 Predamage 事件
    - 拦截原始伤害，取消后施加增加1点的伤害

    参考：ETC_084 (邪弦竖琴) 使用 Predamage 事件拦截并修改伤害
    """
    # OWNER 是装备此 buff 的武器的拥有者（对手英雄）
    # 当对手英雄即将受到伤害时，增加1点伤害
    events = Predamage(OWNER).on(
        lambda self, source, target, amount: [
            Predamage(target, 0),           # 取消原始伤害
            Hit(target, amount + 1)         # 施加增加后的伤害（原始+1）
        ]
    )

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
        GameTag.COST: SET(1), # 永久变为1? 描述未说"本回合"。
    }
