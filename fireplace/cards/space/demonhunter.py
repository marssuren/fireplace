"""
深暗领域 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class GDB_105:
    """破片炮塔 - Shattershard Turret
    3费 2/4 恶魔猎手随从 - 星舰组件
    <b>突袭</b>，<b>风怒</b>
    <b>星舰组件</b>
    
    Rush, Windfury. Starship Piece
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.WINDFURY: True,
    }


class GDB_471:
    """沃罗尼招募官 - Voronei Recruiter
    2费 2/3 恶魔猎手随从 - 德莱尼
    在你的回合结束时，获取一个具有随机奖励效果的4/4乘务员。
    
    At the end of your turn, get a 4/4 Crewmate with a random Bonus Effect.
    """
    race = Race.DRAENEI
    
    # 回合结束时获取一个随机乘务员
    events = OWN_TURN_END.on(lambda self, player: Give(CONTROLLER, RandomCrewmate()))


class GDB_902:
    """潜入 - Infiltrate
    3费 法术
    选择一个随从，对所有其他随从造成3点伤害。
    
    Choose a minion. Deal 3 damage to all other minions.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 对所有其他随从（不包括目标）造成3点伤害
        target_minion = TARGET.entity
        all_other_minions = [m for m in self.game.board if m != target_minion]
        
        for minion in all_other_minions:
            yield Hit(minion, 3)


class SC_011:
    """菌毯肿瘤 - Creep Tumor
    2费 地标
    你的异虫随从拥有+1攻击力和<b>突袭</b>。持续3回合。
    
    Your Zerg minions have +1 Attack and Rush. Lasts 3 turns.
    """
    # 地标类型
    tags = {GameTag.CARDTYPE: CardType.LOCATION}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 持续3回合
        self.turns_remaining = 3
    
    # 异虫随从获得+1攻击力和突袭的光环效果
    update = Refresh(FRIENDLY_MINIONS + ZERG)
    
    class Hand:
        def atk(self, i):
            if self.owner.race == Race.ZERG:
                return i + 1
            return i
        
        def tags(self, tags):
            if self.owner.race == Race.ZERG:
                tags[GameTag.RUSH] = True
            return tags
    
    class Deck:
        def atk(self, i):
            if self.owner.race == Race.ZERG:
                return i + 1
            return i
        
        def tags(self, tags):
            if self.owner.race == Race.ZERG:
                tags[GameTag.RUSH] = True
            return tags
    
    class Board:
        def atk(self, i):
            if self.owner.race == Race.ZERG:
                return i + 1
            return i
        
        def tags(self, tags):
            if self.owner.race == Race.ZERG:
                tags[GameTag.RUSH] = True
            return tags
    
    # 回合开始时倒计时
    events = OWN_TURN_BEGIN.on(
        lambda self, player: [
            setattr(self, 'turns_remaining', getattr(self, 'turns_remaining', 3) - 1),
            Destroy(self) if getattr(self, 'turns_remaining', 0) <= 0 else None
        ][-1]
    )



# RARE

class GDB_110:
    """邪能动力源 - Felfused Battery
    2费 2/3 恶魔猎手随从 - 星舰组件
    在本随从攻击后，使你的其他随从获得+1攻击力。
    <b>星舰组件</b>
    
    After this attacks, give your other minions +1 Attack. Starship Piece
    """
    # 在本随从攻击后，使你的其他随从获得+1攻击力
    events = Attack(SELF).after(Buff(FRIENDLY_MINIONS - SELF, "GDB_110e"))


class GDB_473:
    """猎头 - Headhunt
    1费 法术
    造成2点伤害。获取一个具有随机奖励效果的4/4乘务员。
    
    Deal 2 damage. Get a 4/4 Crewmate with a random Bonus Effect.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)
        
        # 获取一个随机乘务员
        yield Give(CONTROLLER, RandomCrewmate())


class GDB_474:
    """折跃驱动器 - Warp Drive
    3费 法术 - 邪能
    抽两张牌。如果你正在构筑<b>星舰</b>，使抽到的牌的法力值消耗减少（2）点。
    
    Draw 2 cards. If you're building a Starship, they cost (2) less.
    """
    def play(self):
        # 抽两张牌
        drawn_cards = []
        for _ in range(2):
            card = yield Draw(CONTROLLER)
            if card:
                drawn_cards.extend(card)
        
        # 如果正在构筑星舰，使抽到的牌减费(2)
        if self.controller.starship_in_progress:
            for card in drawn_cards:
                yield Buff(card, "GDB_474e")


class GDB_474e:
    """折跃驱动器 - 减费 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.COST: -2}


class SC_009:
    """潜伏者 - Lurker
    4费 2/6 恶魔猎手随从 - 异虫
    在一个友方随从攻击后，随机对一个敌人造成1点伤害<i>（如果你的随从是异虫，则改为造成2点伤害）</i>。
    
    After a friendly minion attacks, deal 1 damage to a random enemy (or 2 if your minion is a Zerg).
    """
    race = Race.ZERG
    
    # 友方随从攻击后触发
    events = Attack(FRIENDLY_MINION).after(
        lambda self, attacker, defender: (
            # 判断攻击者是否是异虫
            Hit(RANDOM_ENEMY_CHARACTER, 2 if attacker.race == Race.ZERG else 1)
        )
    )


class SC_022:
    """异龙 - Mutalisk
    4费 5/2 恶魔猎手随从 - 异虫
    同时对本随从攻击的目标相邻的随从造成伤害<i>（如果相邻位置缺失，则改为对敌方英雄造成伤害）</i>。
    
    Also damages minions next to whomever this attacks (and the enemy hero if a neighbor is missing).
    """
    race = Race.ZERG
    
    # 攻击后触发额外伤害
    events = Attack(SELF).after(
        lambda self, source, defender: (
            # 获取被攻击目标的相邻随从
            MutaliskSplashDamage(self, defender)
        )
    )


def MutaliskSplashDamage(mutalisk, defender):
    """异龙的溅射伤害逻辑"""
    # 如果攻击的是随从
    if defender.type == CardType.MINION and defender.zone == Zone.PLAY:
        # 获取相邻随从
        adjacent = list(defender.adjacent_minions)
        
        # 如果有相邻随从，对它们造成伤害
        if adjacent:
            for minion in adjacent:
                yield Hit(minion, mutalisk.atk)
        else:
            # 如果没有相邻随从，对敌方英雄造成伤害
            yield Hit(defender.controller.hero, mutalisk.atk)
    # 如果攻击的是英雄，不触发额外效果


# EPIC

class GDB_116:
    """怪异奇物 - Eldritch Being
    1费 1/3 恶魔猎手随从
    <b>流放，<b>法术迸发</b>：</b>洗混你的手牌。
    
    Outcast and Spellburst: Shuffle your hand.
    
    官方机制说明：
    - 必须同时满足两个条件才能触发效果
    - 1. 必须以流放方式打出（从手牌最左或最右位置）
    - 2. 打出后在场上时施放法术触发法术迸发
    - 如果不是流放打出，即使触发法术迸发也不会洗混手牌
    """
    # 流放效果：设置标记表示以流放方式打出
    def outcast(self):
        # 设置标记，表示这个随从是以流放方式打出的
        # 使用buff来持久化这个状态
        yield Buff(SELF, "GDB_116_outcast_marker")
    
    # 法术迸发：仅当有流放标记时才洗混手牌
    events = Spellburst(CONTROLLER, 
        lambda self, player, played_card, target=None: (
            ShuffleHandAction() if any(buff.id == "GDB_116_outcast_marker" for buff in self.buffs) else None
        )
    )


class GDB_116_outcast_marker:
    """怪异奇物 - 流放标记
    用于标记这个随从是以流放方式打出的
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


def ShuffleHandAction():
    """洗混手牌的动作"""
    def action(self):
        hand_cards = list(self.controller.hand)
        if hand_cards:
            self.game.random.shuffle(hand_cards)
            for i, card in enumerate(hand_cards):
                card.zone_position = i
    return action




class GDB_119:
    """紧急会议 - Emergency Meeting
    2费 法术
    获取两张4/4的乘务员。将一张法力值消耗小于或等于（3）点的随机恶魔牌置于两者之间。
    
    Get two 4/4 Crewmates. Put a random Demon that costs (3) or less between them.
    """
    def play(self):
        # 获取第一个乘务员
        crewmate1 = yield Give(CONTROLLER, RandomCrewmate())
        
        # 获取一个3费以下的随机恶魔
        demon = yield Give(CONTROLLER, RandomCollectible(race=Race.DEMON, cost_max=3))
        
        # 获取第二个乘务员
        crewmate2 = yield Give(CONTROLLER, RandomCrewmate())
        
        # 调整手牌位置，确保恶魔在两个乘务员之间
        if crewmate1 and demon and crewmate2:
            # 获取手牌列表
            hand = list(self.controller.hand)
            
            # 找到三张牌的位置
            c1_pos = hand.index(crewmate1[0]) if crewmate1[0] in hand else -1
            d_pos = hand.index(demon[0]) if demon[0] in hand else -1
            c2_pos = hand.index(crewmate2[0]) if crewmate2[0] in hand else -1
            
            # 如果都在手牌中，重新排列
            if c1_pos != -1 and d_pos != -1 and c2_pos != -1:
                # 移除这三张牌
                hand.remove(crewmate1[0])
                hand.remove(demon[0])
                hand.remove(crewmate2[0])
                
                # 按照乘务员-恶魔-乘务员的顺序插入到手牌末尾
                hand.extend([crewmate1[0], demon[0], crewmate2[0]])
                
                # 更新所有手牌的位置
                for i, card in enumerate(hand):
                    card.zone_position = i


# LEGENDARY

class GDB_117:
    """蒂尔德拉，反抗军头目 - Dirdra, Rebel Captain
    4费 5/4 恶魔猎手随从 - 德莱尼 - 传说
    <b>突袭</b>。<b>战吼：</b>将全部8种乘务员洗入你的牌库。
    <b>亡语：</b>抽取两张乘务员。
    
    Rush. Battlecry: Shuffle all 8 Crewmates into your deck. Deathrattle: Draw two Crewmates.
    """
    mechanics = [GameTag.RUSH, GameTag.BATTLECRY, GameTag.DEATHRATTLE]
    race = Race.DRAENEI
    
    def play(self):
        # 将全部8种乘务员洗入牌库
        crewmate_ids = [
            "GDB_117t",   # 基础乘务员
            "GDB_117t1",  # 乘务员变体1
            "GDB_117t2",  # 乘务员变体2
            "GDB_117t3",  # 乘务员变体3
            "GDB_117t4",  # 乘务员变体4
            "GDB_117t5",  # 乘务员变体5
            "GDB_117t6",  # 乘务员变体6
            "GDB_117t7",  # 乘务员变体7
        ]
        
        for crewmate_id in crewmate_ids:
            yield Shuffle(CONTROLLER, crewmate_id)
    
    def deathrattle(self):
        # 抽取两张乘务员
        # 从牌库中找到乘务员并抽取
        crewmates_in_deck = [
            card for card in self.controller.deck
            if card.id.startswith("GDB_117t") or card.id == "GDB_119t"
        ]
        
        # 抽取最多两张乘务员
        for _ in range(min(2, len(crewmates_in_deck))):
            # 从牌库中的乘务员中随机选择一张
            if crewmates_in_deck:
                crewmate = self.game.random.choice(crewmates_in_deck)
                crewmates_in_deck.remove(crewmate)
                yield ForceDraw(CONTROLLER, crewmate)


class GDB_118:
    """佐托斯，星辰毁灭者 - Xor'toth, Breaker of Stars
    6费 5/5 恶魔猎手随从 - 恶魔 - 传说
    <b>战吼：</b>将两张星球牌从两侧置入你的手牌。当两颗星球相撞时，对所有敌人造成5点伤害。
    
    Battlecry: Add two Stars to both sides of your hand. When they collide, deal 5 damage to all enemies.
    """
    mechanics = [GameTag.BATTLECRY]
    race = Race.DEMON
    
    def play(self):
        # 在手牌左侧加入阿古斯星球
        star1 = yield Give(CONTROLLER, "GDB_118t1")
        
        # 在手牌右侧加入克罗库恩星球
        star2 = yield Give(CONTROLLER, "GDB_118t2")
        
        # 调整星球位置到手牌两侧
        if star1 and star2:
            hand = list(self.controller.hand)
            
            # 移除两颗星球
            if star1[0] in hand:
                hand.remove(star1[0])
            if star2[0] in hand:
                hand.remove(star2[0])
            
            # 将星球放到手牌两侧
            # 左侧星球放在最左边
            hand.insert(0, star1[0])
            # 右侧星球放在最右边
            hand.append(star2[0])
            
            # 更新所有手牌的位置
            for i, card in enumerate(hand):
                card.zone_position = i


# Buff 定义

class GDB_110e:
    """邪能动力源 - +1攻击力 Buff"""
    tags = {GameTag.ATK: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}


# 辅助函数

def RandomCrewmate():
    """随机选择一个乘务员Token"""
    crewmate_ids = [
        "GDB_117t",   # 基础乘务员
        "GDB_117t1",  # 乘务员变体1
        "GDB_117t2",  # 乘务员变体2
        "GDB_117t3",  # 乘务员变体3
        "GDB_117t4",  # 乘务员变体4
        "GDB_117t5",  # 乘务员变体5
        "GDB_117t6",  # 乘务员变体6
        "GDB_117t7",  # 乘务员变体7
    ]
    
    def selector(entities):
        import random
        return random.choice(crewmate_ids)
    
    return selector
