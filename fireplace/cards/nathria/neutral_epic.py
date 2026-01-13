"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_032:
    """Tight-Lipped Witness - 无语的证人
    <b>Secrets</b> can't be revealed.
    <b>奥秘</b>不能被揭示。
    """
    # 给己方所有奥秘添加"不能被揭示"的标记
    # 核心的 Reveal action 会检查此标记并阻止奥秘被揭示
    update = Refresh(FRIENDLY_SECRETS, buff="MAW_032e")


class MAW_032e:
    """Tight-Lipped Witness Aura - 无语的证人光环"""
    tags = {enums.CANT_BE_REVEALED: True}


class REV_017:
    """Insatiable Devourer - 贪食的吞噬者
    [x]<b>Battlecry:</b> Devour an enemy 
minion and gain its stats. 
 <b>Infuse (5):</b> And its neighbors.
    <b>战吼：</b>吞噬一个敌方随从并获得其属性。<b>注能(5)：</b>同时吞噬相邻随从。
    """
    infuse = 5
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 评估主目标
        main_target = self.target
        if not main_target:
            return
        
        targets = [main_target]
        
        # 如果已注能，添加相邻随从
        if self.infused:
            adjacent = ADJACENT(main_target).eval(self.game, self)
            if adjacent:
                targets.extend(adjacent)
        
        # 吞噬所有目标
        total_atk = 0
        total_health = 0
        
        for target in targets:
            if target and not target.dead:
                total_atk += target.atk
                total_health += target.health
                yield Destroy(target)
        
        # 给自己加属性
        if total_atk > 0 or total_health > 0:
            yield Buff(SELF, "REV_017e", atk=total_atk, health=total_health)


class REV_017e:
    """Insatiable Devourer Buff - 贪食的吞噬者增益"""
    # 动态属性通过 Buff 的 kwargs 传入
    pass


class REV_023:
    """Demolition Renovator - 拆迁修理工
    <b>Tradeable</b>
<b>Battlecry:</b> Destroy 
an enemy location.
    <b>可交易，战吼：</b>摧毁一个敌方地标。
    """
    # Tradeable 机制已在核心实现
    tags = {GameTag.TRADEABLE: True}
    
    def play(self):
        # 摧毁敌方地标
        enemy_locations = [card for card in self.controller.opponent.field 
                          if card.type == CardType.LOCATION]
        if enemy_locations:
            # 如果有多个地标，摧毁第一个（通常只有一个）
            yield Destroy(enemy_locations[0])


class REV_370:
    """Party Crasher - 派对捣蛋鬼
    [x]<b>Battlecry:</b> Choose an
enemy minion. Throw a
random minion from
your hand at it.
    <b>战吼：</b>选择一个敌方随从。将你手牌中的一个随机随从扔向它。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 从手牌中随机选择一个随从
        hand_minions = [card for card in self.controller.hand 
                       if card.type == CardType.MINION and card != self]
        
        if hand_minions:
            thrown_minion = self.game.random.choice(hand_minions)
            # "扔"随从 = 召唤它并让它攻击目标
            summoned = yield Summon(CONTROLLER, thrown_minion)
            if summoned and TARGET and not TARGET.dead:
                # 让召唤的随从攻击目标
                yield Attack(summoned, TARGET)


class REV_843:
    """Sinfueled Golem - 罪能魔像
    <b>Infuse (3):</b> Gain stats equal to the Attack of the minions that <b>Infused</b> this.
    <b>注能(3):</b> 获得等同于为其注能的随从的攻击力的属性。
    """
    infuse = 3
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 显式初始化 infused_minions 列表
        # 注意：此列表会在核心的 Death action (actions.py:407-415) 中被自动填充
        # 当友方随从死亡且此卡在手牌中时，核心会自动追加死亡随从的信息
        self.infused_minions = []
    
    def play(self):
        if self.infused:
            # 计算所有注能随从的总攻击力
            # infused_minions 由核心的 Infuse 机制自动维护
            # 每个元素是一个字典: {'atk': int, 'health': int, 'id': str, 'race': Race}
            total_atk = sum(minion['atk'] for minion in self.infused_minions)
            # 获得等同于攻击力的攻击力和生命值
            if total_atk > 0:
                yield Buff(SELF, "REV_843e", atk=total_atk, health=total_atk)


class REV_843e:
    """Sinfueled Golem Buff - 罪能魔像增益"""
    # 动态属性通过 Buff 的 kwargs 传入
    pass


class REV_960:
    """Ashen Elemental - 灰烬元素
    [x]<b>Battlecry:</b> Whenever your
opponent draws a card next
turn, they take 2 damage.
    <b>战吼：</b>在对手的下个回合中，每当其抽一张牌，便受到2点伤害。
    """
    play = Buff(OPPONENT, "REV_960e")


class REV_960e:
    """Ashen Elemental Effect - 灰烬元素效果"""
    # 对手抽牌时受到伤害，对手回合结束时移除
    events = [
        Draw(OPPONENT).after(lambda self, target, card: Hit(ENEMY_HERO, 2)),
        EndTurn(OPPONENT).on(Destroy(SELF))
    ]


