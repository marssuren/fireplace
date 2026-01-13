"""
深暗领域 - PALADIN
"""
from ..utils import *


# COMMON

class GDB_137:
    """明澈圣契 - Libram of Clarity
    3费 圣骑士法术
    抽两张随从牌。如果本牌的法力值消耗为（0）点，则使其获得+2/+1。
    
    Draw 2 minions. If this costs (0), give them +2/+1.
    """
    def play(self):
        # 抽两张随从牌
        cards = yield Draw(CONTROLLER) * 2
        
        # 如果本牌费用为0，给予+2/+1
        if self.cost == 0:
            for card in cards:
                if card and card.type == CardType.MINION:
                    yield Buff(card, "GDB_137e")


class GDB_137e:
    """+2/+1增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_721:
    """星际旅行者 - Interstellar Wayfarer
    4费 4/2 圣骑士随从 - 德莱尼
    圣盾
    战吼：在本局对战中，你的圣契的法力值消耗减少（1）点。
    
    Divine Shield
    Battlecry: Reduce the Cost of your Librams by (1) this game.
    """
    race = Race.DRAENEI
    
    def play(self):
        # 在本局对战中，圣契的法力值消耗减少1点
        # 参考 outlands/paladin.py 的 BT_020 实现
        yield Buff(CONTROLLER, "GDB_721e")


class GDB_721e:
    """圣契减费光环"""
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + LIBRAM, {GameTag.COST: -1})


class GDB_728:
    """星际研究员 - Interstellar Researcher
    2费 2/2 圣骑士随从 - 德莱尼
    战吼和法术迸发：抽一张圣契牌。
    
    Battlecry and Spellburst: Draw a Libram.
    """
    race = Race.DRAENEI
    tags = {
        GameTag.SPELLBURST: True,
    }
    
    def play(self):
        # 定义抽圣契牌的辅助函数
        def draw_libram():
            """抽一张圣契牌"""
            # 从牌库中找到所有圣契牌
            librams = [card for card in self.controller.deck if card.tags.get(GameTag.LIBRAM, False)]
            if librams:
                # 随机抽一张
                import random
                libram = random.choice(librams)
                yield Draw(CONTROLLER, libram)
        
        # 战吼：抽一张圣契牌
        yield from draw_libram()
    
    # 法术迸发：抽一张圣契牌
    # 注意：spellburst 现在已经在 scriptnames 中，会被正确提取
    spellburst = lambda self: (
        Draw(CONTROLLER, self.game.random.choice([c for c in self.controller.deck if c.tags.get(GameTag.LIBRAM, False)]))
        if [c for c in self.controller.deck if c.tags.get(GameTag.LIBRAM, False)]
        else None
    )


class SC_404:
    """回收地堡 - Salvage the Bunker
    3费 圣骑士法术
    召唤两个2/2并具有嘲讽的陆战队员。你的下一次星舰发射的法力值消耗减少（2）点。
    
    Summon two 2/2 Marines with Taunt. Your next Starship launch costs (2) less.
    """
    def play(self):
        # 召唤两个2/2嘲讽陆战队员
        yield Summon(CONTROLLER, "SC_404t") * 2
        
        # 下一次星舰发射减费2点
        yield Buff(CONTROLLER, "SC_404e")


class SC_404e:
    """星舰发射减费 - Starship Launch Cost Reduction
    
    效果说明:
    - 使你的下一次星舰发射的法力值消耗减少(2)点
    - 这是一次性效果,使用后自动移除
    
    实现机制:
    - 通过starship_launch_cost_reduction属性标记减费数值
    - 核心引擎的LaunchStarship动作会检查此属性(actions.py:1143-1154)
    - 发射星舰时自动应用减费并移除此buff
    
    Your next Starship launch costs (2) less.
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    # 星舰发射减费数值(由核心引擎的LaunchStarship动作读取)
    starship_launch_cost_reduction = 2


# RARE

class GDB_139:
    """信仰圣契 - Libram of Faith
    6费 圣骑士法术（神圣）
    召唤三个3/3并具有圣盾的德莱尼。如果本牌的法力值消耗为（0）点，则使其获得突袭。
    
    Summon three 3/3 Draenei with Divine Shield. If this costs (0), give them Rush.
    """
    def play(self):
        # 召唤三个3/3圣盾德莱尼
        minions = yield Summon(CONTROLLER, "GDB_139t") * 3
        
        # 如果本牌费用为0，给予突袭
        if self.cost == 0:
            for minion in minions:
                if minion:
                    yield Buff(minion, "GDB_139e")


class GDB_139e:
    """突袭"""
    tags = {
        GameTag.RUSH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_462:
    """在轨卫星 - Orbital Satellite
    1费 圣骑士法术
    发现一张德莱尼牌。如果你在本回合中打出过与本牌相邻的牌，则再发现一张。
    
    Discover a Draenei. If you played an adjacent card this turn, Discover another.
    """
    def play(self):
        # 定义检查相邻牌的辅助函数
        def played_adjacent_card():
            """检查本回合是否打出过与本牌相邻的牌
            
            相邻指的是在手牌中位置相邻（位置差为1）
            """
            # 获取本牌在打出前的手牌位置
            my_position = None
            for card, position in self.controller.cards_played_this_turn_with_position:
                if card == self:
                    my_position = position
                    break
            
            if my_position is None:
                return False
            
            # 检查本回合打出的其他牌是否与本牌相邻
            for card, position in self.controller.cards_played_this_turn_with_position:
                if card != self and abs(position - my_position) == 1:
                    return True
            
            return False
        
        # 发现一张德莱尼牌
        yield Discover(CONTROLLER, RandomMinion(race=Race.DRAENEI))
        
        # 检查是否打出过相邻的牌
        if played_adjacent_card():
            # 再发现一张
            yield Discover(CONTROLLER, RandomMinion(race=Race.DRAENEI))


class GDB_726:
    """斩星巨刃 - Interstellar Starslicer
    3费 3/4 圣骑士武器
    战吼和亡语：在本局对战中，你的圣契的法力值消耗减少（1）点。
    
    Battlecry and Deathrattle: Reduce the Cost of your Librams by (1) this game.
    """
    # 战吼：圣契减费
    play = Buff(CONTROLLER, "GDB_726e")
    
    # 亡语：圣契减费
    deathrattle = Buff(CONTROLLER, "GDB_726e")


class GDB_726e:
    """圣契减费光环"""
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + LIBRAM, {GameTag.COST: -1})


class SC_405:
    """超级电容器 - Ultra-Capacitor
    4费 4/4 圣骑士随从 - 星舰组件
    战吼：每有一个其他友方随从，便获得+1/+1。发射时也会触发。
    
    Starship Piece
    Battlecry: Gain +1/+1 for each other friendly minion. Also triggers on launch.
    """
    # 战吼：每有一个其他友方随从，便获得+1/+1
    def play(self):
        count = len(self.controller.field) - 1  # 不包括自己
        if count > 0:
            yield Buff(SELF, "SC_405e", atk=count, health=count)
    
    # 发射时也会触发
    def launch(self):
        """星舰发射时触发
        
        注意：发射时，组件已经不在场上，而是累积到星舰上
        所以这里计算的是当前场上的随从数量
        """
        count = len(self.controller.field)
        if count > 0:
            # 给星舰增加属性
            if self.controller.starship_in_progress:
                yield Buff(self.controller.starship_in_progress, "SC_405e", atk=count, health=count)


class SC_405e:
    """属性增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_412:
    """恶火 - Hellion
    4费 4/4 圣骑士随从 - 机械
    你的其他随从获得+1攻击力。
    <i>（如果你在本局对战中发射过星舰，则会变形。）</i>
    
    Your other minions have +1 Attack.
    <i>(Transforms if you launched a Starship this game.)</i>
    """
    race = Race.MECHANICAL
    
    # 光环：其他随从+1攻击力
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: 1})
    
    # 监听星舰发射，变形为强化版本
    events = LaunchStarship(CONTROLLER).after(
        Morph(SELF, "SC_412t")
    )


# EPIC

class GDB_138:
    """神性圣契 - Libram of Divinity
    4费 圣骑士法术（神圣）
    使一个随从获得+3/+3。如果本牌的法力值消耗为（0）点，则在你的回合结束时，将本牌移回你的手牌。
    
    Give a minion +3/+3. If this costs (0), return this to your hand at the end of your turn.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 使目标获得+3/+3
        yield Buff(TARGET, "GDB_138e")
        
        # 如果费用为0，回合结束时返回手牌
        if self.cost == 0:
            # 给玩家添加一个buff，在回合结束时返回本牌
            yield Buff(CONTROLLER, "GDB_138e2", spell_id=self.id)


class GDB_138e:
    """+3/+3增益"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_138e2:
    """回合结束返回手牌"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    # 回合结束时，返回神性圣契到手牌
    events = OWN_TURN_END.on(
        lambda self, player: Give(CONTROLLER, self.spell_id) if hasattr(self, 'spell_id') else None,
        Destroy(SELF)
    )


class GDB_140:
    """星空光环 - Celestial Aura
    6费 圣骑士法术（神圣）
    在你恰好控制一个随从时，使其攻击力和生命值变为10。持续3回合。
    
    While you have exactly 1 minion in play, its Attack and Health are 10. Lasts 3 turns.
    """
    def play(self):
        # 给玩家添加光环效果，持续3回合
        yield Buff(CONTROLLER, "GDB_140e")


class GDB_140e:
    """星空光环效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化剩余回合数
        self.turns_remaining = 3
    
    # 光环：当恰好有1个随从时，使其攻击力和生命值变为10
    update = lambda self, entities: [
        Refresh(minion, {GameTag.ATK: SET(10), GameTag.HEALTH: SET(10)})
        for minion in self.controller.field
        if len(self.controller.field) == 1
    ]
    
    # 每个回合结束时减少计数
    events = OWN_TURN_END.on(
        lambda self, player: [
            setattr(self, 'turns_remaining', self.turns_remaining - 1),
            Destroy(SELF) if self.turns_remaining <= 0 else None
        ]
    )


# LEGENDARY

class GDB_141:
    """伊瑞尔，希望信标 - Yrel, Beacon of Hope
    5费 5/5 圣骑士随从 - 德莱尼（传说）
    突袭
    亡语：从旧时间线中获取三张不同的圣契牌！
    
    Rush
    Deathrattle: Get three different Librams from an older timeline!
    """
    race = Race.DRAENEI
    
    def deathrattle(self):
        # 从旧时间线获取三张不同的圣契牌
        # 这里指的是从所有圣契牌中随机选择3张不同的
        # 参考官方数据，圣契牌包括：
        # - Libram of Clarity (GDB_137)
        # - Libram of Faith (GDB_139)
        # - Libram of Divinity (GDB_138)
        # - Libram of Justice (BT_011) - 来自外域
        # - Libram of Hope (BT_024) - 来自外域
        # - Libram of Wisdom (BT_025) - 来自外域
        # - Libram of Judgment (DMF_236) - 来自暗月马戏团
        
        libram_pool = [
            "GDB_137",  # Libram of Clarity
            "GDB_139",  # Libram of Faith
            "GDB_138",  # Libram of Divinity
            "BT_011",   # Libram of Justice
            "BT_024",   # Libram of Hope
            "BT_025",   # Libram of Wisdom
            "DMF_236",  # Libram of Judgment
        ]
        
        # 随机选择3张不同的圣契
        import random
        selected_librams = random.sample(libram_pool, min(3, len(libram_pool)))
        
        for libram_id in selected_librams:
            yield Give(CONTROLLER, libram_id)


class GDB_144:
    """露米娅 - Lumia
    6费 9/9 圣骑士随从（传说）
    吸血
    在一个英雄受到伤害后，使其在本回合的剩余时间内免疫。
    
    Lifesteal
    After a hero takes damage, they become Immune for the rest of the turn.
    """
    # 监听英雄受到伤害
    events = Damage(HERO).after(
        lambda self, target, amount: Buff(target, "GDB_144e")
    )


class GDB_144e:
    """免疫本回合"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    # 回合结束时移除
    events = TurnEnd(ALL_PLAYERS).on(Destroy(SELF))
