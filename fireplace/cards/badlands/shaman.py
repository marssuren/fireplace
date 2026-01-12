"""
决战荒芜之地 - SHAMAN
"""
from ..utils import *


# COMMON

class DEEP_008:
    """针岩图腾 - Needlerock Totem
    在你的回合结束时，获得2点护甲值并抽一张牌。
    At the end of your turn, gain 2 Armor and draw a card.
    """
    # Type: MINION | Cost: 2 | Rarity: COMMON | Stats: 0/2 | Race: TOTEM
    events = OWN_TURN_END.on(
        GainArmor(FRIENDLY_HERO, 2),
        Draw(CONTROLLER)
    )


class DEEP_009:
    """向下深挖 - Digging Straight Down
    对一个随从造成$8点伤害。发掘一个宝藏。
    Deal $8 damage to a minion. Excavate a treasure.
    """
    # Type: SPELL | Cost: 4 | Rarity: COMMON | School: NATURE | Mechanics: EXCAVATE
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        yield Hit(TARGET, 8)
        yield Excavate(CONTROLLER)


class WW_024:
    """活体原野岩 - Living Prairie
    战吼：如果你在上个回合使用过元素牌，召唤两只3/3并具有突袭的牛。
    Battlecry: If you played an Elemental last turn, summon two 3/3 Cows with Rush.
    """
    # Type: MINION | Cost: 5 | Rarity: COMMON | Stats: 5/4 | Race: ELEMENTAL
    def play(self):
        # 检查上回合是否使用过元素
        if self.controller.elemental_played_last_turn > 0:
            # 召唤2个3/3突袭的牛
            for _ in range(2):
                yield Summon(CONTROLLER, "WW_024t")


class WW_024t:
    """牛 - Cow"""
    # 3/3随从，突袭
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.RUSH: True,
        GameTag.CARDRACE: Race.BEAST
    }


class WW_325:
    """脱水 - Dehydrate
    吸血。对一个随从造成$4点伤害。快枪：法力值消耗为(1)点。
    Lifesteal. Deal $4 damage to a minion. Quickdraw: Costs (1).
    """
    # Type: SPELL | Cost: 3 | Rarity: COMMON | Mechanics: LIFESTEAL, QUICKDRAW
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    lifesteal = True
    
    # 快枪：本回合获得时，费用变为1（减少2费）
    cost_mod = lambda self, i: -2 if self.drawn_this_turn else 0
    
    play = Hit(TARGET, 4)


class WW_327:
    """仙人掌割水工 - Cactus Cutter
    战吼：抽一张法术牌。如果你在本回合中施放了该法术，便获得+1/+2和嘲讽。
    Battlecry: Draw a spell. If you cast it this turn, gain +1/+2 and Taunt.
    """
    # Type: MINION | Cost: 2 | Rarity: COMMON | Stats: 2/2 | Race: MURLOC
    def play(self):
        # 抽一张法术牌
        spell = yield ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))
        if spell:
            # 给抽到的法术添加追踪buff
            yield Buff(spell, "WW_327e_tracker")
            # 给自己添加监听buff
            yield Buff(SELF, "WW_327e")


class WW_327e:
    """仙人掌割水工监听buff"""
    # 当控制者使用带有追踪标记的法术时触发
    events = Play(CONTROLLER, FRIENDLY + SPELL + ID("WW_327e_tracker")).after(
        Buff(OWNER, "WW_327e2"),
        Destroy(SELF)
    )


class WW_327e_tracker:
    """法术追踪标记"""
    # 当这张法术被使用后移除标记
    events = Play(CONTROLLER, SELF).after(Destroy(SELF))


class WW_327e2:
    """+1/+2和嘲讽"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.TAUNT: True
    }


# RARE

class WW_080:
    """两栖药剂 - Amphibious Elixir
    恢复#5点生命值。发现一张法术牌。
    Restore #5 Health. Discover a spell.
    """
    # Type: SPELL | Cost: 2 | Rarity: RARE | School: NATURE | Mechanics: DISCOVER
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    
    def play(self):
        yield Heal(TARGET, 5)
        yield GenericChoice(CONTROLLER, SPELL)


class WW_090:
    """巨型风滚草！ - Giant Tumbleweed!!!
    对所有随从造成$6点伤害。召唤一个6/6的风滚草。
    Deal $6 damage to all minions. Summon a 6/6 Tumbleweed.
    """
    # Type: SPELL | Cost: 7 | Rarity: RARE | School: NATURE
    def play(self):
        yield Hit(ALL_MINIONS, 6)
        yield Summon(CONTROLLER, "WW_090t")


class WW_090t:
    """风滚草 - Tumbleweed"""
    # 6/6随从
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6
    }


class WW_326:
    """矿车巡逻兵 - Minecart Cruiser
    突袭，过载：(2)。战吼：如果你在上个回合使用过元素牌，则不会过载。
    Rush, Overload: (2). Battlecry: If you played an Elemental last turn, don't Overload.
    """
    # Type: MINION | Cost: 3 | Rarity: RARE | Stats: 4/5 | Race: ELEMENTAL
    rush = True
    overload = 2
    
    def play(self):
        # 如果上回合使用过元素，取消过载
        if self.controller.elemental_played_last_turn > 0:
            # 减少下回合的过载水晶
            self.controller.overload_next -= 2


# EPIC

class WW_027:
    """可靠陪伴 - Trusty Companion
    使一个随从获得+2/+3。如果它有随从类型，则抽一张该类型的牌。
    Give a minion +2/+3. If it has a minion type, draw one of that type.
    """
    # Type: SPELL | Cost: 2 | Rarity: EPIC
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        # 给目标+2/+3
        yield Buff(TARGET, "WW_027e")
        
        # 检查目标是否有种族
        target = self.target
        if target and hasattr(target, 'race') and target.race:
            # 抽一张相同种族的牌
            race = target.race
            yield ForceDraw(RANDOM(FRIENDLY_DECK + MINION + Race(race)))


class WW_027e:
    """+2/+3"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3
    }


class WW_382:
    """步移山丘 - Walking Mountain
    突袭，吸血，超级风怒。过载：(2)
    Rush, Lifesteal, Mega-Windfury. Overload: (2)
    """
    # Type: MINION | Cost: 9 | Rarity: EPIC | Stats: 4/16 | Race: ELEMENTAL
    rush = True
    lifesteal = True
    mega_windfury = True
    overload = 2


# LEGENDARY

class WW_010:
    """荷利戴医生 - Doctor Holli'dae
    战吼：如果你的套牌里没有相同的牌，则装备九蛙法杖。
    Battlecry: If your deck started with no duplicates, equip the Staff of the Nine Frogs.
    """
    # Type: MINION | Cost: 5 | Rarity: LEGENDARY | Stats: 4/5
    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    
    def play(self):
        # 检查起始套牌是否无重复
        if self.powered_up:
            # 装备九蛙法杖（武器）
            yield Summon(CONTROLLER, "WW_010t")



class WW_010t:
    """九蛙法杖 - Staff of the Nine Frogs
    在你的英雄攻击后，召唤一只1/1并具有嘲讽的青蛙。（每只青蛙都比上一只更大！）
    After your hero attacks, summon a 1/1 Frog with Taunt. (Each Frog is bigger than the last!)"""
    # Type: WEAPON | Cost: 5 | Attack: 2 | Durability: 9
    # 每次英雄攻击后召唤的青蛙会递增（1/1, 2/2, 3/3...）
    # 使用武器的progress属性追踪青蛙大小
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'progress'):
            self.progress = 0
    
    def trigger_after_hero_attack(self):
        """英雄攻击后触发"""
        # 增加计数
        self.progress += 1
        # 召唤青蛙，大小为 progress / progress
        frog = yield Summon(CONTROLLER, "WW_010t2")
        if frog:
            # 设置青蛙的属性
            yield Buff(frog, "WW_010t2e", atk=self.progress, max_health=self.progress)
    
    events = Attack(FRIENDLY_HERO).after(
        lambda self, source, *args: list(source.trigger_after_hero_attack()) if hasattr(source, 'trigger_after_hero_attack') else None
    )


class WW_010t2:
    """青蛙 - Frog"""
    # 基础1/1青蛙，嘲讽
    # 实际属性会被WW_010t的事件动态设置
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.TAUNT: True,
        GameTag.CARDRACE: Race.BEAST
    }


class WW_010t2e:
    """青蛙属性增益"""
    # 动态设置的属性增益
    pass



class WW_026:
    """灾变飓风斯卡尔 - Skarr, the Catastrophe
    战吼：对所有敌人造成1点伤害（每连续一个回合使用元素牌，伤害便+1）。
    Battlecry: Deal 1 damage to all enemies (improved by each turn in a row you've played an Elemental).
    """
    # Type: MINION | Cost: 7 | Rarity: LEGENDARY | Stats: 7/7 | Race: ELEMENTAL
    # 注意：这个卡牌使用 elemental_streak 属性追踪连续回合使用元素
    # 该属性已在Player类（player.py第106行）和game.py（407-410行）中实现
    def play(self):
        # 获取连续元素回合数（基础伤害1 + 连续回合数）
        consecutive_turns = getattr(self.controller, 'elemental_streak', 0)
        damage = 1 + consecutive_turns
        
        # 对所有敌人造成伤害
        yield Hit(ENEMY_CHARACTERS, damage)




