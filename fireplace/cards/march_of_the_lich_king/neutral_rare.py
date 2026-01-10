"""巫妖王的进军 - 迷你扩展包 (March of the Lich King)"""
from ..utils import *


class RLK_220:
    """顽强的萨莱因 (Tenacious San'layn)
    吸血。每当本随从进行攻击，对敌方英雄造成2点伤害。
    机制: LIFESTEAL, TRIGGER_VISUAL
    """
    tags = {GameTag.LIFESTEAL: True}
    events = Attack(SELF).after(Hit(ENEMY_HERO, 2))


class RLK_653:
    """感染的食尸鬼 (Infectious Ghoul)
    亡语：随机使一个友方随从获得“亡语：召唤一个感染的食尸鬼。”
    机制: DEATHRATTLE
    """
    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS), "RLK_653e")


class RLK_653e:
    """感染的食尸鬼增益 (Infectious Ghoul Buff)"""
    deathrattle = Summon(CONTROLLER, "RLK_653")


class RLK_830:
    """血肉巨兽 (Flesh Behemoth)
    嘲讽。亡语：抽取另一张亡灵牌并召唤一个它的复制。
    机制: DEATHRATTLE, TAUNT
    """
    tags = {GameTag.TAUNT: True}
    
    def deathrattle(self, card):
        # 抽取一张亡灵牌
        drawn = yield ForceDraw(RANDOM(FRIENDLY_DECK + UNDEAD))
        if drawn:
            # 召唤一个它的复制
            yield Summon(CONTROLLER, ExactCopy(drawn))


class RLK_950:
    """传送导师 (Translocation Instructor)
    战吼：选择一个敌方随从，与敌方牌库中的随机一个随从交换。
    机制: BATTLECRY
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        if TARGET:
            # 获取敌方牌库中的随机随从
            deck_minion = RANDOM(ENEMY_DECK + MINION)
            if deck_minion:
                # 交换：将场上随从洗入牌库，将牌库随从召唤到场上
                yield Shuffle(OPPONENT, TARGET)
                yield Summon(OPPONENT, deck_minion)


class RLK_951:
    """验尸官 (Coroner)
    战吼：冻结一个敌方随从。法力渴求（6）：先将其沉默。
    机制: BATTLECRY, MANATHIRST
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 法力渴求（6）：先将其沉默
        if self.controller.max_mana >= 6:
            yield Silence(TARGET)
        # 冻结目标
        yield Freeze(TARGET)


class RLK_957:
    """哀嚎的女妖 (Wailing Banshee)
    亡语：随机使一个友方亡灵获得+2/+1。
    机制: DEATHRATTLE
    """
    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS + UNDEAD), "RLK_957e")


class RLK_957e:
    """哀嚎的女妖增益 (Wailing Banshee Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }
    health = 1


