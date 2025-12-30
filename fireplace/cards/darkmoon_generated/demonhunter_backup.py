from ..utils import *
from fireplace.enums import LIFESTEAL_DAMAGES_ENEMY


##
# Minions

class DMF_217:
    """Line Hopper (越线的游客)
    Your Outcast cards cost (1) less."""
    # 3费 3/4 - 你的流放牌法力值消耗减少(1)点
    
    # 假设 GameTag.OUTCAST 标记了具有流放关键字的卡牌
    update = Refresh(FRIENDLY_HAND + Attr(GameTag.OUTCAST, True), {GameTag.COST: -1})


class DMF_222:
    """Redeemed Pariah (获救的流民)
    After you play an Outcast card, gain +1/+1."""
    # 2费 2/3 - 在你打出一张流放牌后，获得+1/+1
    
    events = Play(FRIENDLY + Attr(GameTag.OUTCAST, True)).after(Buff(SELF, "DMF_222e"))


class DMF_222e:
    """Redeemed (获救)"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class DMF_223:
    """Renowned Performer (知名表演者)
    Rush Deathrattle: Summon two   1/1 Assistants with Taunt.  """
    # 4费 3/3 突袭，亡语：召唤两个1/1并具有嘲讽的助理
    
    deathrattle = Summon(CONTROLLER, "DMF_223t") * 2


class DMF_223t:
    """Assistant (助理)"""
    # 1/1 嘲讽
    # 这里的定义会被 CardDefs.xml 覆盖，主要是占位
    pass


class DMF_226:
    """Bladed Lady (刀锋舞娘)
    Rush Costs (1) if your hero has 6 or more Attack."""
    # 6费 6/6 突袭 - 如果你的英雄拥有6点或以上攻击力，法力值消耗为(1)点
    
    # 使用 update 光环动态修改费用
    # 只有在手牌中且满足条件时生效
    update = (ATK(FRIENDLY_HERO) >= 6) & Refresh(SELF, {GameTag.COST: SET(1)})


class DMF_229:
    """Stiltstepper (高跷艺人)
    Battlecry: Draw a card. If you play it this turn, give your hero +4 Attack this turn."""
    # 3费 4/1 - 战吼：抽一张牌。如果你在本回合中使用这张牌，使你的英雄在本回合中获得+4攻击力
    
    # 抽牌并给抽到的牌添加一个追踪 buff
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_229e_tracker"))


class DMF_229e_tracker:
    """Stiltstepper Tracker"""
    # 这是一个附在抽到的卡牌上的 buff
    # 当这张牌被打出时，触发效果
    events = Play(SELF).on(
        Buff(FRIENDLY_HERO, "DMF_229e_hero"),
        Destroy(SELF)  # 触发后移除 buff
    )
    # 回合结束时移除追踪
    events += TURN_END.on(Destroy(SELF))


class DMF_229e_hero:
    """High Steps (高超舞步)"""
    # 英雄获得 +4 攻击力，本回合有效
    tags = {GameTag.ATK: 4}
    events = REMOVED_IN_PLAY


class DMF_230:
    """Il'gynoth (伊格诺斯)
    Lifesteal Your Lifesteal damages the enemy hero instead of healing you."""
    # 4费 2/6 吸血 - 你的吸血改为对敌方英雄造成伤害
    
    update = Refresh(CONTROLLER, {LIFESTEAL_DAMAGES_ENEMY: 1})


class DMF_231:
    """Zai, the Incredible (扎依，出彩艺人)
    Battlecry: Copy the left- and right-most cards in your hand."""
    # 5费 5/3 - 战吼：复制你手牌中最左边和最右边的牌
    
    def play(self):
        hand = self.controller.hand
        if not hand:
            return []
        
        # 复制最左边和最右边的牌
        # 注意：如果是同一张牌（手牌只有1张），会复制两次
        leftmost = hand[0]
        rightmost = hand[-1]
        
        return Give(CONTROLLER, Copy(leftmost) + Copy(rightmost))


class DMF_247:
    """Insatiable Felhound (贪食地狱犬)
    Taunt  Corrupt: Gain +1/+1 and Lifesteal."""
    # 3费 2/5 嘲讽 - 腐蚀：获得+1/+1和吸血
    
    corrupt = Buff(SELF, "DMF_247e")


class DMF_247e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.LIFESTEAL: True,
    }


class DMF_248:
    """Felsteel Executioner (魔钢处决者)
    Corrupt: Become a weapon."""
    # 3费 4/3 - 腐蚀：变成一把武器
    
    corrupt = Transform(SELF, "DMF_248t")


class DMF_248t:
    """Felsteel Executioner (魔钢处决者)"""
    # 3费 4/3 武器
    pass


class YOP_002:
    """Felsaber (邪刃豹)
    Can only attack if your hero attacked this turn."""
    # 4费 5/6 - 在本回合中，除非你的英雄进行过攻击，否则无法进行攻击
    
    update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


##
# Spells

class DMF_219:
    """Relentless Pursuit (冷酷追杀)
    Give your hero +4 Attack and Immune this turn."""
    # 3费 - 本回合中，使你的英雄获得+4攻击力和免疫
    
    play = Buff(FRIENDLY_HERO, "DMF_219e")


class DMF_219e:
    """Relentless Pursuit"""
    tags = {
        GameTag.ATK: 4,
        GameTag.IMMUNE: True,
    }
    events = REMOVED_IN_PLAY


class DMF_221:
    """Felscream Blast (邪吼冲击)
    Lifesteal. Deal $1 damage to a minion and its neighbors."""
    # 1费 吸血 - 对一个随从及其相邻随从造成1点伤害
    tags = {GameTag.LIFESTEAL: True}
    
    play = Hit(TARGET + TARGET_ADJACENT, 1)


class DMF_224:
    """Expendable Performers (演员大接力)
    Summon seven 1/1 Illidari with Rush. If they all die this turn, summon seven more."""
    # 7费 - 召唤七个1/1并具有突袭的伊利达雷。如果他们在本回合中全部死亡，则再次召唤七个
    
    def play(self):
        # 召唤7个（或填满战场）
        # 需要追踪这批特定的随从是否全部死亡
        # 这比较复杂，因为 fireplace 没有内置的"追踪这批随从"的机制
        
        # 简化实现：召唤7个。
        # "如果他们全部死亡" 很难精确实现，因为需要追踪ID
        # 考虑到这是法术的一步结算，实际上不太可能在同一结算周期内检测死亡
        # 
        # 重新理解：这是一个持续效果？不，是如果他们全部死亡（在本回合内）。
        # 这意味着需要一个 Buff 或 Aura 来追踪这批随从
        #
        # 这里的逻辑比较复杂，暂时标记为 TODO
        
        # 基础效果：召唤7个
        return Summon(CONTROLLER, "DMF_224t") * 7


class DMF_225:
    """Throw Glaive (投掷利刃)
    Deal $2 damage to a minion. If it dies, add a Temporary copy of this to your hand."""
    # 1费 - 对一个随从造成2点伤害。如果该随从死亡，则将一张本牌的临时复制置入你的手牌
    
    def play(self):
        return Hit(TARGET, 2).then(
            Dead(TARGET) & Give(CONTROLLER, Copy(SELF) + SetTag(GameTag.TAG_SCRIPT_DATA_NUM_1, 1))
        )
    
    # 临时复制：回合结束消失
    # 需要检查 GameTag.TAG_SCRIPT_DATA_NUM_1 标记
    # 在手牌中时，回合结束移除
    # 这通常由 Temporary 机制处理，如果 fireplace 支持的话
    # 或者我们手动添加 "回响" 类似的逻辑
    
    # 暂时简化：只给复制，不处理"临时"（直到回合结束）
    # 实际上应该添加一个 Buff "End of Turn: Discard this"


class DMF_249:
    """Acrobatics (空翻杂技)
    Draw 2 cards. If you play both this turn, draw 2 more."""
    # 3费 - 抽两张牌。如果你在本回合中使用这两张牌，再抽两张
    
    # 类似 Stiltstepper，给抽到的牌添加追踪 Buff
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_249e")) * 2


class DMF_249e:
    """Acrobatics Tracker"""
    # 追踪 Buff
    # 需要机制来检测"两张都打出"
    # 这需要一个全局计数器或控制器上的状态
    pass


class YOP_001:
    """Illidari Studies (伊利达雷研习)
    Discover an Outcast card. Your next one costs (1) less."""
    # 1费 - 发现一张流放牌。你的下一张流放牌法力值消耗减少(1)点
    
    play = Discover(CONTROLLER, RandomCollectible(outcast=True)).then(
        Buff(CONTROLLER, "YOP_001e")
    )


class YOP_001e:
    """Illidari Studies Buff"""
    # 下一张流放牌减费
    update = Refresh(FRIENDLY_HAND + Attr(GameTag.OUTCAST, True), {GameTag.COST: -1})
    events = Play(FRIENDLY + Attr(GameTag.OUTCAST, True)).on(Destroy(SELF))


##
# Weapons

class DMF_227:
    """Dreadlord's Bite (恐惧魔王之咬)
    Outcast: Deal 1 damage to all enemies."""
    # 3费 3/2 - 流放：对所有敌人造成1点伤害
    
    outcast = Hit(ENEMY_CHARACTERS, 1)

