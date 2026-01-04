from ..utils import *
from fireplace.dsl.lazynum import EventArgument

class JAM_024:
    """Ambient Lightspawn - 布景光耀之子
    4费 2/5 元素
    过量治疗：随机使另一个友方随从获得+2/+2。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
        GameTag.RACE: Race.ELEMENTAL,
    }
    # 过量治疗：Buff随机友方随从（排除自己）
    overheal = Buff(RandomMinion(FRIENDLY_MINIONS - SELF), "JAM_024e")

class JAM_024e:
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2}

class JAM_022:
    """Deafen - 致聋术
    1费法术
    沉默一个随从。连击：并对其造成2点伤害。
    （注：实现逻辑遵循提供的骨架描述，虽然标准卡牌通常是直接造成3点伤害）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        yield Silence(TARGET)
        # 连击：造成伤害
        if self.controller.combo:
            yield Hit(TARGET, 2)

class ETC_449:
    """Fan Club - 粉丝俱乐部
    1费 地标 3耐久
    为所有友方角色恢复3点生命值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 1,
        GameTag.HEALTH: 3,  # 地标的耐久度用 Health 表示
    }
    # 地标激活效果:为所有友方角色恢复3点生命值
    activate = Heal(FRIENDLY_CHARACTERS, 3)

class JAM_027:
    """Fanboy - 饭圈迷弟
    3费 2/2
    抉择：使一个友方随从获得+2攻击力和突袭；或者+2生命值和吸血。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.CHOOSE_ONE: True,
    }
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    choose = ("JAM_027a", "JAM_027b")
    
    def play(self):
        # 抉择逻辑由核心处理，根据 choice 触发对应 Buff
        if self.choice == "JAM_027a":
            yield Buff(TARGET, "JAM_027ae")
        elif self.choice == "JAM_027b":
            yield Buff(TARGET, "JAM_027be")

class JAM_027a:
    """Grip - 握手会"""
    tags = {GameTag.CARDTYPE: CardType.SPELL} # Token
class JAM_027b:
    """Shout - 呐喊助威"""
    tags = {GameTag.CARDTYPE: CardType.SPELL} # Token

class JAM_027ae:
    tags = {GameTag.ATK: 2, GameTag.RUSH: True}
class JAM_027be:
    tags = {GameTag.HEALTH: 2, GameTag.LIFESTEAL: True}

class ETC_312:
    """Idol's Adoration - 爱豆的爱
    1费 0/3 武器
    你的英雄技能法力值消耗为（0）点。在你使用技能后，失去1点耐久度。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.WEAPON,
    }
    # 装备时 Buff 英雄技能
    # 使用光环或 Buff？
    # 武器在场时，光环效果
    # 监听：使用技能 -> 失去耐久
    
    # 光环：英雄技能消耗0
    auras = [
        Buff(FRIENDLY_HERO_POWER, "ETC_312e")
    ]
    
    # 监听：使用技能
    events = Activate(CONTROLLER, HERO_POWER).on(
        Hit(SELF, 1) # 失去1耐久 = 受到1伤害
    )

class ETC_312e:
    tags = {GameTag.COST_SET: 0}

class ETC_338:
    """Power Chord: Synchronize - 真弦术：合
    2费法术
    选择一个随从，将一张它的复制置入你的手牌。压轴：使其均获得+1/+2。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        target = self.target
        # 复制置入首牌，并捕获该复制
        # Give 返回 card list
        copies = yield Give(CONTROLLER, Copy(target))
        
        # 压轴检查（核心已修复Finale触发时机，但此处需要在一个逻辑流中同时操作原版和复制品）
        # 如果使用核心的 finale = [...]，无法方便地获取 copies 变量。
        # 因此这里手动进行压轴判定。
        # 注意：Action执行时费用已支付，mana即为剩余mana
        if self.controller.mana == 0:
            if copies:
                yield Buff(copies[0], "ETC_338e")
            yield Buff(target, "ETC_338e")

class ETC_338e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 2}

class ETC_332:
    """Dreamboat - 梦中男神
    2费 2/3
    战吼：为所有其他友方随从恢复3点生命值。每有一个被过量治疗，便获得+1/+1。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    
    def play(self):
        others = self.controller.field.exclude(self)
        
        # 计算将要被过量治疗的数量
        # 过量治疗判定：当前生命值 + 3 > 最大生命值
        overheal_count = 0
        for m in others:
            if m.health + 3 > m.max_health:
                overheal_count += 1
        
        # 执行治疗
        yield Heal(others, 3)
        
        # 获得 Buff
        if overheal_count > 0:
            yield Buff(SELF, "ETC_332e") * overheal_count

class ETC_332e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}

class JAM_025:
    """Funnel Cake - 漏斗蛋糕
    2费法术
    为一个随从及其相邻随从恢复3点生命值。每有一个随从受到过量治疗，便复原一个法力水晶。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        targets = [self.target] + self.target.adjacent_minions
        
        # 计算过量数量
        overheal_count = 0
        for m in targets:
            if m.health + 3 > m.max_health:
                overheal_count += 1
                
        yield Heal(targets, 3)
        
        if overheal_count > 0:
            yield GainMana(CONTROLLER, overheal_count)

class ETC_314:
    """Harmonic Pop - 悦耳流行歌
    6费法术
    对所有随从造成3点伤害。召唤一个6/6的流行歌星。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
    }
    
    def play(self):
        yield Hit(ALL_MINIONS, 3)
        yield Summon(CONTROLLER, "ETC_314t")
        
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "ETC_314t2"))

class ETC_314t2:
    """Dissonant Pop - 刺耳流行歌
    6费法术
    对所有随从造成6点伤害。召唤一个3/3的流行歌星。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
    }
    def play(self):
        yield Hit(ALL_MINIONS, 6)
        yield Summon(CONTROLLER, "ETC_314t3")

    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "ETC_314"))

class ETC_314t:
    """Pop Star - 流行歌星 (6/6)"""
    tags = {GameTag.ATK: 6, GameTag.HEALTH: 6, GameTag.COST: 6}
class ETC_314t3:
    """Pop Star - 流行歌星 (3/3)"""
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.COST: 3}

class JAM_023:
    """Plagiarizarrr - 盗版海盗
    2费 3/2 海盗
    战吼：获取你对手牌库顶的一张牌的复制。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RACE: Race.PIRATE,
    }
    def play(self):
        # 对手牌库顶
        if self.controller.opponent.deck:
            top_card = self.controller.opponent.deck[-1]
            yield Give(CONTROLLER, Copy(top_card))

class ETC_305:
    """Shadow Chord: Distort - 暗弦术：改
    3费法术
    使一个随从获得-5/-5。如果该随从拥有0点攻击力，将其消灭。
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
        yield Buff(TARGET, "ETC_305e")
        # 检查攻击力
        if self.target.atk == 0:
            yield Destroy(TARGET)

class ETC_305e:
    tags = {GameTag.ATK: -5, GameTag.HEALTH: -5}

class ETC_316:
    """Fight Over Me - 粉丝互动
    4费法术
    选择两个敌方随从，使其互相攻击！将死亡的随从的复制置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        # 需要至少2个敌方随从才能发挥完全效果，但1个也能打（打不出只能选1个）
        # REQ_MINIMUM_ENEMY_MINIONS: 2 ?
    }
    
    def play(self):
        target1 = self.target
        # 选择第二个目标
        # 排除第一个目标
        others = self.controller.opponent.field.exclude(target1)
        if not others:
            return # 只有一个敌人，无法互殴
            
        # 选择第二个
        target2 = yield Choose(others, count=1)
        if not target2:
            return
        target2 = target2[0]
        
        # 互相攻击
        yield Attack(target1, target2)
        
        # 检查死亡
        if target1.dead:
            yield Give(CONTROLLER, Copy(target1))
        if target2.dead:
            yield Give(CONTROLLER, Copy(target2))

class ETC_339:
    """Heartthrob - 心动歌手
    3费 3/4
    过量治疗：随机召唤一个法力值消耗等同于过量治疗量的随从。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    # 过量治疗：召唤 Cost = Amount 的随从
    # 使用 EventArgument('amount') 获取传递的 overheal_amount (在 actions.py 中修复的逻辑)
    overheal = Summon(CONTROLLER, RandomMinion(cost=EventArgument('amount')))

class ETC_334:
    """Heartbreaker Hedanis - 碎心歌手赫达尼斯
    4费 3/6
    战吼：对本随从造成4点伤害。过量治疗：随机对一个敌人造成5点伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 4,
    }
    
    # 战吼：打自己4
    play = Hit(SELF, 4)
    
    # 过量治疗：打5
    overheal = Hit(RANDOM_ENEMY_CHARACTER, 5)

class ETC_335:
    """Love Everlasting - 真爱永恒
    3费法术
    你每个回合使用的第一张法术牌的法力值消耗减少（2）点。此效果持续到你在你的回合中未使用法术牌为止。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 施加永久 Enchantment 到控制器
        yield Buff(CONTROLLER, "ETC_335e")

class ETC_335e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 逻辑：
    # 1. 回合开始，重置 "本回合已减费" 标记 (First Spell logic)
    #    Fireplace 核心并没有 "First Spell" 自动标记。我们得自己做。
    # 2. 减费光环：Condition: SpellsPlayedThisTurn == 0.
    #    TAG: SPELLS_COST_MOD = -2
    # 3. 回合结束判定：如果 SpellsPlayedThisTurn == 0，销毁自己。
    
    # 光环：如果本回合还没打过法术，手牌法术-2
    # 条件：CONTROLLER.spells_played_this_turn == 0
    # 注意：spells_played_this_turn 在打出时增加。
    # 当第一张打出时，变为1，光环失效。符合 "First spell" 逻辑。
    auras = [
        Buff(FRIENDLY_HAND + SPELL, "ETC_335buff")
    ]
    
    events = [
        # 回合结束检查
        OwnTurnEnd(CONTROLLER).on(
            # 如果本回合没打过法术
            Condition(
                Equal(Attr(CONTROLLER, GameTag.NUM_SPELLS_PLAYED_THIS_TURN), 0),
                Destroy(SELF)
            )
        )
    ]

# 减费效果 Buff
class ETC_335buff:
    tags = {GameTag.COST: -2}
