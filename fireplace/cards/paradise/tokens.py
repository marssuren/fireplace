"""
胜地历险记 - Token 卡牌
"""
from ..utils import *

# Death Knight Tokens

class VAC_445t:
    """夜场食尸鬼 - Night Ghoul"""
    # 1/1 亡灵
    race = Race.UNDEAD


class VAC_514t:
    """恐惧猎犬 - Dreadhound"""
    # 1/1 亡灵+野兽
    # 复生
    reborn = True
    races = [Race.UNDEAD, Race.BEAST]


# Demon Hunter Tokens

class VAC_925t:
    """海盗 - Pirate (from Sigil of Skydiving)"""
    # 1/1 海盗 冲锋
    charge = True
    race = Race.PIRATE


class VAC_929t:
    """海盗 - Pirate (from Dangerous Cliffside)"""
    # 1/1 海盗 冲锋
    charge = True
    race = Race.PIRATE


class VAC_933t:
    """降落伞 - Parachute"""
    # 1费法术
    # Cast When Drawn: 召唤一个1/1并具有冲锋的海盗
    cast_when_drawn = Summon(CONTROLLER, "VAC_933t2")


class VAC_933t2:
    """海盗 - Pirate (from Parachute)"""
    # 1/1 海盗 冲锋
    charge = True
    race = Race.PIRATE


# Druid Tokens

class VAC_511t:
    """龙 - Dragon (from Dozing Dragon)"""
    # 3/5 龙 嘲讽
    taunt = True
    race = Race.DRAGON


class WORK_024t:
    """熊 - Bear (from Handle with Bear)"""
    # 3/3 野兽 嘲讽
    # 在手牌中每回合获得+1/+1
    taunt = True
    race = Race.BEAST

    class Hand:
        # 在你的回合开始时，如果在手牌中，获得+1/+1
        events = OWN_TURN_BEGIN.on(Buff(SELF, "WORK_024te"))


class WORK_024te:
    """熊的增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# Hunter Tokens

class VAC_412t:
    """鱼虫 - Worm (from Catch of the Day)"""
    # 2/1 野兽
    race = Race.BEAST


class WORK_018t:
    """小马 - Pony (from Workhorse)"""
    # 2/1 野兽
    race = Race.BEAST


class VAC_410t:
    """小鸟 - Bird (from Furious Fowls)"""
    # 3/3 野兽
    # 攻击时免疫
    race = Race.BEAST
    
    # 攻击时免疫的实现
    events = Attack(SELF).on(
        Buff(SELF, "VAC_410te")
    )


class VAC_410te:
    """攻击时免疫效果"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    # 攻击结束后移除免疫
    events = Attack(OWNER).after(Destroy(SELF))


class VAC_413t:
    """鳄鱼 - Crocolisk (from Ranger Gilly)"""
    # 2/3 野兽
    race = Race.BEAST


# Mage Tokens

class VAC_520t:
    """银樽海韵 - Seabreeze Chalice (2 Drinks left)"""
    # 饮品法术第二次使用版本
    def play(self):
        # 造成2点伤害，随机分配到所有敌方随从
        for _ in range(2):
            targets = self.game.board.get_enemies(self.controller).filter(type=CardType.MINION)
            if targets:
                target = self.game.random.choice(targets)
                yield Hit(target, 1)
        
        # 返回1杯版本
        yield Give(CONTROLLER, "VAC_520t2")


class VAC_520t2:
    """银樽海韵 - Seabreeze Chalice (1 Drink left)"""
    # 饮品法术第三次使用版本（最后一次，不再返回）
    def play(self):
        # 造成2点伤害，随机分配到所有敌方随从
        for _ in range(2):
            targets = self.game.board.get_enemies(self.controller).filter(type=CardType.MINION)
            if targets:
                target = self.game.random.choice(targets)
                yield Hit(target, 1)
        # 最后一次使用，不再返回手牌


class VAC_509t:
    """水元素 - Water Elemental (from Tsunami)"""
    # 3/6 元素
    # 冻结：攻击后冻结目标
    race = Race.ELEMENTAL
    
    # 攻击后冻结目标
    events = Attack(SELF).after(
        lambda self, attacker, defender: Freeze(defender)
    )


# Paladin Tokens

class VAC_921t:
    """防晒霜 - Sunscreen
    1费法术：使一个随从获得+1/+2
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            yield Buff(TARGET, "VAC_921te")


class VAC_921te:
    """防晒霜增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class VAC_916t:
    """神圣佳酿 - Divine Brew (2 Drinks left)"""
    # Drink Spell 第二次使用版本
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 给予圣盾
        if TARGET:
            yield SetTags(TARGET, {GameTag.DIVINE_SHIELD: True})
        
        # 返回1杯版本
        yield Give(CONTROLLER, "VAC_916t2")


class VAC_916t2:
    """神圣佳酿 - Divine Brew (1 Drink left)"""
    # Drink Spell 第三次使用版本（最后一次）
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 给予圣盾
        if TARGET:
            yield SetTags(TARGET, {GameTag.DIVINE_SHIELD: True})
        # 最后一次使用，不再返回手牌


class VAC_558t:
    """海盗 - Pirate (from Sea Shanty)"""
    # 5/5 海盗
    race = Race.PIRATE


class VAC_923t:
    """圣沙泽尔 - Sanc'Azel (Location form)
    地标形态：使一个友方随从获得+3攻击力和突袭，然后变回随从形态
    Give a friendly minion +3 Attack and Rush. Turn back into a minion.
    """
    # 地标效果
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def activate(self):
        if TARGET:
            # 给予+3攻击力和突袭
            yield Buff(TARGET, "VAC_923te")
        
        # 变回随从形态（Morph回原卡）
        yield Morph(SELF, "VAC_923")


class VAC_923te:
    """圣沙泽尔地标增益效果"""
    tags = {
        GameTag.RUSH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }


# Priest Tokens

class VAC_404t:
    """夜影花茶 - Nightshade Tea (2 Drinks left)"""
    # Drink Spell 第二次使用版本
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 对目标随从造成2点伤害
        if TARGET:
            yield Hit(TARGET, 2)
        
        # 对友方英雄造成2点伤害
        yield Hit(FRIENDLY_HERO, 2)
        
        # 返回1杯版本
        yield Give(CONTROLLER, "VAC_404t2")


class VAC_404t2:
    """夜影花茶 - Nightshade Tea (1 Drink left)"""
    # Drink Spell 第三次使用版本（最后一次）
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 对目标随从造成2点伤害
        if TARGET:
            yield Hit(TARGET, 2)
        
        # 对友方英雄造成2点伤害
        yield Hit(FRIENDLY_HERO, 2)
        # 最后一次使用，不再返回手牌


class WORK_017t:
    """吉尔尼斯宣传单 - Gilneas Brochure
    Silence a minion and give it -2/-2. (Flips each turn.)
    沉默一个随从并使其获得-2/-2。（每回合翻面。）
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 沉默目标随从
            yield Silence(TARGET)
            # 给予-2/-2
            yield Buff(TARGET, "WORK_017te")
    
    # 翻面机制：在手牌中每回合翻转回 Silvermoon Brochure
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "WORK_017"))


class WORK_017te:
    """吉尔尼斯宣传单 - 属性减益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: -2,
        GameTag.HEALTH: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# Warlock Tokens

class VAC_940t:
    """邪能兽 - Felbeast (from Party Fiend)"""
    # 1/1 恶魔
    race = Race.DEMON


class VAC_943t:
    """小鬼 - Imp (from Sacrificial Imp)"""
    # 6/6 恶魔 嘲讽
    taunt = True
    race = Race.DEMON


class VAC_951t:
    """"健康"饮品 - "Health" Drink (2 Drinks left)"""
    # Drink Spell 第二次使用版本
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 对目标造成3点伤害（带吸血效果）
        if TARGET:
            damage_dealt = yield Hit(TARGET, 3)
            if damage_dealt:
                actual_damage = damage_dealt[0] if isinstance(damage_dealt, list) else damage_dealt
                if actual_damage > 0:
                    yield Heal(FRIENDLY_HERO, actual_damage)

        # 返回1杯版本
        yield Give(CONTROLLER, "VAC_951t2")


class VAC_951t2:
    """"健康"饮品 - "Health" Drink (1 Drink left)"""
    # Drink Spell 第三次使用版本（最后一次）
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 对目标造成3点伤害（带吸血效果）
        if TARGET:
            damage_dealt = yield Hit(TARGET, 3)
            if damage_dealt:
                actual_damage = damage_dealt[0] if isinstance(damage_dealt, list) else damage_dealt
                if actual_damage > 0:
                    yield Heal(FRIENDLY_HERO, actual_damage)
        # 最后一次使用，不再返回手牌


class VAC_945t:
    """乌洛波斯，世界之蛇 - Ourobos, World Serpent (from Party Planner Vona)
    8-mana 8/8 Beast with Taunt
    Deathrattle: Give a minion in your hand 'Deathrattle: Summon Ourobos.'

    官方验证：8费 8/8 野兽，嘲讽
    亡语：使你手牌中的一个随从获得"亡语：召唤乌洛波斯"
    """
    mechanics = [GameTag.TAUNT, GameTag.DEATHRATTLE]
    race = Race.BEAST

    def deathrattle(self):
        # 随机选择手牌中的一个随从
        minions_in_hand = [c for c in self.controller.hand if c.type == CardType.MINION]
        if minions_in_hand:
            target = self.game.random.choice(minions_in_hand)
            # 给予该随从"亡语：召唤乌洛波斯"
            yield Buff(target, "VAC_945te")


class VAC_945te:
    """乌洛波斯亡语效果"""
    tags = {GameTag.DEATHRATTLE: True, GameTag.CARDTYPE: CardType.ENCHANTMENT}

    def deathrattle(self):
        # 召唤乌洛波斯
        yield Summon(CONTROLLER, "VAC_945t")


# Shaman Tokens

class VAC_323t:
    """麦芽岩浆 - Malted Magma (2 Drinks left)"""
    # Drink Spell 第二次使用版本
    def play(self):
        # 对所有敌方角色造成1点伤害（包括英雄）
        enemy_characters = self.game.board.get_enemies(self.controller)
        for character in enemy_characters:
            yield Hit(character, 1)
        
        # 返回1杯版本
        yield Give(CONTROLLER, "VAC_323t2")


class VAC_323t2:
    """麦芽岩浆 - Malted Magma (1 Drink left)"""
    # Drink Spell 第三次使用版本（最后一次，不再返回）
    def play(self):
        # 对所有敌方角色造成1点伤害（包括英雄）
        enemy_characters = self.game.board.get_enemies(self.controller)
        for character in enemy_characters:
            yield Hit(character, 1)
        # 最后一次使用，不再返回手牌


class VAC_305t:
    """冰霜元素 - Frosty Elemental
    2/4 元素，嘲讽，亡语：获得4点护甲值
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True
    }
    race = Race.ELEMENTAL
    
    def deathrattle(self):
        # 获得4点护甲
        yield GainArmor(CONTROLLER, 4)


class WORK_030t:
    """黑石山宣传单 - Blackrock Brochure (翻面版本)
    Deal $3 damage to a minion and 1 to its neighbors. (Flips each turn.)
    对一个随从造成$3点伤害，并对其相邻随从造成1点伤害。（每回合翻面。）
    
    官方数据：Icecrown Brochure 翻面后变成 Blackrock Brochure
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        target = self.target
        if target:
            # 对目标造成3点伤害
            yield Hit(target, 3)
            
            # 对相邻随从造成1点伤害
            if target.zone == Zone.PLAY and hasattr(target, 'adjacent_minions'):
                for adj in target.adjacent_minions:
                    yield Hit(adj, 1)
    
    # 翻面机制：在手牌中每回合翻转回 Icecrown Brochure
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "WORK_030"))



# Carress, Cabaret Star - 21种变形形态
# 每种形态根据施放的两个派系组合产生不同的战吼效果

# 辅助函数：执行单个派系效果
def execute_school_effect(card, school):
    """执行单个派系的效果"""
    if school == SpellSchool.ARCANE:
        # Arcane: Draw 2 cards
        yield Draw(CONTROLLER) * 2
    elif school == SpellSchool.FEL:
        # Fel: Deal 2 damage to all enemy minions
        enemy_minions = card.game.board.get_enemies(card.controller).filter(type=CardType.MINION)
        for minion in enemy_minions:
            yield Hit(minion, 2)
    elif school == SpellSchool.FIRE:
        # Fire: Deal 6 damage to the enemy hero
        yield Hit(ENEMY_HERO, 6)
    elif school == SpellSchool.FROST:
        # Frost: Freeze three random enemy minions
        enemy_minions = list(card.game.board.get_enemies(card.controller).filter(type=CardType.MINION))
        if enemy_minions:
            targets = card.game.random.sample(enemy_minions, min(3, len(enemy_minions)))
            for target in targets:
                yield Freeze(target)
    elif school == SpellSchool.HOLY:
        # Holy: Restore 6 Health to your hero
        yield Heal(FRIENDLY_HERO, 6)
    elif school == SpellSchool.NATURE:
        # Nature: Gain +2/+2 and Taunt
        yield Buff(card, "VAC_449_nature_buff")
    elif school == SpellSchool.SHADOW:
        # Shadow: Destroy 2 random enemy minions
        enemy_minions = list(card.game.board.get_enemies(card.controller).filter(type=CardType.MINION))
        if enemy_minions:
            targets = card.game.random.sample(enemy_minions, min(2, len(enemy_minions)))
            for target in targets:
                yield Destroy(target)


class VAC_449_nature_buff:
    """Nature派系效果的Buff"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    atk = 2
    max_health = 2


# VAC_449t - Arcane + Fire
class VAC_449t:
    """Carress, Showstopper (Arcane + Fire)
    Battlecry: Draw 2 cards. Deal 6 damage to the enemy hero.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.ARCANE)
        yield from execute_school_effect(self, SpellSchool.FIRE)


# VAC_449t2 - Arcane + Nature
class VAC_449t2:
    """Carress, Showstopper (Arcane + Nature)
    Battlecry: Draw 2 cards. Gain +2/+2 and Taunt.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.ARCANE)
        yield from execute_school_effect(self, SpellSchool.NATURE)


# VAC_449t3 - Arcane + Fel
class VAC_449t3:
    """Carress, Showstopper (Arcane + Fel)
    Battlecry: Draw 2 cards. Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.ARCANE)
        yield from execute_school_effect(self, SpellSchool.FEL)


# VAC_449t4 - Arcane + Frost
class VAC_449t4:
    """Carress, Showstopper (Arcane + Frost)
    Battlecry: Draw 2 cards. Freeze three random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.ARCANE)
        yield from execute_school_effect(self, SpellSchool.FROST)


# VAC_449t5 - Arcane + Holy
class VAC_449t5:
    """Carress, Showstopper (Arcane + Holy)
    Battlecry: Draw 2 cards. Restore 6 Health to your hero.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.ARCANE)
        yield from execute_school_effect(self, SpellSchool.HOLY)


# VAC_449t6 - Arcane + Shadow
class VAC_449t6:
    """Carress, Showstopper (Arcane + Shadow)
    Battlecry: Draw 2 cards. Destroy 2 random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.ARCANE)
        yield from execute_school_effect(self, SpellSchool.SHADOW)


# VAC_449t7 - Fire + Nature
class VAC_449t7:
    """Carress, Showstopper (Fire + Nature)
    Battlecry: Deal 6 damage to the enemy hero. Gain +2/+2 and Taunt.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FIRE)
        yield from execute_school_effect(self, SpellSchool.NATURE)


# VAC_449t8 - Fire + Fel
class VAC_449t8:
    """Carress, Showstopper (Fire + Fel)
    Battlecry: Deal 6 damage to the enemy hero. Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FIRE)
        yield from execute_school_effect(self, SpellSchool.FEL)


# VAC_449t9 - Fire + Frost
class VAC_449t9:
    """Carress, Showstopper (Fire + Frost)
    Battlecry: Deal 6 damage to the enemy hero. Freeze three random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FIRE)
        yield from execute_school_effect(self, SpellSchool.FROST)


# VAC_449t10 - Fire + Holy
class VAC_449t10:
    """Carress, Showstopper (Fire + Holy)
    Battlecry: Deal 6 damage to the enemy hero. Restore 6 Health to your hero.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FIRE)
        yield from execute_school_effect(self, SpellSchool.HOLY)


# VAC_449t11 - Fire + Shadow
class VAC_449t11:
    """Carress, Showstopper (Fire + Shadow)
    Battlecry: Deal 6 damage to the enemy hero. Destroy 2 random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FIRE)
        yield from execute_school_effect(self, SpellSchool.SHADOW)


# VAC_449t12 - Holy + Frost
class VAC_449t12:
    """Carress, Showstopper (Holy + Frost)
    Battlecry: Restore 6 Health to your hero. Freeze three random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.HOLY)
        yield from execute_school_effect(self, SpellSchool.FROST)


# VAC_449t13 - Holy + Nature
class VAC_449t13:
    """Carress, Showstopper (Holy + Nature)
    Battlecry: Restore 6 Health to your hero. Gain +2/+2 and Taunt.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.HOLY)
        yield from execute_school_effect(self, SpellSchool.NATURE)


# VAC_449t14 - Shadow + Frost
class VAC_449t14:
    """Carress, Showstopper (Shadow + Frost)
    Battlecry: Destroy 2 random enemy minions. Freeze three random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.SHADOW)
        yield from execute_school_effect(self, SpellSchool.FROST)


# VAC_449t15 - Shadow + Nature
class VAC_449t15:
    """Carress, Showstopper (Shadow + Nature)
    Battlecry: Destroy 2 random enemy minions. Gain +2/+2 and Taunt.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.SHADOW)
        yield from execute_school_effect(self, SpellSchool.NATURE)


# VAC_449t16 - Shadow + Fel
class VAC_449t16:
    """Carress, Showstopper (Shadow + Fel)
    Battlecry: Destroy 2 random enemy minions. Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.SHADOW)
        yield from execute_school_effect(self, SpellSchool.FEL)


# VAC_449t17 - Frost + Nature
class VAC_449t17:
    """Carress, Showstopper (Frost + Nature)
    Battlecry: Freeze three random enemy minions. Gain +2/+2 and Taunt.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FROST)
        yield from execute_school_effect(self, SpellSchool.NATURE)


# VAC_449t18 - Holy + Shadow
class VAC_449t18:
    """Carress, Showstopper (Holy + Shadow)
    Battlecry: Restore 6 Health to your hero. Destroy 2 random enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.HOLY)
        yield from execute_school_effect(self, SpellSchool.SHADOW)


# VAC_449t19 - Frost + Fel
class VAC_449t19:
    """Carress, Showstopper (Frost + Fel)
    Battlecry: Freeze three random enemy minions. Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.FROST)
        yield from execute_school_effect(self, SpellSchool.FEL)


# VAC_449t20 - Holy + Fel
class VAC_449t20:
    """Carress, Showstopper (Holy + Fel)
    Battlecry: Restore 6 Health to your hero. Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.HOLY)
        yield from execute_school_effect(self, SpellSchool.FEL)


# VAC_449t21 - Nature + Fel
class VAC_449t21:
    """Carress, Showstopper (Nature + Fel)
    Battlecry: Gain +2/+2 and Taunt. Deal 2 damage to all enemy minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        yield from execute_school_effect(self, SpellSchool.NATURE)
        yield from execute_school_effect(self, SpellSchool.FEL)


# Neutral Common Tokens

class VAC_421t:
    """野兽 - Beast (from Snoozin' Zookeeper)"""
    # 8/8 野兽
    race = Race.BEAST


# Neutral Epic Tokens

class VAC_523t:
    """混调师的特调 - Mixologist's Special
    1费法术：让玩家从9个效果中选择2个，组合成自定义药水
    
    官方效果选项：
    1. 召唤一个2/2的恶魔
    2. 召唤一个本局对战中死亡的友方随从
    3. 使你的随从获得+2生命值
    4. 冻结一个随机的敌方随从
    5. 造成3点伤害
    6. 对所有随从造成2点伤害
    7. 获得4点护甲
    8. 抽一张牌
    9. 将一张随机恶魔牌置入你的手牌
    """
    # 类似 Kazakus 的实现
    # 第一步：选择第一个效果
    def play(self):
        # 创建9个效果选项
        effect_options = [
            "VAC_523t_effect1",   # 召唤2/2恶魔
            "VAC_523t_effect2",   # 复活随从
            "VAC_523t_effect3",   # 随从+2生命
            "VAC_523t_effect4",   # 冻结随机敌方随从
            "VAC_523t_effect5",   # 造成3点伤害
            "VAC_523t_effect6",   # AOE 2伤害
            "VAC_523t_effect7",   # 获得4护甲
            "VAC_523t_effect8",   # 抽一张牌
            "VAC_523t_effect9",   # 获得随机恶魔
        ]
        
        # 第一次选择
        first_choice = yield Discover(CONTROLLER, effect_options)
        
        if first_choice:
            first_effect_id = first_choice[0].id
            
            # 第二次选择（从剩余的效果中选择）
            remaining_effects = [e for e in effect_options if e != first_effect_id]
            second_choice = yield Discover(CONTROLLER, remaining_effects)
            
            if second_choice:
                second_effect_id = second_choice[0].id
                
                # 创建组合药水并执行两个效果
                # 执行第一个效果
                yield from self._execute_effect(first_effect_id)
                # 执行第二个效果
                yield from self._execute_effect(second_effect_id)
    
    def _execute_effect(self, effect_id):
        """执行指定的药水效果"""
        if effect_id == "VAC_523t_effect1":
            # 召唤2/2恶魔
            yield Summon(CONTROLLER, "VAC_523t_demon")
        elif effect_id == "VAC_523t_effect2":
            # 复活一个随从
            if self.controller.graveyard:
                minions = [c for c in self.controller.graveyard if c.type == CardType.MINION]
                if minions:
                    target = self.game.random.choice(minions)
                    yield Summon(CONTROLLER, target.id)
        elif effect_id == "VAC_523t_effect3":
            # 随从+2生命
            for minion in self.controller.field:
                yield Buff(minion, "VAC_523t_health")
        elif effect_id == "VAC_523t_effect4":
            # 冻结随机敌方随从
            enemies = self.game.board.get_enemies(self.controller).filter(type=CardType.MINION)
            if enemies:
                target = self.game.random.choice(enemies)
                yield Freeze(target)
        elif effect_id == "VAC_523t_effect5":
            # 造成3点伤害
            # 注意：此效果在组合药水中会自动对随机敌人造成伤害
            # 因为药水本身不支持目标选择（类似 Kazakus）
            enemies = self.game.board.get_enemies(self.controller)
            if enemies:
                target = self.game.random.choice(enemies)
                yield Hit(target, 3)
        elif effect_id == "VAC_523t_effect6":
            # AOE 2伤害
            for character in self.game.board:
                if character.type == CardType.MINION:
                    yield Hit(character, 2)
        elif effect_id == "VAC_523t_effect7":
            # 获得4护甲
            yield GainArmor(CONTROLLER, 4)
        elif effect_id == "VAC_523t_effect8":
            # 抽一张牌
            yield Draw(CONTROLLER)
        elif effect_id == "VAC_523t_effect9":
            # 获得随机恶魔
            yield Give(CONTROLLER, RandomCollectible(card_class=CardClass.NEUTRAL, race=Race.DEMON))


# 辅助 Token 定义

class VAC_523t_demon:
    """2/2恶魔 (from Mixologist's Special)"""
    race = Race.DEMON


class VAC_523t_health:
    """混调师药水 - 生命值增益"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    max_health = 2


# 效果占位符（用于发现选择）
class VAC_523t_effect1:
    """召唤2/2恶魔"""
    pass

class VAC_523t_effect2:
    """复活随从"""
    pass

class VAC_523t_effect3:
    """随从+2生命"""
    pass

class VAC_523t_effect4:
    """冻结敌方随从"""
    pass

class VAC_523t_effect5:
    """造成3点伤害"""
    pass

class VAC_523t_effect6:
    """AOE 2伤害"""
    pass

class VAC_523t_effect7:
    """获得4护甲"""
    pass

class VAC_523t_effect8:
    """抽一张牌"""
    pass

class VAC_523t_effect9:
    """获得随机恶魔"""
    pass


class VAC_935t:
    """手提箱 - Suitcase (from Carry-On Grub)"""
    # 1费法术
    # 正式声明属性：装入的卡牌ID列表（在 VAC_935 战吼中设置）
    packed_cards = []  # 默认为空列表
    
    def play(self):
        # 从手提箱中取出装入的卡牌
        cards_to_give = getattr(self, 'packed_cards', [])
        for card_id in cards_to_give:
            # 将卡牌加入手牌
            yield Give(CONTROLLER, card_id)


# ========== Neutral Legendary Tokens ==========

# VAC_321 - Incindius Tokens
class VAC_321t:
    """爆发 - Eruption (Level 1)"""
    # 1费火焰法术
    # Cast When Drawn: 对所有敌人造成伤害（可升级）
    # Incindius会在回合结束时增加eruption_damage属性
    
    # 正式声明属性：爆发伤害等级（默认为1）
    eruption_damage = 1
    
    # Cast When Drawn效果
    @property
    def cast_when_drawn(self):
        """抽到时造成伤害"""
        # 使用实例属性，如果不存在则使用类属性默认值
        damage = getattr(self, 'eruption_damage', 1)
        return [Hit(ENEMY_CHARACTERS, damage)]


# VAC_955 - Gorgonzormu Tokens
class VAC_955t:
    """美味奶酪 - Delicious Cheese"""
    # 2费法术
    # 召唤三个法力值消耗为(1)的随从
    # 在手牌中每回合升级
    
    # 正式声明属性：召唤随从的费用（默认为1）
    summon_cost = 1
    
    class Hand:
        """在手牌中每回合升级"""
        def on_turn_begin(self):
            """回合开始时升级召唤费用"""
            # 增加召唤费用（最高10费）
            current_cost = getattr(self, 'summon_cost', 1)
            if current_cost < 10:
                self.summon_cost = current_cost + 1
        
        events = OWN_TURN_BEGIN.on(
            lambda self, player: setattr(self, 'summon_cost', min(10, getattr(self, 'summon_cost', 1) + 1))
        )
    
    def play(self):
        # 召唤3个指定费用的随从
        cost = getattr(self, 'summon_cost', 1)
        # 从标准卡池中随机选择3个该费用的随从
        for _ in range(3):
            yield Summon(CONTROLLER, RandomCollectible(type=CardType.MINION, cost=cost))


# VAC_959 - Griftah Amulet Tokens (真品)
class VAC_959t:
    """移动护符 - Amulet of Mobility (真品)"""
    # 1费法术：抽3张牌
    def play(self):
        yield Draw(CONTROLLER) * 3


class VAC_959t2:
    """移动护符 - Amulet of Mobility (假货)"""
    # 1费法术：抽3张牌，然后弃2张
    def play(self):
        yield Draw(CONTROLLER) * 3
        # 弃2张牌
        if len(self.controller.hand) >= 2:
            yield Discard(RANDOM(CONTROLLER + CARD_IN_HAND)) * 2


class VAC_959t3:
    """生物护符 - Amulet of Critters (真品)"""
    # 1费法术：召唤一个随机的4费嘲讽随从
    def play(self):
        minion = yield Summon(CONTROLLER, RandomCollectible(type=CardType.MINION, cost=4))
        if minion:
            yield Buff(minion[0], "VAC_959t3e")


class VAC_959t3e:
    """生物护符嘲讽效果"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class VAC_959t4:
    """生物护符 - Amulet of Critters (假货)"""
    # 1费法术：召唤一个随机的4费随从，但无法攻击
    def play(self):
        minion = yield Summon(CONTROLLER, RandomCollectible(type=CardType.MINION, cost=4))
        if minion:
            yield Buff(minion[0], "VAC_959t4e")


class VAC_959t4e:
    """生物护符无法攻击效果"""
    tags = {
        GameTag.CANT_ATTACK: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class VAC_959t5:
    """能量护符 - Amulet of Energy (真品)"""
    # 1费法术：为你的英雄恢复12点生命值
    def play(self):
        yield Heal(FRIENDLY_HERO, 12)


class VAC_959t6:
    """能量护符 - Amulet of Energy (假货)"""
    # 1费法术：为你的英雄恢复12点生命值，然后受到6点伤害
    def play(self):
        yield Heal(FRIENDLY_HERO, 12)
        yield Hit(FRIENDLY_HERO, 6)


class VAC_959t7:
    """激情护符 - Amulet of Passions (真品)"""
    # 1费法术：获得一个敌方随从的控制权
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            yield Steal(TARGET)


class VAC_959t8:
    """激情护符 - Amulet of Passions (假货)"""
    # 1费法术：获得一个敌方随从的控制权，但本回合攻击力为1
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            yield Steal(TARGET)
            yield Buff(TARGET, "VAC_959t8e")


class VAC_959t8e:
    """激情护符攻击力限制"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    atk = lambda self, i: 1  # 设置攻击力为1


class VAC_959t9:
    """步伐护符 - Amulet of Strides (真品)"""
    # 1费法术：使你手牌中所有卡牌的法力值消耗减少(1)点
    def play(self):
        for card in self.controller.hand:
            yield Buff(card, "VAC_959t9e")


class VAC_959t9e:
    """步伐护符减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    tags = {GameTag.COST: -1}


class VAC_959t10:
    """步伐护符 - Amulet of Strides (假货)"""
    # 1费法术：使你手牌中所有随从的法力值消耗减少(1)点
    def play(self):
        for card in self.controller.hand:
            if card.type == CardType.MINION:
                yield Buff(card, "VAC_959t9e")  # 复用真品的buff


class VAC_959t11:
    """追踪护符 - Amulet of Tracking (真品)"""
    # 1费法术：获取3张随机传说卡牌
    def play(self):
        for _ in range(3):
            yield Give(CONTROLLER, RandomCollectible(rarity=Rarity.LEGENDARY))


class VAC_959t12:
    """追踪护符 - Amulet of Tracking (假货)"""
    # 1费法术：获取3张随机普通卡牌
    def play(self):
        for _ in range(3):
            yield Give(CONTROLLER, RandomCollectible(rarity=Rarity.COMMON))


class VAC_959t13:
    """伤害护符 - Amulet of Damage (真品)"""
    # 1费法术：造成6点伤害
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        if TARGET:
            yield Hit(TARGET, 6)


class VAC_959t14:
    """伤害护符 - Amulet of Damage (假货)"""
    # 1费法术：对一个随从造成6点伤害
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            yield Hit(TARGET, 6)


# WORK_027 - Dreamplanner Zephrys Tour Tokens
class WORK_027t1:
    """奢华之旅 - Extravagant Tour"""
    # 占位符Token，用于选择界面
    pass


class WORK_027t2:
    """忙碌之旅 - Hectic Tour"""
    # 占位符Token，用于选择界面
    pass


class WORK_027t3:
    """朴素之旅 - Modest Tour"""
    # 占位符Token，用于选择界面
    pass


# VAC_702 - Marin the Manager Treasure Tokens
class VAC_702t:
    """扎洛格的王冠 - Zarog's Crown"""
    # 3费法术
    # 发现一张传说随从，召唤它的两个复制
    def play(self):
        # 发现一张传说随从
        discovered = yield Discover(CONTROLLER, RandomCollectible(type=CardType.MINION, rarity=Rarity.LEGENDARY))
        if discovered:
            minion_id = discovered[0]
            # 召唤2个该随从的复制
            yield Summon(CONTROLLER, minion_id) * 2


class VAC_702t2:
    """奇妙法杖 - Wondrous Wand"""
    # 3费法术
    # 抽3张牌，使其法力值消耗减少(3)点
    def play(self):
        # 抽3张牌
        drawn_cards = yield Draw(CONTROLLER) * 3
        # 给抽到的牌减3费
        if drawn_cards:
            for card in drawn_cards:
                if card:
                    yield Buff(card, "VAC_702t2e")


class VAC_702t2e:
    """奇妙法杖减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    tags = {GameTag.COST: -3}


class VAC_702t3:
    """黄金狗头人 - Golden Kobold"""
    # 3费 6/6 嘲讽随从
    # 战吼：将你的手牌替换为传说随从，其法力值消耗减少(1)点
    mechanics = [GameTag.BATTLECRY, GameTag.TAUNT]
    
    def play(self):
        # 记录当前手牌数量
        hand_size = len(self.controller.hand)
        
        # 移除所有手牌
        for card in list(self.controller.hand):
            yield Destroy(card)
        
        # 给予同样数量的传说随从
        for _ in range(hand_size):
            legendary = yield Give(CONTROLLER, RandomCollectible(type=CardType.MINION, rarity=Rarity.LEGENDARY))
            if legendary:
                # 减1费
                yield Buff(legendary[0], "VAC_702t3e")


class VAC_702t3e:
    """黄金狗头人减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    tags = {GameTag.COST: -1}


class VAC_702t4:
    """托林的圣杯 - Tolin's Goblet"""
    # 3费法术
    # 抽一张牌，用它的复制填满你的手牌
    def play(self):
        # 抽一张牌
        drawn = yield Draw(CONTROLLER)
        
        if drawn and drawn[0]:
            card_id = drawn[0].id
            # 计算还能加入多少张牌（最多10张手牌）
            space_left = 10 - len(self.controller.hand)
            
            # 用该牌的复制填满手牌
            for _ in range(space_left):
                yield Give(CONTROLLER, card_id)


# ========== Warrior Tokens ==========

class VAC_338t:
    """腱力金杯 - Cup o' Muscle (2 Drinks left)
    Give a minion in your hand +2/+1. (2 Drinks left!)
    给你手牌中的一个随从+2/+1。（剩余2杯！）
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_IN_HAND: 0}

    def play(self):
        # 给手牌中的目标随从 +2/+1
        yield Buff(TARGET, "VAC_338e")
        # 给玩家一张 VAC_338t2 (1杯剩余版本)
        yield Give(CONTROLLER, "VAC_338t2")


class VAC_338t2:
    """腱力金杯 - Cup o' Muscle (1 Drink left)
    Give a minion in your hand +2/+1. (Last Drink!)
    给你手牌中的一个随从+2/+1。（最后一杯！）
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_IN_HAND: 0}

    def play(self):
        # 给手牌中的目标随从 +2/+1
        yield Buff(TARGET, "VAC_338e")
        # 最后一次使用，不再返回手牌


class VAC_525t:
    """面包片 - Slice of Bread
    When you have 2 of these, they become a Sandwich that summons minions from your hand.
    当你拥有2片面包时，它们会变成三明治，可以召唤你手牌中的随从。
    """
    # 监听卡牌被加入手牌的事件，检查是否有2片面包
    events = Give(CONTROLLER).after(
        lambda self, source, target, card: _check_sandwich(card.controller) if card.controller else None
    )


def _check_sandwich(player):
    """检查手牌中是否有2片面包，如果有则创建三明治"""
    # 找到手牌中所有的面包片
    bread_slices = [c for c in player.hand if c.id == "VAC_525t"]

    if len(bread_slices) >= 2:
        # 获取两片面包的位置
        first_bread = bread_slices[0]
        second_bread = bread_slices[1]

        # 获取它们在手牌中的索引
        first_index = player.hand.index(first_bread)
        second_index = player.hand.index(second_bread)

        # 确保顺序正确
        if first_index > second_index:
            first_index, second_index = second_index, first_index
            first_bread, second_bread = second_bread, first_bread

        # 找到两片面包之间的随从
        sandwiched_minions = []
        for i in range(first_index + 1, second_index):
            card = player.hand[i]
            if card.type == CardType.MINION:
                sandwiched_minions.append(card.id)

        # 如果有随从被夹住，创建三明治
        if sandwiched_minions:
            # 移除两片面包和中间的随从
            yield Destroy(first_bread)
            yield Destroy(second_bread)
            for i in range(first_index + 1, second_index):
                card = player.hand[i]
                if card.type == CardType.MINION:
                    yield Destroy(card)

            # 创建三明治法术并加入手牌
            sandwich = yield Give(player, "VAC_525t2")
            if sandwich:
                # 将被夹住的随从ID列表存储到三明治中
                sandwich[0].sandwiched_minions = sandwiched_minions


class VAC_525t2:
    """三明治 - Minion Sandwich
    Summon the minions that were sandwiched. (They won't trigger their Battlecries.)
    召唤被夹住的随从。（不会触发战吼。）
    """
    # 2费法术
    # 正式声明属性：被夹住的随从ID列表
    sandwiched_minions = []

    def play(self):
        # 召唤所有被夹住的随从（不触发战吼）
        minions_to_summon = getattr(self, 'sandwiched_minions', [])
        for minion_id in minions_to_summon:
            # 使用 Summon 而不是 Play，这样不会触发战吼
            yield Summon(CONTROLLER, minion_id)


class VAC_533t:
    """主菜 - Entrée
    Deathrattle: Your opponent summons a minion from their deck.
    亡语：你的对手从其牌库中召唤一个随从。
    """
    # 0/4 随从
    # 亡语效果在 VAC_533e 中实现
    pass

