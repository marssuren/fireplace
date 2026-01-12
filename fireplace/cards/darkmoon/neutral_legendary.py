from ..utils import *


##
# Minions

class DMF_002:
    """N'Zoth, God of the Deep (恩佐斯，深渊之神)
    Battlecry: Resurrect a friendly minion of each minion type."""
    # 9?5/7 - 战吼：复活每种随从类型的一个友方随?
    
    def play(self):
        dead_minions = self.controller.graveyard.filter(type=CardType.MINION)
        
        races_seen = set()
        to_resurrect = []
        
        for minion in dead_minions:
            race = getattr(minion, 'race', None)
            if race and race not in races_seen:
                races_seen.add(race)
                to_resurrect.append(minion)
        
        return [Summon(CONTROLLER, Copy(minion)) for minion in to_resurrect]


class DMF_004:
    """Yogg-Saron, Master of Fate (尤格-萨隆，命运主?
    Battlecry: If you've cast 10 spells this game, spin the Wheel of Yogg-Saron."""
    # 10?7/5 - 战吼：如果你在本局对战中施放过10个法术，旋转尤格-萨隆之轮
    
    def play(self):
        spells_cast = getattr(self.controller, 'spells_cast_this_game', 0)
        
        if spells_cast >= 10:
            effects = [
                Draw(CONTROLLER) * 5,
                Summon(CONTROLLER, RandomMinion()) * 7,
                Hit(ENEMY_CHARACTERS, 10),
                GainArmor(FRIENDLY_HERO, 10),
                CastSpell(RandomSpell()) * 5,
            ]
            return RandomChoice(effects)
        return []


class DMF_074:
    """Silas Darkmoon (希拉斯·暗?
    Battlecry: Choose a direction to rotate all minions."""
    # 7?4/4 - 战吼：选择一个方向旋转所有随?
    
    choose = ("DMF_074a", "DMF_074b")


class DMF_074a:
    """Rotate Left (逆时针旋?"""
    
    # 逆时针旋转：
    # - 发动者的随从：向右移动一个位?
    # - 对手的随从：向左移动一个位?
    play = RotateMinions(False)  # False = counterclockwise


class DMF_074b:
    """Rotate Right (顺时针旋?"""
    
    # 顺时针旋转：
    # - 发动者的随从：向左移动一个位?
    # - 对手的随从：向右移动一个位?
    play = RotateMinions(True)  # True = clockwise


class DMF_188:
    """Y'Shaarj, the Defiler (亚煞极，污染之源)
    Battlecry: Add a copy of each Corrupted card you've played this game to your hand. They cost (0) this turn."""
    # 10?10/10 - 战吼：将你在本局对战中打出的每张已腐蚀的卡牌的一张复制置入你的手牌。在本回合中，这些卡牌的法力值消耗为(0)?
    
    def play(self):
        corrupted_played = getattr(self.controller, 'corrupted_cards_played', [])
        
        actions = []
        for card_id in corrupted_played:
            actions.append(Give(CONTROLLER, card_id))
        
        return actions


class DMF_254:
    """C'Thun, the Shattered (克苏恩，破碎之劫)
    Start of Game: Break into pieces. Battlecry: Deal 30 damage randomly split among all enemies."""
    # 10?6/6 - 游戏开始时：分裂成碎片。战吼：随机对所有敌方角色造成总共30点伤?
    
    def play(self):
        yield Hit(RANDOM(ENEMY_CHARACTERS), 1) * 30


class YOP_018:
    """Keywarden Ivory (钥匙守护者艾芙瑞)
    Battlecry: Discover a Dual Class spell from any class. Spellburst: Get another copy."""
    # 5?4/5 - 战吼：发现一张任意职业的双职业法术。法术迸发：再获取一张该法术的复?
    
    def play(self):
        yield GenericChoice(CONTROLLER, RandomSpell(multi_class=True) * 3)
    
    spellburst = Give(CONTROLLER, Copy(SPELLBURST_CARD))


class YOP_035:
    """Moonfang (月牙)
    Can only take 1 damage at a time."""
    # 5?6/6 - 每次只能受到1点伤?
    
    events = Predamage(SELF).on(
        lambda self, source, *args: 
            SetTags(SELF, {GameTag.PREDAMAGE: min(args[0] if args else 1, 1)})
    )
