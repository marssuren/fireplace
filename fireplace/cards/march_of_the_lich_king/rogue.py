"""巫妖王的进军 - 潜行者 (March of the Lich King - Rogue)"""
from ..utils import *


class RLK_216:
    """尸腐鼠 (Rotten Rodent)
    战吼：使你牌库中所有亡语牌的法力值消耗减少（1）点。
    机制: BATTLECRY
    """
    def play(self):
        # 为牌库中所有亡语牌减费
        for card in self.controller.deck:
            if card.has_deathrattle:
                yield Buff(card, "RLK_216e")


class RLK_216e:
    """尸腐鼠增益 (Rotten Rodent Buff)"""
    tags = {GameTag.COST: -1}


class RLK_217:
    """天灾幻术师 (Scourge Illusionist)
    亡语：将你牌库中另一个亡语随从的4/4复制置入你的手牌，其法力值消耗减少（4）点。
    机制: DEATHRATTLE
    """
    def deathrattle(self):
        # 从牌库中找到另一个亡语随从
        deathrattle_minions = [c for c in self.controller.deck if c.type == CardType.MINION and c.has_deathrattle and c != self]
        if deathrattle_minions:
            chosen = self.game.random.choice(deathrattle_minions)
            # 创建4/4复制
            copy = self.controller.card(chosen.id)
            copy.atk = 4
            copy.max_health = 4
            # 减费4费
            yield Give(CONTROLLER, Buff(copy, "RLK_217e"))


class RLK_217e:
    """天灾幻术师增益 (Scourge Illusionist Buff)"""
    tags = {GameTag.COST: -4}


class RLK_529:
    """淬毒渗透者 (Noxious Infiltrator)
    剧毒。战吼：如果在你的上回合之后有友方亡灵死亡，对一个随从造成1点伤害。
    机制: BATTLECRY, POISONOUS
    """
    tags = {GameTag.POISONOUS: True}
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 如果上回合之后有友方亡灵死亡，造成伤害
        if self.controller.undead_died_last_turn and TARGET:
            yield Hit(TARGET, 1)


class RLK_567:
    """殒命暗影 (Shadow of Demise)
    每当你施放一个法术，变形成为该法术的复制。
    机制: TRIGGER_VISUAL
    """
    events = Play(CONTROLLER, SPELL).after(
        Morph(SELF, Copy(Play.CARD))
    )


class RLK_568:
    """配药师 (Concoctor)
    战吼：随机将一份药剂置入你的手牌。
    机制: BATTLECRY
    """
    play = Give(CONTROLLER, RandomPotion())


class RLK_569:
    """药水腰带 (Potion Belt)
    发现2份药剂。
    机制: DISCOVER
    """
    def play(self):
        # 发现2次药剂
        yield Discover(CONTROLLER, RandomPotion())
        yield Discover(CONTROLLER, RandomPotion())


class RLK_570:
    """食尸鬼炼金师 (Ghoulish Alchemist)
    战吼：你的下一份药剂的法力值消耗为（0）点。
    机制: BATTLECRY
    """
    def play(self):
        # 设置“下一份药剂减费”标记
        self.controller.next_potion_cost_zero = True





class RLK_571:
    """邪恶药剂师 (Vile Apothecary)
    在你的回合结束时，随机将一份药剂置入你的手牌。
    机制: TRIGGER_VISUAL
    """
    events = OWN_TURN_END.on(
        Give(CONTROLLER, RandomPotion())
    )


class RLK_572:
    """药剂大师普崔塞德 (Potionmaster Putricide)
    在一个随从死亡后，将一份药剂置入你的手牌。
    机制: TRIGGER_VISUAL
    """
    events = Death(MINION).after(
        Give(CONTROLLER, RandomPotion())
    )


class RLK_573:
    """鬼魅攻击 (Ghostly Strike)
    造成$1点伤害。连击：抽一张牌。
    机制: COMBO
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0
    }
    
    def play(self):
        yield Hit(TARGET, 1)
        # 连击：抽一张牌
        if self.controller.combo:
            yield Draw(CONTROLLER)


class RandomPotion:
    """随机药剂选择器"""
    # 左姆的药剂列表（来自通灵学园）
    POTIONS = [
        "CFM_021",  # Freezing Potion
        "CFM_065",  # Volcanic Potion  
        "CFM_620",  # Potion of Polymorph
        "CFM_603",  # Potion of Madness
        "CFM_604",  # Greater Healing Potion
        "CFM_661",  # Pint-Size Potion
        "CFM_662",  # Dragonfire Potion
        "CFM_094",  # Felfire Potion
        "CFM_608",  # Blastcrystal Potion
        "CFM_611",  # Bloodfury Potion
    ]
    
    def evaluate(self, source):
        import random
        return random.choice(self.POTIONS)


