"""
深暗领域 - 中立 - COMMON
"""
from ..utils import *


class GDB_101:
    """次元核心 - Dimensional Core
    Divine Shield Starship Piece

    2费 2/2 中立随从 - 星舰组件
    <b>圣盾</b>
    <b>星舰组件</b>
    """
    tags = {
        GameTag.DIVINE_SHIELD: True,
    }
    # 星舰组件标记会在卡牌数据中自动设置


class GDB_130:
    """水晶焊工 - Crystal Welder
    2费 2/3 中立随从
    <b>嘲讽</b>。<b>战吼：</b>如果你正在构筑<b>星舰</b>，获得+2/+2。
    
    Taunt. Battlecry: If you're building a Starship, gain +2/+2.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 检查是否正在构筑星舰
        if self.controller.starship_in_progress:
            # 获得+2/+2
            yield Buff(self, "GDB_130e")


class GDB_130e:
    """焊接强化 - Welded Enhancement"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class GDB_310:
    """虚灵神谕者 - Ethereal Oracle
    4费 2/3 中立随从
    <b>法术伤害+1</b>
    <b><b>法术迸发</b>：</b>抽两张法术牌。
    
    Spell Damage +1. Spellburst: Draw 2 spells.
    """
    tags = {
        GameTag.SPELLPOWER: True,
        GameTag.SPELLBURST: True,
    }
    spellpower = 1
    
    events = SpellBurst(CONTROLLER).on(
        ForceDraw(CONTROLLER, 2).filter(lambda card: card.type == CardType.SPELL)
    )


class GDB_311:
    """深空策展人 - Deep Space Curator
    3费 2/4 中立随从
    <b><b>法术迸发</b>：</b>随机获取一张法力值消耗与法术相同的随从牌，并将其法力值消耗变为（0）点。
    
    Spellburst: Get a random minion of the spell's Cost. Set its Cost to (0).
    """
    tags = {
        GameTag.SPELLBURST: True,
    }
    
    def spellburst_effect(self, source, spell):
        """法术迸发效果：获取法术费用的随从并设为0费"""
        # 获取与法术费用相同的随机随从
        cards = yield Give(CONTROLLER, RandomMinion(cost=spell.cost))
        if cards:
            # 将获得的随从费用设为0
            yield Buff(cards[0], "GDB_311e")
    
    events = SpellBurst(CONTROLLER).on(
        lambda self, source, spell: self.spellburst_effect(source, spell)
    )


class GDB_311e:
    """策展收藏 - Curated Collection"""
    tags = {
        GameTag.COST: SET(0),
    }


class GDB_320:
    """艾瑞达蛮兵 - Eredar Brute
    7费 5/6 中立随从 - 恶魔
    <b>嘲讽</b>。<b>吸血</b>
    每有一个敌方随从，本牌的法力值消耗便减少（1）点。
    
    Taunt. Lifesteal. Costs (1) less for each enemy minion.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
    }
    race = Race.DEMON
    
    cost_mod = lambda self, i: -Count(ENEMY_MINIONS)


class GDB_322:
    """光注魔刃豹 - Lightfused Manasaber
    6费 6/6 中立随从 - 野兽
    <b>突袭</b>。<b><b>法术迸发</b>：</b>获得<b>圣盾</b>。
    
    Rush. Spellburst: Gain Divine Shield.
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.SPELLBURST: True,
    }
    race = Race.BEAST
    
    events = SpellBurst(CONTROLLER).on(
        SetTags(SELF, {GameTag.DIVINE_SHIELD: True})
    )


class GDB_330:
    """乌祖尔暴怒者 - Ur'zul Rager
    3费 5/1 中立随从 - 恶魔
    <b>吸血</b>
    <b><b>法术迸发</b>：</b>随机攻击一个敌方随从。
    
    Lifesteal. Spellburst: Attack a random enemy minion.
    """
    tags = {
        GameTag.LIFESTEAL: True,
        GameTag.SPELLBURST: True,
    }
    race = Race.DEMON
    
    events = SpellBurst(CONTROLLER).on(
        Attack(SELF, RANDOM_ENEMY_MINION)
    )


class GDB_333:
    """太空海盗 - Space Pirate
    1费 2/1 中立随从 - 海盗
    <b>亡语：</b>你的下一张武器牌法力值消耗减少（1）点。
    
    Deathrattle: Your next weapon costs (1) less.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    race = Race.PIRATE
    
    deathrattle = Buff(FRIENDLY_HAND + WEAPON, "GDB_333e")


class GDB_333e:
    """海盗的战利品 - Pirate's Plunder"""
    tags = {
        GameTag.COST: -1,
    }
    one_turn_effect = True


class GDB_435:
    """月石重拳手 - Moonstone Mauler
    2费 2/2 中立随从 - 元素
    <b>战吼：</b>将3张小行星洗入你的牌库。当抽到小行星时会对一个随机敌人造成2点伤害。
    
    Battlecry: Shuffle 3 Asteroids into your deck that deal 2 damage to a random enemy when drawn.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.ELEMENTAL
    
    def play(self):
        # 将3张小行星洗入牌库
        for i in range(3):
            yield Shuffle(CONTROLLER, "GDB_435t")


class GDB_435t:
    """小行星 - Asteroid
    Cast When Drawn: 对一个随机敌人造成2点伤害
    
    Cast When Drawn: Deal 2 damage to a random enemy.
    """
    tags = {
        GameTag.TOPDECK: True,  # Cast When Drawn
    }
    
    def draw(self):
        # 对一个随机敌人造成2点伤害
        yield Hit(RANDOM_ENEMY_CHARACTER, 2)


class GDB_461:
    """星域戒卫 - Astral Vigilant
    1费 1/2 中立随从
    <b>战吼：</b>获取你使用的上一个德莱尼的一张复制。
    
    Battlecry: Get a copy of the last Draenei you played.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 获取上一个使用的德莱尼
        last_draenei = None
        for card in reversed(self.controller.cards_played_this_game):
            if card.race == Race.DRAENEI and card != self:
                last_draenei = card
                break
        
        if last_draenei:
            yield Give(CONTROLLER, last_draenei.id)


class GDB_463:
    """困窘的机械师 - Troubled Mechanic
    2费 2/1 中立随从 - 德莱尼
    <b>圣盾</b>。<b><b>法术迸发</b>：</b>抽一张德莱尼牌。
    
    Divine Shield. Spellburst: Draw a Draenei.
    """
    tags = {
        GameTag.DIVINE_SHIELD: True,
        GameTag.SPELLBURST: True,
    }
    race = Race.DRAENEI
    
    events = SpellBurst(CONTROLLER).on(
        ForceDraw(CONTROLLER).filter(lambda card: card.race == Race.DRAENEI)
    )


class GDB_720:
    """星光漫游者 - Starlight Wanderer
    1费 2/1 中立随从 - 德莱尼
    <b>战吼：</b>你使用的下一个德莱尼获得+2/+1。
    
    Battlecry: The next Draenei you play gains +2/+1.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DRAENEI
    
    play = Buff(CONTROLLER, "GDB_720e")


class GDB_720e:
    """星光祝福 - Starlight Blessing
    下一个德莱尼获得+2/+1
    
    Player enchantment: Next Draenei gains +2/+1
    """
    events = Play(CONTROLLER, MINION + DRAENEI).on(
        Buff(Play.CARD, "GDB_720e2"), Destroy(SELF)
    )


class GDB_720e2:
    """星光祝福 - Starlight Blessing"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }


class GDB_722:
    """红衣指挥官 - Crimson Commander
    3费 4/3 中立随从 - 德莱尼
    <b>战吼，亡语：</b>使你手牌中的所有德莱尼获得+1/+1。
    
    Battlecry and Deathrattle: Give all Draenei in your hand +1/+1.
    """
    tags = {
        GameTag.BATTLECRY: True,
        GameTag.DEATHRATTLE: True,
    }
    race = Race.DRAENEI
    
    play = Buff(FRIENDLY_HAND + DRAENEI, "GDB_722e")
    deathrattle = Buff(FRIENDLY_HAND + DRAENEI, "GDB_722e")


class GDB_722e:
    """指挥官的激励 - Commander's Inspiration"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class GDB_723:
    """影像操作师 - Hologram Operator
    2费 3/2 中立随从 - 德莱尼
    <b>战吼：</b>随机获取3张<b>临时</b>德莱尼牌。
    
    Battlecry: Get 3 random Temporary Draenei.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DRAENEI
    
    def play(self):
        # 获取3张随机临时德莱尼
        for i in range(3):
            # 直接给予随机德莱尼并标记为临时
            cards = yield Give(CONTROLLER, RandomCollectible(race=Race.DRAENEI))
            if cards:
                # 给予临时标记（GHOSTLY）
                yield Buff(cards[0], "GDB_723e")


class GDB_723e:
    """临时投影 - Temporary Projection"""
    tags = {
        GameTag.GHOSTLY: True,  # 临时标记
    }


class GDB_860:
    """辰鳞星圣 - Starscale Constellar
    5费 4/7 中立随从 - 龙
    <b><b>法术迸发</b>：</b>本随从的攻击力翻倍。
    
    Spellburst: Double this minion's Attack.
    """
    tags = {
        GameTag.SPELLBURST: True,
    }
    race = Race.DRAGON
    
    def spellburst_effect(self, source, spell):
        """法术迸发效果：攻击力翻倍"""
        # 获取当前攻击力并添加等量buff
        current_atk = self.atk
        yield Buff(SELF, "GDB_860e", atk=current_atk)
    
    events = SpellBurst(CONTROLLER).on(
        lambda self, source, spell: self.spellburst_effect(source, spell)
    )


class GDB_860e:
    """星辰之力 - Stellar Power
    攻击力翻倍
    
    Double Attack
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    # atk 会在 Buff 调用时动态设置


class GDB_861:
    """遇险的航天员 - Stranded Spaceman
    2费 2/3 中立随从 - 德莱尼
    <b>战吼：</b>你使用的下一个德莱尼会获得+2生命值和<b>突袭</b>。
    
    Battlecry: The next Draenei you play gains +2 Health and Rush.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DRAENEI
    
    play = Buff(CONTROLLER, "GDB_861e")


class GDB_861e:
    """航天员的祝福 - Spaceman's Blessing
    下一个德莱尼获得+2生命值和突袭
    
    Player enchantment: Next Draenei gains +2 Health and Rush
    """
    events = Play(CONTROLLER, MINION + DRAENEI).on(
        Buff(Play.CARD, "GDB_861e2"), Destroy(SELF)
    )


class GDB_861e2:
    """航天员的祝福 - Spaceman's Blessing"""
    tags = {
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
    }


class GDB_863:
    """月球开拓者 - Lunar Trailblazer
    5费 6/4 中立随从 - 德莱尼
    <b>战吼：</b>将你手牌中一张随机法术牌的法力值消耗变为本随从的法力值消耗。
    
    Battlecry: Set the Cost of a random spell in your hand to this minion's Cost.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DRAENEI
    
    def play(self):
        # 随机选择手牌中的一张法术牌
        spells = self.controller.hand.filter(type=CardType.SPELL)
        if spells:
            spell = random.choice(spells)
            # 将法术的费用设置为本随从的费用（5费）
            yield Buff(spell, "GDB_863e")


class GDB_863e:
    """开拓者的调整 - Trailblazer's Adjustment"""
    tags = {
        GameTag.COST: SET(5),
    }


class GDB_874:
    """太空生物学家 - Astrobiologist
    2费 2/2 中立随从 - 德莱尼
    <b>战吼：</b>在你的下个回合开始时，<b>发现</b>一张法术牌。
    
    Battlecry: At the start of your next turn, Discover a spell.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DRAENEI
    
    play = Buff(CONTROLLER, "GDB_874e")


class GDB_874e:
    """生物学研究 - Biological Research
    下回合开始时发现一张法术
    
    Player enchantment: Discover a spell at start of next turn
    """
    events = OWN_TURN_BEGIN.on(
        Discover(CONTROLLER, RandomSpell()),
        Destroy(SELF)
    )


class GDB_877:
    """逃生舱 - Escape Pod
    3费 2/1 中立随从
    <b>突袭</b>。<b>亡语：</b>
    使相邻的随从获得+1/+1和<b>突袭</b>。
    
    Rush. Deathrattle: Give adjacent minions +1/+1 and Rush.
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Buff(ADJACENT_MINIONS, "GDB_877e")


class GDB_877e:
    """逃生加速 - Escape Boost"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.RUSH: True,
    }


class GDB_878:
    """脑鳃鱼人 - Braingill
    3费 3/2 中立随从 - 鱼人
    <b>战吼：</b>使你的其他鱼人获得"<b>亡语：</b>
    抽一张牌。"
    
    Battlecry: Give your other Murlocs "Deathrattle: Draw a card."
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.MURLOC
    
    play = Buff(FRIENDLY_MINIONS + MURLOC - SELF, "GDB_878e")


class GDB_878e:
    """脑鳃的智慧 - Braingill's Wisdom
    亡语：抽一张牌
    
    Deathrattle: Draw a card
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Draw(CONTROLLER)


# 星际争霸联动卡牌

class SC_000:
    """孵化池 - Spawning Pool
    2费 地标 - 异虫
    获取一张1/1的跳虫。<b>亡语：</b>在本回合中，你的异虫随从拥有<b>突袭</b>。
    
    Get a 1/1 Zergling. Deathrattle: Your Zerg minions have Rush this turn.
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.DEATHRATTLE: True,
    }
    
    def activate(self):
        # 获取一张跳虫
        yield Give(CONTROLLER, "SC_000t")
    
    deathrattle = Buff(FRIENDLY_MINIONS + ZERG, "SC_000e")


class SC_000t:
    """跳虫 - Zergling
    1费 1/1 异虫随从
    
    1/1 Zerg minion
    """
    race = Race.ZERG


class SC_000e:
    """孵化池的祝福 - Spawning Pool's Blessing
    本回合获得突袭
    
    Rush this turn
    """
    tags = {
        GameTag.RUSH: True,
    }
    one_turn_effect = True


class SC_003:
    """巢群虫后 - Hive Queen
    5费 3/5 中立随从 - 异虫
    在你的回合结束时，获取一张幼虫，它会变形为随机异虫随从。
    
    At the end of your turn, get a Larva that transforms into random Zerg minions.
    """
    race = Race.ZERG
    
    events = OWN_TURN_END.on(
        Give(CONTROLLER, "SC_003t")
    )


class SC_003t:
    """幼虫 - Larva
    0费 法术
    变形为一个随机异虫随从。
    
    Transform into a random Zerg minion.
    """
    def play(self):
        # 随机获取一个异虫随从
        yield Give(CONTROLLER, RandomMinion(race=Race.ZERG))


class SC_015:
    """坑道虫 - Nydus Worm
    3费 法术 - 异虫
    抽两张异虫牌。这些牌的法力值消耗减少（1）点。
    
    Draw two Zerg cards. They cost (1) less.
    """
    def play(self):
        # 抽两张异虫牌
        cards = yield ForceDraw(CONTROLLER, 2).filter(lambda card: card.race == Race.ZERG)
        # 使这些牌的费用减少1点
        for card in cards:
            yield Buff(card, "SC_015e")


class SC_015e:
    """坑道虫的加速 - Nydus Worm's Boost"""
    tags = {
        GameTag.COST: -1,
    }


class SC_403:
    """星港 - Starport
    3费 地标 - 人类
    召唤一个2/1的星舰组件，其在发射时拥有效果。
    
    Summon a 2/1 Starship Piece with an effect when launched.
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
    }
    
    def activate(self):
        # 召唤一个2/1星舰组件
        yield Summon(CONTROLLER, "SC_403t")


class SC_403t:
    """人类星舰组件 - Terran Starship Piece
    2费 2/1 星舰组件
    <b>星舰组件</b>
    发射时：抽一张牌。
    
    Starship Piece. When launched: Draw a card.
    """
    tags = {
        GameTag.STARSHIP_PIECE: True,
    }
    
    def launch(self):
        # 发射时抽一张牌
        yield Draw(CONTROLLER)


class SC_408:
    """幽灵 - Ghost
    3费 3/3 中立随从 - 人类
    <b>潜行</b>。<b>战吼：</b>如果你正在构筑<b>星舰</b>，消灭你对手手牌中法力值消耗最低的牌。
    
    Stealth. Battlecry: If you're building a Starship, destroy the lowest-Cost card in your opponent's hand.
    """
    tags = {
        GameTag.STEALTH: True,
        GameTag.BATTLECRY: True,
    }
    race = Race.TERRAN
    
    def play(self):
        # 检查是否正在构筑星舰
        if self.controller.starship_in_progress:
            # 找到对手手牌中费用最低的牌
            enemy_hand = list(self.controller.opponent.hand)
            if enemy_hand:
                lowest_cost_card = min(enemy_hand, key=lambda c: c.cost)
                yield Destroy(lowest_cost_card)


class SC_410:
    """升空 - Lift Off
    2费 法术 - 人类
    抽两张人类牌。召唤一个2/1的星舰组件，其在发射时拥有效果。
    
    Draw 2 Terran cards. Summon a 2/1 Starship Piece with an effect when launched.
    """
    def play(self):
        # 抽两张人类牌
        yield ForceDraw(CONTROLLER, 2).filter(lambda card: card.race == Race.TERRAN)
        # 召唤一个2/1星舰组件
        yield Summon(CONTROLLER, "SC_403t")


class SC_750:
    """时空提速 - Chrono Boost
    3费 法术 - 神族
    抽两张神族牌。召唤一个3/4并具有<b>冲锋</b>的狂热者。
    
    Draw 2 Protoss cards. Summon a 3/4 Zealot with Charge.
    """
    def play(self):
        # 抽两张神族牌
        yield ForceDraw(CONTROLLER, 2).filter(lambda card: card.race == Race.PROTOSS)
        # 召唤一个3/4狂热者
        yield Summon(CONTROLLER, "SC_750t")


class SC_750t:
    """狂热者 - Zealot
    3费 3/4 神族随从
    <b>冲锋</b>
    
    3/4 Protoss minion with Charge
    """
    tags = {
        GameTag.CHARGE: True,
    }
    race = Race.PROTOSS


class SC_751:
    """折跃门 - Warp Gate
    1费 法术 - 神族
    你的下一张神族随从牌法力值消耗减少（3）点。
    
    Your next Protoss minion costs (3) less.
    """
    def play(self):
        # 给予玩家一个buff，下一张神族随从减少3费
        yield Buff(CONTROLLER, "SC_751e")


class SC_751e:
    """折跃门能量 - Warp Gate Energy
    下一张神族随从减少3费
    
    Player enchantment: Next Protoss minion costs (3) less
    """
    events = Play(CONTROLLER, MINION + PROTOSS).on(
        Buff(Play.CARD, "SC_751e2"), Destroy(SELF)
    )


class SC_751e2:
    """折跃门能量 - Warp Gate Energy"""
    tags = {
        GameTag.COST: -3,
    }


class SC_753:
    """光子炮台 - Photon Cannon
    2费 法术 - 神族
    造成$3点伤害。如果这消灭了一个随从，你的神族随从在本局对战中法力值消耗减少（1）点。
    
    Deal $3 damage. If this kills a minion, your Protoss minions cost (1) less this game.
    """
    def play(self, target):
        # 造成3点伤害
        yield Hit(target, 3)
        
        # 检查目标是否是随从且被消灭
        if target.type == CardType.MINION and target.to_be_destroyed:
            # 给予玩家一个永久buff，神族随从减少1费
            yield Buff(CONTROLLER, "SC_753e")


class SC_753e:
    """光子炮台能量 - Photon Cannon Energy
    神族随从减少1费
    
    Player enchantment: Protoss minions cost (1) less
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    class Hand:
        """手牌光环效果"""
        def cost(self, i):
            # 检查是否是神族随从
            if (self.owner.type == CardType.MINION and 
                hasattr(self.owner, 'race') and 
                self.owner.race == Race.PROTOSS):
                return i - 1
            return None


class SC_753e2:
    """光子炮台能量 - Photon Cannon Energy"""
    tags = {
        GameTag.COST: -1,
    }
