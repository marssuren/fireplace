"""
深暗领域 - Token 卡牌
"""
from ..utils import *

# Death Knight Tokens

class SC_001t:
    """爆虫 - Baneling
    1/1 异虫随从
    <b>亡语：</b>对所有敌方随从造成2点伤害。
    
    1/1 Zerg minion
    Deathrattle: Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.DEATHRATTLE]
    race = Race.ZERG
    
    def deathrattle(self):
        # 对所有敌方随从造成2点伤害
        enemy_minions = self.game.board.filter(ENEMY_MINIONS)
        for minion in enemy_minions:
            yield Hit(minion, 2)


class GDB_113t:
    """亡灵 - Undead
    5/5 亡灵随从，嘲讽
    
    5/5 Undead with Taunt
    """
    tags = {GameTag.TAUNT: True}
    race = Race.UNDEAD


# Demon Hunter Tokens

class GDB_118t1:
    """阿古斯 - Argus (Star of Origination)
    1费 法术
    星球牌 - 左侧星球
    当本牌与另一颗星球相撞时，对所有敌人造成5点伤害。
    
    When this collides with another Star, deal 5 damage to all enemies.
    
    机制说明：
    - 当任何牌被打出或手牌位置变化时，检查两颗星球是否相邻
    - 如果两颗星球相邻（中间没有其他牌），触发碰撞
    - 碰撞时对所有敌人造成5点伤害，并移除两颗星球
    """
    # 监听任何牌被打出，检测是否导致星球碰撞
    events = Play(CONTROLLER).after(
        lambda self, source, card: CheckAndTriggerStarCollision(self.controller)
    )
    
    def play(self):
        # 打出星球牌时也检测碰撞
        yield CheckAndTriggerStarCollision(self.controller)


class GDB_118t2:
    """克罗库恩 - Krokuun (Star of Conclusion)
    1费 法术
    星球牌 - 右侧星球
    当本牌与另一颗星球相撞时，对所有敌人造成5点伤害。
    
    When this collides with another Star, deal 5 damage to all enemies.
    """
    # 监听任何牌被打出，检测是否导致星球碰撞
    events = Play(CONTROLLER).after(
        lambda self, source, card: CheckAndTriggerStarCollision(self.controller)
    )
    
    def play(self):
        # 打出星球牌时也检测碰撞
        yield CheckAndTriggerStarCollision(self.controller)


def CheckAndTriggerStarCollision(player):
    """检测并触发星球碰撞
    
    检查手牌中是否有两颗星球相邻：
    - 遍历手牌，找到所有星球牌
    - 检查它们的位置是否相邻
    - 如果相邻，触发碰撞效果
    """
    def action(self):
        hand = list(player.hand)
        
        # 找到所有星球牌及其位置
        stars = []
        for card in hand:
            if card.id in ("GDB_118t1", "GDB_118t2"):
                stars.append(card)
        
        # 如果有两颗星球
        if len(stars) >= 2:
            # 按位置排序
            stars.sort(key=lambda c: c.zone_position)
            
            # 检查是否相邻（位置差为1）
            for i in range(len(stars) - 1):
                star1 = stars[i]
                star2 = stars[i + 1]
                
                # 检查两颗星球是否直接相邻（中间没有其他牌）
                if star2.zone_position - star1.zone_position == 1:
                    # 星球碰撞！
                    # 对所有敌人造成5点伤害
                    yield Hit(ENEMY_CHARACTERS, 5)
                    
                    # 移除两颗星球（从手牌中移除）
                    yield Discard(star1)
                    yield Discard(star2)
                    
                    # 只触发一次碰撞
                    return
    
    return action



class GDB_117t:
    """乘务员 - Crewmate (基础版本)
    4费 4/4 德莱尼随从
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t1:
    """乘务员 - Engine Crewmate
    4费 4/4 德莱尼随从
    <b>圣盾</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Divine Shield. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.DIVINE_SHIELD: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t2:
    """乘务员 - Tactical Crewmate
    4费 4/4 德莱尼随从
    <b>风怒</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Windfury. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.WINDFURY: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t3:
    """乘务员 - Gunner Crewmate
    4费 4/4 德莱尼随从
    <b>突袭</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Rush. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.RUSH: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t4:
    """乘务员 - Medic Crewmate
    4费 4/4 德莱尼随从
    <b>嘲讽</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Taunt. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.TAUNT: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t5:
    """乘务员 - Scout Crewmate
    4费 4/4 德莱尼随从
    <b>扰魔</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Elusive. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.ELUSIVE: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t6:
    """乘务员 - Admin Crewmate
    4费 4/4 德莱尼随从
    <b>复生</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Reborn. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.REBORN: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_117t7:
    """乘务员 - Security Crewmate
    4费 4/4 德莱尼随从
    <b>吸血</b>
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Lifesteal. Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    tags = {GameTag.LIFESTEAL: True}
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


class GDB_119t:
    """乘务员 - Crewmate (4/4 version from Emergency Meeting)
    4费 4/4 德莱尼随从
    <b>战吼：</b>召唤你手牌中与本随从相邻的所有乘务员。
    
    Battlecry: Summon every adjoining Crewmate in your hand.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DRAENEI
    
    def play(self):
        yield from SummonAdjoiningCrewmates(self)


def SummonAdjoiningCrewmates(crewmate):
    """召唤手牌中与本乘务员相邻的所有乘务员
    
    这是乘务员的核心机制：
    - 当打出一个乘务员时，会召唤所有与它相邻的乘务员
    - "相邻"指的是在手牌中位置连续，中间没有非乘务员卡牌
    - 如果多个乘务员连在一起，打出任意一个会召唤整个链条
    """
    # 获取手牌
    hand = list(crewmate.controller.hand)
    
    # 找到本乘务员在手牌中的位置（打出前的位置）
    # 注意：此时乘务员已经被打出，不在手牌中了
    # 我们需要从 cards_played_this_turn_with_position 中获取位置信息
    crewmate_position = None
    for card, position in crewmate.controller.cards_played_this_turn_with_position:
        if card == crewmate:
            crewmate_position = position
            break
    
    if crewmate_position is None:
        return
    
    # 收集所有相邻的乘务员
    crewmates_to_summon = []
    
    # 向左查找相邻乘务员
    for pos in range(crewmate_position - 1, -1, -1):
        # 找到该位置的牌
        card_at_pos = None
        for card in hand:
            if card.zone_position == pos:
                card_at_pos = card
                break
        
        if card_at_pos and IsCrewmate(card_at_pos):
            crewmates_to_summon.insert(0, card_at_pos)
        else:
            break  # 遇到非乘务员，停止查找
    
    # 向右查找相邻乘务员
    for pos in range(crewmate_position + 1, 10):  # 手牌最多10张
        card_at_pos = None
        for card in hand:
            if card.zone_position == pos:
                card_at_pos = card
                break
        
        if card_at_pos and IsCrewmate(card_at_pos):
            crewmates_to_summon.append(card_at_pos)
        else:
            break  # 遇到非乘务员，停止查找
    
    # 召唤所有相邻的乘务员
    for crew in crewmates_to_summon:
        yield Summon(crewmate.controller, crew)


def IsCrewmate(card):
    """判断一张牌是否是乘务员"""
    return card.id.startswith("GDB_117t") or card.id == "GDB_119t"


# Hunter Tokens

class GDB_840t:
    """异星野兽 - Alien Beast
    3/5 野兽
    战吼：攻击生命值最低的敌人
    
    3/5 Beast
    Battlecry: Attack the lowest Health enemy
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.BATTLECRY: True,
    }
    race = Race.BEAST
    
    def play(self):
        # 找到生命值最低的敌人
        enemies = list(self.game.board.filter(ENEMY_CHARACTERS))
        if enemies:
            # 按生命值排序，选择最低的
            lowest_health_enemy = min(enemies, key=lambda e: e.health)
            # 攻击该敌人
            yield Attack(SELF, lowest_health_enemy)


class GDB_237t:
    """异星野兽 - Alien Beast
    2/4 野兽，嘲讽
    
    2/4 Beast with Taunt
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.TAUNT: True,
    }
    race = Race.BEAST


class GDB_846t:
    """追踪 - Tracking
    1费 英雄技能
    从你的牌库中<b>发现</b>一张牌。
    
    1 Mana Hero Power
    Discover a card from your deck.
    """
    tags = {
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.HERO_POWER,
    }
    
    def use(self, target=None):
        # 从牌库中发现一张牌
        # 参考 TOY_851 (无底玩具箱) 的实现
        # 使用 GenericChoice 从牌库中选择，然后给予副本
        cards = yield GenericChoice(CONTROLLER, FRIENDLY_DECK)
        if cards:
            discovered_card = cards[0]
            # 将发现的牌的副本加入手牌（原牌留在牌库中）
            yield Give(CONTROLLER, discovered_card.id)


def SetZone(card, zone):
    """设置卡牌区域的辅助函数（已废弃，保留以防其他地方使用）"""
    def action(source):
        if card:
            card.zone = zone
    return action


# Druid Tokens

class SC_756t:
    """拦截机 - Interceptor
    4/1 机械随从
    在召唤时攻击随机敌人
    
    4/1 Mechanical minion
    Attacks a random enemy when summoned
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 1,
    }
    race = Race.MECHANICAL
    
    # 召唤时攻击随机敌人
    events = Summon(SELF).after(
        Attack(SELF, RANDOM_ENEMY_CHARACTER)
    )


# Warlock Tokens

class GDB_124t:
    """恶魔 - Demon
    6/6 恶魔，嘲讽
    
    6/6 Demon with Taunt
    """
    tags = {GameTag.TAUNT: True}
    race = Race.DEMON


# Mage Tokens

# Neutral Tokens

# Neutral Tokens

class GDB_120t1:
    """攻击指令 - Attack Protocol
    1费 法术
    使你的星舰获得+3攻击力。
    
    Give your Starship +3 Attack.
    """
    tags = {
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    def play(self, target=None):
        # 找到玩家的星舰
        starship = None
        for minion in self.controller.field:
            if hasattr(minion, 'is_starship') and minion.is_starship:
                starship = minion
                break
        
        if starship:
            yield Buff(starship, "GDB_120t1e")


class GDB_120t1e:
    """攻击指令 - Attack Protocol Buff
    +3攻击力
    """
    tags = {
        GameTag.ATK: 3,
    }


class GDB_120t2:
    """防御指令 - Defense Protocol
    1费 法术
    使你的星舰获得+3生命值。
    
    Give your Starship +3 Health.
    """
    tags = {
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    def play(self, target=None):
        # 找到玩家的星舰
        starship = None
        for minion in self.controller.field:
            if hasattr(minion, 'is_starship') and minion.is_starship:
                starship = minion
                break
        
        if starship:
            yield Buff(starship, "GDB_120t2e")


class GDB_120t2e:
    """防御指令 - Defense Protocol Buff
    +3生命值
    """
    tags = {
        GameTag.HEALTH: 3,
    }


class GDB_120t3:
    """速度指令 - Speed Protocol
    1费 法术
    使你的星舰获得<b>突袭</b>。
    
    Give your Starship Rush.
    """
    tags = {
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    def play(self, target=None):
        # 找到玩家的星舰
        starship = None
        for minion in self.controller.field:
            if hasattr(minion, 'is_starship') and minion.is_starship:
                starship = minion
                break
        
        if starship:
            yield Buff(starship, "GDB_120t3e")


class GDB_120t3e:
    """速度指令 - Speed Protocol Buff
    突袭
    """
    tags = {
        GameTag.RUSH: True,
    }


class SC_004t:
    """虫群女王 - Hive Queen
    2/5 异虫随从
    
    2/5 Zerg minion
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
    }
    race = Race.ZERG


class SC_754t:
    """狂热者 - Zealot
    3/4 神族随从
    <b>冲锋</b>
    
    3/4 Protoss minion with Charge
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.CHARGE: True,
    }
    race = Race.PROTOSS


# Rogue Tokens

class SC_752t:
    """执政官 - Archon
    8费 8/8 潜行者随从
    在你的回合结束时，对敌方英雄造成8点伤害，对其随从造成2点伤害。
    
    8/8 Rogue minion
    At the end of your turn, deal 8 damage to the enemy hero and 2 damage to their minions.
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 8,
        GameTag.CARDTYPE: CardType.MINION,
    }
    
    # 在回合结束时，对敌方英雄造成8点伤害，对其随从造成2点伤害
    events = OwnTurnEnd(CONTROLLER).on(
        Hit(ENEMY_HERO, 8),
        Hit(ENEMY_MINIONS, 2)
    )


# Paladin Tokens

class SC_404t:
    """陆战队员 - Marine
    2/2 人类随从
    <b>嘲讽</b>
    
    2/2 Terran minion with Taunt
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.TAUNT: True,
    }
    race = Race.TERRAN


class GDB_139t:
    """信仰德莱尼 - Draenei of Faith
    3/3 德莱尼随从
    <b>圣盾</b>
    
    3/3 Draenei with Divine Shield
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.DIVINE_SHIELD: True,
    }
    race = Race.DRAENEI


class SC_412t:
    """强化恶火 - Hellion (Upgraded)
    4费 4/4 圣骑士随从 - 机械
    你的其他随从获得+2攻击力。
    
    Your other minions have +2 Attack.
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.CARDTYPE: CardType.MINION,
    }
    race = Race.MECHANICAL
    
    # 光环：其他随从+2攻击力（升级版）
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: 2})


# Shaman Tokens

class GDB_901t:
    """小行星 - Asteroid
    1费 法术
    抽到时施放：对一个随机敌人造成2点伤害。

    Cast When Drawn: Deal 2 damage to a random enemy.

    机制说明：
    - 这是由极紫外破坏者、陨石风暴等卡牌生成的Token
    - 抽到时自动施放，对随机敌人造成伤害
    - 如果玩家有流彩巨岩的buff，伤害会增加1点
    """
    tags = {
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.TOPDECK: True,  # Cast When Drawn
    }

    def draw(self):
        # 基础伤害为2点
        damage = 2

        # 检查玩家是否有流彩巨岩的buff（GDB_434e）
        for buff in self.controller.buffs:
            if buff.id == "GDB_434e":
                damage += 1
                break

        # 对一个随机敌人造成伤害
        yield Hit(RANDOM_ENEMY_CHARACTER, damage)


class GDB_447t:
    """星系投影 - Galaxy's Lens
    2费 地标 - 耐久度2
    吸收你施放的下一个法术的能量。使用：释放吸收的法术。

    Absorbs the power of the next spell you cast.
    Use: Release the absorbed spell.

    机制说明：
    - 这是由预言者努波顿的亡语生成的地标
    - 监听玩家施放法术，吸收第一个法术的ID和目标信息
    - 使用地标时，创建法术副本并施放（重复法术效果）
    - 参考 paradise/hunter.py VAC_415 的实现模式
    """
    tags = {
        GameTag.COST: 2,
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.HEALTH: 2,  # 耐久度
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.absorbed_spell_id = None
        self.absorbed_spell_target = None

    # 监听玩家施放法术，吸收第一个法术
    events = Play(CONTROLLER, SPELL).after(
        lambda self, source, card: [
            setattr(self, 'absorbed_spell_id', card.id),
            setattr(self, 'absorbed_spell_target', card.target if hasattr(card, 'target') else None)
        ] if not self.absorbed_spell_id else None
    )

    def use(self, target=None):
        """使用地标：释放吸收的法术

        创建吸收的法术副本并施放，重复其效果
        """
        if self.absorbed_spell_id:
            # 创建法术副本
            spell_copy = self.controller.card(self.absorbed_spell_id, self.controller)

            # 施放法术副本
            if self.absorbed_spell_target and self.absorbed_spell_target.zone == Zone.PLAY:
                # 如果原法术有目标且目标仍在场，使用相同目标
                yield Play(CONTROLLER, spell_copy, target=self.absorbed_spell_target)
            elif hasattr(spell_copy, 'requirements') and spell_copy.requirements:
                # 如果法术需要目标但原目标不可用，尝试随机选择合适目标
                # 这里简化处理：如果需要目标则不施放（实际游戏中可能需要玩家选择）
                # 为了完整性，我们尝试找一个合适的目标
                yield Play(CONTROLLER, spell_copy)
            else:
                # 不需要目标的法术
                yield Play(CONTROLLER, spell_copy)

            # 清除吸收的法术信息
            self.absorbed_spell_id = None
            self.absorbed_spell_target = None


class SC_413t:
    """攻城坦克（攻城模式）- Siege Tank (Siege Mode)
    5费 5/5 萨满随从 - 机械
    战吼：对所有敌方随从造成10点伤害。

    Battlecry: Deal 10 damage to all enemy minions.

    机制说明：
    - 这是攻城坦克在发射过星舰后的强化版本
    - 从对单体造成10点伤害升级为对所有敌方随从造成10点伤害
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.BATTLECRY: True,
    }
    race = Race.MECHANICAL

    def play(self):
        # 对所有敌方随从造成10点伤害
        yield Hit(ENEMY_MINIONS, 10)


# Warlock Tokens

class SC_019t:
    """雷兽 - Ultralisk
    8/8 野兽随从，突袭

    8/8 Beast with Rush
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.RUSH: True,
    }
    race = Race.BEAST


class GDB_124t:
    """恶兆恶魔 - Bad Omen Demon
    6/6 恶魔随从，嘲讽

    6/6 Demon with Taunt
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6,
        GameTag.TAUNT: True,
    }
    race = Race.DEMON


# Warlock Buff Effects

class GDB_121e:
    """����а��Ч�� - Foreboding Flame Effect
    ������֮��Ķ�ħ�ķ���ֵ���ļ��٣�1���㡣

    Demons that didn't start in your deck cost (1) less.
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    class Hand:
        """�������ħ���ѹ⻷"""
        def apply(self, target):
            # ����Ƿ��Ƕ�ħ���Ҳ�����ʼ�����е���
            if hasattr(target, 'race') and target.race == Race.DEMON:
                # ����Ƿ������������
                if not getattr(target, 'started_in_deck', True):
                    target.cost -= 1

    update = Hand()


class GDB_122e:
    """����аı���� - Infernal Stratagem Buff
    +3/+3
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class GDB_122e2:
    """����аı����Ч�� - Infernal Stratagem Cost Reduction
    �����һ�Ŷ�ħ�Ʒ���ֵ���ļ��٣�2���㡣

    Your next Demon costs (2) less.
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    class Hand:
        """��һ�Ŷ�ħ���ѹ⻷"""
        def apply(self, target):
            # ����Ƿ��Ƕ�ħ��
            if hasattr(target, 'race') and target.race == Race.DEMON:
                target.cost -= 2

    update = Hand()

    # ʹ��һ�κ��Ƴ�
    events = Play(CONTROLLER, DEMON).after(Destroy(SELF))


class GDB_123e:
    """Abduction Ray Cost Reduction
    Cost reduced by (2).
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -2,
    }


class GDB_124e:
    """Bad Omen Delayed Summon Effect
    In 2 turns, summon two 6/6 Demons with Taunt.
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turns_remaining = 2
    
    # Monitor turn start to count down
    events = Turn(CONTROLLER).on(
        lambda self, source: self._countdown()
    )
    
    def _countdown(self):
        """Count down turns and summon when ready"""
        self.turns_remaining -= 1
        
        if self.turns_remaining <= 0:
            # Summon two 6/6 Demons with Taunt
            yield Summon(CONTROLLER, "GDB_124t") * 2
            # Remove this buff
            yield Destroy(SELF)


class GDB_123t:
    """Abduction Ray (Repeatable Token)
    Get a random Demon. Reduce its Cost by (2). Repeatable this turn.
    
    This token is destroyed at end of turn.
    """
    requirements = {}
    
    def play(self):
        # Get a random Demon
        yield RandomCard(CONTROLLER, race=Race.DEMON)
        # Reduce cost by 2
        yield Buff(Find(CONTROLLER_HAND + FRIENDLY + LAST_CARD_PLAYED), "GDB_123e")
        # Generate another token for repeating
        yield Give(CONTROLLER, "GDB_123t")
    
    # Destroy at end of turn
    events = OWN_TURN_END.on(Destroy(SELF))

# Warrior Tokens

class GDB_234t:
    """复制孢子 - Replicating Spore
    Summon a random 5-Cost minion. Your future Replicating Spores summon it as well.
    
    5费 战士法术
    召唤一个随机的法力值消耗为（5）点的随从。你之后的复制孢子也会召唤该随从。
    
    机制说明：
    - 第一次使用时，随机选择一个5费随从并召唤
    - 将选择的随从ID存储到玩家属性中
    - 之后的复制孢子会召唤相同的随从
    """
    requirements = {}
    
    def play(self):
        # 检查玩家是否已经选择了复制孢子的随从
        if not hasattr(self.controller, 'replicating_spore_minion'):
            # 第一次使用，随机选择一个5费随从
            minion_id = yield RandomMinion(cost=5)
            # 存储选择的随从ID
            self.controller.replicating_spore_minion = minion_id
            # 召唤该随从
            yield Summon(CONTROLLER, minion_id)
        else:
            # 之后的使用，召唤相同的随从
            yield Summon(CONTROLLER, self.controller.replicating_spore_minion)


class SC_414t:
    """雷神，爆炸载荷 - Thor, Explosive Payload
    Battlecry: Deal 5 damage. Repeat at a random enemy for each Starship you've launched this game.
    
    8费 8/8 战士随从 - 机械
    <b>战吼：</b>造成5点伤害。你在本局对战中每发射过一次<b>星舰</b>，便对一个随机敌人重复一次。
    """
    race = Race.MECHANICAL
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    
    def play(self):
        # 第一次造成5点伤害（如果有目标）
        if TARGET:
            yield Hit(TARGET, 5)
        
        # 对每个发射过的星舰，对随机敌人造成5点伤害
        starships_launched = self.controller.starships_launched_this_game
        for _ in range(starships_launched):
            # 找到随机敌方目标
            enemies = self.controller.opponent.field + [self.controller.opponent.hero]
            if enemies:
                import random
                target = random.choice(enemies)
                yield Hit(target, 5)
